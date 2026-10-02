#!/usr/bin/env python3
"""Record the actual systemd health invocation outcome through ExecStopPost."""

import datetime
import json
import os

PREFIX = 'ETL_SOAK_HEALTH '


def main():
    record = {'observed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'invocation_id': os.environ.get('INVOCATION_ID', ''),
              'result': os.environ.get('SERVICE_RESULT', ''),
              'exit_code': os.environ.get('EXIT_CODE', ''),
              'exit_status': os.environ.get('EXIT_STATUS', '')}
    print(PREFIX + json.dumps(record), flush=True)


if __name__ == '__main__':
    main()
