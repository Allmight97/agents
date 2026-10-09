# Oura MCP

A private, read-only MCP that gives an agent live access to the Oura API v2 data
authorized for one Oura account. Two tools: `oura_catalog` lists the mapped
collections; `oura_query` calls Oura and returns its native response with
pagination and provenance.

```text
ChatGPT            -> OpenAI Secure MCP Tunnel -> Synology NAS -> Oura API
Claude Code, Grok  -> https://<public hostname>/mcp + bearer token -> NAS -> Oura API
```

There is no stdio transport, synthetic-data mode, cache, summary layer, or
hosted cloud service. The NAS stores only the rotating Oura credential; health
responses are never stored.

## NAS setup

1. In OpenAI Platform, create a tunnel and a runtime API key with tunnel
   read/use access (ChatGPT path).
2. Copy `.env.example` to `.env` and enter the Oura and OpenAI values. For the
   plugin path set `MCP_PUBLIC_HOSTNAME` to the hostname the reverse proxy
   forwards in `Host`, and `MCP_ACCESS_TOKEN` to a fresh secret of at least 32
   characters (`openssl rand -hex 32`). Leave both empty to keep the MCP
   reachable only through the tunnel.
3. In Synology DSM, reverse-proxy the HTTPS hostname used by
   `OURA_REDIRECT_URI` to `http://127.0.0.1:8787`. Register the exact callback
   URI with Oura.
4. Start both containers from Synology Container Manager or with:

   ```bash
   docker compose up -d --build
   ```

5. Start the one-time Oura authorization without putting the setup key in a URL:

   ```bash
   curl -X POST -H "X-Setup-Key: $SETUP_KEY" \
     https://your-nas.example.com/admin/oura/authorize
   ```

   Open the returned authorization URL. Oura documents that omitting `scope`
   requests every scope available to the application.

6. ChatGPT: add the created tunnel. The tunnel client reaches the container by
   its service name `oura-mcp`, which needs no bearer token.

## Who may call `/mcp`

- Host `oura-mcp` (the tunnel client): always. The reverse proxy must preserve
  the public request hostname; it must never rewrite it to `oura-mcp`.
- Public host: accepted only when both `MCP_PUBLIC_HOSTNAME` and
  `MCP_ACCESS_TOKEN` are set. Requests require `Authorization: Bearer <token>`;
  a missing or wrong token returns 401.
- Local diagnostics: `localhost` and `127.0.0.1` are accepted, and require the
  bearer token when one is set. Unknown hosts return 403. Browser origins
  other than ChatGPT and localhost are rejected; CLI clients send no Origin.

An unset or empty access token disables the public hostname even if
`MCP_PUBLIC_HOSTNAME` is configured. Nonempty tokens shorter than 32 characters
refuse startup. Run `npm test` to check these boundaries and the public/tunnel
authentication behavior.

## Claude Code and Grok Build

```bash
claude plugin install oura-mcp@personal
```

The install prompts for the MCP URL (`https://<public hostname>/mcp`) and the
access token; the token goes to the keychain, not to `settings.json`. The
server then appears as `oura` with its two tools, and `/oura-mcp:oura` is a
user-only skill naming their bounds. Grok Build also discovers the installed
Claude plugin and its skill. Grok Build 1.0.46 does not resolve the plugin's
`${user_config.*}` values: its connection test fails with the literal URL
placeholder. Configure a native user MCP entry in `~/.grok/config.toml` to
supply the URL and bearer header; this takes precedence over the plugin's
server definition:

```toml
[mcp_servers.oura]
url = "https://your-nas.example.com/mcp"
headers = { Authorization = "Bearer <MCP_ACCESS_TOKEN>" }
```

Keep that file private when storing a token there. Grok also supports
`${ENVIRONMENT_VARIABLE}` in headers when the variable is present in the
process environment. Verify the installed client's connection with
`grok mcp doctor oura --json`; catalog presence alone does not prove access.

Codex is not in the catalog: a Codex plugin's `mcp.json` carries a URL but no
bearer token. Use ChatGPT's tunnel connection there.
