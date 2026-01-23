# Apache Web Server (Ubuntu)

This component installs and configures the Apache HTTP server on Ubuntu systems, including virtual host setup.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `app_user` | Owner of the web document root. | `sammy` |
| `http_host` | The domain name or IP of the host. | `your_domain` |
| `http_conf` | Name of the Apache virtual host config file. | `your_domain.conf` |
| `http_port` | Port to listen on (default 80). | `80` |
| `disable_default` | Whether to disable the default Apache site. | `true` |