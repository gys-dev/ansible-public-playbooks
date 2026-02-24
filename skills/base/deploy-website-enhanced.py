#!/usr/bin/env python3
"""
Enhanced Deploy Website Skill
Integrates with existing Ansible infrastructure for comprehensive website deployment
"""

import argparse
import subprocess
import sys
import os
import json
import shutil
from pathlib import Path
import tempfile
import zipfile

class EnhancedDeployWebsiteSkill:
    def __init__(self):
        self.config = {
            'user': 'deploy',
            'home_dir': '/home/deploy',
            'app_dir': '/home/deploy/app',
            'nginx_dir': '/etc/nginx',
            'pm2_dir': '/etc/pm2',
            'ssl_dir': '/etc/letsencrypt',
            'ansible_dir': '/Users/tranducy/Documents/Project/ansible-script-public',
            'common_dir': '/Users/tranducy/Documents/Project/ansible-script-public/common',
            'stacks_dir': '/Users/tranducy/Documents/Project/ansible-script-public/stacks'
        }

    def run(self, args):
        """Main entry point for the enhanced skill"""
        parser = argparse.ArgumentParser(description='Enhanced production website deployment')
        parser.add_argument('--source', required=True, help='Path to project source code or Git URL')
        parser.add_argument('--domain', required=True, help='Domain name for production website')
        parser.add_argument('--ssl', action='store_true', help='Enable SSL/TLS certificates')
        parser.add_argument('--pm2', action='store_true', help='Use PM2 for process management')
        parser.add_argument('--nginx', action='store_true', help='Configure Nginx as reverse proxy')
        parser.add_argument('--database', action='store_true', help='Set up database')
        parser.add_argument('--env', default='.env', help='Environment variables file')
        parser.add_argument('--branch', default='main', help='Git branch to deploy')
        parser.add_argument('--user', default='deploy', help='Deployment user')
        parser.add_argument('--stack', help='Application stack (lamp, lemp, node, etc.)')
        parser.add_argument('--database_type', help='Database type (mysql, postgresql, mongo)')
        parser.add_argument('--app_type', help='Application type (node, python, php)')
        parser.add_argument('--port', type=int, help='Application port')
        parser.add_argument('--debug', action='store_true', help='Enable debug mode')

        parsed_args = parser.parse_args(args)

        # Update config with parsed arguments
        self.config.update(vars(parsed_args))

        try:
            self.deploy_website()
            print("\n✅ Enhanced deployment completed successfully!")
            print(f"Website is now available at: https://{self.config['domain']}")
            return 0
        except Exception as e:
            print(f"\n❌ Enhanced deployment failed: {str(e)}")
            if self.config.get('debug'):
                import traceback
                traceback.print_exc()
            return 1

    def deploy_website(self):
        """Main enhanced deployment workflow"""
        print("🚀 Starting enhanced production website deployment...")

        # Step 1: Environment Preparation
        print("\n1. 📋 Setting up enhanced deployment environment...")
        self.setup_enhanced_environment()

        # Step 2: System Configuration
        print("\n2. 🖥️  Configuring system with Ansible...")
        self.configure_system_with_ansible()

        # Step 3: Application Deployment
        print("\n3. 📁 Setting up application with Ansible...")
        self.deploy_application_with_ansible()

        # Step 4: Service Configuration
        print("\n4. ⚙️  Configuring services with Ansible...")
        self.configure_services_with_ansible()

        # Step 5: SSL Certificate Setup
        if self.config['ssl']:
            print("\n5. 🔒 Setting up SSL certificates with Ansible...")
            self.setup_ssl_with_ansible()

        # Step 6: Finalization
        print("\n6. 🔧 Starting and enabling services...")
        self.finalize_services()

        print("\n🎉 Enhanced deployment completed!")

    def setup_enhanced_environment(self):
        """Create enhanced deployment environment"""
        # Create deployment user
        if not self.user_exists(self.config['user']):
            print(f"Creating enhanced deployment user: {self.config['user']}")
            subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', self.config['user']], check=True)

        # Create directories
        os.makedirs(self.config['home_dir'], exist_ok=True)
        os.makedirs(self.config['app_dir'], exist_ok=True)
        os.makedirs(f"{self.config['home_dir']}/.ssh", exist_ok=True)
        subprocess.run(['sudo', 'chmod', '700', f"{self.config['home_dir']}/.ssh"], check=True)

        # Configure firewall
        self.configure_firewall()

        # Set up SSH keys
        self.setup_ssh_keys()

    def configure_system_with_ansible(self):
        """Configure system using existing Ansible playbooks"""
        # Run setup_ubuntu playbook
        print("🔗 Running system setup playbook...")
        self.run_ansible_playbook('common/setup_ubuntu/playbook.yml')

        # Run node-user playbook if needed
        if self.config.get('app_type') == 'node':
            print("📦 Configuring Node.js user environment...")
            self.run_ansible_playbook('common/node-user/playbook.yml')

        # Run docker_ubuntu if needed
        if self.config.get('stack') == 'docker':
            print("🐳 Configuring Docker environment...")
            self.run_ansible_playbook('common/docker_ubuntu/playbook.yml')

    def deploy_application_with_ansible(self):
        """Deploy application using Ansible"""
        # Clone repository or copy source
        if self.config['source'].startswith('http'):
            print(f"Cloning repository: {self.config['source']}")
            subprocess.run(['git', 'clone', self.config['source'], self.config['app_dir']], check=True)
            subprocess.run(['git', '-C', self.config['app_dir'], 'checkout', self.config['branch']], check=True)
        else:
            source_path = Path(self.config['source'])
            if not source_path.exists():
                raise Exception(f"Source directory not found: {self.config['source']}")

            print(f"Copying source from: {self.config['source']}")
            if source_path.is_dir():
                subprocess.run(['sudo', 'cp', '-r', str(source_path), self.config['app_dir']], check=True)
            else:
                raise Exception("Source must be a directory")

        # Configure application environment
        self.configure_application_environment()

    def configure_services_with_ansible(self):
        """Configure services using Ansible"""
        # Configure PM2 if needed
        if self.config['pm2']:
            print("⚡ Configuring PM2 with Ansible...")
            self.run_ansible_playbook('common/pm2/playbook.yml')

        # Configure Nginx if needed
        if self.config['nginx']:
            print("🌐 Configuring Nginx with Ansible...")
            self.run_ansible_playbook('common/nginx-site/playbook.yml')

        # Configure database if needed
        if self.config['database']:
            print("🗄️  Configuring database with Ansible...")
            if self.config.get('database_type') == 'mysql':
                # Find and run MySQL playbook
                mysql_playbook = self.find_playbook('mysql')
                if mysql_playbook:
                    self.run_ansible_playbook(mysql_playbook)
            elif self.config.get('database_type') == 'postgresql':
                postgresql_playbook = self.find_playbook('postgresql')
                if postgresql_playbook:
                    self.run_ansible_playbook(postgresql_playbook)
            elif self.config.get('database_type') == 'mongo':
                mongo_playbook = self.find_playbook('mongo')
                if mongo_playbook:
                    self.run_ansible_playbook(mongo_playbook)

    def setup_ssl_with_ansible(self):
        """Set up SSL certificates using Ansible"""
        # Update Nginx configuration with domain
        nginx_vars = f"{self.config['ansible_dir']}/common/nginx-site/vars/default.yml"
        if os.path.exists(nginx_vars):
            with open(nginx_vars, 'r') as f:
                content = f.read()

            content = content.replace('server_name: example.com', f'server_name: {self.config["domain"]}')
            content = content.replace('node_port: 3300', f'node_port: {self.config.get("port", 3000)}')

            with open(nginx_vars, 'w') as f:
                f.write(content)

        # Run SSL certificate setup
        print("🔐 Setting up SSL certificates with Ansible...")
        self.run_ansible_playbook('common/nginx-site/playbook.yml')

    def finalize_services(self):
        """Start and enable final services"""
        # Start PM2 application
        if self.config['pm2']:
            print("⚡ Starting PM2 application...")
            subprocess.run(['sudo', 'pm2', 'start', 'ecosystem.config.js'], cwd=self.config['app_dir'], check=True)
            subprocess.run(['sudo', 'pm2', 'save'], check=True)
            subprocess.run(['sudo', 'pm2', 'startup'], check=True)

        # Restart Nginx
        if self.config['nginx']:
            print("🌐 Restarting Nginx...")
            subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'], check=True)
            subprocess.run(['sudo', 'systemctl', 'enable', 'nginx'], check=True)

        # Set up log rotation
        self.setup_log_rotation()

    def configure_application_environment(self):
        """Configure application environment variables"""
        env_file = f"{self.config['app_dir']}/{self.config['env']}"

        if os.path.exists(env_file):
            print(f"Using existing environment file: {env_file}")
        else:
            print(f"Creating environment file: {env_file}")
            with open(env_file, 'w') as f:
                f.write(f"NODE_ENV=production\n")
                f.write(f"DOMAIN={self.config['domain']}\n")
                f.write(f"PORT={self.config.get('port', 3000)}\n")

                # Add common environment variables
                if self.config.get('app_type') == 'node':
                    f.write(f"NPM_CONFIG_PRODUCTION=true\n")

                if self.config.get('app_type') == 'python':
                    f.write(f"PYTHONUNBUFFERED=1\n")

    def setup_log_rotation(self):
        """Set up log rotation"""
        print("📝 Setting up log rotation...")
        # Create logrotate configuration
        logrotate_config = f"/etc/logrotate.d/{self.config['user']}"
        logrotate_content = f"""
{self.config['home_dir']}/logs/*.log {{
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 {self.config['user']} {self.config['user']}
    postrotate
        sudo pm2 reload all > /dev/null
    endscript
}}
"""
        with open(logrotate_config, 'w') as f:
            f.write(logrotate_content)

    def configure_firewall(self):
        """Configure firewall rules"""
        print("🔒 Configuring firewall...")
        try:
            subprocess.run(['sudo', 'ufw', 'allow', '22'], check=True)
            subprocess.run(['sudo', 'ufw', 'allow', '80'], check=True)
            subprocess.run(['sudo', 'ufw', 'allow', '443'], check=True)
            subprocess.run(['sudo', 'ufw', 'enable'], check=True)
            print("✅ Firewall configured successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Could not configure firewall automatically")

    def setup_ssh_keys(self):
        """Set up SSH keys for deployment"""
        print("🔐 Setting up SSH keys...")
        ssh_dir = f"{self.config['home_dir']}/.ssh"
        subprocess.run(['sudo', 'chmod', '700', ssh_dir], check=True)

        # Generate SSH key if it doesn't exist
        private_key = f"{ssh_dir}/id_rsa"
        if not os.path.exists(private_key):
            print("🔑 Generating SSH key pair...")
            subprocess.run(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-f', private_key, '-N', ''], check=True)

        # Authorize the public key
        public_key = f"{private_key}.pub"
        if os.path.exists(public_key):
            with open(public_key, 'r') as f:
                public_key_content = f.read().strip()

            authorized_keys = f"{ssh_dir}/authorized_keys"
            with open(authorized_keys, 'a') as f:
                f.write(public_key_content + '\n')

            subprocess.run(['sudo', 'chmod', '600', authorized_keys], check=True)

    def run_ansible_playbook(self, playbook_path):
        """Run an Ansible playbook"""
        full_path = f"{self.config['ansible_dir']}/{playbook_path}"
        if not os.path.exists(full_path):
            print(f"⚠️  Playbook not found: {full_path}")
            return

        print(f"🔧 Running Ansible playbook: {playbook_path}")
        subprocess.run(['ansible-playbook', '-i', 'hosts', full_path], check=True)

    def find_playbook(self, keyword):
        """Find a playbook by keyword"""
        # Search in common directory
        common_playbooks = Glob(path=self.config['common_dir'], pattern=f"**/{keyword}*.yml")
        if common_playbooks:
            return f"common/{keyword}/{keyword}.yml"

        # Search in stacks directory
        stacks_playbooks = Glob(path=self.config['stacks_dir'], pattern=f"**/{keyword}*.yml")
        if stacks_playbooks:
            return f"stacks/{keyword}/{keyword}.yml"

        return None

    def user_exists(self, username):
        """Check if a user exists"""
        try:
            subprocess.run(['id', '-u', username], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

def main():
    """Main entry point"""
    skill = EnhancedDeployWebsiteSkill()

    # Parse command line arguments
    import sys
    args = sys.argv[1:]

    # If no arguments, show help
    if not args:
        print("Usage: /claude deploy-website --source /path/to/project --domain example.com [options]")
        print("\nEnhanced options:")
        print("  --source PATH      Path to project source code or Git URL")
        print("  --domain DOMAIN    Domain name for production website")
        print("  --ssl              Enable SSL/TLS certificates")
        print("  --pm2              Use PM2 for process management")
        print("  --nginx            Configure Nginx as reverse proxy")
        print("  --database         Set up database")
        print("  --env FILE         Environment variables file (default: .env)")
        print("  --branch BRANCH    Git branch to deploy (default: main)")
        print("  --user USER        Deployment user (default: deploy)")
        print("  --stack STACK      Application stack (lamp, lemp, node, etc.)")
        print("  --database_type TYPE Database type (mysql, postgresql, mongo)")
        print("  --app_type TYPE    Application type (node, python, php)")
        print("  --port PORT        Application port")
        print("  --debug            Enable debug mode")
        return 1

    return skill.run(args)

if __name__ == "__main__":
    sys.exit(main())