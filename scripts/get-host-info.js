#!/usr/bin/env node

const shared = require('./shared');
const path = require('path');

async function handleRequest(request) {
  const basePath = path.join(__dirname, '..');
  const inventoryPath = request.params?.inventory_path || request.inventory_path;

  return shared.getHostInfo(basePath, inventoryPath);
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