# LAMP Stack (Ubuntu)

Provision a full stack environment including Linux, Apache, MySQL, and PHP on Ubuntu.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `mysql_root_password` | The root password for the MySQL server. | `mysql_root_password` |
| `app_user` | The owner of the web document root. | `root` |
| `http_host` | The domain name or IP for the Apache server. | `your_domain` |
| `http_conf` | The Apache virtual host configuration file name. | `your_domain.conf` |
| `http_port` | The port for the web server to listen on. | `80` |