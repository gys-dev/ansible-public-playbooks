#!/bin/bash

# Install Skills for this project (Claude and Antigravity)

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Global Antigravity skills path
AGENT_SKILLS_BASE="$HOME/.gemini/antigravity/skills"

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

install_claude() {
    print_header "Installing Claude Code skills"
    ./install-claude-skills-dynamic.sh
    
    # Register skills (if directories exist in home)
    if [ -d "$HOME/.claude/skills/deploy-website" ]; then
        print_status "Registering Claude skills..."
        "$HOME/.claude/skills/deploy-website/register.sh" || true
    fi
    if [ -d "$HOME/.claude/skills/deploy-website-enhanced" ]; then
        "$HOME/.claude/skills/deploy-website-enhanced/register.sh" || true
    fi
    
    print_status "Claude Code skills installed and registered successfully"
}

install_agent() {
    print_header "Installing Antigravity Agent skills (Global)"
    
    # Create the global skills directory structure
    mkdir -p "$AGENT_SKILLS_BASE/deploy-website/scripts"
    mkdir -p "$AGENT_SKILLS_BASE/deploy-website-enhanced/scripts"
    
    # Create Antigravity-specific SKILL.md for deploy-website in global dir
    cat > "$AGENT_SKILLS_BASE/deploy-website/SKILL.md" << 'EOF'
---
name: deploy-website
description: Basic production website deployment with environment setup, dependency management, and basic serving. Use when deploying simple websites without complex stack requirements.
---

# Deploy Website Skill (Global)

This skill allows Antigravity to perform a basic production website deployment.

## Usage

I should execute the deployment script in this folder with the appropriate arguments:

```bash
python3 "$HOME/.gemini/antigravity/skills/deploy-website/scripts/deploy.py" --source <path> --domain <domain> [options]
```

## Parameters
- `--source`: Path to the website source (local directory or Git URL)
- `--domain`: Domain name for the website
- `--ssl`: Enable SSL certificate (Let's Encrypt)
- `--pm2`: Use PM2 for process management
- `--nginx`: Configure Nginx as reverse proxy
EOF

    # Create Antigravity-specific SKILL.md for deploy-website-enhanced in global dir
    cat > "$AGENT_SKILLS_BASE/deploy-website-enhanced/SKILL.md" << 'EOF'
---
name: deploy-website-enhanced
description: Enhanced production website deployment with full Ansible integration. Use for complex stacks requiring system configuration, database integration, and advanced monitoring.
---

# Enhanced Deploy Website Skill (Global Ansible Integrated)

This skill enables comprehensive production deployments leveraging the project's Ansible infrastructure.

## Usage

I should execute the enhanced deployment script with options matching the target stack:

```bash
python3 "$HOME/.gemini/antigravity/skills/deploy-website-enhanced/scripts/deploy.py" --source <path> --domain <domain> --stack <stack_type> [options]
```

## Parameters
- `--source`: Path to source code or Git URL
- `--domain`: Target domain name
- `--stack`: Application stack (`lamp`, `lemp`, `node`, `python`, `docker`)
- `--database`: Enable database setup
- `--database_type`: Database type (`mysql`, `postgresql`, `mongo`)
- `--ssl`: Enable SSL certificate
- `--debug`: Enable verbose logging
EOF

    # Copy implementation scripts
    if [ -f "skills/base/deploy-website.py" ]; then
        cp "skills/base/deploy-website.py" "$AGENT_SKILLS_BASE/deploy-website/scripts/deploy.py"
    else
        print_warning "Source script skills/base/deploy-website.py not found"
    fi

    if [ -f "skills/base/deploy-website-enhanced.py" ]; then
        cp "skills/base/deploy-website-enhanced.py" "$AGENT_SKILLS_BASE/deploy-website-enhanced/scripts/deploy.py"
    else
        print_warning "Source script skills/base/deploy-website-enhanced.py not found"
    fi
    
    # Make executable
    chmod +x "$AGENT_SKILLS_BASE/deploy-website/scripts/deploy.py" 2>/dev/null || true
    chmod +x "$AGENT_SKILLS_BASE/deploy-website-enhanced/scripts/deploy.py" 2>/dev/null || true
    
    print_status "Antigravity Agent skills installed successfully to $AGENT_SKILLS_BASE"
    print_status "These skills are now available globally for your Antigravity assistant."
}

show_help() {
    echo "Usage: ./install-skills.sh [option]"
    echo ""
    echo "Options:"
    echo "  --claude    Install Claude Code skills (to ~/.claude/skills)"
    echo "  --agent     Install Antigravity Agent skills (to ~/.gemini/antigravity/skills)"
    echo "  --all       Install both Claude and Agent skills"
    echo "  --help      Show this help message"
}

# Main logic
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

case "$1" in
    --claude)
        install_claude
        ;;
    --agent)
        install_agent
        ;;
    --all)
        install_claude
        install_agent
        ;;
    --help)
        show_help
        ;;
    *)
        echo "Unknown option: $1"
        show_help
        exit 1
        ;;
esac

print_status "Task completed successfully"
