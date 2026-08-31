#!/usr/bin/env node
/**
 * Post-Edit Validation Hook for Claude Code
 * Runs linting and basic validation AFTER file edits to catch regressions.
 * Runs ruff check on Python files; can be extended with pytest execution.
 * Logs results; does NOT block the edit (blocking should be done consciously).
 *
 * Setup in .claude/settings.json:
 * {
 *   "hooks": {
 *     "PostToolUse": [{
 *       "matcher": "Write|Edit",
 *       "hooks": [{ "type": "command", "command": "node /path/to/post-edit-validation.js" }]
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
    fs.appendFileSync(file, JSON.stringify({ ts: new Date().toISOString(), hook: 'post-edit-validation', ...data }) + '\n');
  } catch { }
}

// Run ruff check on a Python file
function runRuffCheck(filepath) {
  try {
    const result = spawnSync('uv', ['run', 'ruff', 'check', '--fix', '--exit-zero', '--quiet', filepath], {
      cwd: path.dirname(filepath),
      stdio: 'pipe',
      timeout: 60000
    });
    
    const stderr = result.stderr?.toString().trim();
    const stdout = result.stdout?.toString().trim();
    
    if (result.status === 0) {
      return { status: 'pass', messages: [], output: stdout || '' };
    }
    
    const messages = (stderr || stdout || '').split('\n').filter(m => m.length > 0);
    return { status: 'fail', messages, output: stderr || stdout || `ruff check exited with code ${result.status}` };
  } catch (e) {
    return { status: 'error', messages: [e.message], output: e.message };
  }
}

// Run a quick syntax check on Python files
function syntaxCheck(filepath) {
  try {
    const result = spawnSync('python3', ['-c', 'import sys, py_compile; py_compile.compile(sys.argv[1], doraise=True)', filepath], {
      cwd: path.dirname(filepath),
      stdio: 'pipe',
      timeout: 30000
    });
    
    if (result.status === 0) {
      return { status: 'pass' };
    }
    return { status: 'fail', message: result.stderr?.toString().trim() || 'Syntax error' };
  } catch (e) {
    return { status: 'error', message: e.message };
  }
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
  
  // Validate Python files
  if (ext === '.py') {
    // Syntax check first
    const syntaxResult = syntaxCheck(filePath);
    if (syntaxResult.status !== 'pass') {
      log({ level: 'ERROR', type: 'syntax', message: syntaxResult.message, file: filePath, session_id });
    }
    
    // Ruff check
    const ruffResult = runRuffCheck(filePath);
    if (ruffResult.status === 'fail') {
      log({ level: 'WARNING', type: 'lint', messages: ruffResult.messages, file: filePath, session_id });
      // Log each message
      for (const msg of ruffResult.messages) {
        log({ level: 'WARNING', type: 'lint', message: msg, file: filePath, session_id });
      }
    } else if (ruffResult.status === 'pass') {
      log({ level: 'INFO', type: 'lint', message: 'No lint issues found', file: filePath, session_id });
    }
  }

  console.log('{}');
}

if (require.main === module) {
  main();
} else {
  module.exports = { main, runRuffCheck, syntaxCheck };
}