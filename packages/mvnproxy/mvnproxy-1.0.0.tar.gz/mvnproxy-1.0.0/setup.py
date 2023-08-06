from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="mvnproxy",
    version="1.0.0",
    description="mvnproxy",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    entry_points={"console_scripts": ["mvnproxy = mvnproxy.mainapp:main"]},
    install_requires=[
        "flask==1.0.2",
        "uwsgi==2.0.17",
        "eventlet==0.23.0",
        "requests==2.25.1",
        "termcolor_util",
        "elementtree",
    ],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "mvnproxy": ["py.typed"],
    },
)
