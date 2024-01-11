def clean_integer(value: str) -> int or None:
    """
    Cleans a string by extracting numeric characters and converts it to an integer.

    Parameters:
        value (str): The input string.

    Returns:
        int or None: The cleaned integer value or None if the input is invalid.
    """
    if value:
        try:
            return int(''.join(char for char in value if char.isnumeric()))
        except ValueError:
            return None
