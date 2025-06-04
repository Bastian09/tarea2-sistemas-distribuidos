from collections import OrderedDict, defaultdict

class CacheLRU:
    def __init__(self, capacidad):
        self.cache = OrderedDict()
        self.capacidad = capacidad
        self.hits = 0
        self.misses = 0

    def get(self, clave):
        if clave in self.cache:
            self.cache.move_to_end(clave)  # Actualiza el uso reciente
            self.hits += 1
            return self.cache[clave]
        else:
            self.misses += 1
            return None

    def put(self, clave, valor):
        if clave in self.cache:
            self.cache.move_to_end(clave)
        self.cache[clave] = valor
        if len(self.cache) > self.capacidad:
            self.cache.popitem(last=False)  # Elimina el más viejo

class CacheLFU:
    def __init__(self, capacidad):
        self.cache = {}
        self.frecuencias = defaultdict(int)
        self.capacidad = capacidad
        self.hits = 0
        self.misses = 0

    def get(self, clave):
        if clave in self.cache:
            self.frecuencias[clave] += 1
            self.hits += 1
            return self.cache[clave]
        else:
            self.misses += 1
            return None

    def put(self, clave, valor):
        if clave in self.cache:
            self.frecuencias[clave] += 1
        else:
            if len(self.cache) >= self.capacidad:
                # Encontrar la clave menos usada
                clave_menos_usada = min(self.frecuencias, key=self.frecuencias.get)
                del self.cache[clave_menos_usada]
                del self.frecuencias[clave_menos_usada]
            self.cache[clave] = valor
            self.frecuencias[clave] = 1
