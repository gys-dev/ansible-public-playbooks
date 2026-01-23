# LEMP Stack (Ubuntu)

Provision a full stack environment including Linux, Nginx, MySQL, and PHP-FPM on Ubuntu.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `mysql_root_password` | The root password for the MySQL server. | `mysql_root_password` |
| `http_host` | The domain name or IP for the Nginx server. | `your_domain` |
| `http_conf` | The Nginx virtual host configuration file name. | `your_domain.conf` |
| `http_port` | The port for the web server to listen on. | `80` |
