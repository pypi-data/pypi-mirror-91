import os
import unittest

from croudtech_helm_values_parser.values_parser import (
    Release,
    ReleaseList,
    ValuesParser,
)


def test_get_releases():
    repo_path = os.path.realpath(os.path.join(os.getcwd(), "test_repo"))
    release_list = ReleaseList(repo_path)
    for release in release_list.releases():
        assert release.is_release


def test_get_namespaced_releases():
    repo_path = os.path.realpath(os.path.join(os.getcwd(), "test_repo"))
    release_list = ReleaseList(repo_path)
    for release in release_list.releases(namespaces="int-v3-croud"):
        assert release.is_release
        assert release.namespace == "int-v3-croud"

    for release in release_list.releases(namespaces=["int-v3-croud", "int-v3-network"]):
        assert release.is_release
        assert release.namespace in ["int-v3-croud", "int-v3-network"]


def test_get_environment_releases():
    repo_path = os.path.realpath(os.path.join(os.getcwd(), "test_repo"))
    release_list = ReleaseList(repo_path)
    for release in release_list.releases(environments="int"):
        assert release.is_release
        assert release.environment == "int"

    for release in release_list.releases(environments=["int", "prelive"]):
        assert release.is_release
        assert release.environment in ["int", "prelive"]
