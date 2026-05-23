"""
notes_server.py — minimal MCP server for the s-mcp hands-on demo.

This is the provider-side demo: build a custom MCP server that exposes
the sample-content notes folder as Tools, a Resource, and a Prompt.

INSTALL (one-time):
    pip install "mcp[cli]>=1.26.0"

TEST with MCP Inspector (no Claude Code needed):
    mcp dev notes_server.py

WIRE INTO CLAUDE CODE:
    Replace the filesystem server in .mcp.json with:
      "notes": { "command": "python", "args": ["mcp-server/notes_server.py"] }
    Then open Claude Code in the sandbox/ folder and run /mcp.
"""

import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes")

# Path is relative to this file's location; resolves to sandbox/docs/sample-content
_NOTES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "docs", "sample-content")
)


# ── Tools ────────────────────────────────────────────────────────────────────

@mcp.tool()
def list_notes() -> list[str]:
    """List all available note files in the notes directory."""
    return sorted(os.listdir(_NOTES_DIR))


@mcp.tool()
def read_note(filename: str) -> str:
    """Read the contents of a specific note file.

    Args:
        filename: Name of the file to read (use list_notes() first to see options).
    """
    # Prevent path traversal
    resolved = os.path.abspath(os.path.join(_NOTES_DIR, filename))
    if not resolved.startswith(_NOTES_DIR + os.sep) and resolved != _NOTES_DIR:
        return "Error: invalid filename"
    if not os.path.isfile(resolved):
        return f"Not found: {filename}"
    with open(resolved, encoding="utf-8") as f:
        return f.read()


@mcp.tool()
def search_notes(keyword: str) -> list[str]:
    """Search for a keyword across all note files. Returns matching filenames.

    Args:
        keyword: Text to search for (case-insensitive).
    """
    keyword_lower = keyword.lower()
    matches = []
    for fname in sorted(os.listdir(_NOTES_DIR)):
        fpath = os.path.join(_NOTES_DIR, fname)
        if os.path.isfile(fpath):
            with open(fpath, encoding="utf-8") as f:
                if keyword_lower in f.read().lower():
                    matches.append(fname)
    return matches


# ── Resources ─────────────────────────────────────────────────────────────────

@mcp.resource("notes://index")
def notes_index() -> str:
    """Formatted index of all note files with their sizes."""
    lines = ["# Notes directory index\n"]
    for fname in sorted(os.listdir(_NOTES_DIR)):
        fpath = os.path.join(_NOTES_DIR, fname)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            lines.append(f"- {fname}  ({size} bytes)")
    return "\n".join(lines)


# ── Prompts ───────────────────────────────────────────────────────────────────

@mcp.prompt()
def summarize_all_notes() -> str:
    """Summarize the contents of every note in the directory."""
    return (
        "Use list_notes() to get the file list, then read_note() for each file. "
        "Produce a one-paragraph summary per file, then a one-line overall summary."
    )


@mcp.prompt()
def find_action_items() -> str:
    """Find open action items and unresolved issues across all notes."""
    return (
        "Use list_notes() and read_note() to read all files. "
        "Extract every open question, unresolved issue, or action item. "
        "Group them by theme and list them clearly."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
