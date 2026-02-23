#!/bin/bash
# Enhanced deploy-website skill registration

# This script registers the enhanced deploy-website skill with Claude Code

echo "Registering enhanced deploy-website skill..."

# Create skill directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the enhanced skill files
cp /Users/tranducy/Documents/Project/ansible-script-public/skills/deploy-website-enhanced.py ~/.claude/skills/
cp /Users/tranducy/Documents/Project/ansible-script-public/skills/deploy-website-enhanced.md ~/.claude/skills/

# Make the script executable
chmod +x ~/.claude/skills/deploy-website-enhanced.py

echo "✅ Enhanced deploy-website skill registered successfully!"
echo "Usage: /claude deploy-website-enhanced [options]"
echo ""
echo "Available options:"
echo "  --source PATH      Path to project source code or Git URL"
echo "  --domain DOMAIN    Domain name for production website"
echo "  --ssl              Enable SSL/TLS certificates"
echo "  --pm2              Use PM2 for process management"
echo "  --nginx            Configure Nginx as reverse proxy"
echo "  --database         Set up database"
echo "  --env FILE         Environment variables file (default: .env)"
echo "  --branch BRANCH    Git branch to deploy (default: main)"
echo "  --user USER        Deployment user (default: deploy)"
echo "  --stack STACK      Application stack (lamp, lemp, node, etc.)"
echo "  --database_type TYPE Database type (mysql, postgresql, mongo)"
echo "  --app_type TYPE    Application type (node, python, php)"
echo "  --port PORT        Application port"
echo "  --debug            Enable debug mode"

# Test the enhanced skill
if command -v claude-code && claude-code --version > /dev/null 2>&1; then
    echo ""
    echo "🎉 Enhanced skill is ready to use!"
    echo "Try: /claude deploy-website-enhanced --help"
else
    echo ""
    echo "⚠️  Claude Code is not installed. Please install it first:"
    echo "curl -sSL https://claude.ai/code/install | sh"
fi