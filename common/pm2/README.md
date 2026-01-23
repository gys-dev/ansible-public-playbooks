# PM2 Application Management

This component manages Node.js applications using PM2, including deployment scripts and re-boot persistence.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `app_user` | The user who will run the PM2 processes. | `your_app_user` |
| `node_port` | The port the application listens on. | `3300` |
| `app_run_directory` | The directory where the application code resides. | `pango-web-api` |
| `app_name` | The name of the application in PM2. | `pango-web-api` |
| `pm2_deploy_script` | The PM2 command used to start/deploy the app. | (See `vars/default.yml`) |
