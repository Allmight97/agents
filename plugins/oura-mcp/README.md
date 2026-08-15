# Oura MCP

A private, read-only Cloudflare Worker that gives ChatGPT live access to the Oura API v2 data
authorized for one Oura account.

- `oura_catalog` lists all mapped Oura collections.
- `oura_query` calls Oura directly and returns its native response with pagination and provenance.

There is no stdio transport, synthetic-data mode, cache, summary layer, warehouse, or Health Command
integration. Auth0 authorizes ChatGPT. A single Durable Object stores and rotates the Oura OAuth
credential; health responses are never stored.

## Deploy

```bash
npm install
npm run check
npx wrangler login
npx wrangler secret put AUTH0_ISSUER
npx wrangler secret put AUTH0_AUDIENCE
npx wrangler secret put OURA_CLIENT_ID
npx wrangler secret put OURA_CLIENT_SECRET
npx wrangler secret put OURA_REDIRECT_URI
npx wrangler secret put SETUP_KEY
npm run deploy
```

Use the deployed `https://oura-mcp.<account>.workers.dev/oauth/oura/callback` as the Oura redirect
URI. Oura documents that omitting the `scope` authorization parameter requests every scope available
to the application.

Start the one-time Oura authorization without putting the setup key in a URL:

```bash
curl -X POST -H "X-Setup-Key: $SETUP_KEY" \
  https://oura-mcp.<account>.workers.dev/admin/oura/authorize
```

Open the returned authorization URL. Then add
`https://oura-mcp.<account>.workers.dev/mcp` to ChatGPT with OAuth authentication.
