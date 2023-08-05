# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idppnpdongle']

package_data = \
{'': ['*']}

install_requires = \
['gpiozero>=1.5.1,<2.0.0', 'idpmodem>=1.1.2,<2.0.0', 'pigpio>=1.78,<2.0']

setup_kwargs = {
    'name': 'idppnpdongle',
    'version': '0.1.1',
    'description': "Module for interfacing with Inmarsat's IDP Plug-N-Play device.",
    'long_description': '# Inmarsat IDP Plug-N-Play Dongle\n\nThe Plug-N-Play dongle is a small programmable single board computer in a\nblack box intended to be able to quickly demonstrate and prototype \nInternet-of-Things use cases enabled by satellite messaging connectivity.\n\nThe dongle connects directly to an **ST2100** satellite modem manufactured by\n[ORBCOMM](www.orbcomm.com) and provides access to:\n\n  * Serial communications using **AT commands**\n  * Modem **event notification** via discrete output pin to a callback function\n  * Reset via external **reset** pin\n  * 1 pulse-per-second (**PPS**) from GNSS timing via discrete output pin\n\nThe dongle `mode` can be configured to:\n\n1. `transparent` pass through serial commands to a separate third party \nmicrocontroller (default hardware configuration)\n2. `master` act as the application microcontroller \n*(default when using this Python module)*\n3. `proxy` act as a proxy intercepting responses from the modem to a third \nparty microcontroller\n\n## Installation\n\n```\npip install idppnpdongle\n```',
    'author': 'G.Bruce-Payne',
    'author_email': 'geoff.bruce-payne@inmarsat.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Inmarsat/idp-pnpdongle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
