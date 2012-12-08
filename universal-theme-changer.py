#!/usr/bin/python2
import sh,os,sys,fileinput,ConfigParser

def menu_print(msg):
    print msg

def menu(title, msg, options, back=False, back_text="Back", index=True, current="", current_append=" (current)", print_func=menu_print, input_func=raw_input):
    """
    Builds text menu with title, message, and options
    'back' refers to if the menu should allow Back option
    'index' to whether or not value returned should be only index (otherwise it'll return actual option or 'None'
    'current' is an optional highlighted option
    'current_append' is the message to be appended to the highlighted option
    """

    while True:
        choice = 0
        i = 1
        print_func("%s" % title)
        for m in options:
            append = ""
            if current==m:
                append = current_append
            print_func("%s. %s%s" % (i,m,append))
            i += 1
        if back:
            print_func("%s. [ %s ]" % (i, back_text))
        try:
            choice = int(input_func(msg))
        except TypeError:
            continue # loop again
        except ValueError:
            continue
        if choice > 0 and choice <= len(options):
            break
        elif choice == len(options)+1:
            if back:
                return -1 if index else None 
            else:
                continue
    if not index:
        if choice != -1:
            return options[choice-1]
        else:
            return None
    return choice-1


def main():
    themes = {}
    icons = {}

    # TODO: look up current theme and icons
    current_theme = ""
    current_icons = ""

    for theme_path in ('/usr/share/themes', os.path.join(os.path.expanduser('~'),'.themes')):
        try:
            for path in sh.ls('-1', theme_path):
                path = path[:-1] # take off trailing space
                full = os.path.join(theme_path, path)
                gtk2_path = os.path.join(full, 'gtk-2.0')
                gtk3_path = os.path.join(full, 'gtk-3.0')
                if(os.path.isdir(gtk2_path) and os.path.isdir(gtk3_path)):
                    themes[path] = full
        except sh.ErrorReturnCode_2: # path not found
            pass
    theme_selection = menu("Compatible Themes", "Select a theme: ", themes.keys(), index=False, current=current_theme)

    print

    for icon_path in ('/usr/share/icons', os.path.join(os.path.expanduser('~'),'.icons')):
        try:
            for path in sh.ls('-1', icon_path):
                path = path[:-1] # take off trailing space
                full = os.path.join(icon_path, path)
                if(os.path.isdir(full)):
                    icons[path] = full
        except sh.ErrorReturnCode_2: # path not found
            pass

    icon_selection = menu("Compatible Icons", "Select icon set: ", icons.keys(), index=False, current=current_icons)

    print

    if theme_selection or icon_selection:

        # set gtk2
        once = False
        for line in fileinput.input(os.path.join(os.path.expanduser('~'), '.gtkrc-2.0'), inplace=1):
            if not once:
                if theme_selection:
                    print "gtk-theme-name=\"%s\"" % theme_selection
                if icon_selection:
                    print "gtk-icon-theme-name=\"%s\"" % icon_selection
                once = True
            if not line.startswith("gtk-theme-name=") and not line.startswith("gtk-icon-theme-name"):
                print line[:-1]

        # set gtk3
        c = ConfigParser.ConfigParser()
        f = os.path.join(os.environ.get('XDG_CONFIG_HOME'), 'gtk-3.0/settings.ini')
        c.read(f)
        if not c.has_section("Settings"):
            c.add_section("Settings")
        if theme_selection:
            c.set("Settings", "gtk-theme-name", theme_selection)
        if icon_selection:
            c.set("Settings", "gtk-icon-theme-name", icon_selection)
        c.write(open(f,'w'))

        # set Qt to use GTK theme
        c = ConfigParser.ConfigParser()
        f = os.path.join(os.environ.get('XDG_CONFIG_HOME'), 'Trolltech.conf')
        c.read(f)
        if not c.has_section("Qt"):
            c.add_section("Qt")
        c.set("Qt", "style", "GTK+")
        c.write(open(f,'w'))

        # probably won't need these, but here they are anyway:
        if theme_selection:
            os.system("gconftool-2 --type string --set /desktop/gnome/interface/gtk_theme \"%s\"" % theme_selection)
        if icon_selection:
            os.system("gconftool-2 --type string --set /desktop/gnome/interface/icon_theme \"%s\"" % icon_selection)

    return 0

if __name__=="__main__":
    sys.exit(main())

