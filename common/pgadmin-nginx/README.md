# pgAdmin 4 with Nginx

This component installs pgAdmin 4 using pip and configures it to run as a web application behind an Nginx reverse proxy.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `pgadmin4_pip_download`| URL to the pgAdmin 4 wheel file. | (PostgreSQL FTP URL) |
| `pgadmin4_server_port` | Internal port for the pgAdmin server. | `5050` |
| `pgadmin4_server_secret_key` | Secret key for session security. | `your_secret_key` |
| `pgadmin4_initial_user_email` | Initial admin email address. | `admin@example.com` |
| `pgadmin4_initial_user_password` | Initial admin password. | `your_initial_password` |
| `pgadmin4_server_password_salt` | Password salt for security. | `your_password_salt` |
