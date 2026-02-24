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
   ./install-claude-skills-dynamic.sh
   ```

4. **Register the skills**:
   ```bash
   ./install-skills.sh
   ```

### Manual Installation

If you prefer manual installation, you can run:

```bash
# Install skills to user directory
./install-claude-skills-dynamic.sh

# Register skills
~/.claude/skills/deploy-website/register.sh
~/.claude/skills/deploy-website-enhanced/register.sh
```

## Usage

After installation, you can use the skills with the `/` prefix:

```bash
# Basic deployment
/claude deploy-website --source /var/www/myapp --domain myapp.com --ssl

# Enhanced deployment with Ansible integration
/claude deploy-website-enhanced --source /var/www/myapp --domain myapp.com --stack lamp --database --ssl
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
