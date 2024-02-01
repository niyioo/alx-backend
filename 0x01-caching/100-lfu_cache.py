#!/usr/bin/env python3
""" LFUCache module
"""
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ LFUCache class that inherits from BaseCaching
    """

    def __init__(self):
        """ Initialize LFUCache
        """
        super().__init__()
        self.frequency = {}

    def put(self, key, item):
        """ Add an item in the cache using LFU algorithm
        """
        if key is not None and item is not None:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                min_frequency = min(self.frequency.values())
                items_to_discard = [
                    k for k, v in self.frequency.items() if v == min_frequency]
                if len(items_to_discard) > 1:
                    # If more than one item to discard, use LRU algorithm
                    lru_key = min(self.cache_data,
                                  key=lambda k: self.cache_data[k])
                    items_to_discard = [lru_key]

                discarded_key = items_to_discard[0]
                del self.cache_data[discarded_key]
                del self.frequency[discarded_key]
                print("DISCARD:", discarded_key)

            self.cache_data[key] = item
            self.frequency[key] = self.frequency.get(key, 0) + 1

    def get(self, key):
        """ Get an item by key and update frequency
        """
        if key in self.cache_data:
            self.frequency[key] += 1
            return self.cache_data[key]
        return None
