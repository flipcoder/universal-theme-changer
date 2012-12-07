#!/usr/bin/python2
import sh,os,sys

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

    # TODO: look up current theme
    current_theme = ""

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

    print menu("Compatible Themes", "Select a theme: ", themes.keys(), index=False, current=current_theme)

    return 0

if __name__=="__main__":
    sys.exit(main())
