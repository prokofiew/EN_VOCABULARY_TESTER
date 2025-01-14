from controllers.app_controller import App_Controller


def main():
    controller = App_Controller()
    controller.setup_main_menu()  # Setup main menu
    controller.main_menu.display()


if __name__ == "__main__":
    main()
