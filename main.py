from controllers.app_controller import AppController


def main():
    controller = AppController()
    controller.setup_main_menu()  # Setup main menu
    controller.main_menu.display()


if __name__ == "__main__":
    main()
