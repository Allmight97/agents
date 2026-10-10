"""Cost, time and tool calls per benchmark subagent run, read from a Claude Code session's transcripts.

Usage: python3 cost.py <session transcript dir>
  e.g. ~/.claude/projects/-Users-jstar-Projects-audiobook-boss/<session id>
Prices are $/MTok (input, output, cache read); update them when the price list changes.
"""
import glob
import json
import re
import sys
from datetime import datetime

PRICE = {
    'claude-opus-5-5': (4.0, 20.0, 0.20),
    'claude-sonnet-5-5': (2.0, 10.0, 0.20),
    'claude-haiku-5-5': (0.10, 0.50, 0.01),
}


def parse_ts(ts):
    return datetime.fromisoformat(ts.replace('Z', '+00:00'))


def request_cost(model, usage):
    price_in, price_out, price_read = PRICE[model]
    writes = usage.get('cache_creation') or {}
    write_5m = writes.get('ephemeral_5m_input_tokens', usage.get('cache_creation_input_tokens', 0))
    write_1h = writes.get('ephemeral_1h_input_tokens', 0)
    return (
        usage['input_tokens'] * price_in
        + usage.get('cache_read_input_tokens', 0) * price_read
        + write_5m * price_in * 1.25
        + write_1h * price_in * 2
        + usage['output_tokens'] * price_out
    ) / 1e6


def run_row(meta_path):
    desc = json.load(open(meta_path)).get('description', '')
    if not re.match(r'(bench|b2) ', desc):
        return None
    task, combo = desc.split()[1:3]
    cost = 0.0
    tools = 0
    seen = set()
    model = None
    first = last = None
    for line in open(meta_path.replace('.meta.json', '.jsonl')):
        entry = json.loads(line)
        if entry.get('timestamp'):
            first = first or entry['timestamp']
            last = entry['timestamp']
        msg = entry.get('message') or {}
        if msg.get('role') == 'assistant':
            tools += sum(1 for b in msg.get('content') or [] if isinstance(b, dict) and b.get('type') == 'tool_use')
        usage = msg.get('usage')
        if not usage or msg.get('id') in seen:
            continue
        seen.add(msg.get('id'))
        model = msg.get('model')
        cost += request_cost(model, usage)
    secs = (parse_ts(last) - parse_ts(first)).total_seconds() if first else 0
    return task, combo, model, tools, round(cost, 4), round(secs)


rows = sorted(filter(None, (run_row(m) for m in glob.glob(f'{sys.argv[1]}/subagents/*.meta.json'))))
print('task combo model tool_calls usd seconds')
for row in rows:
    print(*row)
