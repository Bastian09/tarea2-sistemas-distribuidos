from cache import CacheLRU, CacheLFU

def probar_lru():
    print("Probando Cache LRU...")
    cache = CacheLRU(capacidad=3)

    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)

    print(cache.get("a"))  # HIT
    cache.put("d", 4)      # Elimina "b" (el más viejo no usado)

    print(cache.get("b"))  # MISS
    print(cache.get("c"))  # HIT

    print(f"Hits: {cache.hits}, Misses: {cache.misses}")

def probar_lfu():
    print("\nProbando Cache LFU...")
    cache = CacheLFU(capacidad=3)

    cache.put("x", 10)
    cache.put("y", 20)
    cache.put("z", 30)

    print(cache.get("x"))  # HIT
    print(cache.get("x"))  # HIT
    print(cache.get("y"))  # HIT

    cache.put("w", 40)  # Elimina "z" (menos usado)

    print(cache.get("z"))  # MISS
    print(cache.get("w"))  # HIT

    print(f"Hits: {cache.hits}, Misses: {cache.misses}")

if __name__ == "__main__":
    probar_lru()
    probar_lfu()
