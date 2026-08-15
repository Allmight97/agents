# Oura MCP

The current proof has one job: let ChatGPT web reach a hosted Streamable HTTP MCP while the
development Mac is off.

It exposes two read-only tools:

- `oura_catalog` lists the 19 mapped Oura API v2 collections.
- `oura_query` returns bounded synthetic data in the envelope the live Oura response will use.

It does not yet call Oura. It has no stdio transport, summary layer, cache, database, container,
deployment-provider configuration, or test framework.

## Run

Use Python 3.13:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app.py --check
.venv/bin/python app.py
```

Set the four values in `.env.example` through the selected host's secret settings. The host only
needs to run the final command at a public HTTPS URL and route `/mcp` to the process.

Auth0 authenticates ChatGPT to this MCP. The official MCP SDK publishes the OAuth resource metadata;
the service verifies the Auth0 token on every request.

After ChatGPT discovers and calls both tools from the hosted proof, add the Oura API call and Oura
OAuth token handling behind `oura_query`.
