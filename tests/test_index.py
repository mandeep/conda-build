# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import json
from logging import getLogger
import os
from os.path import dirname, isdir, join, isfile
import requests
import shutil
import tarfile

from conda_build import api
from conda_build.index import update_index
from conda_build.conda_interface import subdir
from .utils import metadata_dir

log = getLogger(__name__)

# NOTE: The recipes for test packages used in this module are at https://github.com/kalefranz/conda-test-packages


def download(url, local_path):
    # NOTE: The tests in this module download packages from the conda-test channel.
    #       These packages are small, and could easily be included in the conda-build git
    #       repository once their use stabilizes.
    if not isdir(dirname(local_path)):
        os.makedirs(dirname(local_path))
    r = requests.get(url, stream=True)
    with open(local_path, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return local_path


def test_index_on_single_subdir_1(testing_workdir):
    test_package_path = join(testing_workdir, 'osx-64', 'conda-index-pkg-a-1.0-py27h5e241af_0.tar.bz2')
    test_package_url = 'https://conda.anaconda.org/conda-test/osx-64/conda-index-pkg-a-1.0-py27h5e241af_0.tar.bz2'
    download(test_package_url, test_package_path)

    update_index(testing_workdir, channel_name='test-channel')

    # #######################################
    # tests for osx-64 subdir
    # #######################################
    assert isfile(join(testing_workdir, 'osx-64', 'index.html'))
    assert isfile(join(testing_workdir, 'osx-64', 'repodata.json.bz2'))

    with open(join(testing_workdir, 'osx-64', 'repodata.json')) as fh:
        actual_repodata_json = json.loads(fh.read())
    expected_repodata_json = {
        "info": {
            'subdir': 'osx-64',
        },
        "packages": {
            "conda-index-pkg-a-1.0-py27h5e241af_0.tar.bz2": {
                "build": "py27h5e241af_0",
                "build_number": 0,
                "depends": [
                    "python >=2.7,<2.8.0a0"
                ],
                "license": "BSD",
                "md5": "37861df8111170f5eed4bff27868df59",
                "name": "conda-index-pkg-a",
                "sha256": "459f3e9b2178fa33bdc4e6267326405329d1c1ab982273d9a1c0a5084a1ddc30",
                "size": 8733,
                "subdir": "osx-64",
                "timestamp": 1508520039632,
                "version": "1.0",
            },
        },
        "removed": [],
        "repodata_version": 1,
    }
    assert actual_repodata_json == expected_repodata_json

    # #######################################
    # tests for full channel
    # #######################################

    with open(join(testing_workdir, 'channeldata.json')) as fh:
        actual_channeldata_json = json.loads(fh.read())
    expected_channeldata_json = {
        "channeldata_version": 1,
        "packages": {
            "conda-index-pkg-a": {
                "description": "Description field for conda-index-pkg-a. Actually, this is just the python description. "
                                "Python is a widely used high-level, general-purpose, interpreted, dynamic "
                                "programming language. Its design philosophy emphasizes code "
                                "readability, and its syntax allows programmers to express concepts in "
                                "fewer lines of code than would be possible in languages such as C++ or "
                                "Java. The language provides constructs intended to enable clear programs "
                                "on both a small and large scale.",
                "dev_url": "https://github.com/kalefranz/conda-test-packages/blob/master/conda-index-pkg-a/meta.yaml",
                "doc_source_url": "https://github.com/kalefranz/conda-test-packages/blob/master/conda-index-pkg-a/README.md",
                "doc_url": "https://github.com/kalefranz/conda-test-packages/blob/master/conda-index-pkg-a",
                "home": "https://anaconda.org/conda-test/conda-index-pkg-a",
                "license": "BSD",
                "reference_package": "osx-64/conda-index-pkg-a-1.0-py27h5e241af_0.tar.bz2",
                "source_git_rev": "master",
                "source_git_url": "https://github.com/kalefranz/conda-test-packages.git",
                "subdirs": [
                    "osx-64",
                ],
                "summary": "Summary field for conda-index-pkg-a",
                "version": "1.0",
                "activate.d": False,
                "deactivate.d": False,
                "post_link": True,
                "pre_link": False,
                "pre_unlink": False,
                "binary_prefix": False,
                "text_prefix": True,
                "run_exports": {},
            }
        },
        "subdirs": [
            "noarch",
            "osx-64"
        ]
    }
    assert actual_channeldata_json == expected_channeldata_json


def test_index_noarch_osx64_1(testing_workdir):
    test_package_path = join(testing_workdir, 'osx-64', 'conda-index-pkg-a-1.0-py27h5e241af_0.tar.bz2')
    test_package_url = 'https://conda.anaconda.org/conda-test/osx-64/conda-index-pkg-a-1.0-py27h5e241af_0.tar.bz2'
    download(test_package_url, test_package_path)

    test_package_path = join(testing_workdir, 'noarch', 'conda-index-pkg-a-1.0-pyhed9eced_1.tar.bz2')
    test_package_url = 'https://conda.anaconda.org/conda-test/noarch/conda-index-pkg-a-1.0-pyhed9eced_1.tar.bz2'
    download(test_package_url, test_package_path)

    update_index(testing_workdir, channel_name='test-channel')

    # #######################################
    # tests for osx-64 subdir
    # #######################################
    assert isfile(join(testing_workdir, 'osx-64', 'index.html'))
    assert isfile(join(testing_workdir, 'osx-64', 'repodata.json'))  # repodata is tested in test_index_on_single_subdir_1
    assert isfile(join(testing_workdir, 'osx-64', 'repodata.json.bz2'))

    # #######################################
    # tests for noarch subdir
    # #######################################
    assert isfile(join(testing_workdir, 'osx-64', 'index.html'))
    assert isfile(join(testing_workdir, 'osx-64', 'repodata.json.bz2'))

    with open(join(testing_workdir, 'noarch', 'repodata.json')) as fh:
        actual_repodata_json = json.loads(fh.read())
    expected_repodata_json = {
        "info": {
            'subdir': 'noarch',
        },
        "packages": {
            "conda-index-pkg-a-1.0-pyhed9eced_1.tar.bz2": {
                "build": "pyhed9eced_1",
                "build_number": 1,
                "depends": [
                    "python"
                ],
                "license": "BSD",
                "md5": "56b5f6b7fb5583bccfc4489e7c657484",
                "name": "conda-index-pkg-a",
                "noarch": "python",
                "sha256": "7430743bffd4ac63aa063ae8518e668eac269c783374b589d8078bee5ed4cbc6",
                "size": 7882,
                "subdir": "noarch",
                "timestamp": 1508520204768,
                "version": "1.0",
            },
        },
        "removed": [],
        "repodata_version": 1,
    }
    assert actual_repodata_json == expected_repodata_json

    # #######################################
    # tests for full channel
    # #######################################

    with open(join(testing_workdir, 'channeldata.json')) as fh:
        actual_channeldata_json = json.loads(fh.read())
    expected_channeldata_json = {
        "channeldata_version": 1,
        "packages": {
            "conda-index-pkg-a": {
                "description": "Description field for conda-index-pkg-a. Actually, this is just the python description. "
                                "Python is a widely used high-level, general-purpose, interpreted, dynamic "
                                "programming language. Its design philosophy emphasizes code "
                                "readability, and its syntax allows programmers to express concepts in "
                                "fewer lines of code than would be possible in languages such as C++ or "
                                "Java. The language provides constructs intended to enable clear programs "
                                "on both a small and large scale.",
                "dev_url": "https://github.com/kalefranz/conda-test-packages/blob/master/conda-index-pkg-a/meta.yaml",
                "doc_source_url": "https://github.com/kalefranz/conda-test-packages/blob/master/conda-index-pkg-a/README.md",
                "doc_url": "https://github.com/kalefranz/conda-test-packages/blob/master/conda-index-pkg-a",
                "home": "https://anaconda.org/conda-test/conda-index-pkg-a",
                "license": "BSD",
                "reference_package": "noarch/conda-index-pkg-a-1.0-pyhed9eced_1.tar.bz2",
                "source_git_rev": "master",
                "source_git_url": "https://github.com/kalefranz/conda-test-packages.git",
                "subdirs": [
                    "noarch",
                    "osx-64",
                ],
                "summary": "Summary field for conda-index-pkg-a. This is the python noarch version.",  # <- tests that the higher noarch build number is the data collected
                "version": "1.0",
                "activate.d": False,
                "deactivate.d": False,
                "post_link": True,
                "pre_link": False,
                "pre_unlink": False,
                "binary_prefix": False,
                "text_prefix": False,
                "run_exports": {},
            }
        },
        "subdirs": [
            "noarch",
            "osx-64",
        ]
    }
    assert actual_channeldata_json == expected_channeldata_json


def _build_test_index(workdir):
    api.build(os.path.join(metadata_dir, "_index_hotfix_pkgs"), croot=workdir)

    with open(os.path.join(workdir, subdir, 'repodata.json')) as f:
        original_metadata = json.load(f)

    pkg_list = original_metadata['packages']
    assert "track_features_test-1.0-0.tar.bz2" in pkg_list
    assert pkg_list["track_features_test-1.0-0.tar.bz2"]["track_features"] == "dummy"

    assert "hotfix_depends_test-1.0-dummy_0.tar.bz2" in pkg_list
    assert pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["features"] == "dummy"
    assert "zlib" in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"]

    assert "revoke_test-1.0-0.tar.bz2" in pkg_list
    assert "zlib" in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]
    assert "package_has_been_revoked" not in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]

    assert "remove_test-1.0-0.tar.bz2" in pkg_list


def test_gen_patch_py(testing_workdir):
    """
    This is a channel-wide file that applies to many subdirs.  It must have a function with this signature:

    def _patch_repodata(repodata, subdir):

    That function must return a dictionary of patch instructions, of the form:

    {
        "patch_instructions_version": 1,
        "packages": defaultdict(dict),
        "revoke": [],
        "remove": [],
    }

    revoke and remove are lists of filenames. remove makes the file not show up
    in the index (it may still be downloadable with a direct URL to the file).
    revoke makes packages uninstallable by adding an unsatisfiable dependency.
    This can be made installable by including a channel that has that package
    (to be created by @jjhelmus).

    packages is a dictionary, where keys are package filenames. Values are
    dictionaries similar to the contents of each package in repodata.json. Any
    values in provided in packages here overwrite the values in repodata.json.
    Any value set to None is removed.
    """
    _build_test_index(testing_workdir)

    func = """
def _patch_repodata(repodata, subdir):
    pkgs = repodata["packages"]
    import fnmatch
    replacement_dict = {}
    if "track_features_test-1.0-0.tar.bz2" in pkgs:
        replacement_dict["track_features_test-1.0-0.tar.bz2"] = {"track_features": None}
    if "hotfix_depends_test-1.0-dummy_0.tar.bz2" in pkgs:
        replacement_dict["hotfix_depends_test-1.0-dummy_0.tar.bz2"] = {
                             "depends": pkgs["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"] + ["dummy"],
                             "features": None}
    revoke_list = [pkg for pkg in pkgs if fnmatch.fnmatch(pkg, "revoke_test*")]
    remove_list = [pkg for pkg in pkgs if fnmatch.fnmatch(pkg, "remove_test*")]
    return {
        "patch_instructions_version": 1,
        "packages": replacement_dict,
        "revoke": revoke_list,
        "remove": remove_list,
    }
"""
    patch_file = os.path.join(testing_workdir, 'repodata_patch.py')
    with open(patch_file, 'w') as f:
        f.write(func)

    # indexing a second time with the same patchset should keep the removals
    for i in (1, 2):
        update_index(testing_workdir, patch_generator=patch_file, verbose=True)
        with open(os.path.join(testing_workdir, subdir, 'repodata.json')) as f:
            patched_metadata = json.load(f)

        pkg_list = patched_metadata['packages']
        assert "track_features_test-1.0-0.tar.bz2" in pkg_list
        assert "track_features" not in pkg_list["track_features_test-1.0-0.tar.bz2"]
        print("pass %s track features ok" % i)

        assert "hotfix_depends_test-1.0-dummy_0.tar.bz2" in pkg_list
        assert "features" not in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]
        assert "zlib" in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"]
        assert "dummy" in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"]
        print("pass %s hotfix ok" % i)

        assert "revoke_test-1.0-0.tar.bz2" in pkg_list
        assert "zlib" in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]
        assert "package_has_been_revoked" in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]
        print("pass %s revoke ok" % i)

        assert "remove_test-1.0-0.tar.bz2" not in pkg_list
        assert "remove_test-1.0-0.tar.bz2" in patched_metadata['removed'], "removed list not populated in run %d" % i
        print("pass %s remove ok" % i)


def test_channel_patch_instructions_json(testing_workdir):
    _build_test_index(testing_workdir)

    replacement_dict = {}
    replacement_dict["track_features_test-1.0-0.tar.bz2"] = {"track_features": None}
    replacement_dict["hotfix_depends_test-1.0-dummy_0.tar.bz2"] = {
                             "depends": ["zlib", "dummy"],
                             "features": None}

    patch = {
        "patch_instructions_version": 1,
        "packages": replacement_dict,
        "revoke": ["revoke_test-1.0-0.tar.bz2"],
        "remove": ["remove_test-1.0-0.tar.bz2"],
    }

    with open(os.path.join(testing_workdir, subdir, 'patch_instructions.json'), 'w') as f:
        json.dump(patch, f)

    update_index(testing_workdir)

    with open(os.path.join(testing_workdir, subdir, 'repodata.json')) as f:
        patched_metadata = json.load(f)

    pkg_list = patched_metadata['packages']
    assert "track_features_test-1.0-0.tar.bz2" in pkg_list
    assert "track_features" not in pkg_list["track_features_test-1.0-0.tar.bz2"]

    assert "hotfix_depends_test-1.0-dummy_0.tar.bz2" in pkg_list
    assert "features" not in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]
    assert "zlib" in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"]
    assert "dummy" in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"]

    assert "revoke_test-1.0-0.tar.bz2" in pkg_list
    assert "zlib" in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]
    assert "package_has_been_revoked" in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]

    assert "remove_test-1.0-0.tar.bz2" not in pkg_list


def test_patch_from_tarball(testing_workdir):
    """This is how we expect external communities to provide patches to us.
    We can't let them just give us Python files for us to run, because of the
    security risk of arbitrary code execution."""
    _build_test_index(testing_workdir)

    # our hotfix metadata can be generated any way you want.  Hard-code this here, but in general,
    #    people will use some python file to generate this.

    replacement_dict = {}
    replacement_dict["track_features_test-1.0-0.tar.bz2"] = {"track_features": None}
    replacement_dict["hotfix_depends_test-1.0-dummy_0.tar.bz2"] = {
                             "depends": ["zlib", "dummy"],
                             "features": None}

    patch = {
        "patch_instructions_version": 1,
        "packages": replacement_dict,
        "revoke": ["revoke_test-1.0-0.tar.bz2"],
        "remove": ["remove_test-1.0-0.tar.bz2"],
    }
    with open("patch_instructions.json", "w") as f:
        json.dump(patch, f)

    with tarfile.open("patch_archive.tar.bz2", "w:bz2") as archive:
        archive.add("patch_instructions.json", "%s/patch_instructions.json" % subdir)

    update_index(testing_workdir, patch_generator="patch_archive.tar.bz2")

    with open(os.path.join(testing_workdir, subdir, 'repodata.json')) as f:
        patched_metadata = json.load(f)

    pkg_list = patched_metadata['packages']
    assert "track_features_test-1.0-0.tar.bz2" in pkg_list
    assert "track_features" not in pkg_list["track_features_test-1.0-0.tar.bz2"]

    assert "hotfix_depends_test-1.0-dummy_0.tar.bz2" in pkg_list
    assert "features" not in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]
    assert "zlib" in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"]
    assert "dummy" in pkg_list["hotfix_depends_test-1.0-dummy_0.tar.bz2"]["depends"]

    assert "revoke_test-1.0-0.tar.bz2" in pkg_list
    assert "zlib" in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]
    assert "package_has_been_revoked" in pkg_list["revoke_test-1.0-0.tar.bz2"]["depends"]

    assert "remove_test-1.0-0.tar.bz2" not in pkg_list


def test_index_of_removed_pkg(testing_metadata):
    out_files = api.build(testing_metadata)
    for f in out_files:
        os.remove(f)
    api.update_index(testing_metadata.config.croot)
    with open(os.path.join(testing_metadata.config.croot, subdir, 'repodata.json')) as f:
        repodata = json.load(f)
    assert not repodata['packages']
