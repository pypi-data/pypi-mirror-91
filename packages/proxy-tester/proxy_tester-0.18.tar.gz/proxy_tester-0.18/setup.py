import io
import re
from setuptools import setup

import os, sys
import shutil
try:
    os.makedirs(os.path.join(os.path.dirname(__file__), 'proxy_tester'))
except:
    pass
try:
    os.remove(os.path.join('proxy_tester', '__version__.py'))
except:
    pass
shutil.copy2('__version__.py', 'proxy_tester')
shutil.copy2('proxy_tester.py', 'proxy_tester')
shutil.copy2('auto.py', 'proxy_tester')
shutil.copy2('proxy_tester.ini', 'proxy_tester')
shutil.copy2('proxy_tester2.py', 'proxy_tester')
shutil.copy2('__init__.py', 'proxy_tester')

# with io.open("README.rst", "rt", encoding="utf8") as f:
#     readme = f.read()

# with io.open("__version__.py", "rt", encoding="utf8") as f:
    # version = re.search(r"version = \'(.*?)\'", f.read()).group(1)
import __version__
version = __version__.version

requirements = [
        'make_colors>=3.12',
        'requests',
        'bs4',
        'cfscrape',
        'pydebugger',
        'configset',
    ]

setup(
    name="proxy_tester",
    version=version,
    url="https://bitbucket.org/licface/proxy_tester",
    project_urls={
        "Documentation": "https://bitbucket.org/licface/proxy_tester",
        "Code": "https://bitbucket.org/licface/proxy_tester",
    },
    license="BSD",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="proxy_tester like proxychains",
    # long_description=readme,
    # long_description_content_type="text/markdown",
    packages=["proxy_tester"],
    install_requires=requirements,
    entry_points = {
         "console_scripts": [
             "proxy_tester = proxy_tester.proxy_tester:usage",
         ]
    },
    # data_files=['__version__.py', 'README.rst', 'LICENSE.rst'],
    include_package_data=True,
    python_requires=">=2.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
