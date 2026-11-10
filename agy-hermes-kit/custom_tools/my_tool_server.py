"""Minimalni custom MCP server (stdio). Zahteva: pip install mcp"""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("custom_tools")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Saberi dva broja (primer alata; zameni svojom logikom)."""
    return a + b


if __name__ == "__main__":
    mcp.run()
