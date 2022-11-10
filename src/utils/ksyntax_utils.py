import json
import os
import globals


def export_schemes(schemes=None):
    # Make sure the schemes path exists
    if not os.path.exists(globals.KSYNTAX_THEMES_DIR):
        os.makedirs(globals.KSYNTAX_THEMES_DIR)
    light_scheme = schemes.get_ksyntax_highlighting_light()
    dark_scheme = schemes.get_ksyntax_highlighting_dark()

    with open(globals.KSYNTAX_THEMES_DIR+"material-you-dark.theme", 'w', encoding='utf8') as ksyntax_theme:
        json.dump(dark_scheme, ksyntax_theme, indent=4, ensure_ascii=False)
    with open(globals.KSYNTAX_THEMES_DIR+"material-you-light.theme", 'w', encoding='utf8') as ksyntax_theme:
        json.dump(light_scheme, ksyntax_theme, indent=4, ensure_ascii=False)

# TODO: find a way to reload ksyntax themes, if any
# def reload(light=False):
