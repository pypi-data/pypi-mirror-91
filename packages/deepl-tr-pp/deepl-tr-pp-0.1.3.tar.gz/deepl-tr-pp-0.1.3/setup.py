# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepl_tr_pp']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.11.0,<0.12.0',
 'cchardet>=2.1.7,<3.0.0',
 'docx2txt>=0.8,<0.9',
 'environs>=9.2.0,<10.0.0',
 'logzero>=1.6.3,<2.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'pyperclip>=1.8.1,<2.0.0',
 'pyppeteer2>=0.2.2,<0.3.0',
 'pyquery>=1.4.3,<2.0.0',
 'python-docx>=0.8.10,<0.9.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'tqdm>=4.56.0,<5.0.0']

entry_points = \
{'console_scripts': ['deepl-tr-pp = deepl_tr_pp.__main__:main']}

setup_kwargs = {
    'name': 'deepl-tr-pp',
    'version': '0.1.3',
    'description': 'deepl translate via pyppeteer',
    'long_description': '# deepl-tr-pyppeteer\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ba7c2468eb574642892676deafb98ecc)](https://www.codacy.com/gh/ffreemt/deepl-tr-pyppeteer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/deepl-tr-pyppeteer&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/deepl-tr-pp.svg)](https://badge.fury.io/py/deepl-tr-pp)\n\ndeepl translate via pyppeteer\n\n## Installation\n```bash\npip install deepl-tr-pp\n```\nTo update to the latest version:\n```bash\npip install deepl-tr-pp -U\n# poetry add deepl-tr-pp@latest  # if you use poetry\n```\nor clone the github repo, install and run from the source\n```bash\ngit clone clone https://github.com/ffreemt/deepl-tr-pyppeteer\ncd deepl-tr-pyppeteer\npip install poetry\npoetry install --no-dev\n\npoetry run python -m deepl_tr_pp  # equivalent to executing `deepl-tr-pp` below\n```\n\n## Usage\nLanguages supported: `["en", "de", "zh", "fr", "es", "pt", "it", "nl", "pl", "ru", "ja"]` (currently supported by the website)\n\nInput file formats currently supported: txt and docx, files with other suffix (e.g., .csv, .tsv) will simply treated as text.\n\nTo interrupt anytime: `Ctrl-c`. The first few versions may not run too smoothly. If it hangs, press `control` and `c` at the same time to exit.\n\n```bash\ndeepl-tr-pp -p file.txt  # en to zh, default en to zh, dualtext output, docx format\ndeepl-tr-pp -p file.txt -f de   # de to zh\ndeepl-tr-pp -p file.txt -f de -t en  # de to en\n\ndeepl-tr-pp   # browse for a file, en to zh\n\ndeepl-tr-pp --copyfrom   # text from the clipboard, en to zh\n\ndeepl-tr-pp -p file.txt --nodualtext  # en to zh, default en to zh, just translate text\n\ndeepl-tr-pp -p file.txt --nooutput-docx  # default en to zh, dualtext, text format\n```\n\nBy default, the text version of the output is copied to the clipboard, turn this off by --nocopyto\n```bash\ndeepl-tr-pp -p file.txt --nocopyto\n```\n\n### Finer Control Using .env and Environ Variables\nTo show the browser in action or set debug or proxy, create an `.env` file and set the corresponding environ variables (these can also be set from the command line, e.g., `set DEEPLTR_HEADFUL=true` (in Windows) or `export DEEPLTR_HEADFUL=true` (in Linux) ):\n```bash\n# .env\nDEEPLTR_HEADFUL=true\nDEEPLTR_DEBUG=true\n\n# DEEPLTR_HEADFUL=True\n# DEEPLTR_HEADFUL=tRue  # also works\n# DEEPLTR_HEADFUL=False\n# DEEPLTR_HEADFUL=fAlse\n# DEEPLTR_HEADFUL=1\n# DEEPLTR_HEADFUL=\'1\'\n# must use capitals\n# DEEPLTR_PROXY=SOCKS5://127.0.0.1:1080\n\n```\n\n## Help\n```bash\ndeepl-tr-pp  --helpshort\n```\n```bash\n  --[no]copyfrom: copy from clipboard, default false, will attempt to browser\n    for a filepath if copyfrom is set false)\n    (default: \'false\')\n  --[no]copyto: copy the result to clipboard\n    (default: \'true\')\n  --[no]debug: print debug messages.\n    (default: \'false\')\n  -d,--[no]dualtext: dualtext or no dualtext output\n    (default: \'true\')\n  -p,--filepath: source text filepath (relative or absolute), if not provided,\n    clipboard content will be used as source text.\n    (default: \'\')\n  -f,--from-lang: source language, default english)\n    (default: \'en\')\n  -o,--[no]output-docx: output docx or text\n    (default: \'true\')\n  -t,--to-lang: target language, default chinese\n    (default: \'zh\')\n  --[no]version: print version and exit\n    (default: \'false\')\n```\nor\n\n```bash\ndeepl-tr-pp --helpfull\n```\n\n## For Developers\n  * Install `poetry` the way you like it.\n\n  * git clone the repo `https://github.com/ffreemt/deepl-tr-pyppeteer`,\n`cd deepl-tr-pyppeteer`\n    * Or fork first and `git pull` your own repo.\n\n  * `poetry install`\n\n  * Activate the virtual environment, e.g., `.venv\\Scripts\\activate` (In Windows) or `source .venv/bin/activate` (in Linux) provided you set `poetry config --local virtualenvs.in-project true`\n    * `python -m deepl_tr_pp`\n\n  * Code and optionally submit PR\n',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/deepl-tr-pyppeteer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
