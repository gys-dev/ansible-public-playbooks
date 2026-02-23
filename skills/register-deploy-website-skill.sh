#!/bin/bash
# deploy-website skill registration

# This script registers the deploy-website skill with Claude Code

echo "Registering deploy-website skill..."

# Create skill directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the skill files
cp /Users/tranducy/Documents/Project/ansible-script-public/skills/deploy-website.py ~/.claude/skills/
cp /Users/tranducy/Documents/Project/ansible-script-public/skills/deploy-website-skill.md ~/.claude/skills/

# Make the script executable
chmod +x ~/.claude/skills/deploy-website.py

echo "✅ deploy-website skill registered successfully!"
echo "Usage: /claude deploy-website --source /path/to/project --domain example.com [options]"
echo ""
echo "Available options:"
echo "  --source PATH      Path to project source code"
echo "  --domain DOMAIN    Domain name for production website"
echo "  --ssl              Enable SSL/TLS certificates"
echo "  --pm2              Use PM2 for process management"
echo "  --nginx            Configure Nginx as reverse proxy"
echo "  --database         Set up database"
echo "  --env FILE         Environment variables file (default: .env)"
echo "  --branch BRANCH    Git branch to deploy (default: main)"
echo "  --user USER        Deployment user (default: deploy)"

# Test the skill
if command -v claude-code && claude-code --version > /dev/null 2&&1; then
    echo ""
    echo "🎉 Skill is ready to use!"
else
    echo ""
    echo "⚠️  Claude Code is not installed. Please install it first:"
    echo "curl -sSL https://claude.ai/code/install | sh"
fi