#!/usr/bin/env python3
"""Verify every shipped fixture PV's actual deployed store chain through mgmt."""

import argparse
import concurrent.futures
import csv
import datetime
import json
import os
import urllib.parse
import urllib.request

import collect
import contract
import observe


def verify(chain, duration):
    if (observe.OUT / 'observation.json').exists():
        raise RuntimeError('Deployed chain verification must precede the observation')
    hashes = observe.tool_hashes()
    preparation = contract.preparation(observe.OUT, duration, chain)
    fixture = observe.TOOLS / 'pvs-all.csv'
    if contract.digest(fixture) != contract.FIXTURE_SHA:
        raise RuntimeError('Unexpected fixture digest')
    with fixture.open() as stream:
        rows = list(csv.DictReader(stream))

    def query(row):
        url = collect.MGMT + '/getPVTypeInfo?' + urllib.parse.urlencode({'pv': row['pv']})
        with urllib.request.urlopen(url, timeout=30) as response:
            if response.status != 200:
                raise RuntimeError('PV configuration HTTP failure')
            data = json.load(response)
        configuration = contract.deployed_configuration(chain, data['dataStores'])
        return {'pv': row['pv'], 'dataStores': data['dataStores'], 'configuration': configuration}

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        observed = list(executor.map(query, rows))
    if len(observed) != 903 or len({row['pv'] for row in observed}) != 903:
        raise RuntimeError('Exactly 903 distinct fixture configurations are required')
    source = observe.OUT / 'deployed-pv-stores.json'
    if observe.tool_hashes() != hashes:
        raise RuntimeError('Installed tool bundle changed during chain verification')
    collect.write_json(source, observed)
    record = {'schema': contract.SCHEMA, 'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'boot_id': observe.BOOT.read_text().strip(), 'configuration': preparation['configuration'],
              'duration_seconds': duration, 'verified_pvs': len(observed),
              'fixture_sha256': contract.digest(fixture), 'source_sha256': contract.digest(source),
              'tool_hashes': hashes}
    collect.write_json(observe.OUT / 'chain-verification.json', record)
    print(json.dumps({'chain': chain, 'verified_pvs': len(observed)}))


def main():
    os.umask(0o077)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--chain', choices=contract.CHAINS, required=True)
    parser.add_argument('--duration-seconds', type=int, choices=contract.DURATIONS, required=True)
    args = parser.parse_args()
    with collect.locked(observe.OUT.parent / (observe.OUT.name + '.lifecycle.lock')):
        verify(args.chain, args.duration_seconds)


if __name__ == '__main__':
    main()
