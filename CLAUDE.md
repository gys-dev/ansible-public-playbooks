# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

## File Organization

### Variables Structure
```
common/
├── component/
│   ├── vars/default.yml
│   └── playbook.yml
stacks/
├── stack_name/
│   ├── vars/default.yml
│   └── playbook.yml
roles/
└── geerlingguy.* (community roles)
```

### Task Organization
- Tasks are modular and reusable
- Handlers defined for service management
- Templates used for configuration files
- Conditional logic for platform-specific tasks

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

### Maintenance
- Branch `main` uses modern Ansible v2+ syntax
- Legacy support available in `branchv1` for classic `include:` syntax
- Regular updates to community roles
- Template-based configuration for consistency

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

### Role Dependencies
- Community roles in `roles/geerlingguy.*`
- Custom roles in `roles/` directory
- Dependencies managed through `meta/main.yml`