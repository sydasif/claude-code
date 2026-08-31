#!/usr/bin/env node
/**
 * Pre-Edit Analysis Hook for Claude Code
 * Runs cleanup-code analysis BEFORE file edits to identify:
 * - Unused imports
 * - Dead helpers  
 * - Stale docs
 * - Duplicated logic
 * - YAGNI violations
 * Logs findings; does NOT block the edit.
 *
 * Setup in .claude/settings.json:
 * {
 *   "hooks": {
 *     "PreToolUse": [{
 *       "matcher": "Write|Edit",
 *       "hooks": [{ "type": "command", "command": "node /path/to/pre-edit-analysis.js" }]
 *     }],
 *     "PostToolUse": [{
 *       "matcher": "Write|Edit",
 *       "hooks": [{ "type": "command", "command": "node /path/to/format-code.js" }]
 *     }]
 *   }
 * }
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const LOG_DIR = path.join(process.env.HOME, '.claude', 'hooks-logs');

function log(data) {
  try {
    if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
    const file = path.join(LOG_DIR, `${new Date().toISOString().slice(0, 10)}.jsonl`);
    fs.appendFileSync(file, JSON.stringify({ ts: new Date().toISOString(), hook: 'pre-edit-analysis', ...data }) + '\n');
  } catch { }
}

// Simple Python analysis: find potential unused imports and large functions
function analyzePythonFile(filepath) {
  const results = [];
  try {
    if (!fs.existsSync(filepath)) return results;
    const content = fs.readFileSync(filepath, 'utf8');
    // Very basic analysis - check for common patterns
    // In a real implementation, this would use the cleanup-code skill
    
    // Check for import statements
    const importRegex = /^import\s+(.+)$|^from\s+(.+)\s+import/mg;
    let match;
    const imports = [];
    while ((match = importRegex.exec(content)) !== null) {
      imports.push(match[1] || match[2]);
    }
    
    results.push({
      type: 'info',
      message: `File: ${path.basename(filepath)}`,
      findings: `Found ${imports.length} import statements`
    });
    
    // Count function definitions (simple regex)
    const funcRegex = /def\s+(\w+)\s*\(/g;
    const funcMatches = content.match(funcRegex) || [];
    results.push({
      type: 'info', 
      message: `Functions found: ${funcMatches.length}`
    });
    
  } catch (e) {
    results.push({
      type: 'error',
      message: `Analysis failed: ${e.message}`
    });
  }
  return results;
}

async function main() {
  let input = '';
  for await (const chunk of process.stdin) input += chunk;

  let data;
  try {
    data = JSON.parse(input);
  } catch (e) {
    log({ level: 'ERROR', error: e.message });
    return console.log('{}');
  }

  const { tool_name, tool_input, session_id } = data;

  if (!['Write', 'Edit'].includes(tool_name)) {
    return console.log('{}');
  }

  if (!tool_input?.file_path) {
    return console.log('{}');
  }

  const filePath = tool_input.file_path;
  const ext = path.extname(filePath).toLowerCase();
  
  // Only analyze Python files for now
  if (ext === '.py') {
    const results = analyzePythonFile(filePath);
    for (const r of results) {
      log({ level: 'INFO', ...r, file: filePath, session_id });
    }
    // Always allow the edit; just report findings
  }

  console.log('{}');
}

if (require.main === module) {
  main();
} else {
  module.exports = { main, analyzePythonFile };
}