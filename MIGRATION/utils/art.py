import pyfiglet

def textArt(text):
    text = "Migration tool"
    ascii_art = pyfiglet.figlet_format(text, font="standard")
    print(ascii_art)
