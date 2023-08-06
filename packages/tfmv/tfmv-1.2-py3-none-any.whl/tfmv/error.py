"""
error.py

classes for exceptions
"""


class DuplicateError(Exception):
    """exception raised when state operations would create duplicates"""
    def __init__(self, *duplicates: str):
        super().__init__()
        self.duplicates = list(duplicates)
