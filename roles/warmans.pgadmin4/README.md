Pgadmin4
=========

[![Build Status](https://travis-ci.org/warmans/pgadmin4.svg?branch=master)](https://travis-ci.org/warmans/pgadmin4)

Role to setup a pgadmin4 (beta) server. With this role pgadmin4 is configured to run as a web
application. Be aware it's beta software and may not 100% work yet.

Requirements
------------

- systemd

Role Variables
--------------

- `pgadmin4_python2_dist_dir` - Path to python2 dist packages dir
- `pgadmin4_pip_download` - HTTP link to download pgadmin4 .whl file
- `pgadmin4_upgrade_check_enabled` - Check for updates?

Webserver Options

- `pgadmin4_server_bind` - Bind webserver to this address
- `pgadmin4_server_port` - Bind webserver to this port
- `pgadmin4_server_csrf_key` - Secret key for signing CSRF data
- `pgadmin4_server_secret_key` - Secret key for signing cookies
- `pgadmin4_server_password_salt` - Salt used when hashing passwords

Default User

- `pgadmin4_initial_user_email` - default username used to login to the server
- `pgadmin4_initial_user_password` - default password used to login to the server

Password Reset Vars

- `pgadmin4_mail_server`
- `pgadmin4_mail_port`
- `pgadmin4_mail_use_ssl`
- `pgadmin4_mail_username`
- `pgadmin4_mail_password`


License
-------

MIT
