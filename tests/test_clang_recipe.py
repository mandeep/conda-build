import conda_build.api


def test_clang_build():
    conda_build.api.build('/Users/mbhutani/Repos/anaconda-recipes/clang')
