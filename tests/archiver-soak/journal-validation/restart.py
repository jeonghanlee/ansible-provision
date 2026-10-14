"""Verify separate live recording segments across a real dedicated-VM reboot."""

import argparse
import collections
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
import uuid

import basic
import boot_coverage
import journal_coverage
import long
import prepare

SECONDS = 300
UUID_PATH = Path('/sys/class/dmi/id/product_uuid')


def digest(path):
    return long.digest_file(path)


def load(path):
    return json.loads(path.read_text())


def query_sources(path, config):
    """Index unchanged actual query rows by their full journal identity."""
    long.checked_query(path)
    records = {}
    for row in basic.load_rows(path):
        identity = basic.identity(row)
        if identity in records and records[identity] != row:
            raise basic.ConfirmedViolation('A restart query repeats an identity with changed content')
        records[identity] = row
    return basic.source_index(records, config)


def check_boundary(master):
    """Recheck actual retained producer/query inputs without claiming reboot acceptance."""
    prepare.verify(master / 'package')
    if long.inventory(master) != load(master / 'artifact-index.json'):
        raise RuntimeError('The retained restart evidence changed before its boundary recheck')
    destination = master / 'pre-reboot-boundary'
    actions = load(destination / 'schedule.json')
    outcomes = {row['id']: row for row in load(destination / 'outcomes.json')}
    config = load(master / 'package/config.json')
    paths = sorted(destination.glob('direct-*.jsonl'), key=lambda path: int(path.stem.split('-')[-1]))
    if not paths:
        raise RuntimeError('No actual retained boundary query exists')
    indexed = query_sources(paths[-1], config)
    count, sources = 0, {}
    for action in actions:
        outcome = outcomes[action['id']]
        matched = basic.required_records(action, outcome, indexed, config)
        if len(matched) != (2 if action['path'] in ('appliance', 'health') else 1):
            raise RuntimeError('The retained actual boundary source records remain missing or ambiguous')
        count += len(matched)
        sources[action['path']] = len(matched)
    return {'scope': 'retained-real-pre-reboot-source-correlation-only', 'actual_required_records': count,
            'actual_records_by_path': sources, 'all_actual_boundary_sources_correlated': True,
            'whole_scenario_acceptance_established': False}


def child(master, label):
    path = Path(load(master / 'contract.json')['segments'][label])
    if path.parent != prepare.EVIDENCE or not path.name.startswith('long-'):
        raise RuntimeError('The declared restart segment is outside the dedicated evidence root')
    return path


def required_records(directory):
    """Derive required identities from actual independent producer and direct-query evidence."""
    config = load(directory / 'package/config.json')
    direct, first = basic.direct_records(directory / 'direct')
    index = basic.source_index(direct, config)
    outcomes = {}
    for name in ('baseline-outcomes.jsonl', 'outcomes.jsonl'):
        for item in basic.load_rows(directory / name):
            if item['id'] in outcomes:
                raise basic.ConfirmedViolation('Restart producer outcomes repeat an identity')
            outcomes[item['id']] = item
    records, scheduled = {}, set()
    for name in ('baseline-schedule.jsonl', 'schedule.jsonl'):
        for action in basic.load_rows(directory / name):
            if action['id'] in scheduled:
                raise basic.ConfirmedViolation('Restart producer schedules repeat an identity')
            scheduled.add(action['id'])
            outcome = outcomes.get(action['id'])
            if outcome is None:
                raise RuntimeError('A restart producer outcome is missing')
            if not outcome.get('executed') and not (action['path'] == 'appliance' and outcome.get('attempted')):
                raise basic.ConfirmedViolation('A required restart action was not executed')
            matched = basic.required_records(action, outcome, index, config)
            if len(matched) != (2 if action['path'] in ('appliance', 'health') else 1):
                raise RuntimeError('A restart source record set is missing or ambiguous')
            for row in matched:
                identity = basic.identity(row)
                if identity in records:
                    raise basic.ConfirmedViolation('Restart actions claim the same required journal identity')
                records[identity] = row
    if set(outcomes) != scheduled:
        raise basic.ConfirmedViolation('Restart outcomes include an unscheduled action')
    return records, {identity: first[identity] for identity in records}


def boundary(master, directory, config):
    destination = master / 'pre-reboot-boundary'
    destination.mkdir(mode=0o700)
    actions = basic.schedule(uuid.uuid4().hex, config, basic.clock(), 1)
    prepare.save(destination / 'schedule.json', actions)
    outcomes = [basic.emit(action, config, destination) for action in actions]
    prepare.save(destination / 'outcomes.json', outcomes)
    boot = load(directory / 'observation.json')['end_boot']
    anchor = basic.load_rows(directory / 'initial-anchor.jsonl')[0]
    deadline, attempt = time.monotonic() + basic.VISIBILITY_WAIT, 0
    while True:
        path = destination / ('direct-' + str(attempt) + '.jsonl')
        receipt = long.query(config, boot, anchor['__CURSOR'], path)
        if receipt.get('returncode') != 0 or receipt.get('error') or receipt.get('stderr', '').strip():
            raise RuntimeError('The actual pre-reboot boundary query failed')
        index = query_sources(path, config)
        matched = [basic.required_records(action, outcome, index, config)
                   for action, outcome in zip(actions, outcomes)]
        if all(len(rows) == (2 if action['path'] in ('appliance', 'health') else 1)
               for action, rows in zip(actions, matched)):
            break
        if time.monotonic() >= deadline:
            raise RuntimeError('Not every actual pre-reboot boundary source was directly confirmed')
        time.sleep(basic.QUERY_PERIOD)
        attempt += 1
    intervals = sorted((directory / 'collector').glob('interval-*/result.json'),
                       key=lambda path: int(path.parent.name.split('-')[-1]))
    previous = {'system_journal_checkpoint': load(intervals[-1])['checkpoint']}
    native = destination / 'native'
    native.mkdir(mode=0o700)
    prepare.save(native / 'input-state.json', previous)
    window = load(directory / 'restart-window.json')['entry']
    context = load(directory / 'restart-input.json')
    collected = boot_coverage.collect(native, previous, datetime.datetime.now(datetime.timezone.utc), window, context)
    prepare.save(native / 'result.json', collected)
    archived = collections.Counter(basic.identity(row) for row in basic.load_rows(native / 'journal-sequence.jsonl'))
    if not collected['coverage_complete'] or any(archived[basic.identity(row)] != 1 for rows in matched for row in rows):
        raise RuntimeError('Actual pre-reboot boundary records are not archived exactly once')
    result = {'boot_id': boot, 'confirmed': receipt['finished'],
              'actions': [{'action': action, 'outcome': outcome, 'records': rows}
                          for action, outcome, rows in zip(actions, outcomes, matched)],
              'checkpoint': collected['checkpoint'], 'native_result_sha256': digest(native / 'result.json')}
    prepare.save(destination / 'confirmation.json', result)
    return result


def finish(master, errors=None):
    state = load(master / 'observation.json')
    state.update(state='Finished', ended=basic.clock())
    state['errors'].extend(errors or [])
    prepare.save(master / 'observation.json', state)
    prepare.save(master / 'artifact-index.json', long.inventory(master))
    result = replay(master, publish=True)
    prepare.save(master / 'result.json', result)
    return result


def before(config_path):
    prepare.verify(basic.PACKAGE)
    config = prepare.configuration(config_path)
    boot = journal_coverage.BOOT.read_text().strip().replace('-', '')
    master = prepare.EVIDENCE / ('restart-' + uuid.uuid4().hex)
    master.mkdir(mode=0o700)
    shutil.copytree(basic.PACKAGE, master / 'package')
    prepare.save(master / 'package/config.json', config)
    history = sorted({boot, *(row['boot_id'] for row in journal_coverage.file_headers() if row['entries'])})
    contract = {'schema': 1, 'scenario': 'vm-restart', 'live_segment_seconds': SECONDS,
                'periods_seconds': basic.PERIODS, 'collection_seconds': basic.COLLECTION_PERIOD,
                'generation_during_reboot': 'paused', 'pre_boot_id': boot,
                'hardware_uuid': UUID_PATH.read_text().strip().lower(), 'preexisting_boot_ids': history,
                'segments': {label: str(prepare.EVIDENCE / ('long-' + uuid.uuid4().hex))
                             for label in ('before', 'after')},
                'manifest_sha256': digest(master / 'package/manifest.json')}
    prepare.save(master / 'contract.json', contract)
    prepare.save(master / 'observation.json', {'state': 'Recording before reboot', 'started': basic.clock(), 'errors': []})
    try:
        readiness = master / 'readiness'
        readiness.mkdir(mode=0o700)
        if not basic.preflight(config, readiness, allowed_boots=history)['ready']:
            raise RuntimeError('The actual pre-reboot dedicated deployment is not ready')
        for unit in (config['appliance_unit'], 'journal-validation-ioc.service'):
            receipt = basic.command(['systemctl', 'is-enabled', unit], master / ('enabled-' + unit))
            if receipt.get('returncode') != 0 or (master / ('enabled-' + unit)).with_suffix('.stdout').read_text().strip() != 'enabled':
                raise RuntimeError('A required source service is not enabled for the real reboot')
        context = {'journal_boots': history, 'master_contract_sha256': digest(master / 'contract.json'),
                   'master': str(master), 'phase': 'before'}
        directory, result = long.run(config_path, SECONDS, 'restart-before', restart_input=context,
                                     directory=child(master, 'before'))
        if result['overall'] != 'Passed':
            raise RuntimeError('The complete pre-reboot segment did not pass')
        confirmed = boundary(master, directory, config)
        prepare.save(master / 'before.json', {'segment_result_sha256': digest(directory / 'result.json'),
                     'segment_index_sha256': digest(directory / 'artifact-index.json'),
                     'boundary_confirmation_sha256': digest(master / 'pre-reboot-boundary/confirmation.json'),
                     'retained_checkpoint': confirmed['checkpoint'], 'completed': basic.clock()})
        state = load(master / 'observation.json')
        state.update(state='Ready for reboot', generation_pause_began=basic.clock())
        prepare.save(master / 'observation.json', state)
        return master, None
    except Exception as error:
        return master, finish(master, [str(error)])


def after(master):
    prepare.verify(basic.PACKAGE)
    contract = load(master / 'contract.json')
    state = load(master / 'observation.json')
    if state['state'] != 'Reboot requested' or (master / 'result.json').exists():
        raise RuntimeError('The restart scenario is not waiting for its declared reboot')
    boot = journal_coverage.BOOT.read_text().strip().replace('-', '')
    if boot == contract['pre_boot_id'] or UUID_PATH.read_text().strip().lower() != contract['hardware_uuid']:
        raise RuntimeError('A new boot on the same dedicated VM was not established')
    if digest(basic.PACKAGE / 'manifest.json') != contract['manifest_sha256']:
        raise RuntimeError('The restart package changed across the real reboot')
    external = load(master / 'external-boot-observation.json')
    if (external['clock_domain'] != 'control-host' or external['old_boot_id'] != contract['pre_boot_id']
            or external['new_boot_id'] != boot or not external['probes']):
        raise RuntimeError('The real reboot lacks independent external clock and boot observations')
    config_path = master / 'package/config.json'
    config = prepare.configuration(config_path)
    try:
        before_result = load(master / 'before.json')
        context = {'journal_boots': sorted(set(contract['preexisting_boot_ids']) | {boot}),
                   'previous_state': {'system_journal_checkpoint': before_result['retained_checkpoint']},
                   'master_contract_sha256': digest(master / 'contract.json'),
                   'master': str(master), 'phase': 'after'}
        state.update(state='Recording after reboot', post_boot_id=boot, actual_resume=basic.clock())
        prepare.save(master / 'observation.json', state)
        directory, result = long.run(config_path, SECONDS, 'restart-after', restart_input=context,
                                     directory=child(master, 'after'))
        first_anchor = basic.load_rows(child(master, 'before') / 'initial-anchor.jsonl')[0]
        long.query(config, contract['pre_boot_id'], first_anchor['__CURSOR'], master / 'old-boot-final.jsonl')
        prepare.save(master / 'after.json', {'segment_result_sha256': digest(directory / 'result.json'),
                     'segment_index_sha256': digest(directory / 'artifact-index.json'),
                     'boot_id': boot, 'completed': basic.clock()})
        return finish(master)
    except Exception as error:
        return finish(master, [str(error)])


def replay(master, publish=False):
    result = {'scope': 'journal-vm-restart', 'overall': 'Incomplete', 'delivery': 'Incomplete',
              'later_live_read': 'Incomplete', 'collection': 'Incomplete', 'full_day_acceptance': 'Pending',
              'violations': [], 'unresolved': [], 'segments': {}}
    try:
        if long.inventory(master) != load(master / 'artifact-index.json'):
            raise RuntimeError('Original restart evidence differs from its frozen index')
        prepare.verify(master / 'package')
        if digest(Path(__file__)) != digest(master / 'package/restart.py'):
            raise RuntimeError('Restart replay must use its exact original source')
        contract, state = load(master / 'contract.json'), load(master / 'observation.json')
        if contract['live_segment_seconds'] != SECONDS or contract['periods_seconds'] != basic.PERIODS:
            raise RuntimeError('The required restart recording duration or frequencies changed')
        if contract['generation_during_reboot'] != 'paused' or state['state'] != 'Finished':
            raise RuntimeError('The declared restart pause or final state is missing')
        result['unresolved'].extend(state['errors'])
        if state['errors']:
            raise RuntimeError('The restart scenario stopped before completing its declared phases')
        requested = load(master / 'reboot-request.json')
        external = load(master / 'external-boot-observation.json')
        if (requested['command_receipt'].get('returncode') != 0
                or requested['boot_id'] != contract['pre_boot_id']
                or external['clock_domain'] != 'control-host'
                or external['old_boot_id'] != contract['pre_boot_id']
                or external['new_boot_id'] != state['post_boot_id'] or not external['probes']
                or requested['command_receipt']['started']['monotonic_ns'] < state['generation_pause_began']['monotonic_ns']):
            raise RuntimeError('The actual declared reboot request or external observations do not agree')
        required, first_seen, archives, previous = {}, {}, {}, None
        for label in ('before', 'after'):
            directory = child(master, label)
            original = load(directory / 'result.json')
            repeated = long.replay(directory)
            if repeated != original:
                raise RuntimeError('The actual restart segment replay differs from its original')
            result['segments'][label] = original['overall']
            if original['overall'] != 'Passed':
                result['unresolved'].append('The original ' + label + ' segment did not pass')
            result['violations'].extend(original['violations'])
            confirmation = load(master / (label + '.json'))
            if (digest(directory / 'result.json') != confirmation['segment_result_sha256']
                    or digest(directory / 'artifact-index.json') != confirmation['segment_index_sha256']):
                raise RuntimeError('A frozen restart segment result changed')
            segment_contract = load(directory / 'contract.json')
            segment_state = load(directory / 'observation.json')
            context = load(directory / 'restart-input.json')
            if context['master_contract_sha256'] != digest(master / 'contract.json'):
                raise RuntimeError('The actual restart segment is not bound to its original parent contract')
            expected_boots = contract['preexisting_boot_ids'] if label == 'before' else sorted(
                set(contract['preexisting_boot_ids']) | {state['post_boot_id']})
            if context['journal_boots'] != expected_boots:
                raise RuntimeError('The actual restart segment accepted different journal boot identities')
            expected_boot = contract['pre_boot_id'] if label == 'before' else state['post_boot_id']
            if segment_state['start_boot'] != expected_boot or segment_state['end_boot'] != expected_boot:
                raise RuntimeError('A restart segment has an unexpected actual boot identity')
            if ((segment_state['ended']['monotonic_ns'] - segment_contract['start']['monotonic_ns']) / 1e9 < SECONDS
                    or segment_contract['scenario'] != 'restart-' + label):
                raise RuntimeError('An actual restart live segment did not complete its declared duration')
            segment_records, segment_first = required_records(directory)
            for identity, row in segment_records.items():
                if identity in required:
                    raise basic.ConfirmedViolation('Restart segments repeat a required record identity')
                required[identity] = row
                first_seen[identity] = segment_first[identity]
            if label == 'before':
                boundary_result = load(master / 'pre-reboot-boundary/confirmation.json')
                if (digest(master / 'pre-reboot-boundary/confirmation.json') != confirmation['boundary_confirmation_sha256']
                        or boundary_result['checkpoint'] != confirmation['retained_checkpoint']
                        or digest(master / 'pre-reboot-boundary/native/result.json') != boundary_result['native_result_sha256']):
                    raise RuntimeError('The actual pre-reboot boundary checkpoint changed')
                for action in boundary_result['actions']:
                    for row in action['records']:
                        identity = basic.identity(row)
                        if identity in required:
                            raise basic.ConfirmedViolation('The pre-reboot boundary repeats a required identity')
                        required[identity] = row
                        first_seen[identity] = boundary_result['confirmed']
            intervals = sorted((directory / 'collector').glob('interval-*'),
                               key=lambda path: int(path.name.split('-')[-1]))
            if label == 'before':
                intervals.append(master / 'pre-reboot-boundary/native')
            for interval in intervals:
                if not (interval / 'journal-coverage.json').is_file():
                    result['unresolved'].append('A real restart native interval lacks complete coverage')
                    continue
                proof = load(interval / 'journal-coverage.json')
                source = interval / 'journal-sequence.jsonl'
                if not proof['coverage_complete'] or digest(source) != proof['source_sha256']:
                    raise RuntimeError('A restart native archive lacks its actual unchanged coverage proof')
                boot_coverage.verify(interval, proof)
                records = basic.load_rows(source)
                if (not records or records[0]['__CURSOR'] != proof['system_anchor']
                        or records[-1]['__CURSOR'] != proof['system_tail']):
                    raise RuntimeError('The actual restart archive and its declared boundaries disagree')
                journal_coverage.validate_interval(records, records[0], records[-1], proof['boot_id'])
                if previous is not None and records[0]['_BOOT_ID'] == previous['_BOOT_ID']:
                    if records[0] != previous:
                        raise RuntimeError('Adjacent same-boot restart collector boundaries disagree')
                    records = records[1:]
                for row in records:
                    identity = basic.identity(row)
                    if identity in archives:
                        raise basic.ConfirmedViolation('A restart archive repeats a journal identity')
                    archives[identity] = row
                previous = basic.load_rows(source)[-1]
            if label == 'after':
                retained = load(directory / 'collector/interval-0/input-state.json')
                if retained != {'system_journal_checkpoint': load(master / 'before.json')['retained_checkpoint']}:
                    raise RuntimeError('The original actual pre-reboot collector checkpoint was reset')
        live, final_seen = {}, {}
        for path in (master / 'old-boot-final.jsonl', child(master, 'after') / 'final-live.jsonl'):
            receipt = long.checked_query(path)
            for row in basic.load_rows(path):
                live[basic.identity(row)] = row
                final_seen[basic.identity(row)] = receipt['finished']
        missing_live = [identity for identity, row in required.items() if live.get(identity) != row]
        result['missing_or_changed_live_identities'] = [list(identity) for identity in missing_live]
        if missing_live:
            raise basic.ConfirmedViolation('Required restart records are missing or changed in the final live journal')
        result.update(delivery='Passed', later_live_read='Passed', actual_required_records=len(required),
                      live_boot_count=len({row['_BOOT_ID'] for row in required.values()}))
        if result['live_boot_count'] != 2:
            raise RuntimeError('Two distinct actual boot identities were not established')
        if {row['_BOOT_ID'] for row in required.values()} != {contract['pre_boot_id'], state['post_boot_id']}:
            raise RuntimeError('The required source records have unexpected boot identities')
        missing_archive = [identity for identity, row in required.items() if archives.get(identity) != row]
        result['unarchived_required_records'] = len(missing_archive)
        result['missing_or_changed_archive_identities'] = [list(identity) for identity in missing_archive]
        comparisons = []
        for identity in sorted(required, key=lambda value: json.dumps(value)):
            age = (datetime.datetime.fromisoformat(final_seen[identity]['utc']) -
                   datetime.datetime.fromisoformat(first_seen[identity]['utc'])).total_seconds()
            if age < 0:
                raise RuntimeError('UTC moved backwards between a restart record confirmation and final read')
            comparisons.append(json.dumps({'identity': identity, 'first_confirmed': first_seen[identity],
                               'final_read': final_seen[identity], 'age_utc_seconds': age,
                               'cross_boot_monotonic_comparison_used': False,
                               'live_payload_matches': live.get(identity) == required[identity],
                               'archive_payload_matches': archives.get(identity) == required[identity]}, sort_keys=True))
        comparison_bytes = ('\n'.join(comparisons) + '\n').encode()
        comparison_path = master / 'comparisons.jsonl'
        if publish:
            comparison_path.write_bytes(comparison_bytes)
        elif not comparison_path.is_file() or comparison_path.read_bytes() != comparison_bytes:
            raise RuntimeError('The original per-record restart comparisons do not reproduce')
        result['comparisons_sha256'] = hashlib.sha256(comparison_bytes).hexdigest()
        if not missing_archive and not result['unresolved']:
            result['collection'] = 'Passed'
            result['overall'] = 'Passed'
        else:
            result['unresolved'].append('The complete restart archive has not been established')
    except basic.ConfirmedViolation as error:
        result['violations'].append(str(error))
        result['overall'] = 'Failed'
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        result['unresolved'].append(str(error))
    if result['violations']:
        result['overall'] = 'Failed'
    return result


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    initial = commands.add_parser('before')
    initial.add_argument('--config', type=Path, default=prepare.PREFIX / 'config.json')
    for name in ('after', 'replay', 'check-boundary'):
        command = commands.add_parser(name)
        command.add_argument('directory', type=Path)
    args = parser.parse_args()
    if args.action == 'before':
        directory, result = before(args.config)
    elif args.action == 'check-boundary':
        print(json.dumps(check_boundary(args.directory), sort_keys=True))
        return 0
    else:
        directory = args.directory
        result = after(directory) if args.action == 'after' else replay(directory)
    print(json.dumps({'evidence': str(directory), 'phase': load(directory / 'observation.json')['state'],
                      'result': result}, sort_keys=True))
    return 0 if result is None or result['overall'] == 'Passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
