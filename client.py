"""Bloom Filter URL Dedup Crawler.
100% Python Standard Library.
"""
import math
import hashlib

class BloomFilterUrlDedupCrawler:
    """In-memory Bloom filter for URL and document hash deduplication."""

    def __init__(self, size_bits: int = 65536, hash_count: int = 5):
        self.size_bits = size_bits
        self.hash_count = hash_count
        self.bit_array = 0
        self.items_count = 0

    def _hashes(self, item: str):
        h1 = int(hashlib.md5(item.encode("utf-8")).hexdigest(), 16)
        h2 = int(hashlib.sha1(item.encode("utf-8")).hexdigest(), 16)
        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.size_bits

    def add(self, item: str) -> bool:
        exists = self.might_contain(item)
        for bit_offset in self._hashes(item):
            self.bit_array |= (1 << bit_offset)
        if not exists:
            self.items_count += 1
        return not exists

    def might_contain(self, item: str) -> bool:
        for bit_offset in self._hashes(item):
            if not (self.bit_array & (1 << bit_offset)):
                return False
        return True

    def stats(self) -> dict:
        bits_set = bin(self.bit_array).count("1")
        fpp = math.pow(bits_set / self.size_bits, self.hash_count) if self.size_bits > 0 else 1.0
        return {
            "items_count": self.items_count,
            "size_bits": self.size_bits,
            "bits_set": bits_set,
            "estimated_fpp": round(fpp, 6)
        }
