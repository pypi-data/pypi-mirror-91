""" Python install script """
from setuptools import setup, find_packages

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True


except ImportError:
    bdist_wheel = None


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="liteblue",
    version="0.0.15",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blueshed/liteblue/",
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data={"liteblue.apps": ["static/*", "simple/*"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "invoke",
        "alembic",
        "sqlalchemy",
        "pymysql",
        "aioredis",
        "tornado",
    ],
    entry_points={"console_scripts": ["liteblue=liteblue.apps:program.run"]},
)
