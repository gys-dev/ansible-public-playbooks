# Enhanced Deploy Website Skill

A comprehensive skill for deploying full production websites that integrates seamlessly with the existing Ansible infrastructure.

## Usage

```bash
# Enhanced deployment with all options
/claude deploy-website-enhanced --source /path/to/project --domain example.com --ssl --pm2 --nginx --database --stack lamp --app_type node

# Basic deployment
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl

# Git-based deployment with specific branch
/claude deploy-website-enhanced --source https://github.com/user/repo.git --domain myapp.com --branch develop --ssl --pm2

# Database-specific deployment
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --database --database_type postgresql --app_type python
```

## Parameters

### Required
- `--source`: Path to project source code or Git URL
- `--domain`: Domain name for production website

### Optional
- `--ssl`: Enable SSL/TLS certificates (Let's Encrypt)
- `--pm2`: Use PM2 for process management (Node.js applications)
- `--nginx`: Configure Nginx as reverse proxy
- `--database`: Set up database (MySQL/PostgreSQL/MongoDB)
- `--env`: Environment variables file (default: .env)
- `--branch`: Git branch to deploy (default: main)
- `--user`: Deployment user (default: deploy)
- `--stack`: Application stack (lamp, lemp, node, etc.)
- `--database_type`: Database type (mysql, postgresql, mongo)
- `--app_type`: Application type (node, python, php)
- `--port`: Application port (default: auto-detect)
- `--debug`: Enable debug mode

## Features

### Enhanced Integration
- **Ansible Integration**: Leverages existing playbooks in `common/` and `stacks/` directories
- **Modular Architecture**: Reuses existing Ansible roles and configurations
- **Consistent Patterns**: Follows the same deployment patterns as the main project

### Comprehensive Deployment
- **Environment Setup**: Creates dedicated deployment user, configures SSH, sets up firewall
- **System Configuration**: Uses Ansible playbooks for system setup and package installation
- **Application Deployment**: Git repository cloning, build process execution, configuration management
- **Service Management**: PM2 process management, Nginx reverse proxy, SSL/TLS certificates
- **Database Setup**: MySQL/PostgreSQL/MongoDB configuration and security
- **Monitoring**: Health checks, log rotation, automated backups

### Advanced Features
- **Stack Support**: Deploy complete application stacks (LAMP, LEMP, Node.js, etc.)
- **Database Integration**: Automatic database setup and configuration
- **SSL Management**: Automated SSL certificate setup with Let's Encrypt
- **Environment Detection**: Auto-detects application type and configures accordingly
- **Port Management**: Auto-detects and configures application ports
- **Log Rotation**: Automated log rotation and management
- **SSH Security**: Enhanced SSH key management and security

## Integration with Ansible Infrastructure

This enhanced skill fully integrates with the existing Ansible infrastructure:

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

## Implementation Details

### Environment Preparation
1. **User Creation**: Creates dedicated deployment user with sudo privileges
2. **SSH Configuration**: Generates SSH keys and configures secure access
3. **Firewall Setup**: Configures UFW firewall with appropriate rules
4. **Directory Structure**: Creates organized directory structure for deployment

### System Configuration
1. **Ansible Playbooks**: Runs existing Ansible playbooks for system setup
2. **Package Installation**: Installs required system packages and dependencies
3. **Service Configuration**: Configures system services and startup scripts
4. **Security Hardening**: Applies security best practices and configurations

### Application Deployment
1. **Source Retrieval**: Clones Git repositories or copies source code
2. **Dependency Installation**: Installs application dependencies based on type
3. **Build Process**: Executes build scripts and asset optimization
4. **Configuration Management**: Creates and manages environment files

### Service Management
1. **PM2 Configuration**: Sets up PM2 process management for Node.js applications
2. **Nginx Setup**: Configures Nginx reverse proxy and SSL termination
3. **Database Setup**: Configures and secures databases
4. **Service Startup**: Starts and enables all required services

### SSL Certificate Management
1. **Domain Configuration**: Updates Nginx configuration with custom domain
2. **Certificate Request**: Automatically requests SSL certificates from Let's Encrypt
3. **Certificate Installation**: Installs and configures SSL certificates
4. **Auto-renewal**: Sets up automated SSL certificate renewal

## Security Features

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

## Monitoring and Maintenance

### Service Monitoring
- **PM2 Monitoring**: Process monitoring and health checks
- **Nginx Status**: Nginx service status and configuration validation
- **Database Monitoring**: Database connection and performance monitoring
- **SSL Status**: SSL certificate validity and renewal status

### Log Management
- **Log Rotation**: Automated log rotation and compression
- **Log Aggregation**: Centralized log management and analysis
- **Error Monitoring**: Real-time error detection and alerting
- **Performance Metrics**: Application performance monitoring

### Backup and Recovery
- **Automated Backups**: Scheduled database and configuration backups
- **Disaster Recovery**: Comprehensive disaster recovery procedures
- **Version Control**: Git-based version control for configuration
- **Rollback Support**: Easy rollback to previous versions

## Examples

### Basic Node.js Deployment
```bash
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --pm2 --nginx
```

### LAMP Stack Deployment
```bash
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --stack lamp --database --database_type mysql
```

### Python/Django Deployment
```bash
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --app_type python --database --database_type postgresql
```

### MongoDB + Node.js Stack
```bash
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --stack mongo_node --database --database_type mongo
```

### Debug Mode Deployment
```bash
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --ssl --debug
```

## Error Handling

### Common Issues
1. **Port Conflicts**: Checks for port availability and suggests alternatives
2. **SSL Certificate Failures**: Provides detailed error messages and troubleshooting steps
3. **Database Connection Issues**: Validates database connectivity and configuration
4. **Permission Errors**: Handles file permission issues with appropriate sudo usage

### Troubleshooting Commands
```bash
# Check service status
sudo systemctl status nginx
sudo pm2 status

# Verify SSL certificates
sudo certbot certificates

# Check firewall configuration
sudo ufw status

# Review logs
sudo tail -f /var/log/nginx/error.log
sudo pm2 logs
```

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

## Requirements

- Ubuntu 18.04/20.04+ (tested)
- Claude Code CLI installed
- Root/sudo access for system configuration
- Domain name with DNS configured
- Git repository access (if using Git source)

## Support

For issues or feature requests, please check the skill documentation or create an issue in the project repository.