from typing import TypeVar, Generic, List, Optional, Tuple


K = TypeVar('K')
V = TypeVar('V')


class HashTable(Generic[K, V]):
    def __init__(self, size: int):
        self.size = size
        # chaining: table is a list of buckets, bucket is a list of pairs
        self.table: List[List[Tuple[K, V]]] = [[] for _ in range(self.size)]

    def _hash_function(self, key: K) -> int:
        # modulo ensures the index fits within the table's bounds [0 to size-1]
        return hash(key) % self.size

    def insert(self, key: K, value: V) -> bool:
        key_hash = self._hash_function(key)
        bucket = self.table[key_hash]

        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                # if already exists replace the whole tuple
                bucket[i] = (key, value)
                return True

        bucket.append((key, value))
        return True

    def delete(self, key: K) -> bool:
        key_hash = self._hash_function(key)
        bucket = self.table[key_hash]

        for i, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket.pop(i)
                return True
        return False

    def get(self, key: K) -> Optional[V]:
        key_hash = self._hash_function(key)
        bucket = self.table[key_hash]

        for stored_key, stored_value in bucket:
            if stored_key == key:
                return stored_value
        return None


table = HashTable[str, int](3)
table.insert("apple", 10)
table.insert("orange", 20)
table.insert("banana", 30)

print(f"Get apple: {table.get('apple')}")
print(f"Deleted apple? {table.delete('apple')}")
print(f"Get apple after delete: {table.get('apple')}")
