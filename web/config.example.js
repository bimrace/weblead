/* ============================================================================
   BIMRACE — public runtime configuration.
   Copy to config.js and fill in. SAFE TO PUBLISH: the anon key is designed to
   be public and is constrained by RLS.
   NEVER put the service_role key in this file or anywhere in /web.
   ========================================================================== */
window.BIMRACE_CONFIG = {
  supabaseUrl: 'https://YOUR-PROJECT.supabase.co',
  supabaseAnonKey: 'YOUR_ANON_PUBLISHABLE_KEY',

  // false = browser inserts straight into crm.enquiry_submissions (RLS-protected).
  // true  = route through the lead-intake Edge Function for rate limiting,
  //         Turnstile verification and IP hashing. Deploy the function first.
  useEdgeFunction: false,

  email: 'info@bimrace.com',
  thankYouUrl: '/thank-you.html'
};
