# printfactory

`printfactory` is a package, primarily for printing PDF files to a physical printer.

[![License?][shield-license]](LICENSE)

**Example**

    import pathlib
    import printfactory

    printer = printfactory.Printer(
        printer_name='My Printers Name',
    )

    print_file = pathlib.Path('path/to/my.pdf')
    printer.send(print_file)

## Table of Contents

- [Why?](#why)
- [Changelog](#changelog)

## Why?

The motivation for this project was to have a simple Python interface for printing PDF files to a physical printer.
Only public available and free software should be used on the client or server using this package. 


## printfactory package

    printfactory
        .list_printers()        # list/get available printers in system

        Printer()               # Generic Printer class for printing a file with a PrintTool
            .send()             # send a file to a printer using a PrintTool

        AcroPrinter(Printer)    # Subclass of Printer() for Adobe Acrobat
        AcroRdPrinter(Printer)  # Subclass of AcroPrinter() for Adobe Reader
       [FoxitPrinter(Printer)]  # Subclass of Printer() for Foxit Reader
       [LPRPrinter(Printer)]    # Subclass of Printer() for LPR printing on Linux like systems

        PrintTools()            # List/Enum of implemented tools for printing a file
            .find()             # Find a PrintTool in system

        PrintTool()             # List/Enum of implemented tools for printing a file
            Adobe Acrobat
            Adobe Reader
            Foxit Reader
            LPR


    printer = printfactory.Printer('PrinterName')   # return Printer class
    printer.tool => AdobeReader                     # autodetect path
    printed = printer.send('PathToPDFDocument')     # return True or False



## Changelog

All notable changes to this project will be documented in the [CHANGELOG.md](CHANGELOG.md).



[shield-license]:  https://img.shields.io/badge/license-MIT-blue.svg
