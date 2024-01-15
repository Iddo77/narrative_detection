import os


def read_from_file(file_path: str) -> str:
    """
    Reads the contents of a file.

    Args:
    file_path (str): Path to the file to be read.

    Returns:
    str: Contents of the file.
    """
    with open(file_path, 'r') as file:
        return file.read()


def write_to_file(file_path: str, data: str) -> None:
    """
    Writes a string to a file.

    Args:
    file_path (str): Path to the file where the data will be written.
    data (str): The data to write to the file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(data)
