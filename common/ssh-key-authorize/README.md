# SSH Key Authorization

This component authorizes local SSH public keys on remote servers to enable secure, passwordless login.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `app_user` | The remote user to authorize the key for. | `example.com` |
| `app_password` | The sudo password for the remote user (required for initial copy). | `your_secure_password_here` |
