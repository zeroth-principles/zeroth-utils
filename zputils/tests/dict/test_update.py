"""test_dict util file contains test cases for dict util file."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

from zputils.dict.update import deep_update, custom_serializer, json_dump
import pytest
import json

"""test cases for deep_update function"""

def test_simple_update():
    a = {"x": 1, "y": 2}
    b = {"y": 3, "z": 4}
    result = deep_update(a, b)
    assert result == {"x": 1, "y": 3, "z": 4}

def test_nested_update():
    a = {"x": {"y": 1, "z": 2}}
    b = {"x": {"z": 3, "w": 4}}
    result = deep_update(a, b)
    assert result == {"x": {"y": 1, "z": 3, "w": 4}}

def test_deeply_nested_update():
    a = {"x": {"y": {"z": 1, "w": 2}, "v": 3}}
    b = {"x": {"y": {"w": 4}}}
    result = deep_update(a, b)
    assert result == {"x": {"y": {"z": 1, "w": 4}, "v": 3}}

def test_non_dict_values():
    a = {"x": 1, "y": [1, 2, 3], "z": "hello"}
    b = {"x": 2, "y": [4, 5, 6], "z": "world"}
    result = deep_update(a, b)
    assert result == {"x": 2, "y": [4, 5, 6], "z": "world"}

def test_add_new_nested_dict():
    a = {"x": 1}
    b = {"y": {"z": 2}}
    result = deep_update(a, b)
    assert result == {"x": 1, "y": {"z": 2}}

def test_no_overlapping_keys():
    a = {"x": 1}
    b = {"y": 2}
    result = deep_update(a, b)
    assert result == {"x": 1, "y": 2}

def test_update_with_empty_dict():
    a = {"x": 1, "y": 2}
    b = {}
    result = deep_update(a, b)
    assert result == {"x": 1, "y": 2}

    result = deep_update(b, a)
    assert result == {"x": 1, "y": 2}


"""test cases for json_dump function"""

def test_custom_serializer_with_function():
    result = custom_serializer(print)
    assert result == "<built-in function print>"

def test_custom_serializer_with_lambda():
    result = custom_serializer(lambda x: x + 1)
    assert result.startswith("<function test_custom_serializer_with_lambda.<locals>.<lambda>")

def test_custom_serializer_with_non_callable():
    with pytest.raises(TypeError, match="Object of type int is not JSON serializable"):
        custom_serializer(123)

def test_json_dump_with_function():
    data = {
        "name": "Alice",
        "func": print
    }
    result = json_dump(data)
    expected = json.dumps({"name": "Alice", "func": "<built-in function print>"})
    assert result == expected

def test_json_dump_with_lambda():
    data = {
        "name": "Bob",
        "func": lambda x: x + 1
    }
    result = json_dump(data)
    assert "name" in result
    assert "func" in result

def test_json_dump_with_standard_data():
    data = {
        "name": "Charlie",
        "age": 30
    }
    result = json_dump(data)
    expected = json.dumps(data)
    assert result == expected

def test_json_dump_with_unserializable_data():
    class DummyClass:
        pass

    data = {
        "name": "David",
        "object": DummyClass()
    }
    with pytest.raises(TypeError, match="Object of type DummyClass is not JSON serializable"):
        json_dump(data)
