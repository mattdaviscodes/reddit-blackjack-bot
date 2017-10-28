"""Helper functions for blackjack.py."""


def active_marker():
    """Return an ascii arrow to indicate active hand."""
    return "\n\n<-\n"


def merge_ascii(ascii_list=None, *args):
    """Merge a series of multi-line ascii art units into a single unit.

    This method is totally unreadable, but it works. Might want to refactor
    later to be more developer-friendly.

    :return: single-string ascii representation of all cards
    """

    if ascii_list:
        ascii = [item.split('\n') for item in ascii_list]
    else:
        ascii = [arg.split('\n') for arg in args]
    return '\n'.join([' '.join(line) for line in zip(*ascii)])