class ansi_colors:
    default     = "0"

    black       = "30"
    red         = "31"
    green       = "32"
    yellow      = "33"
    blue        = "34"
    magenta     = "35"
    cyan        = "36"
    white       = "37"

    bold        = "1"
    dim         = "2"
    underline   = "4"
    inverted    = "7"

def color(*colors):
    """
    Returns ASCII escape string of colors from given colors and modifiers.
    """
    ansi_color_str = "\x1b["

    for color in colors:
        ansi_color_str += f";{color}"

    return f"{ansi_color_str}m"
