'use strict';

const fs = require('fs');
const path = require('path');

const required = ['SUPABASE_URL', 'SUPABASE_ANON_KEY'];
const missing = required.filter((name) => !process.env[name]);
if (missing.length) {
  throw new Error(`Missing Amplify environment variables: ${missing.join(', ')}`);
}

const config = {
  supabaseUrl: process.env.SUPABASE_URL,
  supabaseAnonKey: process.env.SUPABASE_ANON_KEY,
  useEdgeFunction: process.env.USE_EDGE_FUNCTION === 'true',
  email: process.env.CONTACT_EMAIL || 'info@bimrace.com',
  thankYouUrl: '/thank-you.html'
};

const output = `window.BIMRACE_CONFIG = ${JSON.stringify(config, null, 2)};\n`;
fs.writeFileSync(path.join(__dirname, '..', 'site', 'config.js'), output);