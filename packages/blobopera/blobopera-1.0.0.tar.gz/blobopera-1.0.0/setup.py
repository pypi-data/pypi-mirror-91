# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blobopera', 'blobopera.backend', 'blobopera.command', 'blobopera.languages']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'matplotlib>=3.3.3,<4.0.0',
 'more-itertools>=8.6.0,<9.0.0',
 'music21>=6.3.0,<7.0.0',
 'numpy>=1.19.4,<2.0.0',
 'proto-plus>=1.13.0,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['blobopera = blobopera.command:application']}

setup_kwargs = {
    'name': 'blobopera',
    'version': '1.0.0',
    'description': 'Unofficial toolkit for Google Arts & Culture Blob Opera',
    'long_description': '<h1 align="center">Blob Opera Toolkit</h1>\n\n<p align="center">\n    <a href="https://github.com/0x2b3bfa0/python-blobopera/actions">\n        <img alt="test" src="https://github.com/0x2b3bfa0/python-blobopera/workflows/test/badge.svg?branch=main">\n    </a>\n    <a href="https://github.com/0x2b3bfa0/python-blobopera/actions">\n        <img alt="lint" src="https://github.com/0x2b3bfa0/python-blobopera/workflows/lint/badge.svg?branch=main">\n    </a>\n    <a href="https://github.com/0x2b3bfa0/python-blobopera/actions">\n        <img alt="lint" src="https://github.com/0x2b3bfa0/python-blobopera/workflows/coverage/badge.svg?branch=main">\n    </a>\n    <a href="https://www.gnu.org/licenses/gpl-3.0">\n        <img alt="license" src="https://img.shields.io/badge/license-GPL3-blue.svg">\n    </a>\n    <a href="https://github.com/psf/black">\n        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n    </a>\n</p>\n\n## Description\n\nUnofficial toolkit to convert MusicXML files into [Blob Opera][1] scores with\nreal lyrics, loosely inspired by [OverlappingElvis/blob-opera-midi][2].\n\n## Documentation\n\n* Full [command documentation][12].\n* Generated [module documentation][19].\n\n## Samples\n\n* **[Adeste Fideles][5]** ([_source_][7], [_information_][6])\n* **[Symphony No. 9 (Beethoven)][13]** ([_source_][15], [_information_][14])\n* **[Ave Maria (Schubert)][20]** ([_source_][21], [_information_][22])\n\n## Usage\n\n1. Create a score file:\n   Use [MuseScore][3] or similar to create a four-part score\n   (soprano, alto, tenor and bass) with a single line of lyrics and export it\n   to [MusicXML][4]. You can download MusicXML files from MuseScore\n   by using [this tool][8].\n\n2. Install the requirements (using [poetry][11]):\n   ```bash\n   poetry install\n   ```\n\n3. Convert the score file:\n   ```bash\n   poetry run blobopera recording import input.musicxml output.binary\n   ```\n\n4. Upload the recording:\n   ```bash\n   poetry run blobopera recording upload output.binary\n   ```\n\n5. Visit the generated link with your browser.\n\n## Known issues\n\n* Pronunciation is far from perfect and consonants may be too faint\n  to articulate the supporting note; feel free to add more\n  language-phoneme maps.\n\n* Timing can go completely off if the source score has metronome marks on it\n  because they are being interpreted only for the first of the four parts.\n  Please delete all the tempo marks on the score and use the `--tempo` option\n  within the `recording create` subcommand in order to modify the global tempo:\n  0.5 will slow down the entire recording to half the original speed.\n\n## Contributing\n\nContributions are welcome! Don\'t forget to run `poetry run poe all` to\nvalidate your code before starting a pull request.\n\n[1]: https://artsandculture.google.com/experiment/blob-opera/AAHWrq360NcGbw\n[2]: https://github.com/OverlappingElvis/blob-opera-midi\n[3]: https://musescore.org/en\n[4]: https://en.wikipedia.org/wiki/MusicXML\n[5]: https://g.co/arts/hrjRDrpL5G7LrjRx7\n[6]: https://en.wikipedia.org/wiki/O_Come,_All_Ye_Faithful\n[7]: https://musescore.com/user/29729/scores/416701\n[8]: https://github.com/Xmader/musescore-downloader\n[11]: https://python-poetry.org/docs/\n[12]: ./documentation/command\n[13]: https://g.co/arts/vFxPVuuTATXNvX9F8\n[14]: https://en.wikipedia.org/wiki/Symphony_No._9_(Beethoven)#IV._Finale\n[15]: https://musescore.com/user/34418260/scores/6430537\n[16]: https://artsandculture.google.com/experiment/blob-opera/AAHWrq360NcGbw?cp=eyJyIjoiNVNxb0RhRlB1VnRuIn0.\n[17]: https://en.wikipedia.org/wiki/Mateo_Flecha\n[18]: https://musescore.com/user/28092/scores/85307\n[19]: https://0x2b3bfa0.github.io/python-blobopera\n[20]: https://g.co/arts/xQGR5aWBwuDeGqTq8\n[21]: http://www.cafe-puccini.dk/Schubert_GdurMesse.aspx\n[22]: https://en.wikipedia.org/wiki/Ave_Maria_(Schubert)\n',
    'author': 'Helio Machado',
    'author_email': '0x2b3bfa0@googlemail.com',
    'maintainer': 'Helio Machado',
    'maintainer_email': '0x2b3bfa0@googlemail.com',
    'url': 'https://github.com/0x2b3bfa0/python-blobopera',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
