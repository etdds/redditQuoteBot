from enum import Enum
from typing import Dict, Callable
from os.path import splitext


class FileTypes(Enum):
    """Defines known filetypes which can be resolved
    """
    JSON = ".json"
    CSV = ".csv"


class FileAssociator():
    """Create a file associator which assigns file extensions to callbacks
    """

    def __init__(self, associations: Dict[FileTypes, Callable]):
        """Initialise

        Args:
            associations (Dict[FileTypes, Callable]): A map a filetypes to callback handler to use on read or write invocations
        """
        self.associations = associations

    def resolve_file_type(self, path: str) -> FileTypes:
        """Get the type of file resolved from a filepath, with an extension

        Args:
            path (str): The filepath to resolve.

        Raises:
            LookupError: The detected file extension has no associated filetype.

        Returns:
            FileTypes: The resolved extension
        """
        _, extension = splitext(path)
        for file_type in FileTypes:
            if file_type.value == extension:
                return file_type
        raise LookupError(f"Unknown file extension {extension}")

    def read(self, path: str):
        """Open a file for reading, and call the registered handler.

        Args:
            path (str): Path to file to open.

        Raises:
            KeyError: No handler is registered for the found filetype.
            LookupError: The detected file extension has no associated filetype.

        Returns:
            _type_: Any return value from the associated file handler.
        """
        file_type = self.resolve_file_type(path)
        with open(path, "r", encoding="utf-8") as file_handler:
            try:
                return self.associations[file_type](file_handler)
            except KeyError as exp:
                raise KeyError("Not file handler installed for file type.") from exp

    def write(self, path: str, *args):
        """Open a file for writing, and call the registered handler.

        Args:
            path (str): Path to file to open.

        Raises:
            KeyError: No handler is registered for the found filetype.
            LookupError: The detected file extension has no associated filetype.

        Returns:
            _type_: Any return value from the associated file handler.
        """
        file_type = self.resolve_file_type(path)
        with open(path, "w", encoding="utf-8") as file_handler:
            try:
                return self.associations[file_type](file_handler, args)
            except KeyError as exp:
                raise KeyError("Not file handler installed for file type.") from exp
