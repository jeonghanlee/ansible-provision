"""Execute a raw SSH command with private stdin and no target-side Python."""

from ansible.module_utils.common.text.converters import to_bytes
from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):
    TRANSFERS_FILES = False
    _VALID_ARGS = frozenset(("cmd", "stdin"))

    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp, task_vars)
        result["_ansible_no_log"] = True
        command = self._task.args.get("cmd")
        payload = self._task.args.get("stdin")
        if not self._task.no_log:
            return dict(result, failed=True, msg="raw_stdin requires no_log: true")
        if not isinstance(command, str) or not command.strip():
            return dict(result, failed=True, msg="raw_stdin requires a nonempty cmd string")
        if not isinstance(payload, str) or not payload:
            return dict(result, failed=True, msg="raw_stdin requires a nonempty stdin string")
        if self._connection.transport != "ssh":
            return dict(result, failed=True, msg="raw_stdin requires the SSH connection plugin")
        if self._task.environment and any(self._task.environment):
            return dict(result, failed=True, msg="raw_stdin does not support environment")
        if self._task.check_mode:
            return dict(result, skipped=True, changed=False)

        result.update(self._low_level_execute_command(command, in_data=to_bytes(payload)))
        result["changed"] = True
        if result.get("rc", 0) != 0:
            result.update(failed=True, msg="non-zero return code")
        return result
