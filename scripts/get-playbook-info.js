#!/usr/bin/env node

const shared = require('./shared');
const path = require('path');

async function handleRequest(request) {
  const basePath = path.join(__dirname, '..');
  const method = request.method || request.action;

  switch (method) {
    case 'list-playbooks':
      return shared.findPlaybooks(basePath);

    case 'get-playbook-info':
      const playbookPath = request.params?.playbook_path || request.playbook_path;
      if (!playbookPath) throw new Error('playbook_path is required');
      return shared.getPlaybookInfo(basePath, playbookPath);

    default:
      throw new Error(`Unknown method: ${method}`);
  }
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
  handleRequest({
    method: 'get-playbook-info',
    params: { playbook_path: process.argv[2] }
  }).then(result => {
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  }).catch(err => {
    console.error(err.message);
    process.exit(1);
  });
}