'use strict';
// Generates portal/config.js at deploy time from Amplify environment variables.
// The publishable key is safe in the browser (RLS enforces access); the secret
// key must never be set on the portal app.
const fs = require('fs');
const path = require('path');

const missing = ['SUPABASE_URL', 'SUPABASE_ANON_KEY'].filter((n) => !process.env[n]);
if (missing.length) throw new Error(`Missing Amplify environment variables: ${missing.join(', ')}`);
if (/^sb_secret_|service_role/i.test(process.env.SUPABASE_ANON_KEY)) {
  throw new Error('SUPABASE_ANON_KEY looks like a secret key. Use the publishable key.');
}

const config = { supabaseUrl: process.env.SUPABASE_URL, supabaseAnonKey: process.env.SUPABASE_ANON_KEY };
fs.writeFileSync(path.join(__dirname, 'config.js'),
  `window.BIMRACE_CONFIG = ${JSON.stringify(config, null, 2)};\n`);
console.log('portal/config.js written for', config.supabaseUrl);
