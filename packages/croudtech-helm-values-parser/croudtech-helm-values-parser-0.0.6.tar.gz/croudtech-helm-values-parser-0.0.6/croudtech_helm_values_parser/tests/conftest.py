import json
import os

import pytest

base_path = os.path.join(os.getcwd(), "test_repo")

test_data = [
    {
        "path": "/test/repo/base/path/environment/namespace1/namespace2/the-chart-name/release.yaml",
        "base_path": "/test/repo/base/path",
        "test_property_methods": {
            "chart": "the-chart-name",
            "release": "environment-namespace1-namespace2-the-chart-name-release",
            "environment": "environment",
            "app_name": "release",
            "namespace": "environment-namespace1-namespace2",
            "all_files": [
                "/test/repo/base/path/_system.yaml",
                "/test/repo/base/path/common.yaml",
                "/test/repo/base/path/environment/_system.yaml",
                "/test/repo/base/path/environment/namespace1/_the-chart-name/common.yaml",
                "/test/repo/base/path/environment/namespace1/_the-chart-name/_system.yaml",
                "/test/repo/base/path/environment/common.yaml",
                "/test/repo/base/path/environment/namespace1/_system.yaml",
                "/test/repo/base/path/environment/namespace1/common.yaml",
                "/test/repo/base/path/environment/namespace1/namespace2/_system.yaml",
                "/test/repo/base/path/environment/namespace1/namespace2/common.yaml",
                "/test/repo/base/path/environment/namespace1/namespace2/the-chart-name/_system.yaml",
                "/test/repo/base/path/environment/namespace1/namespace2/the-chart-name/common.yaml",
                "/test/repo/base/path/environment/namespace1/namespace2/the-chart-name/release.yaml",
            ],
            "files": [],
            "values": {},
            "combined_values": {},
        },
    },
    {
        "path": "/test/repo/base/path/environmentname/namespace1/the-chart-name/release.yaml",
        "base_path": "/test/repo/base/path",
        "test_property_methods": {
            "chart": "the-chart-name",
            "release": "environmentname-namespace1-the-chart-name-release",
            "environment": "environmentname",
            "app_name": "release",
            "namespace": "environmentname-namespace1",
            "all_files": [
                "/test/repo/base/path/_system.yaml",
                "/test/repo/base/path/common.yaml",
                "/test/repo/base/path/environmentname/_system.yaml",
                "/test/repo/base/path/environmentname/namespace1/_the-chart-name/common.yaml",
                "/test/repo/base/path/environmentname/namespace1/_the-chart-name/_system.yaml",
                "/test/repo/base/path/environmentname/common.yaml",
                "/test/repo/base/path/environmentname/namespace1/_system.yaml",
                "/test/repo/base/path/environmentname/namespace1/common.yaml",
                "/test/repo/base/path/environmentname/namespace1/the-chart-name/_system.yaml",
                "/test/repo/base/path/environmentname/namespace1/the-chart-name/common.yaml",
                "/test/repo/base/path/environmentname/namespace1/the-chart-name/release.yaml",
            ],
            "files": [],
            "values": {},
            "combined_values": {},
        },
    },
    {
        "path": os.path.join(
            base_path, "int/v3/croud/croudtech-v3-service/acl-api.yaml"
        ),
        "base_path": base_path,
        "test_property_methods": {
            "chart": "croudtech-v3-service",
            "release": "int-v3-croud-croudtech-v3-service-acl-api",
            "environment": "int",
            "app_name": "acl-api",
            "namespace": "int-v3-croud",
            "all_files": [
                os.path.join(base_path, "_system.yaml"),
                os.path.join(base_path, "common.yaml"),
                os.path.join(base_path, "int/_system.yaml"),
                os.path.join(base_path, "int/v3/_croudtech-v3-service/common.yaml"),
                os.path.join(base_path, "int/v3/_croudtech-v3-service/_system.yaml"),
                os.path.join(base_path, "int/common.yaml"),
                os.path.join(base_path, "int/v3/_system.yaml"),
                os.path.join(base_path, "int/v3/common.yaml"),
                os.path.join(base_path, "int/v3/croud/_system.yaml"),
                os.path.join(base_path, "int/v3/croud/common.yaml"),
                os.path.join(
                    base_path, "int/v3/croud/croudtech-v3-service/_system.yaml"
                ),
                os.path.join(
                    base_path, "int/v3/croud/croudtech-v3-service/common.yaml"
                ),
                os.path.join(
                    base_path, "int/v3/croud/croudtech-v3-service/acl-api.yaml"
                ),
            ],
            "files": [
                os.path.join(base_path, "int/v3/_croudtech-v3-service/common.yaml"),
                os.path.join(
                    base_path, "int/v3/croud/croudtech-v3-service/_system.yaml"
                ),
                os.path.join(
                    base_path, "int/v3/croud/croudtech-v3-service/acl-api.yaml"
                ),
            ],
            "values": {
                os.path.join(base_path, "int/v3/_croudtech-v3-service/common.yaml"): {
                    "test": {
                        "value1": "common_value1",
                        "value2": "common_value2",
                        "list_value": [
                            "common_value_1",
                            "common_value_2",
                            "common_value_3",
                            "common_value_4",
                            "common_value_5",
                            "common_value_6",
                        ],
                    },
                    "testcommon": {
                        "value1": "common_value1",
                        "value2": "common_value2",
                        "testnested": {
                            "valuenested1": "nestedcommon1",
                            "valuenested2": "nestedcommon1",
                        },
                    },
                },
                os.path.join(
                    base_path, "int/v3/croud/croudtech-v3-service/_system.yaml"
                ): {},
                os.path.join(
                    base_path, "int/v3/croud/croudtech-v3-service/acl-api.yaml"
                ): {
                    "test": {
                        "value1": "release_value1",
                        "list_value": ["release_value_3"],
                    },
                    "testcommon": {
                        "value2": "release_value2",
                        "testnested": {"valuenested2": "nestedrelease1"},
                    },
                    "extra_values": {"env": {"TEST_ENV": 123}},
                },
            },
            "combined_values": {
                "test": {
                    "value1": "release_value1",
                    "list_value": ["release_value_3"],
                    "value2": "common_value2",
                },
                "testcommon": {
                    "value2": "release_value2",
                    "testnested": {
                        "valuenested2": "nestedrelease1",
                        "valuenested1": "nestedcommon1",
                    },
                    "value1": "common_value1",
                },
                "extra_values": {"env": {"TEST_ENV": 123}},
            },
        },
    },
]


def pytest_generate_tests(metafunc):
    if "test_data" in metafunc.fixturenames:
        test_data_fixtures = []
        for test_item in test_data:
            for test_method, return_value in test_item["test_property_methods"].items():
                test_data_fixture = {
                    "path": test_item["path"],
                    "base_path": test_item["base_path"],
                    "method": test_method,
                    "return_value": return_value,
                }
                test_data_fixtures.append(test_data_fixture)
        metafunc.parametrize("test_data", test_data_fixtures)
