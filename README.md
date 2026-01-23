# Ansible Public Playbooks

A comprehensive collection of production-ready Ansible playbooks and roles designed for automated server provisioning and application stack orchestration. Primarily optimized for **Ubuntu 18.04/20.04+**.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Ansible and `sshpass` installed on your local machine.

```bash
# MacOS
brew install ansible
brew install hudochenkov/sshpass/sshpass

# Ubuntu/Debian
sudo apt update
sudo apt install ansible sshpass
```

### 2. Configuration
1. **Inventory**: Edit the `hosts` file with your server IP and credentials.
   ```ini
   [web]
   your_host ansible_host=0.0.0.0 ansible_user=root ansible_password=your_password
   ```
2. **Variables**: Every component has a `vars/default.yml`. Review and update these before running a playbook.

---

## 🏗️ Project Structure

The repository is organized for both modularity and ease of deployment:

*   **`common/`**: Standalone playbooks for individual services and system tasks.
*   **`stacks/`**: Orchestrated playbooks for complex application environments (LAMP, LEMP, etc.).
*   **`roles/`**: Modular, reusable roles (including standard community roles).

---

## 🛠️ Supported Components

### Web & Proxy Servers
*   **Apache**: Standard and optimized configurations.
*   **Nginx**: High-performance web server and reverse proxy setup.
*   **Certbot**: SSL/TLS certificate automation for Nginx.

### Databases
*   **MySQL**: Automated installation and secure configuration.
*   **PostgreSQL**: Deployment with user and database management.
*   **MongoDB**: NoSQL database setup for Node.js environments.

### Runtimes & Management
*   **Node.js**: Version management via NVM, including Yarn and PM2.
*   **PHP**: Support for various versions and FPM configurations.
*   **PM2**: Process management for Node.js applications with startup persistence.

### Security & System
*   **Initial Setup**: User creation, sudo configuration, and SSH hardening.
*   **UFW**: Automated firewall rules for all services.
*   **SSH Management**: Key generation and authorized_key distribution.

### Administration Tools
*   **PHPMyAdmin**: Web interface for MySQL/MariaDB (Apache/Nginx).
*   **PGAdmin4**: Web interface for PostgreSQL management.

---

## 📦 Available Stacks

Deploy complete environments with a single command:

| Stack Name | Description | Command Example |
| :--- | :--- | :--- |
| **LAMP** | Linux, Apache, MySQL, PHP | `ansible-playbook -i hosts stacks/lamp_ubuntu/playbook.yml` |
| **LEMP** | Linux, Nginx, MySQL, PHP-FPM | `ansible-playbook -i hosts stacks/lemp_ubuntu/playbook.yml` |
| **WordPress** | Ready-to-use WordPress on LAMP | `ansible-playbook -i hosts stacks/wordpress-lamp_ubuntu/playbook.yml` |
| **Node + MySQL** | Node.js (NVM) with MySQL Backend | `ansible-playbook -i hosts stacks/mysql_node/playbook.yml` |
| **Node + Mongo** | Node.js (NVM) with MongoDB Backend | `ansible-playbook -i hosts stacks/mongo_node/playbook.yml` |
| **Node + Postgres**| Node.js (NVM) with PostgreSQL Backend | `ansible-playbook -i hosts stacks/postgresql_node/playbook.yml` |

---

## 📖 Usage Examples

### Run a Common Service Playbook
To set up Docker on your server:
```bash
ansible-playbook -i hosts common/docker_ubuntu/playbook.yml
```

### Run a Specific Host from Inventory
```bash
ansible-playbook -i hosts -l host0 common/setup_ubuntu/playbook.yml
```

### Advanced: Skipping Host Key Checking
```bash
export ANSIBLE_HOST_KEY_CHECKING=False
ansible-playbook -i hosts stacks/lemp_ubuntu/playbook.yml
```

---

## 📌 Maintenance Notes

This project supports two execution formats:
*   **Branch `main` (v2)**: Optimized for modern Ansible using `include_tasks`, structured YAML maps, and boolean values.
*   **Branch `branchv1`**: Legacy support using the classic `include:` syntax.

---
*Developed by gys-dev*
