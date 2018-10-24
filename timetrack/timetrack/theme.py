colors = {
    "primary": "teal darken-2",
    "secondary": "teal lighten-2",
    "primary_text": "teal-text text-darken-2",
    "secondary_text": "teal-text text-lighten-2",
    "light_text": "white-text",
    "dark_text": "black-text",
}


def apply(c):
    c.update({"colors": colors})
    return c
