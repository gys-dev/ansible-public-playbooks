#!/usr/bin/env node

const shared = require('./shared');
const path = require('path');

async function handleRequest(request) {
  const basePath = path.join(__dirname, '..');
  const params = request.params || request;

  if (!params.playbook_path) throw new Error('playbook_path is required');

  return shared.executePlaybook(basePath, params);
}

// Handle incoming requests via STDIN
process.stdin.on('data', async (data) => {
  try {
    const request = JSON.parse(data.toString().trim());
    const response = await handleRequest(request);
    process.stdout.write(JSON.stringify(response) + '\n');
  } catch (error) {
    process.stdout.write(JSON.stringify({ error: error.message }) + '\n');
  }
});