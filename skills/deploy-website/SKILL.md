---
name: deploy-website
description: Basic production website deployment with environment setup, dependency management, and basic serving. Use when deploying simple websites without complex stack requirements.
argument-hint: [domain] [--ssl] [--pm2] [--nginx]
disable-model-invocation: true
---

# Deploy Website Skill

## Usage

```bash
/claude deploy-website --source /path/to/project --domain example.com --ssl --pm2 --nginx
```

## Parameters

- `--source`: Path to the website source code
- `--domain`: Domain name for the website
- `--ssl`: Enable SSL certificate (Let's Encrypt)
- `--pm2`: Use PM2 for process management
- `--nginx`: Configure Nginx as reverse proxy

## Implementation

This skill provides basic website deployment functionality. It handles:
- Environment setup
- Dependency management
- Basic serving configuration
- Optional SSL setup
- Optional process management with PM2
- Optional Nginx reverse proxy configuration

For enhanced deployment with full Ansible integration, use the `deploy-website-enhanced` skill instead.
