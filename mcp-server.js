#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
    CallToolRequestSchema,
    ListToolsRequestSchema,
    ErrorCode,
    McpError
} = require('@modelcontextprotocol/sdk/types.js');
const shared = require('./scripts/shared');

// Cross-platform PATH configuration to ensure binaries are found
const platform = process.platform;
const separator = platform === 'win32' ? ';' : ':';
const commonPaths = platform === 'win32'
    ? ['C:\\Program Files\\nodejs\\', 'C:\\ProgramData\\chocolatey\\bin']
    : ['/usr/local/bin', '/usr/bin', '/bin', '/usr/sbin', '/sbin'];

const currentPath = process.env.PATH || '';
const paths = currentPath.split(separator);
commonPaths.forEach(p => {
    if (!paths.includes(p) && fs.existsSync(p)) {
        paths.push(p);
    }
});
process.env.PATH = paths.join(separator);

// Read configuration
const configPath = path.join(__dirname, 'mcp-config.json');
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));

/**
 * MCP Server Implementation using official SDK
 */
class AnsibleMCPServer {
    constructor() {
        this.server = new Server(
            {
                name: config.name || "ansible-script-mcp",
                version: config.version || "1.0.0",
            },
            {
                capabilities: {
                    tools: {},
                },
            }
        );

        this.basePath = __dirname;
        this.setupHandlers();

        // Error handling
        this.server.onerror = (error) => console.error('[MCP Error]', error);
        process.on('SIGINT', async () => {
            await this.server.close();
            process.exit(0);
        });
    }

    setupHandlers() {
        // List available tools
        this.server.setRequestHandler(ListToolsRequestSchema, async () => {
            return {
                tools: config.tools,
            };
        });

        // Handle tool calls
        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;

            try {
                const result = await this.executeTool(name, args);
                return {
                    content: [
                        {
                            type: 'text',
                            text: typeof result === 'string' ? result : JSON.stringify(result, null, 2),
                        },
                    ],
                };
            } catch (error) {
                if (error instanceof McpError) {
                    throw error;
                }
                return {
                    content: [
                        {
                            type: 'text',
                            text: `Action failed: ${error.message}`,
                        },
                    ],
                    isError: true,
                };
            }
        });
    }

    async executeTool(name, args = {}) {
        switch (name) {
            case 'list-playbooks':
                const allPlaybooks = shared.findPlaybooks(this.basePath);
                if (args.category) {
                    return allPlaybooks.filter(pb => pb.category === args.category);
                }
                return allPlaybooks;

            case 'get-playbook-info':
                return shared.getPlaybookInfo(this.basePath, args.playbook_path);

            case 'get-variable-schema':
                const varPath = args.playbook_path.replace('.yml', '/vars/default.yml').replace('playbook.yml', 'vars/default.yml');
                const varFullPath = path.join(this.basePath, varPath);
                return shared.getVariableSchema(fs.existsSync(varFullPath) ? varFullPath : '');

            case 'execute-playbook':
                return shared.executePlaybook(this.basePath, args);

            case 'get-host-info':
                return shared.getHostInfo(this.basePath, args.inventory_path);

            case 'get-system-info':
                return shared.getSystemInfo(this.basePath, args.host, args.user);

            case 'suggest-playbook':
                const playbooks = shared.findPlaybooks(this.basePath);
                return shared.suggestPlaybooks(args.requirements, playbooks);

            default:
                throw new McpError(
                    ErrorCode.MethodNotFound,
                    `Unknown tool: ${name}`
                );
        }
    }

    async run() {
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        console.error('Ansible MCP Server running on stdio');
    }
}

const server = new AnsibleMCPServer();
server.run().catch((error) => {
    console.error('Fatal error in server:', error);
    process.exit(1);
});
