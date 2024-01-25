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
        Returns a dictionary with hypermedia
        pagination information based on index.

        Args:
        - index (int): The current start index of the return page.
        - page_size (int): The number of items per page.

        Returns:
        - Dict: Hypermedia pagination information.
        """
        assert index is None or (index >= 0 and index < len(
            self.__indexed_dataset)), "Index is out of range."
        assert page_size > 0, "Page size should be greater than 0."

        start_index = index if index is not None else 0
        end_index = start_index + page_size
        dataset = self.__indexed_dataset

        page_data = [dataset[i]
                     for i in range(start_index, min(end_index, len(dataset)))]

        next_index = end_index if end_index < len(dataset) else None

        return {
            "index": start_index,
            "data": page_data,
            "page_size": page_size,
            "next_index": next_index
        }
