# AGENTS.md

This file provides guidance to AI Agents (like **Antigravity** and **Claude Code**) when working with code in this repository.

## Project Overview

This is a comprehensive collection of production-ready Ansible playbooks and roles for automated server provisioning and application stack orchestration, primarily optimized for Ubuntu 18.04/20.04+.

## Key Architecture Patterns

### Modular Structure
- **`common/`**: Standalone playbooks for individual services and system tasks
- **`stacks/`**: Orchestrated playbooks for complex application environments (LAMP, LEMP, etc.)
- **`roles/`**: Modular, reusable roles (including standard community roles)

### Playbook Design Pattern
- Uses modern Ansible v2+ syntax with `include_tasks` and structured YAML
- Variables defined in `vars/default.yml` files
- Each component has its own hosts file for isolated execution
- Follow the pattern: `ansible-playbook -i hosts playbook.yml`

## Common Development Tasks

### Building & Running
```bash
# Run a common service playbook
ansible-playbook -i hosts common/docker_ubuntu/playbook.yml

# Run a specific host from inventory
ansible-playbook -i hosts -l host0 common/setup_ubuntu/playbook.yml

# Deploy complete stacks
ansible-playbook -i hosts stacks/lamp_ubuntu/playbook.yml
ansible-playbook -i hosts stacks/lemp_ubuntu/playbook.yml
```

### Configuration Management
- Edit `hosts` file with your server IP and credentials
- Review and update `vars/default.yml` files before running playbooks
- Mandatory: `export ANSIBLE_HOST_KEY_CHECKING=False` for automation

### Testing & Validation
```bash
# Syntax check
ansible-playbook -i hosts playbook.yml --syntax-check

# Dry run
ansible-playbook -i hosts playbook.yml --check

# List tasks without execution
ansible-playbook -i hosts playbook.yml --list-tasks
```

## Important Configuration

### Ansible Settings
- `ansible.cfg` configured for Ubuntu with pipelining enabled
- Hash behavior set to `merge` for variable precedence
- SSH control master for performance

### Inventory Management
- Default hosts file at repository root
- Component-specific hosts files in subdirectories
- Use `-l host0` to target specific hosts

## MCP Tooling (ansible-script-mcp)

Agents should utilize the following tools for enhanced interaction:
- `list-playbooks`: Browse available automation tasks.
- `get-variable-schema`: Inspect required variables for a playbook.
- `execute-playbook`: Run Ansible tasks directly.
- `get-system-info`: Verify target server state.
- `suggest-playbook`: Find the best playbook for a user's requirement.

## Best Practices

### Security
- Use `sshpass` for password-based authentication during development
- Configure UFW firewall rules for all services
- SSH key management through dedicated playbooks
- MySQL secure installation with root password setup

### Performance
- Enable pipelining in ansible.cfg
- Use `force_color` for better output readability
- Control master persistence for SSH connections
- `hash_behaviour=merge` for variable management

## Common Troubleshooting

### Connection Issues
```bash
# Check SSH connectivity
ansible all -i hosts -m ping

# Debug with verbose output
ansible-playbook -i hosts playbook.yml -v
```

### Variable Issues
- Ensure `vars/default.yml` is properly formatted YAML
- Check variable precedence with `--list-tasks`
- Use `--extra-vars` for testing specific values

## Custom AI Agent Skills

This repository includes custom agent skills for enhanced website deployment functionality, compatible with **Antigravity** and Claude Code.

### Available Skills

#### deploy-website (Basic)
- **Purpose**: Basic production website deployment
- **Features**: Environment setup, dependency management, basic serving
- **Antigravity Location**: `~/.gemini/antigravity/skills/deploy-website/`
- **When to use**: Simple deployments without complex stack requirements

#### deploy-website-enhanced (Recommended)
- **Purpose**: Enhanced production website deployment with full Ansible integration
- **Features**: Complete system configuration, stack support, database integration, advanced monitoring
- **Antigravity Location**: `~/.gemini/antigravity/skills/deploy-website-enhanced/`
- **When to use**: Production deployments requiring full infrastructure setup

### Skill Installation

The skills are automatically installed to the global Antigravity skills directory when running the main installation script:

```bash
./install-skills.sh
```

### Skill Integration with Ansible Infrastructure

The enhanced skill fully integrates with the existing Ansible infrastructure:

#### Reused Components
- **System Setup**: `common/setup_ubuntu/playbook.yml`
- **User Management**: `common/node-user/playbook.yml`
- **Service Management**: `common/pm2/playbook.yml`, `common/nginx-site/playbook.yml`
- **Database Setup**: Playbooks from `stacks/` directory
- **Security**: SSH key management, firewall configuration

#### Enhanced Features
- **Dynamic Configuration**: Automatically updates Ansible variables based on deployment parameters
- **Stack Detection**: Automatically finds and uses appropriate stack playbooks
- **Environment Variables**: Creates and manages environment files for different application types
- **Port Configuration**: Auto-detects and configures application ports
- **SSL Integration**: Enhanced SSL certificate management with Let's Encrypt

### Skill Architecture (Antigravity)

The skills are structured for Antigravity:

```
~/.gemini/antigravity/skills/
├── deploy-website/
│   └── SKILL.md              # Skill definition with instructions
├── deploy-website-enhanced/
│   └── SKILL.md              # Skill definition with instructions
```

---
*Maintained by gys-dev. For human-focused documentation, see [README.md](README.md).*
