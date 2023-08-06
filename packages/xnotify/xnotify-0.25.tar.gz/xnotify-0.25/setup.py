import io
import re
from setuptools import setup

import os
import shutil
try:
    os.remove(os.path.join('xnotify', '__version__.py'))
except:
    pass
shutil.copy2('__version__.py', 'xnotify')

# with io.open("README.rst", "rt", encoding="utf8") as f:
#     readme = f.read()

# with io.open("__version__.py", "rt", encoding="utf8") as f:
    # version = re.search(r"version = \'(.*?)\'", f.read()).group(1)
import __version__
version = __version__.version

setup(
    name="xnotify",
    version=version,
    url="https://bitbucket.org/licface/xnotify",
    project_urls={
        "Documentation": "https://github.com/cumulus13/xnotify",
        "Code": "https://github.com/cumulus13/xnotify",
    },
    license="BSD",
    author="Hadi Cahyadi LD",
    author_email="cumulus13@gmail.com",
    maintainer="cumulus13 Team",
    maintainer_email="cumulus13@gmail.com",
    description="Send notification to growl libnotify pushbullet NotifyMyDevice",
    # long_description=readme,
    # long_description_content_type="text/markdown",
    packages=["xnotify"],
    install_requires=[
        'make_colors>=3.12',
        'configset',
        'argparse',
        'configparser',
        'sendgrowl',
        'pydebugger',
        'pushbullet_py',
        'playsound'
    ],
    entry_points = {
         "console_scripts": [
             "xnotify = xnotify:usage",
         ]
    },
    data_files=['__version__.py'],
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
    ],
)
