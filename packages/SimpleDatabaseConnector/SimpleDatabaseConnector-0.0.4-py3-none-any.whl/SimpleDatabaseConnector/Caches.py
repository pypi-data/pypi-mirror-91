import hashlib, sys, copy, atexit, os, pickle

class DatabaseCache:
    def __init__(self, cache_location="", size_limit=20, mem_limit=4096, hash_algo="sha256"):
        self.cache = dict()
        self.order = []

        self.cache_path = cache_location + "cache.bin"

        self.hash_algo = hash_algo
        self.hasher = hashlib.new(self.hash_algo)
        
        self.size_limit = size_limit
        self.mem_limit = mem_limit

        self.startup()
        atexit.register(self.exit_handler)

    def exit_handler(self):
        if len(self.order) == 0:
            return

        data = {
            'cache': self.cache,
            'order': self.order,
        }

        with open(self.cache_path, 'wb+') as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    def startup(self):
        if not os.path.isfile(self.cache_path):
            return

        with open(self.cache_path, 'rb') as f:
            data = pickle.load(f)
            self.cache = data['cache']
            self.order = data['order']

    def add(self, query, data, args=[]):
        if len(args) > 0:
            query = self.process_query(query, args)
        
        hashed = self.get_identifier(query)
        
        if self.check_overflow(data):
            self.order.append(hashed)
            self.cache[hashed] = data

    def check(self, query, args=[]):
        if len(args) > 0:
            query = self.process_query(query, args)
        
        hashed = self.get_identifier(query)

        if hashed not in self.cache:
            return None

        return self.cache[hashed]

    def refresh(self):
        self.hasher = hashlib.new(self.hash_algo)
        
    def process_query(self, query, args):
        for arg in args:
            query = query.replace('?', arg, 1)

        return query

    def get_identifier(self, query):
        self.hasher.update(query.encode('utf-8'))
        hashed = self.hasher.hexdigest()
        self.refresh()
        
        return hashed

    def calculate_full_cache_size(self):
        size = sys.getsizeof(self.cache)

        for item in self.cache:
            size += sys.getsizeof(item)

        return size

    def check_overflow(self, data):
        if sys.getsizeof(data) >= (self.mem_limit / 2):
            print("It's a big one chief! ", sys.getsizeof(data))
            return False

        future_size = self.calculate_full_cache_size() + sys.getsizeof(data)
        
        if (len(self.cache) + 1) == self.size_limit:
            self.pop_first()

        while future_size > self.mem_limit:
            future_size -= self.pop_first()

        return True

    def pop_first(self):
        key = self.order[0]
        mem_size = sys.getsizeof(self.cache[key])
        del self.cache[key]
        del self.order[0]

        return mem_size

    def pop_cache(self):
        self.cache = dict()
        self.order = []
