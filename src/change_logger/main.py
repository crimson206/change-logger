"""
Main module for the package
"""

from semantic_release import changelog

def hello_world(name: str = "World") -> str:
    """
    Returns a greeting message.

    Args:
        name: The name to greet

    Returns:
        A greeting string
    """
    return f"Hello, {name}!"


def add_numbers(a: int, b: int) -> int:
    """
    Adds two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b

    1234
    """
    return a + b
