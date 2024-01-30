#!/usr/bin/env python3
""" LIFOCache module
"""


class BaseCaching():
    """ BaseCaching defines:
      - constants of your caching system
      - where your data are stored (in a dictionary)
    """
    MAX_ITEMS = 4

    def __init__(self):
        """ Initialize
        """
        self.cache_data = {}

    def print_cache(self):
        """ Print the cache
        """
        print("Current cache:")
        for key in sorted(self.cache_data.keys()):
            print("{}: {}".format(key, self.cache_data.get(key)))

    def put(self, key, item):
        """ Add an item in the cache
        """
        raise NotImplementedError(
            "put must be implemented in your cache class")

    def get(self, key):
        """ Get an item by key
        """
        raise NotImplementedError(
            "get must be implemented in your cache class")


class LIFOCache(BaseCaching):
    """ LIFOCache class that inherits from BaseCaching
    """

    def __init__(self):
        """ Initialize LIFOCache
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache using LIFO algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                discarded_key = self.order.pop()
                del self.cache_data[discarded_key]
                print("DISCARD:", discarded_key)

            self.cache_data[key] = item
            self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
