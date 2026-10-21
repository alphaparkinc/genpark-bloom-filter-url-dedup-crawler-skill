"""MCP Server for Bloom Filter URL Dedup Crawler.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import BloomFilterUrlDedupCrawler

bf = BloomFilterUrlDedupCrawler()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "add_item",
                                "description": "Add URL or item to Bloom filter and check if it was newly added",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "item": {"type": "string"}
                                    },
                                    "required": ["item"]
                                }
                            },
                            {
                                "name": "might_contain",
                                "description": "Probabilistically check if URL or item is already seen in Bloom filter",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "item": {"type": "string"}
                                    },
                                    "required": ["item"]
                                }
                            },
                            {
                                "name": "get_stats",
                                "description": "Get Bloom filter capacity and false positive probability stats",
                                "inputSchema": {"type": "object"}
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "add_item":
                    res = {"item": args.get("item"), "is_new": bf.add(args.get("item", ""))}
                elif call_name == "might_contain":
                    res = {"item": args.get("item"), "might_contain": bf.might_contain(args.get("item", ""))}
                elif call_name == "get_stats":
                    res = bf.stats()
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
