# Docker Setup (Ubuntu)

This component installs Docker on Ubuntu systems and provisions a set of initial containers.

## 📋 Variables

Define these variables in `vars/default.yml`:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `create_containers` | Number of containers to create. | `4` |
| `default_container_name` | Prefix name for the created containers. | `docker` |
| `default_container_image` | Docker image to use for the containers. | `ubuntu` |
| `default_container_command` | Command to run inside the containers. | `sleep 1d` |