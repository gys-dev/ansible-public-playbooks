# SSH Key Generation

This component generates an SSH key pair on the remote server for a specified user.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `app_user` | The user for whom to generate the SSH key. | `myapp` |
| `ssh_key_filename` | The filename for the generated private key. | `id_rsa` |
