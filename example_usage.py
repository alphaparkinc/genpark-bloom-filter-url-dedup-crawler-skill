"""Example usage for Bloom Filter URL Dedup Crawler."""
from client import BloomFilterUrlDedupCrawler
import json

bf = BloomFilterUrlDedupCrawler(size_bits=65536, hash_count=5)

urls = [
    "https://genpark.ai/about",
    "https://github.com/alphaparkinc",
    "https://genpark.ai/about"  # Duplicate
]

for url in urls:
    is_new = bf.add(url)
    print(f"URL: {url} -> Newly Added: {is_new}")

print("Stats:", json.dumps(bf.stats(), indent=2))
