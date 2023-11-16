# FORMAT CLASS

class Format:
    """Class that formats messages."""
    def __init__(self) -> None:
        """Constructor method."""
        pass

    @staticmethod
    def underline(message: str) -> str:
        """Method that underlines a message."""
        return f'\033[4m{message}\033[0m'
    
    @staticmethod
    def bold(message: str) -> str:
        """Method that bolds a message."""
        return f'\033[1m{message}\033[0m'
    
    @staticmethod
    def main(message: str) -> str:
        """Method that creates a main message."""
        return f'\033[95m{message}\033[0m'
    
    @staticmethod
    def info(message: str) -> str:
        """Method that creates an info message."""
        return f'\033[94m{message}\033[0m'

    @staticmethod
    def warning(message: str) -> str:
        """Method that creates a warning message."""
        return f'\033[93m{message}\033[0m'
    
    @staticmethod
    def error(message: str) -> str:
        """Method that creates an error message."""
        return f'\033[91m{message}\033[0m'
    
    @staticmethod
    def format(message: str, format: tuple) -> str:
        """Method that formats a message according to the 'format' argument."""
        output = message
        if 'underline' in format:
            output = Format.underline(output)
        if 'bold' in format:
            output = Format.bold(output)
        if 'main' in format:
            output = Format.main(output)
        if 'info' in format:
            output = Format.info(output)
        if 'warning' in format:
            output = Format.warning(output)
        if 'error' in format:
            output = Format.error(output)
        return output
