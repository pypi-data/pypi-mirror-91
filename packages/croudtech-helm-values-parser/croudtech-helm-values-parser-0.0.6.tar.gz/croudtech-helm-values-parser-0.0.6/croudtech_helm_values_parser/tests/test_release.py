import json
import unittest

from croudtech_helm_values_parser.values_parser import Release, ValuesParser


def test_methods(test_data):
    release = Release(base_path=test_data["base_path"], path=test_data["path"])
    test_method = test_data["method"]
    result = getattr(release, test_method)

    assert result == test_data["return_value"]
