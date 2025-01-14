class MenuOption:
    def __init__(self, label, action=None, submenu=None):
        self.label = label
        self.action = action
        self.submenu = submenu

    def execute(self, *args):
        if self.action:
            if args:
                self.action(*args)
            else:
                self.action()
        elif self.submenu:
            self.submenu.display()
