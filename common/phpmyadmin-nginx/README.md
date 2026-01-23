# phpMyAdmin (Nginx)

This component installs and configures phpMyAdmin to run under the Nginx web server using PHP-FPM.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `phpmyadmin_php_fpm_socket` | The name/path of the PHP-FPM socket. | `php8.1-fpm` |
| `phpmyadmin_server_host` | Hostname of the MySQL server. | `localhost` |
| `phpmyadmin_server_user` | MySQL user for phpMyAdmin. | `root` |
| `phpmyadmin_server_password` | Password for the MySQL user. | `your_mysql_root_password` |
