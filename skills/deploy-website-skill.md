# Deploy Website Skill

A comprehensive skill for deploying full production websites with automated environment setup, dependency management, and production serving.

## Usage
```bash
# Deploy a production website
/claude deploy-website --source /path/to/project --domain example.com --ssl

# Deploy with custom configuration
/claude deploy-website --source /path/to/project --domain example.com --ssl --pm2 --nginx --database
```

## Parameters

### Required
- `--source`: Path to the project source code
- `--domain`: Domain name for the production website

### Optional
- `--ssl`: Enable SSL/TLS certificates (Let's Encrypt)
- `--pm2`: Use PM2 for process management (Node.js applications)
- `--nginx`: Configure Nginx as reverse proxy
- `--database`: Set up database (MySQL/PostgreSQL)
- `--env`: Environment variables file (default: .env)
- `--branch`: Git branch to deploy (default: main)
- `--user`: Deployment user (default: deploy)

## Features

### Environment Setup
- Creates dedicated deployment user
- Configures SSH keys and permissions
- Sets up firewall (UFW) rules
- Installs system dependencies

### Dependency Management
- Node.js/NPM dependencies installation
- Python requirements installation
- System package installation
- Environment variable configuration

### Code Deployment
- Git repository cloning and checkout
- Build process execution
- Configuration file management
- Asset optimization

### Production Serving
- PM2 process management for Node.js apps
- Nginx reverse proxy configuration
- SSL/TLS certificate setup with Let's Encrypt
- Health check endpoints
- Log rotation and monitoring

## Implementation

### 1. Environment Preparation
```bash
# Create deployment user
sudo useradd -m -s /bin/bash deploy

# Configure SSH
sudo mkdir -p /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh

# Set up firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. Dependency Installation
```bash
# Install Node.js and NPM
sudo apt update
sudo apt install -y curl
sudo curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install PM2
sudo npm install -g pm2

# Install Nginx
sudo apt install -y nginx

# Install SSL tools
sudo apt install -y certbot python3-certbot-nginx
```

### 3. Application Setup
```bash
# Clone repository
git clone https://github.com/user/repo.git /home/deploy/app
cd /home/deploy/app
git checkout main

# Install dependencies
npm install

# Build application
npm run build

# Configure environment
cp .env.example .env
```

### 4. PM2 Configuration
```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'production-app',
    script: 'dist/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production'
    },
    error_file: '/var/log/pm2/error.log',
    out_file: '/var/log/pm2/out.log',
    log_file: '/var/log/pm2/combined.log',
    merge_logs: true,
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z'
  }]
};
```

### 5. Nginx Configuration
```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 6. SSL Certificate Setup
```bash
# Obtain SSL certificate
sudo certbot --nginx -d example.com --non-interactive --agree-tos --email admin@example.com

# Auto-renew SSL certificates
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 7. Service Management
```bash
# Start PM2 application
sudo pm2 start ecosystem.config.js
sudo pm2 save
sudo pm2 startup

# Configure Nginx
sudo systemctl enable nginx
sudo systemctl restart nginx

# Set up log rotation
sudo logrotate -f /etc/logrotate.d/pm2
```

## Security Configuration

### Firewall Rules
```bash
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```

### SSH Security
```bash
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd
```

### SSL Hardening
```nginx
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

## Monitoring and Maintenance

### Health Checks
```bash
# PM2 health check
sudo pm2 status
sudo pm2 logs
sudo pm2 monit

# Nginx status
sudo systemctl status nginx
sudo nginx -t

# SSL certificate status
sudo certbot certificates
```

### Backup and Recovery
```bash
# Database backup
sudo mysqldump -u root -p database_name > backup.sql

# Configuration backup
sudo tar -czf /backup/config.tar.gz /etc/nginx /home/deploy/app
```

## Integration with Ansible

The skill integrates with existing Ansible infrastructure:

### Ansible Playbook Integration
```yaml
- name: Deploy production website
  hosts: webservers
  become: yes
  tasks:
    - name: Install dependencies
      apt: name={{ item }} state=present
      loop: [nginx, nodejs, npm, certbot]

    - name: Clone repository
      git: repo=https://github.com/user/repo.git dest=/home/deploy/app version=main

    - name: Install PM2 globally
      npm: name=pm2 global=yes

    - name: Configure Nginx
      template: src=nginx.conf dest=/etc/nginx/sites-available/example.com

    - name: Enable site
      file: src=/etc/nginx/sites-available/example.com dest=/etc/nginx/sites-enabled/example.com state=link

    - name: Restart services
      service: name={{ item }} state=restarted
      loop: [nginx, pm2]
```

## Error Handling

### Common Issues
1. **Port conflicts**: Check if port 80/443 is already in use
2. **SSL certificate failures**: Verify domain DNS configuration
3. **PM2 process failures**: Check application logs
4. **Nginx configuration**: Validate syntax with `nginx -t`

### Troubleshooting Commands
```bash
# Check port usage
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Check logs
sudo tail -f /var/log/nginx/error.log
sudo pm2 logs

# Verify SSL
sudo certbot certificates
sudo openssl s_client -connect example.com:443 -servername example.com
```

## Best Practices

### Security
- Use HTTPS everywhere
- Implement proper firewall rules
- Regular security updates
- Monitor logs for suspicious activity

### Performance
- Enable gzip compression in Nginx
- Use caching for static assets
- Optimize database queries
- Monitor application performance

### Reliability
- Set up automated backups
- Implement monitoring and alerting
- Use load balancing for high traffic
- Regular maintenance and updates

## Examples

### Basic Deployment
```bash
/claude deploy-website --source /var/www/myapp --domain myapp.com --ssl
```

### Advanced Deployment with Database
```bash
/claude deploy-website --source /var/www/myapp --domain myapp.com --ssl --pm2 --nginx --database --env .env.prod
```

### Git-based Deployment
```bash
/claude deploy-website --source https://github.com/user/repo.git --domain myapp.com --branch develop --ssl
```