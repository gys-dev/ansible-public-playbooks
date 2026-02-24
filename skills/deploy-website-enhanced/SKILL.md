---
name: deploy-website-enhanced
description: Enhanced production website deployment with full Ansible integration, stack support, database integration, and advanced monitoring. Use when deploying production websites requiring complete infrastructure setup.
argument-hint: [domain] [--stack lamp|lemp|node|python] [--database] [--database_type mysql|postgresql|mongo] [--ssl] [--debug]
disable-model-invocation: true
---

# Enhanced Deploy Website Skill

## Usage

```bash
/claude deploy-website-enhanced --source /path/to/project --domain example.com --stack lamp --database --database_type mysql --ssl --debug
```

## Parameters

- `--source`: Path to the website source code
- `--domain`: Domain name for the website
- `--stack`: Application stack (lamp, lemp, node, python)
- `--database`: Enable database support
- `--database_type`: Database type (mysql, postgresql, mongo)
- `--ssl`: Enable SSL certificate (Let's Encrypt)
- `--debug`: Enable debug mode

## Implementation

This skill provides enhanced website deployment with full Ansible integration. It handles:
- Complete system configuration
- Stack-specific deployment (LAMP, LEMP, Node.js, Python)
- Database integration and setup
- Advanced monitoring and logging
- Enhanced SSL management
- Environment detection and configuration
- Port auto-detection
- Security hardening

This skill integrates with the existing Ansible infrastructure in the project, reusing components like system setup, user management, service management, and security configurations.
