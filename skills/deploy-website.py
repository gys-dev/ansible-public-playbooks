#!/usr/bin/env python3
"""
Deploy Website Skill Implementation
Handles full production website deployment with environment setup, dependencies, and serving.
"""

import argparse
import subprocess
import sys
import os
import json
import shutil
from pathlib import Path

class DeployWebsiteSkill:
    def __init__(self):
        self.config = {
            'user': 'deploy',
            'home_dir': '/home/deploy',
            'app_dir': '/home/deploy/app',
            'nginx_dir': '/etc/nginx',
            'pm2_dir': '/etc/pm2',
            'ssl_dir': '/etc/letsencrypt'
        }

    def run(self, args):
        """Main entry point for the skill"""
        parser = argparse.ArgumentParser(description='Deploy production website')
        parser.add_argument('--source', required=True, help='Path to project source code')
        parser.add_argument('--domain', required=True, help='Domain name for production website')
        parser.add_argument('--ssl', action='store_true', help='Enable SSL/TLS certificates')
        parser.add_argument('--pm2', action='store_true', help='Use PM2 for process management')
        parser.add_argument('--nginx', action='store_true', help='Configure Nginx as reverse proxy')
        parser.add_argument('--database', action='store_true', help='Set up database')
        parser.add_argument('--env', default='.env', help='Environment variables file')
        parser.add_argument('--branch', default='main', help='Git branch to deploy')
        parser.add_argument('--user', default='deploy', help='Deployment user')

        parsed_args = parser.parse_args(args)

        # Update config with parsed arguments
        self.config.update(vars(parsed_args))

        try:
            self.deploy_website()
            print("\n✅ Deployment completed successfully!")
            print(f"Website is now available at: https://{self.config['domain']}")
            return 0
        except Exception as e:
            print(f"\n❌ Deployment failed: {str(e)}")
            return 1

    def deploy_website(self):
        """Main deployment workflow"""
        print("🚀 Starting production website deployment...")

        # Step 1: Environment Setup
        print("\n1. 📋 Setting up deployment environment...")
        self.setup_environment()

        # Step 2: Dependency Installation
        print("\n2. 📦 Installing system dependencies...")
        self.install_dependencies()

        # Step 3: Application Setup
        print("\n3. 📁 Setting up application...")
        self.setup_application()

        # Step 4: PM2 Configuration
        if self.config['pm2']:
            print("\n4. ⚙️  Configuring PM2 process management...")
            self.configure_pm2()

        # Step 5: Nginx Configuration
        if self.config['nginx']:
            print("\n5. 🌐 Configuring Nginx reverse proxy...")
            self.configure_nginx()

        # Step 6: SSL Certificate Setup
        if self.config['ssl']:
            print("\n6. 🔒 Setting up SSL certificates...")
            self.setup_ssl()

        # Step 7: Service Management
        print("\n7. 🔧 Starting and enabling services...")
        self.manage_services()

        print("\n🎉 Deployment completed!")

    def setup_environment(self):
        """Create deployment user and configure environment"""
        # Create deployment user
        if not self.user_exists(self.config['user']):
            print(f"Creating user: {self.config['user']}")
            subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', self.config['user']], check=True)

        # Create directories
        os.makedirs(self.config['home_dir'], exist_ok=True)
        os.makedirs(self.config['app_dir'], exist_ok=True)

        # Configure SSH
        ssh_dir = f"{self.config['home_dir']}/.ssh"
        os.makedirs(ssh_dir, exist_ok=True)
        subprocess.run(['sudo', 'chmod', '700', ssh_dir], check=True)

        # Configure firewall
        self.configure_firewall()

    def install_dependencies(self):
        """Install system dependencies"""
        # Update package lists
        subprocess.run(['sudo', 'apt', 'update'], check=True)

        # Install common dependencies
        packages = ['curl', 'git', 'build-essential', 'libssl-dev', 'python3-pip']
        subprocess.run(['sudo', 'apt', 'install', '-y'] + packages, check=True)

        # Install Node.js and NPM if needed
        if self.check_for_package('package.json'):
            print("📦 Installing Node.js and NPM...")
            subprocess.run(['curl', '-fsSL', 'https://deb.nodesource.com/setup_lts.x'], check=True)
            subprocess.run(['sudo', '-E', 'bash', '-'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'nodejs'], check=True)

        # Install PM2 if needed
        if self.config['pm2']:
            print("🔧 Installing PM2...")
            subprocess.run(['sudo', 'npm', 'install', '-g', 'pm2'], check=True)

        # Install Nginx if needed
        if self.config['nginx']:
            print("🌐 Installing Nginx...")
            subprocess.run(['sudo', 'apt', 'install', '-y', 'nginx'], check=True)

        # Install SSL tools if needed
        if self.config['ssl']:
            print("🔒 Installing SSL tools...")
            subprocess.run(['sudo', 'apt', 'install', '-y', 'certbot', 'python3-certbot-nginx'], check=True)

    def setup_application(self):
        """Clone and setup the application"""
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

        # Install application dependencies
        if self.check_for_package('package.json'):
            print("📦 Installing Node.js dependencies...")
            subprocess.run(['npm', 'install'], cwd=self.config['app_dir'], check=True)

        if self.check_for_package('requirements.txt'):
            print("📦 Installing Python dependencies...")
            subprocess.run(['pip3', 'install', '-r', 'requirements.txt'], cwd=self.config['app_dir'], check=True)

        # Build application if needed
        if self.check_for_script('build'):
            print("🖥️  Building application...")
            subprocess.run(['npm', 'run', 'build'], cwd=self.config['app_dir'], check=True)

        # Configure environment variables
        self.configure_environment()

    def configure_pm2(self):
        """Reuse existing PM2 configuration"""
        pm2_dir = f"{self.config['app_dir']}/common/pm2"

        if not os.path.exists(pm2_dir):
            print(f"Creating PM2 directory: {pm2_dir}")
            os.makedirs(pm2_dir, exist_ok=True)

            # Copy existing PM2 configuration
            subprocess.run(['cp', '-r', '/Users/tranducy/Documents/Project/ansible-script-public/common/pm2', pm2_dir], check=True)

        print(f"Reusing existing PM2 configuration from: {pm2_dir}")

    def configure_nginx(self):
        """Reuse existing Nginx configuration"""
        nginx_conf_dir = f"{self.config['app_dir']}/common/nginx-site"

        if not os.path.exists(nginx_conf_dir):
            print(f"Creating Nginx directory: {nginx_conf_dir}")
            os.makedirs(nginx_conf_dir, exist_ok=True)

            # Copy existing Nginx configuration
            subprocess.run(['cp', '-r', '/Users/tranducy/Documents/Project/ansible-script-public/common/nginx-site', nginx_conf_dir], check=True)

            # Update variables with custom domain and port
            vars_path = f"{nginx_conf_dir}/vars/default.yml"
            if os.path.exists(vars_path):
                with open(vars_path, 'r') as f:
                    content = f.read()

                content = content.replace('server_name: example.com', f'server_name: {self.config[\"domain\"]}')
                content = content.replace('node_port: 3300', f'node_port: {self.get_port()}')

                with open(vars_path, 'w') as f:
                    f.write(content)

        print(f"Reusing existing Nginx configuration from: {nginx_conf_dir}")

    def setup_ssl(self):
        """Set up SSL certificates"""
        # Create SSL directory
        ssl_dir = f"{self.config['ssl_dir']}/live/{self.config['domain']}"
        os.makedirs(ssl_dir, exist_ok=True)

        # Get SSL certificate
        print(f"Obtaining SSL certificate for {self.config['domain']}...")
        try:
            subprocess.run(['sudo', 'certbot', 'certonly', '--nginx', '-d', self.config['domain'],
                          '--non-interactive', '--agree-tos', '--email', f'admin@{self.config['domain']}',
                          '--keep-until-expiring'], check=True)
            print("✅ SSL certificate obtained successfully")
        except subprocess.CalledProcessError:
            print("⚠️  SSL certificate could not be obtained automatically")
            print("Please run: sudo certbot --nginx -d {}".format(self.config['domain']))

    def manage_services(self):
        """Start and enable services"""
        # Start PM2 application
        if self.config['pm2']:
            print("🔧 Starting PM2 application...")
            subprocess.run(['sudo', 'pm2', 'start', 'ecosystem.config.js'], cwd=self.config['app_dir'], check=True)
            subprocess.run(['sudo', 'pm2', 'save'], check=True)
            subprocess.run(['sudo', 'pm2', 'startup'], check=True)

        # Restart Nginx
        if self.config['nginx']:
            print("🔧 Restarting Nginx...")
            subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'], check=True)
            subprocess.run(['sudo', 'systemctl', 'enable', 'nginx'], check=True)

    def configure_environment(self):
        """Configure environment variables"""
        env_file = f"{self.config['app_dir']}/{self.config['env']}"

        if os.path.exists(env_file):
            print(f"Using existing environment file: {env_file}")
        else:
            print(f"Creating environment file: {env_file}")
            with open(env_file, 'w') as f:
                f.write(f"NODE_ENV=production\n")
                f.write(f"DOMAIN={self.config['domain']}\n")
                f.write(f"PORT={self.get_port()}\n")

                # Add common environment variables
                if self.check_for_package('package.json'):
                    f.write(f"NPM_CONFIG_PRODUCTION=true\n")

                if self.check_for_package('requirements.txt'):
                    f.write(f"PYTHONUNBUFFERED=1\n")

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

    def get_start_script(self):
        """Get the start script for PM2"""
        if self.check_for_package('package.json'):
            # Check for common start scripts
            scripts = ['start', 'server', 'app', 'prod', 'production']
            for script in scripts:
                if self.has_npm_script(script):
                    return f"npm run {script}"

            # Default to npm start
            return "npm start"

        return "index.js"

    def get_port(self):
        """Get the port to use"""
        # Check for common port configurations
        if self.check_for_package('package.json'):
            # Check for port in environment file
            env_file = f"{self.config['app_dir']}/{self.config['env']}"
            if os.path.exists(env_file):
                with open(env_file) as f:
                    for line in f:
                        if line.startswith('PORT='):
                            return line.split('=')[1].strip()

        # Default port
        return "3000"

    def check_for_package(self, filename):
        """Check if a package file exists"""
        return os.path.exists(f"{self.config['app_dir']}/{filename}")

    def has_npm_script(self, script_name):
        """Check if package.json has a specific npm script"""
        package_file = f"{self.config['app_dir']}/package.json"
        if not os.path.exists(package_file):
            return False

        with open(package_file) as f:
            package_data = json.load(f)

        return 'scripts' in package_data and script_name in package_data['scripts']

    def check_for_script(self, script_name):
        """Check if a script exists in package.json"""
        package_file = f"{self.config['app_dir']}/package.json"
        if not os.path.exists(package_file):
            return False

        with open(package_file) as f:
            package_data = json.load(f)

        return 'scripts' in package_data and script_name in package_data['scripts']

    def user_exists(self, username):
        """Check if a user exists"""
        try:
            subprocess.run(['id', '-u', username], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

def main():
    """Main entry point"""
    skill = DeployWebsiteSkill()

    # Parse command line arguments
    import sys
    args = sys.argv[1:]

    # If no arguments, show help
    if not args:
        print("Usage: /claude deploy-website --source /path/to/project --domain example.com [options]")
        print("\nOptions:")
        print("  --source PATH      Path to project source code")
        print("  --domain DOMAIN    Domain name for production website")
        print("  --ssl              Enable SSL/TLS certificates")
        print("  --pm2              Use PM2 for process management")
        print("  --nginx            Configure Nginx as reverse proxy")
        print("  --database         Set up database")
        print("  --env FILE         Environment variables file (default: .env)")
        print("  --branch BRANCH    Git branch to deploy (default: main)")
        print("  --user USER        Deployment user (default: deploy)")
        return 1

    return skill.run(args)

if __name__ == "__main__":
    sys.exit(main())