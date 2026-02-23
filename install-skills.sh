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
