"""
Seed knowledge base for Nimbus Support.
~28 articles across 4 categories. This is what the retrieval layer (RAG)
searches over. Add more articles any time from the Knowledge Base page —
no code changes needed.
"""

KB_ARTICLES = [
    # ---------------- Account Access ----------------
    {
        "category": "Account Access",
        "title": "How to reset your password",
        "content": "To reset your Nimbus password: 1) Go to the sign-in page and click 'Forgot password'. 2) Enter your account email and click 'Send reset link'. 3) Check your inbox for an email from support@nimbus.app (also check spam/junk). 4) Click the link and choose a new password of at least 8 characters. 5) Sign in with your new password. Reset links expire after 30 minutes.",
        "keywords": "password reset forgot login locked out cannot sign in",
    },
    {
        "category": "Account Access",
        "title": "Enabling or disabling two-factor authentication (2FA)",
        "content": "To manage 2FA: 1) Sign in and open Settings then Security. 2) Click 'Enable two-factor authentication'. 3) Scan the QR code with an authenticator app such as Google Authenticator, Authy, or 1Password. 4) Enter the 6-digit code to confirm. 5) Save your backup codes somewhere safe. To disable 2FA, open the same Security page and click 'Disable'.",
        "keywords": "2fa mfa two-factor authenticator security code verification",
    },
    {
        "category": "Account Access",
        "title": "How to change your account email address",
        "content": "To change your account email: 1) Go to Settings then Profile. 2) Enter your new email and click 'Save'. 3) We send a confirmation link to the NEW address, you must click it to complete the change. 4) Your old email continues to work for sign-in until the new one is confirmed. If you no longer have access to your old email, contact support with proof of account ownership.",
        "keywords": "change email update email new address",
    },
    {
        "category": "Account Access",
        "title": "I'm locked out and 2FA codes aren't working",
        "content": "If your authenticator codes are being rejected, first check that your phone's clock is set to automatic/network time, since 2FA codes are time-based and drift causes failures. If that doesn't fix it, use one of your saved backup codes from when you enabled 2FA. If you have no backup codes and are fully locked out, this requires manual identity verification by a human agent.",
        "keywords": "locked out 2fa not working backup codes time drift",
    },
    {
        "category": "Account Access",
        "title": "Deleting your account",
        "content": "To permanently delete your account: 1) Go to Settings then Account then Danger Zone. 2) Click 'Delete account'. 3) Confirm by typing your account email. This is irreversible: it deletes your data, tickets, and billing history after a 14-day grace period, during which you can cancel the deletion by signing back in. Active subscriptions are cancelled but not refunded automatically.",
        "keywords": "delete account close account remove account irreversible",
    },
    {
        "category": "Account Access",
        "title": "Managing team members and roles",
        "content": "Admins can invite teammates from Settings then Team then Invite. Roles are Admin (full access, billing), Editor (can edit but not manage billing or delete the workspace), and Viewer (read-only). To change someone's role, click their name in the Team list and select a new role. Only Admins can remove other Admins.",
        "keywords": "team members roles permissions invite admin editor viewer",
    },
    {
        "category": "Account Access",
        "title": "Single sign-on (SSO) setup for Business plans",
        "content": "SSO via SAML 2.0 is available on the Business plan. To set it up: 1) Go to Settings then Security then SSO. 2) Enter your identity provider's metadata URL (Okta, Azure AD, or Google Workspace are supported). 3) Map the email and name attributes. 4) Test with a single user before enforcing SSO for the whole workspace, since enforcing it too early can lock everyone out if misconfigured.",
        "keywords": "sso saml okta azure ad single sign-on enterprise login",
    },

    # ---------------- Billing ----------------
    {
        "category": "Billing",
        "title": "Updating your payment method",
        "content": "To update your payment method: 1) Go to Settings then Billing then Payment methods. 2) Click 'Add new card' or 'Update' on an existing card. 3) Enter your card details, we accept Visa, Mastercard, and Amex, and billing address. 4) Click 'Save'. The new card is charged on your next billing date; there is no way to switch cards mid-cycle for a prorated charge.",
        "keywords": "payment credit card update card billing details payment method",
    },
    {
        "category": "Billing",
        "title": "Changing your subscription plan",
        "content": "To change your plan: 1) Go to Settings then Billing then Subscription. 2) Choose Starter at $9/user/month, Team at $19/user/month, or Business at $39/user/month. 3) Confirm. Upgrades take effect immediately and you're charged a prorated amount for the rest of the current cycle. Downgrades take effect at the start of your next billing cycle, not immediately.",
        "keywords": "change plan upgrade downgrade subscription pricing tier",
    },
    {
        "category": "Billing",
        "title": "Refund policy and requesting a refund",
        "content": "Nimbus offers a 14-day money-back guarantee on all annual plans and first-time monthly subscriptions. To request a refund, email billing@nimbus.app with your invoice number and reason. Refunds for accidental duplicate charges are processed automatically within 5-7 business days once confirmed by billing; refunds outside the 14-day window are reviewed case by case.",
        "keywords": "refund money back duplicate charge billing dispute",
    },
    {
        "category": "Billing",
        "title": "Understanding your invoice and line items",
        "content": "Each invoice lists: the plan tier, number of active seats billed that cycle, any add-ons (extra storage, priority support), applicable tax, and the total. Seat count is based on the highest number of active users at any point in the billing cycle, not the average. You can download PDF invoices from Settings then Billing then Invoice history.",
        "keywords": "invoice line items seats tax total download pdf",
    },
    {
        "category": "Billing",
        "title": "Why was I charged twice this month?",
        "content": "A duplicate-looking charge is usually one of: (a) an annual-to-monthly plan switch generating a prorated charge alongside the regular one, (b) a failed payment retry that succeeded on a second attempt while the first also went through, or (c) adding a seat mid-cycle, which bills the new seat separately. Check Settings then Billing then Invoice history for the itemized breakdown before assuming it's an error.",
        "keywords": "charged twice duplicate charge billing error double charge",
    },
    {
        "category": "Billing",
        "title": "Applying a coupon or promo code",
        "content": "Promo codes can be applied at checkout when starting a new subscription, or from Settings then Billing then 'Add promo code' for an existing subscription. Codes are case-sensitive and typically apply to the next billing cycle rather than retroactively. Only one promo code can be active per workspace at a time.",
        "keywords": "coupon promo code discount voucher",
    },
    {
        "category": "Billing",
        "title": "Failed payment and dunning process",
        "content": "If a card payment fails, we retry automatically after 1, 3, and 7 days. You'll get an email each time. After the third failed retry, the workspace is downgraded to read-only mode until payment succeeds, but no data is deleted. To avoid this, update your card proactively from Settings then Billing before it expires.",
        "keywords": "failed payment card declined dunning read-only downgraded",
    },
    {
        "category": "Billing",
        "title": "Getting a copy of a tax invoice / GST invoice",
        "content": "Tax-compliant invoices (including GST/VAT number if provided) are auto-generated for every charge and available under Settings then Billing then Invoice history. To add your company's tax ID so it appears on future invoices, go to Settings then Billing then Tax information and enter it before your next billing date; it cannot be added retroactively to past invoices.",
        "keywords": "tax invoice gst vat company details business invoice",
    },

    # ---------------- Technical ----------------
    {
        "category": "Technical",
        "title": "The app is slow or freezing",
        "content": "If Nimbus is slow or freezing: 1) Check status.nimbus.app for any ongoing incident. 2) Clear your browser cache or try an incognito window to rule out extensions. 3) Confirm you're on a supported browser (latest Chrome, Firefox, Edge, or Safari). 4) Large workspaces with 10,000+ records can be slower on the dashboard view specifically; switching to list view usually helps. If none of this resolves it, this needs a human agent to check server-side logs.",
        "keywords": "slow freezing lag performance loading unresponsive",
    },
    {
        "category": "Technical",
        "title": "Integrating Nimbus with Slack",
        "content": "To connect Slack: 1) Go to Settings then Integrations then Slack then 'Connect'. 2) Authorize the Nimbus Slack app in your workspace. 3) Choose which channel receives notifications. 4) Pick which event types to forward (new ticket, escalation, resolution). Only workspace Admins can install integrations. Disconnecting removes the webhook but doesn't delete past messages already sent to Slack.",
        "keywords": "slack integration connect webhook notifications",
    },
    {
        "category": "Technical",
        "title": "API authentication and generating an API key",
        "content": "Generate an API key from Settings then Developer then API keys then 'New key'. Include it as a Bearer token in the Authorization header of every request. Keys are shown only once at creation, so store them securely; if lost, revoke and regenerate rather than trying to retrieve the original. Rate limit is 100 requests/minute per key on the Team plan and 500/minute on Business.",
        "keywords": "api key authentication token bearer rate limit developer",
    },
    {
        "category": "Technical",
        "title": "Mobile app not syncing",
        "content": "If the mobile app shows stale data: 1) Pull down on any list screen to force a manual refresh. 2) Check you're signed into the same workspace as the web app, users can accidentally have two accounts. 3) Confirm background app refresh is enabled in your phone's settings for Nimbus. 4) Log out and back in as a last resort, this clears the local cache. Sync typically resumes automatically within 60 seconds of reconnecting to the internet.",
        "keywords": "mobile app sync not syncing stale data refresh",
    },
    {
        "category": "Technical",
        "title": "Browser compatibility and system requirements",
        "content": "Nimbus supports the latest two major versions of Chrome, Firefox, Edge, and Safari. Internet Explorer is not supported. For the desktop app, Windows 10+ and macOS 12+ are required. Some layout issues on very old OS versions are known and won't be fixed since those platforms are past their support window.",
        "keywords": "browser compatibility system requirements supported unsupported",
    },
    {
        "category": "Technical",
        "title": "Setting up webhooks for custom automation",
        "content": "Webhooks let external systems react to Nimbus events in real time. Go to Settings then Developer then Webhooks then 'Add endpoint', paste your HTTPS URL, and select event types like ticket.created or ticket.resolved. Nimbus signs every payload with an HMAC-SHA256 signature in the X-Nimbus-Signature header so you can verify authenticity. Failed deliveries are retried up to 5 times with exponential backoff.",
        "keywords": "webhook automation custom integration hmac signature",
    },
    {
        "category": "Technical",
        "title": "Exporting your data (CSV/JSON)",
        "content": "To export data: 1) Go to Settings then Data then Export. 2) Choose the data type (tickets, contacts, or knowledge base articles). 3) Choose CSV or JSON format. 4) Click 'Generate export'. Large exports (50,000+ rows) are emailed as a download link rather than generated instantly, since they're processed in the background.",
        "keywords": "export data csv json download backup",
    },
    {
        "category": "Technical",
        "title": "Troubleshooting steps failed, app still not working",
        "content": "If you've already tried clearing cache, checking status.nimbus.app, and switching browsers with no luck, this is no longer a self-serve issue. Please note down: the exact error message or screenshot, your browser and OS version, and approximately when it started. This needs to be handed to a human engineer, standard troubleshooting steps have been exhausted.",
        "keywords": "troubleshooting failed still broken persisting issue not working",
    },

    # ---------------- General ----------------
    {
        "category": "General",
        "title": "Contacting human support directly",
        "content": "If you'd rather skip the assistant, you can always reach a human at support@nimbus.app or via the 'Talk to a person' button in the chat widget. Business plan customers get a dedicated Slack Connect channel with a 4-hour response SLA on business days.",
        "keywords": "human support contact talk to a person escalate SLA",
    },
    {
        "category": "General",
        "title": "Nimbus status page and incident history",
        "content": "Live uptime and incident history are published at status.nimbus.app, including past postmortems for any major outage. You can subscribe to email or SMS alerts for future incidents from that page.",
        "keywords": "status page uptime incident outage downtime",
    },
    {
        "category": "General",
        "title": "Data privacy and where data is stored",
        "content": "Nimbus stores customer data in AWS data centers in the US and EU depending on your workspace's selected region, set at creation and not changeable afterward. We are SOC 2 Type II certified and GDPR compliant. Data processing agreements (DPAs) are available on request from privacy@nimbus.app.",
        "keywords": "privacy data storage region gdpr soc2 compliance dpa",
    },
    {
        "category": "General",
        "title": "Requesting a feature",
        "content": "Feature requests can be submitted from the in-app 'Feedback' button or via feedback.nimbus.app, where you can also upvote existing requests. The product team reviews the top-voted requests quarterly; there's no guaranteed timeline for any individual request.",
        "keywords": "feature request feedback roadmap suggestion",
    },
]
