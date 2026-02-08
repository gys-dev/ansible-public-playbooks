const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Get all playbook files from the project structure
 * @param {string} basePath 
 * @returns {Array} Array of playbook objects
 */
const projectRoot = path.join(__dirname, '..');

function findPlaybooks(basePath = projectRoot) {
    const playbooks = [];

    // Common playbooks - checking subdirectories for playbook.yml
    const commonDir = path.join(basePath, 'common');
    if (fs.existsSync(commonDir)) {
        const commonDirs = fs.readdirSync(commonDir);
        for (const dirName of commonDirs) {
            const dirPath = path.join(commonDir, dirName);
            if (fs.statSync(dirPath).isDirectory()) {
                const playbookPath = path.join(dirPath, 'playbook.yml');
                if (fs.existsSync(playbookPath)) {
                    playbooks.push({
                        path: path.relative(basePath, playbookPath),
                        name: dirName,
                        category: 'common',
                        description: getDescriptionFromPlaybook(playbookPath)
                    });
                }
            }
        }
    }

    // Stack playbooks
    const stacksDir = path.join(basePath, 'stacks');
    if (fs.existsSync(stacksDir)) {
        const stackDirs = fs.readdirSync(stacksDir);
        for (const stackDir of stackDirs) {
            const stackPath = path.join(stacksDir, stackDir);
            if (fs.statSync(stackPath).isDirectory()) {
                const playbookPath = path.join(stackPath, 'playbook.yml');
                if (fs.existsSync(playbookPath)) {
                    playbooks.push({
                        path: path.relative(basePath, playbookPath),
                        name: stackDir,
                        category: 'stacks',
                        description: getDescriptionFromPlaybook(playbookPath)
                    });
                }
            }
        }
    }

    // Role playbooks (excluding community roles)
    const rolesDir = path.join(basePath, 'roles');
    if (fs.existsSync(rolesDir)) {
        const roleDirs = fs.readdirSync(rolesDir);
        for (const roleDir of roleDirs) {
            if (!roleDir.startsWith('geerlingguy')) { // Skip community roles
                const rolePath = path.join(rolesDir, roleDir);
                if (fs.statSync(rolePath).isDirectory()) {
                    const playbookPath = path.join(rolePath, 'tasks', 'main.yml');
                    if (fs.existsSync(playbookPath)) {
                        playbooks.push({
                            path: path.relative(basePath, playbookPath),
                            name: roleDir,
                            category: 'roles',
                            description: getDescriptionFromRole(roleDir)
                        });
                    }
                }
            }
        }
    }

    return playbooks;
}

/**
 * Extract description from first commented line of a playbook
 * @param {string} playbookPath 
 * @returns {string}
 */
function getDescriptionFromPlaybook(playbookPath) {
    try {
        const content = fs.readFileSync(playbookPath, 'utf8');
        const match = content.match(/^#\s*(.*)/m);
        return match ? match[1].trim() : 'No description available';
    } catch (error) {
        return 'No description available';
    }
}

/**
 * Static mapping of role descriptions
 * @param {string} roleName 
 * @returns {string}
 */
function getDescriptionFromRole(roleName) {
    const descriptions = {
        'certbot_nginx': 'SSL certificate automation for Nginx',
        'setup_ubuntu': 'Initial Ubuntu server setup',
        'apache_ubuntu': 'Apache web server installation',
        'nginx-site': 'Nginx site configuration with SSL',
        'docker_ubuntu': 'Docker installation and container management',
        'node-user': 'Node.js user and environment setup',
        'pm2': 'PM2 process management setup',
        'ssh-key-gen': 'SSH key generation',
        'ssh-key-authorize': 'SSH key authorization'
    };
    return descriptions[roleName] || 'Custom role';
}

/**
 * Get detailed information about a playbook
 * @param {string} basePath 
 * @param {string} playbookPath 
 * @returns {Object}
 */
function getPlaybookInfo(basePath, playbookPath) {
    const fullPath = playbookPath.startsWith('/') ? playbookPath : path.join(basePath, playbookPath);
    if (!fs.existsSync(fullPath)) {
        throw new Error(`Playbook not found: ${playbookPath}`);
    }

    const content = fs.readFileSync(fullPath, 'utf8');

    // Associated variables info
    let varPath = playbookPath.replace('.yml', '/vars/default.yml');
    if (!fs.existsSync(path.join(basePath, varPath))) {
        varPath = playbookPath.replace('playbook.yml', 'vars/default.yml');
    }

    const varFullPath = path.join(basePath, varPath);

    return {
        path: playbookPath,
        description: getDescriptionFromPlaybook(fullPath),
        tasks: extractTasks(content),
        handlers: extractHandlers(content),
        variables: fs.existsSync(varFullPath) ? parseVariables(varFullPath) : {}
    };
}

/**
 * Extract tasks from playbook content
 * @param {string} content 
 * @returns {Array}
 */
function extractTasks(content) {
    const tasks = [];
    const taskRegex = /- name:\s*(.*)\n\s*([^\s][^\n]*)/g;
    let match;

    while ((match = taskRegex.exec(content)) !== null) {
        tasks.push({
            name: match[1].trim(),
            action: match[2].trim().split(':')[0]
        });
    }

    return tasks;
}

/**
 * Extract handlers from playbook content
 * @param {string} content 
 * @returns {Array}
 */
function extractHandlers(content) {
    const handlers = [];
    const handlerRegex = /- name:\s*(.*)\n\s*service:/g;
    let match;

    while ((match = handlerRegex.exec(content)) !== null) {
        handlers.push({
            name: match[1].trim()
        });
    }

    return handlers;
}

/**
 * Extract variables from a variables file
 * @param {string} varFilePath 
 * @returns {Object}
 */
function parseVariables(varFilePath) {
    if (!fs.existsSync(varFilePath)) return {};

    const content = fs.readFileSync(varFilePath, 'utf8');
    const variables = {};
    const lines = content.split('\n');

    for (const line of lines) {
        const match = line.match(/^([^\s#:][^:]+):\s*(.*)/);
        if (match) {
            const key = match[1].trim();
            const value = match[2].trim();

            if (value === 'true' || value === 'false') {
                variables[key] = value === 'true';
            } else if (!isNaN(value) && value !== '') {
                variables[key] = Number(value);
            } else {
                variables[key] = value.replace(/^['"]|['"]$/g, '');
            }
        }
    }
    return variables;
}

/**
 * Generate a JSON schema for variables
 * @param {string} varFilePath 
 * @returns {Object}
 */
function getVariableSchema(varFilePath) {
    const vars = parseVariables(varFilePath);
    const schema = {
        type: 'object',
        properties: {}
    };

    for (const [key, value] of Object.entries(vars)) {
        schema.properties[key] = {
            type: typeof value,
            description: `Variable for ${key}`,
            default: value
        };
    }

    return schema;
}

/**
 * Execute an Ansible playbook
 * @param {string} basePath 
 * @param {Object} options 
 * @returns {Object}
 */
function executePlaybook(basePath, { playbook_path, inventory, variables, limit }) {
    const fullPath = playbook_path.startsWith('/') ? playbook_path : path.join(basePath, playbook_path);
    const inventoryPath = inventory ? (inventory.startsWith('/') ? inventory : path.join(basePath, inventory)) : path.join(basePath, 'hosts');

    if (!fs.existsSync(fullPath)) {
        throw new Error(`Playbook not found: ${playbook_path}`);
    }

    let command = `ansible-playbook -i ${inventoryPath} ${fullPath}`;
    if (limit) command += ` --limit "${limit}"`;
    if (variables) {
        for (const [key, value] of Object.entries(variables)) {
            command += ` --extra-vars "${key}=${value}"`;
        }
    }

    try {
        const output = execSync(command, { encoding: 'utf8', stdio: 'pipe' });
        return { success: true, output };
    } catch (error) {
        return {
            success: false,
            output: error.stderr || error.stdout,
            error: error.message
        };
    }
}

/**
 * Get host information from inventory
 * @param {string} basePath 
 * @param {string} inventoryPath 
 * @returns {Object}
 */
function getHostInfo(basePath, inventoryPath) {
    const fullPath = inventoryPath ? (inventoryPath.startsWith('/') ? inventoryPath : path.join(basePath, inventoryPath)) : path.join(basePath, 'hosts');
    if (!fs.existsSync(fullPath)) {
        throw new Error(`Inventory not found: ${fullPath}`);
    }
    return { content: fs.readFileSync(fullPath, 'utf8') };
}

/**
 * Collect system information from a host
 * @param {string} basePath 
 * @param {string} host 
 * @param {string} user 
 * @returns {Object}
 */
function getSystemInfo(basePath, host, user) {
    const userPart = user ? `-u ${user}` : '';
    const inventoryPath = path.join(basePath, 'hosts');
    const command = `ansible ${host} -i ${inventoryPath} ${userPart} -m setup`;

    try {
        const output = execSync(command, { encoding: 'utf8', stdio: 'pipe' });
        const jsonMatch = output.match(/\{[\s\S]*\}/);
        if (!jsonMatch) throw new Error("Could not parse system info output");
        return { success: true, facts: JSON.parse(jsonMatch[0]) };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

/**
 * Suggest playbooks based on requirements
 * @param {string} requirements 
 * @param {Array} playbooks 
 * @returns {Object}
 */
function suggestPlaybooks(requirements, playbooks) {
    const suggestions = [];
    const req = requirements.toLowerCase();

    for (const pb of playbooks) {
        const name = pb.name.toLowerCase();
        const desc = (pb.description || '').toLowerCase();

        if (req.includes(name) || name.includes(req) || desc.includes(req)) {
            suggestions.push(pb);
            continue;
        }

        // Keywords mapping
        const keywords = {
            'web': ['apache', 'nginx', 'lamp', 'lemp', 'wordpress'],
            'database': ['mysql', 'postgres', 'mongo', 'sql'],
            'node': ['node', 'pm2', 'nvm', 'yarn'],
            'security': ['ssh', 'ufw', 'hardening', 'certbot'],
            'docker': ['docker', 'container']
        };

        for (const [key, list] of Object.entries(keywords)) {
            if (req.includes(key)) {
                if (list.some(item => name.includes(item))) {
                    suggestions.push(pb);
                    break;
                }
            }
        }
    }

    // Limit suggestions
    const finalSuggestions = suggestions.slice(0, 5);

    return {
        suggestions: finalSuggestions,
        count: finalSuggestions.length,
        message: finalSuggestions.length > 0 ? 'Found relevant playbooks' : 'No direct matches found'
    };
}

module.exports = {
    findPlaybooks,
    getPlaybookInfo,
    getDescriptionFromPlaybook,
    getDescriptionFromRole,
    extractTasks,
    extractHandlers,
    parseVariables,
    getVariableSchema,
    executePlaybook,
    getHostInfo,
    getSystemInfo,
    suggestPlaybooks
};
