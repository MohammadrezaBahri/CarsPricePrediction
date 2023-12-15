def clean_integer(value: str) -> int:
    try:
        return int(''.join(char for char in value if char.isnumeric()))
    except ValueError:
        return None


