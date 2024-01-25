#!/usr/bin/env python3
"""
1. Simple pagination
"""

import csv
from typing import List, Tuple
from typing import Optional


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

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns the appropriate page of the dataset based on pagination
        parameters.

        Args:
        - page (int): The current page number (1-indexed).
        - page_size (int): The number of items per page.

        Returns:
        - List[List]: The requested page of the dataset.
        """
        assert isinstance(page, int) and isinstance(
            page_size, int), "Page and page_size should be integers."
        assert page > 0 and page_size > 0, (
            "Page and page_size should be greater than 0."
        )

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        return dataset[start_index:end_index]
