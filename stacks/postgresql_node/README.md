# Node.js + PostgreSQL Stack

A complete environment for Node.js applications with a backend PostgreSQL database.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `node_version` | The version of Node.js to install. | `20` |
| `app_user` | The system user and PostgreSQL owner. | `your_app_user` |
| `postgresql_databases` | List of databases to create. | (See `vars/default.yml`) |
| `postgresql_users` | List of users with database passwords. | (See `vars/default.yml`) |