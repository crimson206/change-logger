"""
Tests for the main module
"""

import pytest
from change_logger.main import hello_world, add_numbers


def test_hello_world_default():
    """Test hello_world with default parameter"""
    result = hello_world()
    assert result == "Hello, World!"


def test_hello_world_with_name():
    """Test hello_world with custom name"""
    result = hello_world("Alice")
    assert result == "Hello, Alice!"


def test_add_numbers():
    """Test add_numbers function"""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0


def test_add_numbers_large():
    """Test add_numbers with large numbers"""
    assert add_numbers(1000000, 2000000) == 3000000