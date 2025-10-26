/**
 * Simple Echo Bot for Telegram
 * This bot echoes back any message it receives
 *
 * Usage:
 * 1. Create a .env file with: BOT_TOKEN=your_token_here
 * 2. Run: node echo-bot.js
 * 3. Send a message to @BuildYourSiteProBot on Telegram
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load .env file
function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) {
    throw new Error('.env file not found');
  }

  const envContent = fs.readFileSync(envPath, 'utf-8');
  const env = {};

  envContent.split('\n').forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) {
      env[key.trim()] = value.trim();
    }
  });

  return env;
}

const envVars = loadEnv();
const BOT_TOKEN = envVars.BOT_TOKEN;

if (!BOT_TOKEN) {
  console.error('Error: BOT_TOKEN not found in .env file');
  process.exit(1);
}

const BASE_URL = `https://api.telegram.org/bot${BOT_TOKEN}`;

/**
 * Make HTTP request to Telegram API
 */
function makeRequest(method, params) {
  return new Promise((resolve, reject) => {
    const url = new URL(`${BASE_URL}/${method}`);

    // Add parameters to URL
    Object.keys(params).forEach(key => {
      url.searchParams.append(key, params[key]);
    });

    https.get(url, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (!response.ok) {
            reject(new Error(`Telegram API error: ${response.description}`));
          } else {
            resolve(response.result);
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

/**
 * Send a message to a chat
 */
async function sendMessage(chatId, text) {
  try {
    const result = await makeRequest('sendMessage', {
      chat_id: chatId,
      text: text,
      parse_mode: 'HTML'
    });
    console.log(`✓ Message sent to chat ${chatId}`);
    return result;
  } catch (error) {
    console.error(`✗ Failed to send message: ${error.message}`);
  }
}

/**
 * Get updates from Telegram (polling)
 */
async function getUpdates(offset = 0) {
  try {
    const updates = await makeRequest('getUpdates', {
      offset: offset,
      timeout: 30
    });
    return updates;
  } catch (error) {
    console.error(`Error getting updates: ${error.message}`);
    return [];
  }
}

/**
 * Execute a Claude command and return the result
 */
async function executeClaudeCommand(prompt) {
  return new Promise((resolve, reject) => {
    const { spawn } = require('child_process');
    const path = require('path');

    // Try different ways to call claude
    const claudePaths = [
      'claude',
      path.join('C:', 'Users', 'info', 'AppData', 'Roaming', 'npm', 'claude.cmd'),
      path.join('C:', 'Users', 'info', 'AppData', 'Roaming', 'npm', 'claude'),
    ];

    let claudeCmd = claudePaths[0];
    for (const p of claudePaths) {
      try {
        const fs = require('fs');
        if (fs.existsSync(p)) {
          claudeCmd = p;
          break;
        }
      } catch (e) {
        // Continue to next path
      }
    }

    // On Windows, use shell to ensure proper execution
    const child = spawn('cmd.exe', [
      '/c',
      `"${claudeCmd}" --dangerously-skip-permissions --print "${prompt}"`
    ], {
      shell: false,
      windowsHide: true
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    child.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve(stdout);
      } else {
        reject(new Error(`Claude command failed: ${stderr || 'Unknown error'}`));
      }
    });

    child.on('error', (err) => {
      reject(new Error(`Failed to execute Claude: ${err.message}`));
    });

    // Timeout after 60 seconds
    setTimeout(() => {
      child.kill();
      reject(new Error('Claude command timed out (60 seconds)'));
    }, 60000);
  });
}

/**
 * Process incoming updates
 */
async function handleUpdate(update) {
  if (!update.message) {
    return;
  }

  const message = update.message;
  const chatId = message.chat.id;
  const userId = message.from.id;
  const userName = message.from.first_name;
  const text = message.text;

  console.log(`\n[${new Date().toLocaleTimeString()}] Message from ${userName} (ID: ${userId})`);
  console.log(`Chat ID: ${chatId}`);
  console.log(`Text: "${text}"`);

  let response;

  // Check if message starts with "claude:"
  if (text.toLowerCase().startsWith('claude:')) {
    const prompt = text.substring(7).trim(); // Remove "claude:" prefix

    if (!prompt) {
      response = 'Error: Please provide a prompt after "claude:"';
      await sendMessage(chatId, response);
      return;
    }

    console.log(`\n⚡ Executing Claude command: "${prompt}"`);
    await sendMessage(chatId, '⏳ Processing Claude command...');

    try {
      const result = await executeClaudeCommand(prompt);
      response = `<b>Claude Response:</b>\n\n<code>${escapeHtml(result)}</code>`;

      // Split into chunks if too long (Telegram max is 4096 chars)
      if (response.length > 4000) {
        const chunks = response.match(/[\s\S]{1,4000}/g) || [];
        for (const chunk of chunks) {
          await sendMessage(chatId, chunk);
        }
      } else {
        await sendMessage(chatId, response);
      }
      console.log('✓ Claude command completed successfully');
    } catch (error) {
      response = `<b>Error executing Claude command:</b>\n<code>${escapeHtml(error.message)}</code>`;
      await sendMessage(chatId, response);
      console.error(`✗ Claude command failed: ${error.message}`);
    }
  } else {
    // Echo the message back
    response = `Echo: ${text}`;
    await sendMessage(chatId, response);
  }
}

/**
 * Escape HTML special characters for Telegram
 */
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Main polling loop
 */
async function startBot() {
  console.log('🤖 BuildYourSiteProBot started!');
  console.log(`📡 Polling for updates every 30 seconds...`);
  console.log(`🔗 Bot URL: https://t.me/BuildYourSiteProBot\n`);

  // Test the bot connection
  try {
    const me = await makeRequest('getMe', {});
    console.log(`✓ Connected as: @${me.username}`);
    console.log(`✓ Bot ID: ${me.id}\n`);
  } catch (error) {
    console.error(`✗ Failed to connect to Telegram: ${error.message}`);
    console.error('Please check your BOT_TOKEN');
    process.exit(1);
  }

  let lastUpdateId = 0;

  // Polling loop
  setInterval(async () => {
    try {
      const updates = await getUpdates(lastUpdateId + 1);

      for (const update of updates) {
        lastUpdateId = Math.max(lastUpdateId, update.update_id);
        await handleUpdate(update);
      }
    } catch (error) {
      console.error(`Error in polling loop: ${error.message}`);
    }
  }, 1000); // Check for updates every second
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n🛑 Bot stopped');
  process.exit(0);
});

// Start the bot
startBot().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
