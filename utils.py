import os
from pathlib import Path
import subprocess
import json
import configparser
import numpy as np
import dbus
from color_utils import hex2rgb, rgb2hex
import importlib.util
USER_HAS_COLR = importlib.util.find_spec("colr") is not None
if USER_HAS_COLR:
    from colr import color
USER_HAS_PYWAL = importlib.util.find_spec("pywal") is not None
if USER_HAS_PYWAL:
    import pywal
import logging
logging.basicConfig(format='pywal:%(module)s: %(message)s',level=logging.DEBUG)
HOME = str(Path.home())
THEME_LIGHT_PATH = HOME+"/.local/share/color-schemes/MaterialYouLight"
THEME_DARK_PATH = HOME+"/.local/share/color-schemes/MaterialYouDark"
SAMPLE_CONFIG_FILE = "sample_config.conf"
CONFIG_FILE = "config.conf"
SAMPLE_CONFIG_PATH = "/usr/lib/kde-material-you-colors/"
USER_CONFIG_PATH = HOME+"/.config/kde-material-you-colors/"
USER_SCHEMES_PATH = HOME+"/.local/share/color-schemes/"
AUTOSTART_SCRIPT = "kde-material-you-colors.desktop"
SAMPLE_AUTOSTART_SCRIPT_PATH = "/usr/lib/kde-material-you-colors/"
USER_AUTOSTART_SCRIPT_PATH = HOME+"/.config/autostart/"
DEFAULT_PLUGIN = 'org.kde.image'
PICTURE_OF_DAY_PLUGIN = 'org.kde.potd'
PLAIN_COLOR_PLUGIN = 'org.kde.color'
PICTURE_OF_DAY_PLUGIN_IMGS_DIR = HOME+'/.cache/plasma_engine_potd/'
PICTURE_OF_DAY_UNSPLASH_PROVIDER = 'unsplash'
PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY = '1065976'
PICTURE_OF_DAY_DEFAULT_PROVIDER = 'apod'  # astronomy picture of the day
KDE_GLOBALS = HOME+"/.config/kdeglobals"
BREEZE_RC = HOME+"/.config/breezerc"
KONSOLE_DIR = HOME+"/.local/share/konsole/"
KONSOLE_COLOR_SCHEME_PATH = KONSOLE_DIR+"MaterialYou.colorscheme"
KONSOLE_COLOR_SCHEME_ALT_PATH = KONSOLE_DIR+"MaterialYouAlt.colorscheme"
KONSOLE_TEMP_PROFILE=KONSOLE_DIR+"TempMyou.profile"
BOLD_TEXT = "\033[1m"
RESET_TEXT = "\033[0;0m"


class Configs():
    """
    Select configuration based on arguments and config file
    
    Returns:
        dict: Settings dictionary
    """
    def __init__(self, args):
        c_light = c_monitor = c_file = c_plugin = c_ncolor = c_iconsdark = c_iconslight = c_pywal = c_pywal_light = c_light_blend_multiplier = c_dark_blend_multiplier = c_on_change_hook = c_sierra_breeze_buttons_color = c_konsole_profile = None 
        # User may just want to set the startup script / default config, do that only and exit
        if args.autostart == True:
            if not os.path.exists(USER_AUTOSTART_SCRIPT_PATH):
                os.makedirs(USER_AUTOSTART_SCRIPT_PATH)
            if not os.path.exists(USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT):
                try:
                    subprocess.check_output("cp "+SAMPLE_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT+" "+USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT,
                                            shell=True)
                    print(
                        f"Autostart script copied to: {USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT}")
                except Exception:
                    quit(1)
            else:
                print(
                    f"Autostart script already exists in: {USER_AUTOSTART_SCRIPT_PATH+AUTOSTART_SCRIPT}")
            quit(0)
        elif args.copyconfig == True:
            if not os.path.exists(USER_CONFIG_PATH):
                os.makedirs(USER_CONFIG_PATH)
            if not os.path.exists(USER_CONFIG_PATH+CONFIG_FILE):
                try:
                    subprocess.check_output("cp "+SAMPLE_CONFIG_PATH+SAMPLE_CONFIG_FILE+" "+USER_CONFIG_PATH+CONFIG_FILE,
                                            shell=True)
                    print(f"Config copied to: {USER_CONFIG_PATH+CONFIG_FILE}")
                except Exception:
                    quit(1)
            else:
                print(
                    f"Config already exists in: {USER_CONFIG_PATH+CONFIG_FILE}")
            quit(0)
        else:
            config = configparser.ConfigParser()
            if os.path.exists(USER_CONFIG_PATH+CONFIG_FILE):
                try:
                    config.read(USER_CONFIG_PATH+CONFIG_FILE)
                    if 'CUSTOM' in config:
                        custom = config['CUSTOM']

                        if 'light' in custom:
                            c_light = custom.getboolean('light')

                        if 'file' in custom:
                            c_file = custom['file']

                        if 'monitor' in custom:
                            c_monitor = custom.getint('monitor')
                            if c_monitor < 0:
                                raise ValueError(
                                    'Config for monitor must be a positive integer')

                        if 'ncolor' in custom:
                            c_ncolor = custom.getint('ncolor')
                            if c_ncolor < 0:
                                raise ValueError(
                                    'Config for ncolor must be a positive integer')

                        if 'plugin' in custom:
                            c_plugin = custom['plugin']

                        if 'iconslight' in custom:
                            c_iconslight = custom['iconslight']

                        if 'iconsdark' in custom:
                            c_iconsdark = custom['iconsdark']
                            
                        if 'pywal' in custom:
                            c_pywal = custom.getboolean('pywal')
                        
                        if 'pywal_light' in custom:
                            c_pywal_light = custom.getboolean('pywal_light')
                            
                        if 'light_blend_multiplier' in custom:
                            c_light_blend_multiplier = custom.getfloat('light_blend_multiplier')
                            
                        if 'dark_blend_multiplier' in custom:
                            c_dark_blend_multiplier = custom.getfloat('dark_blend_multiplier')
                            
                        if 'on_change_hook' in custom:
                            c_on_change_hook = custom['on_change_hook']
                            
                        if 'sierra_breeze_buttons_color' in custom:
                            c_sierra_breeze_buttons_color = custom.getboolean('sierra_breeze_buttons_color')
                            
                        if 'konsole_profile' in custom:
                            c_konsole_profile = custom['konsole_profile']

                except Exception as e:
                    print(f"Please fix your settings file:\n {e}\n")
            if args.dark == True:
                c_light = False
            elif args.light == True:
                c_light = args.light
            elif c_light != None:
                c_light = c_light
                
            if args.pywal == True:
                c_pywal = args.pywal
            elif c_pywal == None:
                c_pywal = args.pywal
                
            if args.pywaldark == True:
                c_pywal_light = False
            elif args.pywallight == True:
                c_pywal_light = args.pywallight
            else:
                c_pywal_light = c_pywal_light

            if args.lbmultiplier != None:
                c_light_blend_multiplier = range_check(args.lbmultiplier, 0, 4)
            elif c_light_blend_multiplier != None:
                c_light_blend_multiplier = range_check(c_light_blend_multiplier, 0, 4)
                
            if args.dbmultiplier != None:
                c_dark_blend_multiplier = range_check(args.dbmultiplier, 0, 4)
            elif c_dark_blend_multiplier != None:
                c_dark_blend_multiplier = range_check(c_dark_blend_multiplier, 0, 4)
                
            if args.file != None:
                c_file = args.file
            elif c_file == None:
                c_file = args.file

            if args.monitor != None:
                if args.monitor < 0:
                    raise ValueError(
                        'Value for --monitor must be a positive integer')
                else:
                    c_monitor = args.monitor
            elif args.monitor == None and c_monitor == None:
                c_monitor = 0
            else:
                c_monitor = c_monitor

            if args.ncolor != None:
                if args.ncolor < 0:
                    raise ValueError(
                        'Value for --ncolor must be a positive integer')
                else:
                    c_ncolor = args.ncolor
            elif args.ncolor == None and c_ncolor == None:
                c_ncolor = 0
            else:
                c_ncolor = c_ncolor

            if args.plugin != None:
                c_plugin = args.plugin
            elif args.plugin == None and c_plugin == None:
                c_plugin = DEFAULT_PLUGIN
            else:
                c_plugin = c_plugin

            if args.iconslight != None:
                c_iconslight = args.iconslight
            elif c_iconslight == None:
                c_iconslight = args.iconslight

            if args.iconsdark != None:
                c_iconsdark = args.iconsdark
            elif c_iconsdark == None:
                c_iconsdark = args.iconsdark
                
            if args.on_change_hook != None:
                c_on_change_hook = args.on_change_hook
            elif c_on_change_hook == None:
                c_on_change_hook = args.on_change_hook
                
            if args.sierra_breeze_buttons_color == True:
                c_sierra_breeze_buttons_color = args.sierra_breeze_buttons_color
            elif c_sierra_breeze_buttons_color != None:
                c_sierra_breeze_buttons_color = c_sierra_breeze_buttons_color
                
            if args.konsole_profile != None:
                c_konsole_profile = args.konsole_profile
            elif c_konsole_profile == None:
                c_konsole_profile = args.konsole_profile


            self._options = {
                'light': c_light,
                'file': c_file,
                'monitor': c_monitor,
                'plugin': c_plugin,
                'ncolor': c_ncolor,
                'iconslight': c_iconslight,
                'iconsdark': c_iconsdark,
                "pywal": c_pywal,
                "pywal_light":  c_pywal_light,
                "lbm": c_light_blend_multiplier,
                "dbm": c_dark_blend_multiplier,
                "on_change_hook": c_on_change_hook,
                "sierra_breeze_buttons_color" : c_sierra_breeze_buttons_color,
                "konsole_profile" : c_konsole_profile
                }

    @property
    def options(self):
        return self._options
    
    
def get_wallpaper_data(plugin=DEFAULT_PLUGIN, monitor=0, file=None):
    """Get current wallpaper or color from text file or plugin + containment combo
    and return a string with its type (color or image file)

    Args:
        script (str): javascript to evaluate
        monitor (int): containment (monitor) number
        plugin (str): wallpaper plugin id

    Returns:
        tuple: (type (int), data (str))
    """
    if file:
        if os.path.exists(file):
            with open(file) as file:
                wallpaper = str(file.read()).replace('file://', '').strip()
                if wallpaper:
                    return ("image",wallpaper)
                else:
                    return None
        else:
            print(f'File "{file}" does not exist')
            return None
    else:
        # special case for picture of the day plugin that requires a
        # directory, provider and a category
        if plugin == PICTURE_OF_DAY_PLUGIN:
            # wait a bit to for wallpaper update
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Provider")+","+d.readConfig("Category"));
            """

            try:
                script_output = tuple(evaluate_script(
                script, monitor, plugin).split(","))
            except:
                script_output = ('','')
            img_provider = script_output[0]
            provider_category = script_output[1]
            
            if img_provider:
                potd = PICTURE_OF_DAY_PLUGIN_IMGS_DIR+img_provider
            else:
                # default provider is astronomic photo of the day
                potd = PICTURE_OF_DAY_PLUGIN_IMGS_DIR+PICTURE_OF_DAY_DEFAULT_PROVIDER

            # unsplash also has a category
            if img_provider == PICTURE_OF_DAY_UNSPLASH_PROVIDER:
                # defaul category doesnt doesnt return id, add it
                if not provider_category:
                    provider_category = PICTURE_OF_DAY_UNSPLASH_DEFAULT_CATEGORY
                potd = f"{potd}:{provider_category}"
                
            if os.path.exists(potd):
                return ("image",potd)
            else:
                return None
        elif plugin == PLAIN_COLOR_PLUGIN:
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Color"));
            """
            try:
                color_rgb =  tuple((evaluate_script(script, monitor, plugin)).split(","))
                r = int(color_rgb[0])
                g = int(color_rgb[1])
                b = int(color_rgb[2])
                
                return ("color",rgb2hex(r, g, b))
            except:
                return None
        else:
            # wallpaper plugin that stores current image
            script = """
            var Desktops = desktops();
                d = Desktops[%s];
                d.wallpaperPlugin = "%s";
                d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                print(d.readConfig("Image"));
            """
            try:
                wallpaper =  evaluate_script(script, monitor, plugin)
                return ("image",wallpaper)
            except:
                return None
            
def evaluate_script(script, monitor, plugin):
    """Make a dbus call to org.kde.PlasmaShell.evaluateScript to get wallpaper data

    Args:
        script (str): js string to evaluate
        monitor (int): containment (monitor) number
        plugin (str): wallpaper plugin id

    Returns:
        string : wallpaper data (wallpaper path or color)
    """
    try:
        bus = dbus.SessionBus()
        plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
        wallpaper_data = str(plasma.evaluateScript(
            script % (monitor, plugin, plugin))).replace('file://', '')
        return wallpaper_data
    except Exception as e:
        print(f'Error getting wallpaper from dbus:\n{e}')
        return None
    
    
def get_last_modification(file):
    """get time of last modification of passed file

    Args:
        file (str): absolute path of file
    """
    if file is not None:
        if os.path.exists(file):
            return os.stat(file).st_mtime
        else:
            return None
    else:
        return None
    
def get_material_you_colors(wallpaper_data, ncolor, flag):
    """ Get material you colors from wallpaper or hex color using material-color-utility

    Args:
        wallpaper_data (tuple): wallpaper (type and data)
        ncolor (int): Alternative color number flag passed to material-color-utility
        flag (str): image or color flag passed to material-color-utility

    Returns:
        str: string data from material-color-utility
    """
    try:
        materialYouColors = subprocess.check_output("material-color-utility "+flag+" '"+wallpaper_data+"' -n "+str(ncolor),
                                                    shell=True, universal_newlines=True).strip()
        return materialYouColors
    except Exception as e:
        print(f'Error trying to get colors from {wallpaper_data}')
        return None

def get_color_schemes(wallpaper, ncolor=None):

    """ Display best colors, allow to select alternative color,
    and make and apply color schemes for dark and light mode

    Args:
        wallpaper (tuple): wallpaper (type and data)
        light (bool): wether use or not light scheme
        ncolor (int): Alternative color number flag passed to material-color-utility
    """
    if wallpaper != None:
        materialYouColors = None
        wallpaper_type = wallpaper[0]
        wallpaper_data = wallpaper[1]
        if wallpaper_type == "image":
            use_flag = "-i"
            if os.path.exists(wallpaper_data):
                if not os.path.isdir(wallpaper_data):
                    # get colors from material-color-utility
                    materialYouColors = get_material_you_colors(wallpaper_data,ncolor=ncolor,flag=use_flag)
                else:
                    print(f"{wallpaper_data} is a directory, aborting :)")
        
        elif wallpaper_type == "color":
            use_flag = "-c"
            materialYouColors = get_material_you_colors(wallpaper_data,ncolor=ncolor,flag=use_flag)
            
        if materialYouColors != None:
            try:
                # parse colors string to json
                colors_json = json.loads(materialYouColors)

                if wallpaper_type != "color":
                    print(f'{BOLD_TEXT}Best colors:', end=' ')
                    for index, col in colors_json['bestColors'].items():
                        if USER_HAS_COLR:
                            print(
                                f'{BOLD_TEXT}{index}:{color(col,fore=col)}', end=' ')
                        else:
                            print(f'{BOLD_TEXT}{index}:{col}', end=' ')
                    print(f'{BOLD_TEXT}')

                seed = colors_json['seedColor']
                sedColor = list(seed.values())[0]
                seedNo = list(seed.keys())[0]
                if USER_HAS_COLR:
                    print(BOLD_TEXT+"Using seed: "+seedNo +
                        ":"+color(sedColor, fore=sedColor))
                else:
                    print(BOLD_TEXT+"Using seed: " +
                        seedNo+":"+sedColor+RESET_TEXT)

                with open('/tmp/kde-material-you-colors.json', 'w', encoding='utf8') as current_scheme:
                    current_scheme.write(json.dumps(
                        colors_json, indent=4, sort_keys=False))

                # generate and apply Plasma color schemes
                #print(f'Settting color schemes for {wallpaper_data}')
                
                return colors_json
                
            except Exception as e:
                print(f'Error:\n {e}')
                return None

    else:
        print(
            f'''Error: Couldn't set schemes with "{wallpaper_data}"''')
        return None


def set_icons(icons_light, icons_dark, light):
    """ Set icon theme with plasma-changeicons for light and dark schemes

    Args:
        icons_light (str): Light mode icon theme
        icons_dark (str): Dark mode icon theme
        light (bool): wether using light or dark mode
    """
    if light and icons_light != None:
        subprocess.run("/usr/lib/plasma-changeicons "+icons_light,
                       shell=True)
    if not light and icons_dark != None:
        subprocess.run("/usr/lib/plasma-changeicons "+icons_dark,
                       shell=True)


def currentWallpaper(options):
    return get_wallpaper_data(plugin=options['plugin'], monitor=options['monitor'], file=options['file'])

def make_plasma_scheme(schemes=None):
    light_scheme=schemes.get_light_scheme()
    dark_scheme=schemes.get_dark_scheme()
    # plasma-apply-colorscheme doesnt allow to apply the same theme twice to reload
    # since I don't know how to reaload it with code lets make a copy and switch between them
    # sadly color settings will show copies too
    
    with open (THEME_LIGHT_PATH+"2.colors", 'w', encoding='utf8') as light_scheme_file:
            light_scheme_file.write(light_scheme)
    with open (THEME_LIGHT_PATH+".colors", 'w', encoding='utf8') as light_scheme_file:
        light_scheme_file.write(light_scheme)
    with open (THEME_DARK_PATH+"2.colors", 'w', encoding='utf8') as dark_scheme_file:
            dark_scheme_file.write(dark_scheme)
    with open (THEME_DARK_PATH+".colors", 'w', encoding='utf8') as dark_scheme_file:
        dark_scheme_file.write(dark_scheme)
        
def apply_color_schemes(light=None):
    
    if light != None:
        if light == True:
            subprocess.run("plasma-apply-colorscheme "+THEME_LIGHT_PATH+"2.colors",
                                        shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
            subprocess.run("plasma-apply-colorscheme "+THEME_LIGHT_PATH+".colors",
                                        shell=True, stderr=subprocess.PIPE)
        elif light == False:
            subprocess.run("plasma-apply-colorscheme "+THEME_DARK_PATH+"2.colors",
                                        shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
            subprocess.run("plasma-apply-colorscheme "+THEME_DARK_PATH+".colors",
                                        shell=True, stderr=subprocess.PIPE)
    else:
        subprocess.run("plasma-apply-colorscheme "+THEME_DARK_PATH+"2.colors",
                                        shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
        subprocess.run("plasma-apply-colorscheme "+THEME_DARK_PATH+".colors",
                                        shell=True, stderr=subprocess.PIPE)
                
def apply_pywal_schemes(light=None, pywal_light=None, use_pywal=False, schemes=None, konsole_light=None):
    if use_pywal != None and use_pywal == True:
        pywal_colors = None
        if pywal_light != None:
            if pywal_light  == True:
                pywal_colors=schemes.get_wal_light_scheme()
            else:
                pywal_light=False
                pywal_colors=schemes.get_wal_dark_scheme()
        elif light != None:
            if light  == True:
                pywal_colors=schemes.get_wal_light_scheme()
            elif light  == False:
                pywal_colors=schemes.get_wal_dark_scheme()
                
        if pywal_colors != None:
                if USER_HAS_PYWAL:
                    #use material you colors for pywal
                    # Apply the palette to all open terminals.
                    # Second argument is a boolean for VTE terminals.
                    # Set it to true if the terminal you're using is
                    # VTE based. (xfce4-terminal, termite, gnome-terminal.)
                    pywal.sequences.send(pywal_colors, vte_fix=False)
                    
                    # Export all template files.
                    pywal.export.every(pywal_colors)
                    
                    # Reload xrdb, i3 and polybar.
                    pywal.reload.env()
                else:
                    print(f"{BOLD_TEXT}[W] pywal option enabled but module is not installed{RESET_TEXT}")
                # print palette
                print_pywal_palette(pywal_colors)


def kde_globals_light():
    kdeglobals = configparser.ConfigParser()
    if os.path.exists(KDE_GLOBALS):
        try:
            kdeglobals.read(KDE_GLOBALS)
            if 'General' in kdeglobals:
                general = kdeglobals['General']
                if 'ColorScheme' in general:
                    if "MaterialYouDark" in general['ColorScheme']:
                        return False
                    elif "MaterialYouLight" in general['ColorScheme']:
                        return True
            else:
                return None
        except Exception as e:
            print(e)
            return None
    else:
        return None

def run_hook(hook):
    if hook != None:
        subprocess.Popen(hook,shell=True)

def range_check(x,min,max):
    if x != None:
        return np.clip(x,min,max)
    else:
        return 1

def kwin_reload():
    subprocess.Popen("qdbus org.kde.KWin /KWin reconfigure",shell=True, stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)
    
def sierra_breeze_button_colors(schemes,light=None):
    if light == True:
        colors = schemes.get_sierra_breeze_light_colors()
    elif light == False:
        colors = schemes.get_sierra_breeze_dark_colors()
    
    breezerc = configparser.ConfigParser()
    # preserve case
    breezerc.optionxform = str
    if os.path.exists(BREEZE_RC):
        try:
            breezerc.read(BREEZE_RC)
            if 'Windeco' in breezerc:
                breezerc['Windeco']['ButtonCloseActiveColor'] = colors['btn_close_active_color']
                breezerc['Windeco']['ButtonMaximizeActiveColor'] = colors['btn_maximize_active_color']
                breezerc['Windeco']['ButtonMinimizeActiveColor'] = colors['btn_minimize_active_color']
                breezerc['Windeco']['ButtonKeepAboveActiveColor'] = colors['btn_keep_above_active_color']
                breezerc['Windeco']['ButtonKeepBelowActiveColor'] = colors['btn_keep_below_active_color']
                breezerc['Windeco']['ButtonOnAllDesktopsActiveColor'] = colors['btn_on_all_desktops_active_color']
                breezerc['Windeco']['ButtonShadeActiveColor'] = colors['btn_shade_active_color']
                
                # Inactive
                breezerc['Windeco']['ButtonCloseInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonMaximizeInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonMinimizeInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonKeepAboveInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonKeepBelowInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonOnAllDesktopsInactiveColor'] = colors['btn_inactive_color']
                breezerc['Windeco']['ButtonShadeInactiveColor'] = colors['btn_inactive_color']
                reload = True
            else:
                reload = False
            if reload == True:
                print(f"Applying SierraBreeze window button colors")
                with open(BREEZE_RC, 'w') as configfile:
                    breezerc.write(configfile,space_around_delimiters=False)
                kwin_reload()
        except Exception as e:
            print(f"Error writing breeze window button colors: \n {e}")

def tup2str(tup):
    return ','.join(map(str,tup))

def print_pywal_palette(pywal_colors):
    if USER_HAS_COLR:
        i=0
        for index, col in pywal_colors['colors'].items():
            if i % 8 == 0:
                    print()
            print(f'{color("    ",back=hex2rgb(col))}', end='')
            i+=1
        print(f'{BOLD_TEXT}')
    elif USER_HAS_PYWAL:
        print(f"{BOLD_TEXT}[I] Install colr python module to keep prior color palettes")
        # Print color palette with pywal
        pywal.colors.palette() 
    else:
        print(f"{BOLD_TEXT}[I] Install pywal or colr python module to show color schemes")

def konsole_export_scheme(light=None, pywal_light=None, schemes=None):
    if pywal_light != None:
        if pywal_light  == True:
            pywal_colors=schemes.get_wal_light_scheme()
        else:
            pywal_light=False
            pywal_colors=schemes.get_wal_dark_scheme()
    elif light != None:
        if light  == True:
            pywal_colors=schemes.get_wal_light_scheme()
        elif light  == False:
            pywal_colors=schemes.get_wal_dark_scheme()
                        
    config = configparser.ConfigParser()
    config.optionxform = str
    if os.path.exists(KONSOLE_COLOR_SCHEME_PATH):
        config.read(KONSOLE_COLOR_SCHEME_PATH)

    sections = ['Background',
                'BackgroundIntense',
                'BackgroundFaint',
                'Color',
                'Foreground',
                'ForegroundIntense',
                'ForegroundFaint',
                'General']
    exp = []
    for section in sections:
        if section == 'Color':
            for n in range(8):
                exp.append(str(f'Color{n}'))
                exp.append(str(f'Color{n}Intense'))
                exp.append(str(f'Color{n}Faint'))
        else:
            exp.append(section)

    for section in exp:
        if not config.has_section(section):
                    config.add_section(section)
    config['Background']['Color'] = tup2str(hex2rgb(pywal_colors['special']['background']))
    config['BackgroundIntense']['Color'] = tup2str(hex2rgb(pywal_colors['special']['background']))
    config['BackgroundFaint']['Color'] = tup2str(hex2rgb(pywal_colors['special']['background']))
    config['Color0']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color0']))
    config['Color1']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color1']))
    config['Color2']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color2']))
    config['Color3']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color3']))
    config['Color4']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color4']))
    config['Color5']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color5']))
    config['Color6']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color6']))
    config['Color7']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color7']))
    
    config['Color0Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color8']))
    config['Color1Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color9']))
    config['Color2Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color10']))
    config['Color3Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color11']))
    config['Color4Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color12']))
    config['Color5Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color13']))
    config['Color6Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color14']))
    config['Color7Intense']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color15']))
    
    config['Color0Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color8']))
    config['Color1Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color9']))
    config['Color2Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color10']))
    config['Color3Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color11']))
    config['Color4Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color12']))
    config['Color5Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color13']))
    config['Color6Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color14']))
    config['Color7Faint']['Color'] = tup2str(hex2rgb(pywal_colors['colors']['color15']))
    
    config['Foreground']['Color'] = tup2str(hex2rgb(pywal_colors['special']['foreground']))
    config['ForegroundIntense']['Color'] = tup2str(hex2rgb(pywal_colors['special']['foreground']))
    config['ForegroundFaint']['Color'] = tup2str(hex2rgb(pywal_colors['special']['foreground']))
    
    config['General']['Description'] = "MaterialYou"
    
    if not config.has_option('General','Blur'):
        config['General']['Blur'] = "true"
    if not config.has_option('General','Opacity'):
        config['General']['Opacity'] = "0.9"
    
    with open(KONSOLE_COLOR_SCHEME_PATH,'w') as configfile:
        config.write(configfile,space_around_delimiters=False)
        
    config['General']['Description'] = "MaterialYouAlt"
    
    with open(KONSOLE_COLOR_SCHEME_ALT_PATH,'w') as configfile:
        config.write(configfile,space_around_delimiters=False)

def make_konsole_mirror_profile(profile=None):
    if profile != None:
        profile_path = KONSOLE_DIR+profile+".profile"
        if os.path.exists(profile_path):
            print(f"konsole: mirror profile ({profile})")
            subprocess.check_output("cp -f '"+profile_path+"' "+KONSOLE_TEMP_PROFILE, shell=True)
            profile = configparser.ConfigParser()
            # preserve case
            profile.optionxform = str
            if os.path.exists(profile_path):
                try:
                    profile.read(profile_path)
                    if 'Appearance' in profile:
                        if profile['Appearance']['ColorScheme'] != "MaterialYou":
                            profile['Appearance']['ColorScheme'] = "MaterialYou"
                            with open(profile_path, 'w') as configfile:
                                profile.write(configfile,space_around_delimiters=False)
                except Exception as e:
                    print(f"Error applying Konsole profile:\n{e}")
                    
            #Mirror profile
            profile = configparser.ConfigParser()
            profile.optionxform = str
            if os.path.exists(KONSOLE_TEMP_PROFILE):
                try:
                    profile.read(KONSOLE_TEMP_PROFILE)
                    if 'Appearance' in profile:
                            profile['Appearance']['ColorScheme'] = "MaterialYouAlt"
                            profile['General']['Name'] = "TempMyou"
                except Exception as e:
                    print(f"Error applying Konsole profile:\n{e}")
                with open(KONSOLE_TEMP_PROFILE, 'w') as configfile:
                        profile.write(configfile,space_around_delimiters=False)


def konsole_reload_profile(profile=None):
    if profile != None:
        print(f"konsole: reload profile ({profile})")
        konsole_dbus_services=subprocess.check_output("qdbus org.kde.konsole*",shell=True,universal_newlines=True).strip().splitlines()
        if konsole_dbus_services:
            for service in konsole_dbus_services:
                try:
                    konsole_sessions=subprocess.check_output("qdbus "+service+" | grep 'Sessions/'",shell=True,universal_newlines=True).strip().splitlines()
                    for session in konsole_sessions:
                        #print(f"service: {service} -> {session}")
                        current_profile=subprocess.check_output("qdbus "+service+" "+session+" org.kde.konsole.Session.profile",shell=True,universal_newlines=True).strip()
                        #print(current_profile)
                        if current_profile == profile:
                            subprocess.check_output("qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile 'TempMyou'",shell=True)
                        else:
                            subprocess.check_output("qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile 'TempMyou'",shell=True)
                            subprocess.check_output("qdbus "+service+" "+session+" org.kde.konsole.Session.setProfile '"+profile+ "'",shell=True)
                except:
                    pass
                
def konsole_apply_color_scheme(light=None, pywal_light=None, schemes=None, profile=None):
    if profile != None:
        profile_path = KONSOLE_DIR+profile+".profile"
        if os.path.exists(profile_path):
            konsole_export_scheme(light, pywal_light, schemes)
            konsole_reload_profile(profile)
        else:
            print(f"{BOLD_TEXT}Konsole Profile: {profile_path} does not exist{RESET_TEXT}")