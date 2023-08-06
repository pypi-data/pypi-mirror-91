import pathlib
import platform
import subprocess

from printfactory.models.print_tools import AdobeReader


def list_printers() -> list:
    """Get a list of installed printers

    :return: List of printers
    """
    args = None
    shell = False
    pltfrm = platform.system()
    if pltfrm == 'Windows':
        args = ['wmic', 'printer', 'get', 'name']
    elif pltfrm == 'Darwin':
        args = ["lpstat -p | awk '{print $2}'"]
        shell = True

    proc = subprocess.run(
        args=args,
        capture_output=True,
        encoding='utf-8',
        text=True,
        shell=shell,
    )

    lines = proc.stdout.splitlines()
    printers = []

    for line in lines:
        line = line.strip()
        if line not in ['', 'Name', '\n']:
            printers.append(line)

    return printers


class Printer:
    """
    Main printer class

        - initialize Printer class
        - set printer options
        - auto-check
            - available pdf reader (Acrobat, Adobe Reader, Foxit Reader, ...)
            - available printers (get list)
        - print document
    """

    def __init__(
            self,
            printer_name: str = None,
            driver_name: str = None,
            port_name: str = None,
            # print_tool: PrintTool = None,
    ):
        """
        Base printfactory class

        :param printer_name: Name of the printer, use systems default printer if not given
        :param driver_name: Driver name that should be used
        :param port_name: Port of the printer
        :param print_tool: Platform dependent tool, used for printing a file
        """
        self.name: str = printer_name
        self.driver: str = driver_name
        self.port: str = port_name
        # self.print_tool = print_tool

        pltfrm = platform.system()
        # if print_tool is None:
        if pltfrm == 'Windows':
            self.print_tool = AdobeReader(
                printer_name=self.name,
                driver_name=self.driver,
                port_name=self.port,
            )
        elif pltfrm == 'Darwin':
            raise NotImplementedError
        else:
            raise NotImplementedError

    def send(self, print_file: pathlib.Path, timeout=30) -> None:
        """
        Send a file to the printer

        :param print_file: File-like object that should be printed
        :param timeout: Timeout in seconds
        :return: True if file was sent to printer, False otherwise
        """
        if not print_file.is_file():
            raise FileNotFoundError

        args = self.print_tool.get_args(print_file=print_file)
        try:
            proc = subprocess.run(args=args, timeout=timeout)
        except subprocess.TimeoutExpired:
            pass


if __name__ == '__main__':
    printer = Printer('EPSON AL-C2800N')
    file = pathlib.Path('../tests/integration/data/my.pdf')
    printer.send(print_file=file)
