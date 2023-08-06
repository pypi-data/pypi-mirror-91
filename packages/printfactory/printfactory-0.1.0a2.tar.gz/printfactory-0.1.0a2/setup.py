# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['printfactory', 'printfactory.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'printfactory',
    'version': '0.1.0a2',
    'description': 'Print PDF files to a local installed printer using a print tool',
    'long_description': "# printfactory\n\n`printfactory` is a package, primarily for printing PDF files to a physical printer.\n\n[![License?][shield-license]](LICENSE)\n\n**Example**\n\n    import pathlib\n    import printfactory\n\n    printer = printfactory.Printer(\n        printer_name='My Printers Name',\n    )\n\n    print_file = pathlib.Path('path/to/my.pdf')\n    printer.send(print_file)\n\n## Table of Contents\n\n- [Why?](#why)\n- [Changelog](#changelog)\n\n## Why?\n\nThe motivation for this project was to have a simple Python interface for printing PDF files to a physical printer.\nOnly public available and free software should be used on the client or server using this package. \n\n\n## printfactory package\n\n    printfactory\n        .list_printers()        # list/get available printers in system\n\n        Printer()               # Generic Printer class for printing a file with a PrintTool\n            .send()             # send a file to a printer using a PrintTool\n\n        AcroPrinter(Printer)    # Subclass of Printer() for Adobe Acrobat\n        AcroRdPrinter(Printer)  # Subclass of AcroPrinter() for Adobe Reader\n       [FoxitPrinter(Printer)]  # Subclass of Printer() for Foxit Reader\n       [LPRPrinter(Printer)]    # Subclass of Printer() for LPR printing on Linux like systems\n\n        PrintTools()            # List/Enum of implemented tools for printing a file\n            .find()             # Find a PrintTool in system\n\n        PrintTool()             # List/Enum of implemented tools for printing a file\n            Adobe Acrobat\n            Adobe Reader\n            Foxit Reader\n            LPR\n\n\n    printer = printfactory.Printer('PrinterName')   # return Printer class\n    printer.tool => AdobeReader                     # autodetect path\n    printed = printer.send('PathToPDFDocument')     # return True or False\n\n\n\n## Changelog\n\nAll notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md).\n\n\n\n[shield-license]:  https://img.shields.io/badge/license-MIT-blue.svg\n",
    'author': 'dl6nm',
    'author_email': 'mail@dl6nm.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dl6nm/printfactory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
