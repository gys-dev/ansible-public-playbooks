# Nginx Site Configuration

This component configures Nginx virtual hosts and proxy settings for web applications.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `server_name` | The primary domain name for the site. | `example.com` |
| `node_port` | The backend port (e.g., Node.js) to proxy traffic to. | `3300` |
| `nginx_vhost_template` | Path to the virtual host Jinja2 template. | `files/vhost.conf.j2` |
| `nginx_remove_default_vhost` | Whether to remove the default Nginx site. | `true` |
| `nginx_vhosts` | A list of virtual host configurations. | (See `vars/default.yml`) |
