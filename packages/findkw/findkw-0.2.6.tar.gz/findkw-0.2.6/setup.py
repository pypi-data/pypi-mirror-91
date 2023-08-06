import setuptools
from setuptools import setup

using_setuptools = True

setup_args = {
    'name': 'findkw',
    'version': '0.2.6',
    'url': 'https://github.com/ga1008/finder',
    'description': 'find the files or words',
    'long_description': open('README.md', encoding="utf-8").read(),
    'author': 'Guardian',
    'author_email': 'zhling2012@live.com',
    'maintainer': 'Guardian',
    'maintainer_email': 'zhling2012@live.com',
    'long_description_content_type': "text/markdown",
    'LICENSE': 'MIT',
    'packages': setuptools.find_packages(),
    'include_package_data': True,
    'zip_safe': False,
    'entry_points': {
        'console_scripts': [
            'findkw = findkw.findkw:find',
        ]
    },

    'classifiers': [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    'install_requires': [
        "basecolors==0.0.2",
    ],
}

setup(**setup_args)
