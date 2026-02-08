#!/usr/bin/env node

const shared = require('./shared');
const path = require('path');
const fs = require('fs');

async function handleRequest(request) {
  const basePath = path.join(__dirname, '..');
  const playbookPath = request.params?.playbook_path || request.playbook_path;

  if (!playbookPath) throw new Error('playbook_path is required');

  const varPath = playbookPath.replace('.yml', '/vars/default.yml').replace('playbook.yml', 'vars/default.yml');
  const varFullPath = path.join(basePath, varPath);

  if (!fs.existsSync(varFullPath)) {
    return { type: 'object', properties: {}, info: "No default variables file found." };
  }

  return shared.getVariableSchema(varFullPath);
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

// Support CLI direct call
if (require.main === module && process.argv.length > 2) {
  handleRequest({ playbook_path: process.argv[2] })
    .then(res => console.log(JSON.stringify(res, null, 2)))
    .catch(err => console.error(err));
}