import math
import json
from random import sample 

def percentage_floored(n:int, percentage: float)-> int:
    return max(math.floor(n * percentage),1)

def adjust_string_length(input_str, length, fill_char):
    """
    Adjusts the length of the input string by appending characters from the left side if needed.

    Args:
    input_str (str): The input string.
    length (int): The desired length of the string.
    fill_char (str): The character to append to the left side if needed.

    Returns:
    str: The adjusted string.

    Raises:
    ValueError: If the length of the string is greater than the specified length.
    """
    if len(input_str) < length:
        return fill_char * (length - len(input_str)) + input_str
    elif len(input_str) == length:
        return input_str
    else:
        raise ValueError(f"Invalid input: Length of the string '{input_str}' is greater than the specified length {length}.")

def read_ndjson(path):
    return [json.loads(line) for line in open(path, 'r')]


def pick_n_random_items(input_list, n):
    # Ensure n is not greater than the length of the input list
    n = min(n, len(input_list))

    # Use random.sample to pick n items randomly
    picked_items = sample(input_list, n)

    # Create a list of non-picked items
    non_picked_items = [item for item in input_list if item not in picked_items]

    # Return a tuple containing the picked items and non-picked items
    return picked_items, non_picked_items
