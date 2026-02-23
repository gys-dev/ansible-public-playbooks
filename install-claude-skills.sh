#!/bin/bash

# Install Claude Code Skills - Template for new machines
# This script installs the custom Claude Code skills to the user's home directory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Claude Code is installed
check_claude_code() {
    print_status "Checking if Claude Code is installed..."
    if ! command -v claude &> /dev/null; then
        print_error "Claude Code CLI is not installed. Please install it first:"
        print_error "  curl -sSL https://code.claude.com/install.sh | sh"
        exit 1
    fi

    print_status "Claude Code is installed"
}

# Create skills directories
create_directories() {
    print_status "Creating skills directories..."

    # Create main skills directory
    mkdir -p ~/.claude/skills

    # Create deploy-website skill directory
    mkdir -p ~/.claude/skills/deploy-website/scripts

    # Create deploy-website-enhanced skill directory
    mkdir -p ~/.claude/skills/deploy-website-enhanced/scripts

    print_status "Skills directories created successfully"
}

# Install deploy-website skill
install_deploy_website() {
    print_status "Installing deploy-website skill..."

    # Create SKILL.md
    cat > ~/.claude/skills/deploy-website/SKILL.md << 'EOF'
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
EOF

    # Copy script
    cp /Users/tranducy/Documents/Project/ansible-script-public/skills/deploy-website.py ~/.claude/skills/deploy-website/scripts/deploy.py

    # Make executable
    chmod +x ~/.claude/skills/deploy-website/scripts/deploy.py

    print_status "deploy-website skill installed successfully"
}

# Install deploy-website-enhanced skill
install_deploy_website_enhanced() {
    print_status "Installing deploy-website-enhanced skill..."

    # Create SKILL.md
    cat > ~/.claude/skills/deploy-website-enhanced/SKILL.md << 'EOF'
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
EOF

    # Copy script
    cp /Users/tranducy/Documents/Project/ansible-script-public/skills/deploy-website-enhanced.py ~/.claude/skills/deploy-website-enhanced/scripts/deploy.py

    # Make executable
    chmod +x ~/.claude/skills/deploy-website-enhanced/scripts/deploy.py

    print_status "deploy-website-enhanced skill installed successfully"
}

# Create registration scripts
create_registration_scripts() {
    print_status "Creating registration scripts..."

    # Create register script for basic skill
    cat > ~/.claude/skills/deploy-website/register.sh << 'EOF'
#!/bin/bash

# Register deploy-website skill

print_status() {
    echo "[INFO] $1"
}

print_status "Registering deploy-website skill..."

# Check if skill is already registered
if claude list-skills | grep -q "deploy-website"; then
    print_status "deploy-website skill is already registered"
    exit 0
fi

# Register the skill
claude skill register ~/.claude/skills/deploy-website/SKILL.md

if [ $? -eq 0 ]; then
    print_status "deploy-website skill registered successfully"
    print_status "Usage: /claude deploy-website --help"
else
    print_status "Failed to register deploy-website skill"
    exit 1
fi
EOF

    # Create register script for enhanced skill
    cat > ~/.claude/skills/deploy-website-enhanced/register.sh << 'EOF'
#!/bin/bash

# Register deploy-website-enhanced skill

print_status() {
    echo "[INFO] $1"
}

print_status "Registering deploy-website-enhanced skill..."

# Check if skill is already registered
if claude list-skills | grep -q "deploy-website-enhanced"; then
    print_status "deploy-website-enhanced skill is already registered"
    exit 0
fi

# Register the skill
claude skill register ~/.claude/skills/deploy-website-enhanced/SKILL.md

if [ $? -eq 0 ]; then
    print_status "deploy-website-enhanced skill registered successfully"
    print_status "Usage: /claude deploy-website-enhanced --help"
else
    print_status "Failed to register deploy-website-enhanced skill"
    exit 1
fi
EOF

    # Make registration scripts executable
    chmod +x ~/.claude/skills/deploy-website/register.sh
    chmod +x ~/.claude/skills/deploy-website-enhanced/register.sh

    print_status "Registration scripts created successfully"
}

# Create installation script for the project
create_project_install_script() {
    print_status "Creating project installation script..."

    cat > /Users/tranducy/Documents/Project/ansible-script-public/install-skills.sh << 'EOF'
#!/bin/bash

# Install Claude Code Skills for this project

set -e

print_status() {
    echo "[INFO] $1"
}

print_status "Installing Claude Code skills..."

# Install both skills
./install-claude-skills.sh

# Register skills
~/.claude/skills/deploy-website/register.sh
~/.claude/skills/deploy-website-enhanced/register.sh

print_status "Claude Code skills installed and registered successfully"
print_status "Available skills:"
print_status "  /claude deploy-website"
print_status "  /claude deploy-website-enhanced"
EOF

    chmod +x /Users/tranducy/Documents/Project/ansible-script-public/install-skills.sh

    print_status "Project installation script created successfully"
}

# Create uninstall script
create_uninstall_script() {
    print_status "Creating uninstall script..."

    cat > /Users/tranducy/Documents/Project/ansible-script-public/uninstall-skills.sh << 'EOF'
#!/bin/bash

# Uninstall Claude Code Skills

set -e

print_status() {
    echo "[INFO] $1"
}

print_status "Uninstalling Claude Code skills..."

# Unregister skills
if claude list-skills | grep -q "deploy-website"; then
    claude skill unregister deploy-website
    print_status "deploy-website skill unregistered"
fi

if claude list-skills | grep -q "deploy-website-enhanced"; then
    claude skill unregister deploy-website-enhanced
    print_status "deploy-website-enhanced skill unregistered"
fi

# Remove directories
rm -rf ~/.claude/skills/deploy-website
rm -rf ~/.claude/skills/deploy-website-enhanced

print_status "Claude Code skills uninstalled successfully"
EOF

    chmod +x /Users/tranducy/Documents/Project/ansible-script-public/uninstall-skills.sh

    print_status "Uninstall script created successfully"
}

# Create README
create_readme() {
    print_status "Creating README file..."

    cat > /Users/tranducy/Documents/Project/ansible-script-public/CLAUDE-SKILLS-README.md << 'EOF'
# Claude Code Skills Installation

This directory contains custom Claude Code skills for enhanced website deployment functionality.

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

### On a New Machine

1. **Install Claude Code CLI** (if not already installed):
   ```bash
   curl -sSL https://code.claude.com/install.sh | sh
   ```

2. **Clone this repository** (if not already cloned):
   ```bash
   git clone <repository-url>
   cd ansible-script-public
   ```

3. **Run the installation script**:
   ```bash
   ./install-claude-skills.sh
   ```

4. **Register the skills**:
   ```bash
   ./install-skills.sh
   ```

### Manual Installation

If you prefer manual installation, you can run:

```bash
# Install skills to user directory
./install-claude-skills.sh

# Register skills
~/.claude/skills/deploy-website/register.sh
~/.claude/skills/deploy-website-enhanced/register.sh
```

## Usage

After installation, you can use the skills with the `/` prefix:

```bash
# Basic deployment
/claude deploy-website --source /path/to/project --domain example.com --ssl

# Enhanced deployment with Ansible integration
/claude deploy-website-enhanced --source /path/to/project --domain example.com --stack lamp --database --ssl
```

## Uninstallation

To remove the skills:

```bash
./uninstall-skills.sh
```

## File Structure

```
~/.claude/skills/
├── deploy-website/
│   ├── SKILL.md              # Skill definition
│   ├── register.sh           # Registration script
│   └── scripts/
│       └── deploy.py         # Implementation script
├── deploy-website-enhanced/
│   ├── SKILL.md              # Skill definition
│   ├── register.sh           # Registration script
│   └── scripts/
│       └── deploy.py         # Implementation script
```

## Requirements

- Claude Code CLI installed
- Python 3.6+ for deployment scripts
- Ansible (included in the main project)
- Root/sudo access for system configuration

## Troubleshooting

### Skill Not Found

If the skill is not found after installation:

```bash
# Check if skill is registered
claude list-skills

# Re-register the skill
~/.claude/skills/deploy-website/register.sh
~/.claude/skills/deploy-website-enhanced/register.sh
```

### Permission Issues

Ensure all scripts have executable permissions:

```bash
chmod +x ~/.claude/skills/deploy-website/register.sh
chmod +x ~/.claude/skills/deploy-website-enhanced/register.sh
```

## Support

For issues or questions about the skills, check the skill documentation or contact the project maintainers.
EOF

    print_status "README file created successfully"
}

# Main installation function
main() {
    print_status "Starting Claude Code Skills installation..."

    # Check prerequisites
    check_claude_code

    # Create directories
    create_directories

    # Install skills
    install_deploy_website
    install_deploy_website_enhanced

    # Create registration scripts
    create_registration_scripts

    # Create project scripts
    create_project_install_script
    create_uninstall_script

    # Create README
    create_readme

    print_status "Claude Code Skills installation completed successfully!"
    print_status ""
    print_status "Next steps:"
    print_status "1. Run './install-skills.sh' to register the skills"
    print_status "2. Use the skills with: /claude deploy-website or /claude deploy-website-enhanced"
    print_status "3. Check 'CLAUDE-SKILLS-README.md' for more information"
}

# Run the installation
main "$@"