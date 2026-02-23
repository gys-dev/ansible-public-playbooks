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
