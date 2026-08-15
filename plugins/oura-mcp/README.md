# Oura MCP

A private, read-only MCP that gives ChatGPT web and desktop live access to the Oura API v2 data
authorized for one Oura account.

```text
ChatGPT -> OpenAI Secure MCP Tunnel -> Synology NAS -> Oura API
```

- `oura_catalog` lists the mapped Oura collections.
- `oura_query` calls Oura directly and returns its native response with pagination and provenance.

There is no stdio transport, synthetic-data mode, cache, summary layer, warehouse, Auth0, or hosted
cloud service. The NAS stores only the rotating Oura credential; health responses are never stored.

## NAS setup

1. In OpenAI Platform, create a tunnel and a runtime API key with tunnel read/use access.
2. Copy `.env.example` to `.env` and enter the Oura and OpenAI values.
3. In Synology DSM, reverse-proxy the HTTPS hostname used by `OURA_REDIRECT_URI` to
   `http://127.0.0.1:8787`. Register the exact callback URI with Oura. The MCP endpoint rejects
   requests arriving through that public hostname; only the state-validated callback and
   setup-key-protected authorization route are usable there.
4. Start both containers from Synology Container Manager or with:

   ```bash
   docker compose up -d --build
   ```

5. Start the one-time Oura authorization without putting the setup key in a URL:

   ```bash
   curl -X POST -H "X-Setup-Key: $SETUP_KEY" \
     https://your-nas.example.com/admin/oura/authorize
   ```

   Open the returned authorization URL. Oura documents that omitting `scope` requests every scope
   available to the application.

6. Add the created tunnel in ChatGPT. The MCP itself stays private on the Docker network; ChatGPT
   reaches it through the outbound OpenAI tunnel while the development Mac is off.

The OpenAI tunnel is specific to supported OpenAI surfaces. A future Grok, Cursor, or public-plugin
deployment will need a public MCP route, but it does not change the two Oura tools or acquisition code.
