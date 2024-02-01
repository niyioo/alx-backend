#!/usr/bin/env python3
""" FIFOCache module
"""


class FIFOCache(BaseCaching):
    """ FIFOCache class that inherits from BaseCaching
    """

    def __init__(self):
        """ Initialize FIFOCache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache using FIFO algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = self.order[0]
                del self.cache_data[discarded_key]
                self.order.pop(0)
                print("DISCARD:", discarded_key)

            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
