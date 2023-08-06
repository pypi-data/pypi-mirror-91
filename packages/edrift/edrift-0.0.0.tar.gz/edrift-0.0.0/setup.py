# Standard library imports
import os
import ast

# Third party imports
from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(module='edrift'):
    """Get version."""
    with open(os.path.join(HERE, module, '__init__.py'), 'r') as f:
        data = f.read()
    lines = data.split('\n')
    for line in lines:
        if line.startswith('VERSION_INFO'):
            version_tuple = ast.literal_eval(line.split('=')[-1].strip())
            version = '.'.join(map(str, version_tuple))
            break
    return version


def get_description():
    """Get long description."""
    with open(os.path.join(HERE, 'README.md'), 'r') as f:
        data = f.read()
    return data


AUTHOR_NAME = ''
AUTHOR_EMAIL = ''

install_requires = [
]

tests_require = [
]

setup(name='edrift',
      version=get_version(),
      description='edrift watershed modeling',
      author=AUTHOR_NAME,
      url='https://github.com/aerispaha/edrift',
      author_email=AUTHOR_EMAIL,
      packages=find_packages(exclude='tests'),
      entry_points={},
      install_requires=install_requires,
      tests_require=tests_require,
      long_description=get_description(),
      long_description_content_type="text/markdown",
      include_package_data=True,
      platforms="OS Independent",
      license="MIT License",
      classifiers=[
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
      ]
      )
