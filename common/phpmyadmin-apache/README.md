# phpMyAdmin (Apache)

This component installs and configures phpMyAdmin to run under the Apache web server.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `phpmyadmin_mysql_host` | Hostname of the MySQL server. | `localhost` |
| `phpmyadmin_mysql_port` | Port of the MySQL server. | `""` |
| `phpmyadmin_mysql_user` | MySQL user for phpMyAdmin. | `root` |
| `phpmyadmin_mysql_password` | Password for the MySQL user. | `your_mysql_root_password` |
