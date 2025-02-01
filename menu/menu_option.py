"""
class represents a single option within a menu
"""


class MenuOption:
    def __init__(self, label, action=None, submenu=None):
        self.label = label
        self.action = action
        self.submenu = submenu

    def execute(self, *args):
        """ method is called when the user
        selects menu option or displaying submenu.
        *args for multiple choices in category menu"""
        if self.action:
            if args:
                self.action(*args)
            else:
                self.action()
        elif self.submenu:
            self.submenu.display()
