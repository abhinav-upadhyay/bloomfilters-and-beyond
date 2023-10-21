import hashlib

class BloomFilter:
    def __init__(self, size: int, nhash: int):
        """
        Initialze the bloom filter for given size, and using
        nhash number of hash functions.
        """
        self.size: int = size
        self.nhash: int = nhash

        # Number of bytes required to store size number of elements
        num_bytes: int = (size + 7) // 8 

        # Initialize a bytearry with all zeros
        self.bit_vector = bytearray(([0] * num_bytes))

        self.hash_functions = [hashlib.sha256,
                               hashlib.sha1,
                               hashlib.md5,
                               hashlib.sha384,
                               hashlib.sha512]


    def _hash(self, data: str, seed: int) -> int:
        hasher = self.hash_functions[seed % len(self.hash_functions)]()
        hasher.update(data.encode('utf-8'))
        digest = int(hasher.hexdigest(), 16)
        return digest % self.size

    def add(self, item: str) -> None:
        for i in range(self.nhash):
            index = self._hash(item, seed=i)
            byte_index, bit_index = divmod(index, 8)
            mask = 1 << bit_index
            self.bit_vector[byte_index] |= mask

    def query(self, item: str) -> bool:
        for i in range(self.nhash):
            index = self._hash(item, seed=i)
            byte_index, bit_index = divmod(index, 8)
            mask = 1 << bit_index
            if (self.bit_vector[byte_index] & mask) == 0:
                return False
        return True

if __name__ == "__main__":
    filter_size = 128
    num_hash_functions = 3
    bloom_filter = BloomFilter(filter_size, num_hash_functions)

    # Add some items to the filter
    items_to_add = ["apple", "banana", "cherry"]
    for item in items_to_add:
        bloom_filter.add(item)

    # Check for membership
    items_to_check = ["apple", "banana", "cherry", "grape"]
    for item in items_to_check:
        if bloom_filter.query(item):
            print(f"'{item}' may be in the set.")
        else:
            print(f"'{item}' is definitely not in the set.")
