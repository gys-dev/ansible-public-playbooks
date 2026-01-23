# Initial Server Setup (Ubuntu)

This component performs the initial hardening and setup for a new Ubuntu server, including user creation and firewall configuration.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `create_user` | The name of the new regular user to create. | `app_user` |
| `copy_local_key` | Path to your local SSH public key to authorize. | (Path to `~/.ssh/id_rsa.pub`) |
| `sys_packages` | List of essential system packages to install. | `['curl', 'vim', 'git', 'ufw']` |