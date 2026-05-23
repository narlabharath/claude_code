# §13 MCP — Hands-on Sandbox

This folder is the hands-on material for the §13 MCP section of the walkthrough.

## What's here

```
sandbox/
├── .mcp.json                        ← Consumer demo: filesystem MCP server config
├── docs/
│   └── sample-content/
│       ├── notes-2024-q1.md         ← Engineering notes Q1 2024
│       ├── notes-2024-q2.md         ← Engineering notes Q2 2024
│       └── customer-feedback.csv   ← Customer feedback data
└── mcp-server/
    ├── notes_server.py              ← Provider demo: custom FastMCP server
    └── requirements.txt
```

## Demo A — Consumer side (use an existing MCP server)

**Goal:** Wire the official filesystem MCP server to Claude Code and see the before/after difference.

**Prerequisites:** Node.js installed (for `npx`).

1. Open Claude Code in `sandbox/`:
   ```
   cd sandbox
   claude
   ```

2. Accept the MCP server approval prompt when it appears.

3. Run `/mcp` to verify the server is connected:
   ```
   > /mcp
   ● filesystem  (connected · 8 tools)
   ```

4. Test with these prompts:
   - `"List all files in docs/sample-content"`
   - `"Read notes-2024-q1.md and summarise the key engineering decisions"`
   - `"What were the main reliability improvements documented in Q2?"`
   - `"Find all mentions of 'webhook' across the notes files"`

## Demo B — Provider side (build a custom MCP server)

**Goal:** Build and test a custom MCP server that exposes the same notes folder with richer tools.

**Prerequisites:** Python 3.12+

1. Install dependencies:
   ```
   cd sandbox/mcp-server
   pip install -r requirements.txt
   ```

2. Test with MCP Inspector (no Claude Code needed — opens a UI in your browser):
   ```
   mcp dev notes_server.py
   ```
   Try each tool:
   - `list_notes()` — should return 3 filenames
   - `read_note("notes-2024-q1.md")` — should return the file content
   - `search_notes("webhook")` — should return both q1 and q2 notes

3. Wire into Claude Code — update `sandbox/.mcp.json`:
   ```json
   {
     "mcpServers": {
       "notes": {
         "command": "python",
         "args": ["mcp-server/notes_server.py"]
       }
     }
   }
   ```

4. Open Claude Code in `sandbox/` and run `/mcp`:
   ```
   > /mcp
   ● notes  (connected · 3 tools, 1 resource, 2 prompts)
   ```

5. Test with the bundled prompts:
   - `/mcp__notes__summarize_all_notes`
   - `/mcp__notes__find_action_items`

## What each server exposes

| Capability | Filesystem server | Custom notes server |
|---|---|---|
| `list_directory` | ✓ | → `list_notes()` |
| `read_file` | ✓ | → `read_note(filename)` |
| `search_files` | ✓ | → `search_notes(keyword)` |
| `write_file` | ✓ | ✗ (read-only by design) |
| `notes://index` resource | ✗ | ✓ |
| `summarize_all_notes` prompt | ✗ | ✓ |
| `find_action_items` prompt | ✗ | ✓ |

The filesystem server is broader (full file access). The custom server is narrower but adds structured Prompts and a Resource index — more useful when you want specific behaviours baked in.
