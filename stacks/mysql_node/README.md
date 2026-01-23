# Node.js + MySQL Stack

A complete environment for Node.js applications with a backend MySQL database.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `node_version` | The version of Node.js to install. | `16` |
| `app_user` | The system user for the application. | `your_app_user` |
| `mysql_root_password` | The root password for MySQL. | `your_mysql_root_password` |
| `mysql_databases` | List of databases to create. | (See `vars/default.yml`) |
| `mysql_users` | List of MySQL users and their privileges. | (See `vars/default.yml`) |