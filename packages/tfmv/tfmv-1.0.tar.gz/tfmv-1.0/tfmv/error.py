class DuplicateError(Exception):
    def __init__(self, *duplicates: str):
        self.duplicates = list(duplicates)
