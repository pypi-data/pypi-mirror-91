# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['download_aptnotes']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'aiohttp[speedups]>=3.7.3,<4.0.0',
 'aiosqlite>=0.16.0,<0.17.0',
 'beautifulsoup4[lxml]>=4.9.3,<5.0.0',
 'janus>=0.6.1,<0.7.0',
 'typer[all]>=0.3.2,<0.4.0',
 'uvloop>=0.14.0,<0.15.0']

extras_require = \
{'tika': ['tika>=1.24,<2.0']}

entry_points = \
{'console_scripts': ['download-aptnotes = download_aptnotes.cli:app']}

setup_kwargs = {
    'name': 'download-aptnotes',
    'version': '0.1.0',
    'description': 'Download and (optionally) parse APTNotes quickly and easily',
    'long_description': '# Download APTNotes\n\nDownload and (optionally) parse [APTNotes](https://github.com/aptnotes/data) quickly and easily\n\n## Installation\n\n```bash\npip install download-aptnotes\n```\n\nTo enable parsing the downloaded PDFs you need to install the extra `tika`. This\nwill try to install the Apache Tika Server which depends on Java 7+. Make sure\nthat you have an adequate version of Java installed before you try to install it\nWithout this extra, the only output format available is `pdf`.\n\n```bash\npip install download-aptnotes[tika]\n```\n\n## Usage\n\n```txt\nUsage: download-aptnotes [OPTIONS]\n\n  Download and (optionally) parse APTNotes quickly and easily\n\nOptions:\n  -f, --format [pdf|sqlite|json|csv]\n                                  Output format  [required]\n  -o, --output PATH               Output path of file or directory  [required]\n  -l, --limit INTEGER             Number of files to download\n  -p, --parallel INTEGER          Number of parallell downloads  [default: 10]\n  --install-completion            Install completion for the current shell.\n  --show-completion               Show completion for the current shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n```\n\nDownload all documents, parse them and store them in an SQLite database:\n\n```bash\ndownload-aptnotes -f sqlite -o aptnotes.sqlite\n```\n\nDownload the first 10 documents in the source list, parse them and store\nthem in an SQLite database:\n\n```bash\ndownload-aptnotes -f sqlite -o aptnotes.sqlite -l 10\n```\n\nDownload all documents and store them as individual files in a directory:\n\n```bash\ndownload-aptnotes -f pdf -o aptnotes/\n```\n\n## Contributing\n\nDependencies:\n\n- Java 7+\n- Poetry\n\nClone this repository and install all dependencies:\n\n````bash\ngit clone https://github.com/nikstur/download-aptnotes.git\ncd download-aptnotes\npoetry install\n````\n',
    'author': 'nikstur',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nikstur/download-aptnotes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
