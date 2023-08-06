# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moin2gitwiki']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'furl>=2.1.0,<3.0.0',
 'requests[socks]>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['moin2gitwiki = moin2gitwiki.cli:moin2gitwiki']}

setup_kwargs = {
    'name': 'moin2gitwiki',
    'version': '0.2.0',
    'description': 'MoinMoin To Git (Markdown) Wiki Converter',
    'long_description': '# MoinMoin To Git (Markdown) Wiki Converter\n\nApp to convert a MoinMoin wiki file tree into a git based wiki as used on\ngithub, gitlab or gitea.\n\n## Current Version\n\nVersion: `0.2.0`\n\n## Translation Method\n\nOriginally the intention was to translate purely by converting the MoinMoin\nmarkup to markdown markup - using the MoinMoin data retrieved from the\nfilesystem.\n\nHowever, although it makes determining the overall page list and revision list\nmuch easier, it was found that translating the wiki markup at this level was\ntoo complex and fragile for this to work without a huge amount of special\ncasing.\n\nSo, after the revision structure is derived from the filesystem, each page\nrevision is retrieved by http requests to the running MoinMoin wiki.  This is\nthen reduced to just the page content (by picking out the content div from the\nhtml), and some light editing applied to simplify the HTML - specifically:-\n\n- Remove the anchor spans that MoinMoin adds - these add no visual or\n  readable content, but confuse the translator\n- Remove paragraph entries with CSS classes that start `line` - these\n  again appear to be for non-required purposes (likely for showing diffs\n  between revisions) - and they break the translator\n- Fix links that point within the wiki - if the target does not exist\n  then the text is left but the link removed.\n- Strips CSS classes off links - again these upset the translator\n- Translate any images that appear to be MoinMoin emoji characters (which\n  are rendered as images) into gollum emoji characters\n\nThis simplified HTML is then passed through the pandoc command:-\n\n    pandoc -f html -t gfm\n\nAnd the resulting Github flavoured Markdown is taken as the new form.\n\nThis handles the vast majority of normal markup correctly, including lists and\nmany types of tables.  Some complicated markup or complex tables end up being\npassed through as HTML - which displays correctly but is less easy to parse\nand edit.\n\n## Issues\n\nThe overall process is not particularly fast.  But this should be something\nyou only do once (or a few attempts) so raw speed is not needed.\n\n## Installation\n\nI have not at this point made this available as a pypi package, although there\nshould be a package file in the releases set on github.\n\nHowever it can be installed from the repo - it uses\n[`poetry`](https://python-poetry.org/) to manage dependancies etc, so the best\nway to make use of this is to install [`poetry`](https://python-poetry.org/)\nfor your python version and then:-\n\n    poetry install\n\nthe command can then be run as\n\n    poetry run moin2gitwiki ...\n\n\n\n----\n',
    'author': 'Nigel Metheringham',
    'author_email': 'nigelm@cpan.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nigelm/moin2gitwiki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
