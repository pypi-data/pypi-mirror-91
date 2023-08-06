from util import Colors, Formaters, BackgroundColors, cologger_print


class Cologger:
    def black(self, text):
        return Colors.BLACK + cologger_print(text)

    def red(self, text):
        return Colors.RED + cologger_print(text)

    def green(self, text):
        return Colors.GREEN + cologger_print(text)

    def yellow(self, text):
        return Colors.YELLOW + cologger_print(text)

    def blue(self, text):
        return Colors.BLUE + cologger_print(text)

    def violet(self, text):
        return Colors.VIOLET + cologger_print(text)

    def beige(self, text):
        return Colors.BEIGE + cologger_print(text)

    def white(self, text):
        return Colors.WHITE + cologger_print(text)

    class BG:
        def black(self, text):
            return BackgroundColors.BLACK + cologger_print(text)

        def red(self, text):
            return BackgroundColors.RED + cologger_print(text)

        def green(self, text):
            return BackgroundColors.GREEN + cologger_print(text)

        def yellow(self, text):
            return BackgroundColors.YELLOW + cologger_print(text)

        def blue(self, text):
            return BackgroundColors.BLUE + cologger_print(text)

        def violet(self, text):
            return BackgroundColors.VIOLET + cologger_print(text)

        def beige(self, text):
            return BackgroundColors.BEIGE + cologger_print(text)

        def white(self, text):
            return BackgroundColors.WHITE + cologger_print(text)

    class FMT:
        def bold(self, text):
            return Formaters.BOLD + cologger_print(text)

        def italic(self, text):
            return Formaters.ITALIC + cologger_print(text)

        def underline(self, text):
            return Formaters.UNDERLINE + cologger_print(text)

        def selected(self, text):
            return Formaters.SELECTED + cologger_print(text)
