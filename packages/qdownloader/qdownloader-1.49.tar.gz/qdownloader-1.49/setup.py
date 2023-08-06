import io
import re
from setuptools import setup

import os, sys
import shutil
# try:
#     os.remove(os.path.join(os.path.dirname(__file__), 'qdownloader'))
# except:
#     pass
try:
    os.makedirs(os.path.join(os.path.dirname(__file__), 'qdownloader'))
except:
    pass
try:
    os.remove(os.path.join('qdownloader', '__version__.py'))
except:
    pass
shutil.copy2('__version__.py', 'qdownloader')
shutil.copy2('qdownloader.py', 'qdownloader')
shutil.copy2('guc.py', 'qdownloader')
shutil.copy2('idm.py', 'qdownloader')
shutil.copy2('__init__.py', 'qdownloader')

# with io.open("README.rst", "rt", encoding="utf8") as f:
#     readme = f.read()

# with io.open("__version__.py", "rt", encoding="utf8") as f:
    # version = re.search(r"version = \'(.*?)\'", f.read()).group(1)
import __version__
version = __version__.version

requirements = [
        'make_colors>=3.12',
        'requests',
        'progressbar2',
        'bs4',
        'clipboard',
        'pydebugger',
        'configset',
        'proxy_tester',
        'safeprint',
        'xnotify',
        'youtube_dl',
    ]

if sys.platform == 'win32':
    requirements.append('pyidm')

setup(
    name="qdownloader",
    version=version,
    url="https://bitbucket.org/licface/qdownloader",
    project_urls={
        "Documentation": "https://bitbucket.org/licface/qdownloader",
        "Code": "https://bitbucket.org/licface/qdownloader",
    },
    license="BSD",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="qdownloader cli",
    # long_description=readme,
    # long_description_content_type="text/markdown",
    packages=["qdownloader"],
    install_requires=requirements,
    entry_points = {
         "console_scripts": [
             "qdownloader = qdownloader.qdownloader:usage",
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
