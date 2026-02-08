#!/usr/bin/env node

const shared = require('./shared');
const path = require('path');

async function handleRequest(request) {
  const basePath = path.join(__dirname, '..');
  const requirements = request.params?.requirements || request.requirements;

  if (!requirements) throw new Error('requirements is required');

  const playbooks = shared.findPlaybooks(basePath);
  return shared.suggestPlaybooks(requirements, playbooks);
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