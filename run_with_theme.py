import sys

from colorama import Fore, Style, just_fix_windows_console


def run_with_theme(main):
    if not sys.stdout.isatty():
        main()
        return

    just_fix_windows_console()

    print("\x1b[?1049h", end="", flush=True)
    try:

        print("\x1b[48;2;23;37;84m" + Fore.WHITE + "\x1b[2J\x1b[H", end="", flush=True)
        main()
    finally:
        print(Style.RESET_ALL + "\x1b[?1049l", end="", flush=True)
