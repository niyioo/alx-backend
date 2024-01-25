#!/usr/bin/env python3
"""
0. Simple helper function
"""

from typing import Tuple


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