# Node User Setup

This component sets up a dedicated system user and installs Node.js using NVM (Node Version Manager).

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `temp_folder` | Path for temporary download files. | `~/tmp` |
| `node_version` | The version of Node.js to install. | `20` |
| `app_user` | The username of the application user to create. | `your_app_user` |
| `app_password` | The password for the application user. | `your_app_password` |
