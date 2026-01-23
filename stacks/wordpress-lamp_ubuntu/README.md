# WordPress on LAMP Stack

Automated installation of WordPress on an optimized LAMP (Apache, MySQL, PHP) stack.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `php_modules` | List of PHP extensions to install. | (Standard WordPress set) |
| `mysql_root_password` | Root password for MySQL management. | `your_mysql_root_password` |
| `mysql_db` | Name of the WordPress database. | `wordpress` |
| `mysql_user` | Dedicated MySQL user for WordPress. | `your_mysql_user` |
| `mysql_password` | Password for the WordPress MySQL user. | `your_mysql_password` |
| `http_host` | Domain name for the WordPress site. | `example.com` |
