import os


def getDefaultSettingsPath() -> str:
    """
    Returns the default user settings path, it depends on the OS
    """
    if os.name == "posix":  # Linux, macOS
        return os.path.expanduser("~/.BiromeVirtual/")
    elif os.name == "nt":  # Windows
        return os.path.join(os.environ["APPDATA"], "BiromeVirtual")
    else:
        # Handle other platforms if needed
        print(f"ERROR: could not determine the default settings path")
        return ""
