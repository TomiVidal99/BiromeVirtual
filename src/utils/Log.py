class Log:
    """
    Wrapping utility class to print out loggin information
    and handle logging in a better way
    """

    def __init__(self) -> None:
        self.allowInfo = True
        self.allowWarn = True
        self.allowError = True
        return None

    def info(self, mes: str) -> None:
        """
        Prints an info message
        """
        if self.allowInfo:
            print(f"--INFO--> {mes}")
        return None

    def warn(self, mes: str) -> None:
        """
        Prints an warn message
        """
        if self.allowWarn:
            print(f"--WARN--> {mes}")
        return None

    def error(self, mes: str) -> None:
        """
        Prints an error message
        """
        if self.allowError:
            print(f"--ERROR--> {mes}")
        return None
