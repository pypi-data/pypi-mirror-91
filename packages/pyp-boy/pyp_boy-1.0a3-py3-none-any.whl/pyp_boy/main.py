def run_gui():
    from pyp_boy.gui import PypBoyGUI

    pbg = PypBoyGUI()
    main_win = pbg.MainWindow('Test Window')
    main_win.run_window()


if __name__ == 'pyp_boy.main' or __name__ == "__main__":
    run_gui()

else:
    print("PypBoy imported! Please bear in mind that this package was made to be used as a whole application.\n"
          "Importing this API is not recommended by the developer and therefore she can't promise that support will be "
          "available for problems with importing the API!! ")
    print(__name__)
