#!/usr/bin/env node

const shared = require('./shared');
const path = require('path');

async function handleRequest(request) {
  const basePath = path.join(__dirname, '..');
  const method = request.method || request.action;

  switch (method) {
    case 'list-playbooks':
      const category = request.params?.category || request.category;
      const allPlaybooks = shared.findPlaybooks(basePath);

      if (category) {
        return allPlaybooks.filter(pb => pb.category === category);
      }
      return allPlaybooks;

    default:
      throw new Error(`Unknown method: ${method}`);
  }
}

// Handle incoming requests via STDIN (MCP style)
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
  const category = process.argv[2];
  handleRequest({ method: 'list-playbooks', params: { category } })
    .then(res => console.log(JSON.stringify(res, null, 2)))
    .catch(err => console.error(err));
}