#!/usr/bin/env python3
"""
3. Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Optional, Tuple, Dict

def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple of start index and end index for pagination.

    Args:
    - page (int): The current page number (1-indexed).
    - page_size (int): The number of items per page.

    Returns:
    - Tuple[int, int]: Start and end indexes for the requested page.
    """
    if page < 1 or page_size < 1:
        raise ValueError("Page and page_size should be positive integers.")

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index

class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns a dictionary with hypermedia pagination information
        based on the start index.

        Args:
        - start_index (int): The current start index of the return page.
        - page_size (int): The number of items per page.

        Returns:
        - Dict: Hypermedia pagination information.
        """
        dataset = self.indexed_dataset()
        assert (
            isinstance(index, int) and
            index in range(len(dataset)),
            "Start index is out of range."
            )
        assert page_size > 0, "Page size should be greater than 0."

        data = []
        current_index, end_index = index, index + page_size

        while current_index < end_index:
            if current_index in dataset.keys():
                data.append(dataset[current_index])
            else:
                end_index += 1
            current_index += 1

        return {
            "index": index,
            "data": data,
            "page_size": len(data),
            "next_index": end_index
        }
    