# Claude Code Skills

This directory contains custom Claude Code skills for enhanced functionality, specifically focused on website deployment and server management.

## Available Skills

### deploy-website (Basic)
- **Purpose**: Basic production website deployment
- **Features**: Environment setup, dependency management, basic serving
- **Usage**: `/claude deploy-website --source /path/to/project --domain example.com --ssl`
- **When to use**: Simple deployments without complex stack requirements

### deploy-website-enhanced (Recommended)
- **Purpose**: Enhanced production website deployment with full Ansible integration
- **Features**: Complete system configuration, stack support, database integration, advanced monitoring
- **Usage**: `/claude deploy-website-enhanced --source /path/to/project --domain example.com --stack lamp --database --ssl`
- **When to use**: Production deployments requiring full infrastructure setup

## Installation

### Enhanced Skill (Recommended)
```bash
# Register the enhanced skill
./register-deploy-website-enhanced-skill.sh

# Test the skill
/claude deploy-website-enhanced --help
```

### Basic Skill
```bash
# Register the basic skill
./register-deploy-website-skill.sh

# Test the skill
/claude deploy-website --help
```

## Key Differences

| Feature | deploy-website | deploy-website-enhanced |
|---------|----------------|------------------------|
| Ansible Integration | No | **Yes** |
| Stack Support | No | **Yes** (LAMP, LEMP, Node.js, etc.) |
| Database Support | No | **Yes** (MySQL, PostgreSQL, MongoDB) |
| Environment Detection | No | **Yes** (Node.js, Python, PHP) |
| Port Auto-detection | No | **Yes** |
| SSL Management | Basic | **Enhanced** (Let's Encrypt integration) |
| Monitoring | Basic | **Comprehensive** |
| Log Rotation | No | **Yes** |
| Security Hardening | Basic | **Enhanced** |
| Debug Mode | No | **Yes** |

## Usage Examples

### Basic Node.js Deployment
```bash
# Basic deployment
/claude deploy-website --source /var/www/myapp --domain myapp.com --ssl

# Enhanced deployment with monitoring
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --pm2 --nginx --debug
```

### LAMP Stack Deployment
```bash
# Enhanced LAMP stack with MySQL
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --stack lamp --database --database_type mysql
```

### Python/Django Deployment
```bash
# Enhanced Python deployment with PostgreSQL
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --app_type python --database --database_type postgresql
```

### MongoDB + Node.js Stack
```bash
# Enhanced MongoDB + Node.js stack
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --stack mongo_node --database --database_type mongo
```

## Integration with Existing Infrastructure

The enhanced skill fully integrates with the existing Ansible infrastructure:

### Reused Components
- **System Setup**: `common/setup_ubuntu/playbook.yml`
- **User Management**: `common/node-user/playbook.yml`
- **Service Management**: `common/pm2/playbook.yml`, `common/nginx-site/playbook.yml`
- **Database Setup**: Playbooks from `stacks/` directory
- **Security**: SSH key management, firewall configuration

### Enhanced Features
- **Dynamic Configuration**: Automatically updates Ansible variables based on deployment parameters
- **Stack Detection**: Automatically finds and uses appropriate stack playbooks
- **Environment Variables**: Creates and manages environment files for different application types
- **Port Configuration**: Auto-detects and configures application ports
- **SSL Integration**: Enhanced SSL certificate management with Let's Encrypt

## Requirements

### System Requirements
- Ubuntu 18.04/20.04+ (tested)
- Claude Code CLI installed
- Root/sudo access for system configuration
- Domain name with DNS configured
- Git repository access (if using Git source)

### Software Requirements
- Ansible (included in the main project)
- Python 3.6+
- Git
- Node.js/npm (for Node.js applications)
- Python pip (for Python applications)
- MySQL/PostgreSQL/MongoDB (if using databases)

## Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Make sure scripts are executable
chmod +x /Users/tranducy/Documents/Project/ansible-script-public/skills/*.sh
chmod +x /Users/tranducy/Documents/Project/ansible-script-public/skills/*.py

# Run with sudo if needed
sudo ./register-deploy-website-enhanced-skill.sh
```

#### Skill Not Found
```bash
# Check if skill is registered
/claude list-skills

# If not found, re-register the skill
./register-deploy-website-enhanced-skill.sh
```

#### Ansible Issues
```bash
# Check Ansible installation
ansible --version

# Run playbook manually for debugging
ansible-playbook -i hosts common/setup_ubuntu/playbook.yml
```

#### SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Renew certificates manually
sudo certbot renew
```

### Debug Mode
Enable debug mode for detailed error messages:
```bash
/claude deploy-website-enhanced --source /path/to/project --domain example.com --ssl --debug
```

## Support

For issues or feature requests:

1. **Check Documentation**: Review the skill documentation in this directory
2. **Test Manually**: Run Ansible playbooks manually to isolate issues
3. **Check Logs**: Review system logs and skill output
4. **Debug Mode**: Enable debug mode for detailed error messages

## Security Considerations

### SSH Security
- **Key-based Authentication**: Enforces SSH key-based authentication
- **Root Login Disabled**: Disables root login for enhanced security
- **Firewall Configuration**: Configures UFW firewall with appropriate rules
- **User Isolation**: Creates dedicated deployment user with limited privileges

### SSL/TLS Security
- **Let's Encrypt Integration**: Automated SSL certificate setup
- **Strong Cipher Suites**: Configures strong SSL/TLS cipher suites
- **Certificate Renewal**: Automated SSL certificate renewal
- **HSTS Support**: Configures HTTP Strict Transport Security

### Application Security
- **Environment Variables**: Secure management of application secrets
- **Database Security**: Secure database configuration and access controls
- **Firewall Rules**: Appropriate firewall rules for application access
- **Log Management**: Secure log rotation and access controls

## Best Practices

### Security
- Use HTTPS everywhere
- Implement proper firewall rules
- Regular security updates
- Monitor logs for suspicious activity
- Use strong passwords and SSH keys

### Performance
- Enable gzip compression in Nginx
- Use caching for static assets
- Optimize database queries
- Monitor application performance
- Implement load balancing for high traffic

### Reliability
- Set up automated backups
- Implement monitoring and alerting
- Use load balancing for high traffic
- Regular maintenance and updates
- Implement disaster recovery procedures

## Future Enhancements

### Planned Features
- **Multi-server Deployment**: Support for deploying across multiple servers
- **Load Balancer Integration**: Automatic load balancer configuration
- **Container Support**: Docker/Kubernetes integration
- **CI/CD Integration**: Automated deployment pipelines
- **Monitoring Integration**: Integration with monitoring services (Prometheus, Grafana)

### Contributing

1. **Fork the Repository**: Create a fork of the main project
2. **Create Feature Branch**: Create a branch for your feature
3. **Implement Changes**: Make your changes to the skills
4. **Test Thoroughly**: Test your changes with various deployment scenarios
5. **Submit Pull Request**: Submit your changes for review

## License

This project is part of the main Ansible script collection and follows the same licensing terms as the main project.