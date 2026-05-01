# TODO

Deferred follow-up work for `ansible-provision`.

## Host setup

- Add SSH key existence check to `bin/setup_host.bash` (look for
  `~/.ssh/id_ed25519.pub` or `~/.ssh/id_rsa.pub`, warn if missing).
  ansible reaches managed nodes over SSH, so the check belongs in
  the host setup just as it does in the sister `cloud-provision`
  repo. Initial setup intentionally landed with `ansible-core`
  install only; SSH key handling is the next increment.
