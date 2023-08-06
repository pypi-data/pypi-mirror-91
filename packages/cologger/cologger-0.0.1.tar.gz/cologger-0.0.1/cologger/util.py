class Formaters:
    END = "\33[0m"
    BOLD = "\33[1m"
    ITALIC = "\33[3m"
    UNDERLINE = "\33[4m"
    SELECTED = "\33[7m"


class Colors:
    BLACK = "\33[30m"
    RED = "\33[31m"
    GREEN = "\33[32m"
    YELLOW = "\33[33m"
    BLUE = "\33[34m"
    VIOLET = "\33[35m"
    BEIGE = "\33[36m"
    WHITE = "\33[37m"


class BackgroundColors:
    BLACK = "\33[40m"
    RED = "\33[41m"
    GREEN = "\33[42m"
    YELLOW = "\33[43m"
    BLUE = "\33[44m"
    VIOLET = "\33[45m"
    BEIGE = "\33[46m"
    WHITE = "\33[47m"


def cologger_print(text):
    return text + Formaters.END
