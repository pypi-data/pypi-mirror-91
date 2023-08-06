import os

__all__ = ["pause", "clearscreen"]


#########################
# Misc. helpers
#########################

def pause():
    """ Does 'Press any key to continue' """
    if os.name == "nt":
        print()
        os.system("pause")
    else:
        input("\nPress Enter to continue . . . ")

def clearscreen():
    """ Clear the terminal/command prompt """
    os.system("cls" if os.name=="nt" else "clear")