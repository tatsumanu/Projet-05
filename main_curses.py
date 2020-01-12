# -*-coding:'utf8'-*-

import curses
from constants import header, end
from database_class import Database
from menu_class import Menu
from math import ceil


def draw_menu(stdscr):
    k = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    """ Loop where k is the last character pressed. Run the program
    until 'q' is pressed """
    while (k != 'q'):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Refresh the screen
        stdscr.refresh()

        # Some variables
        title = header[:width-1]
        subtitle = menu.text
        keystr = "Votre choix: {}".format(k)[:width-1]
        statusbarstr = end
        if k == 0:
            keystr = "En attente de votre choix..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_keystr = int(
            (width // 2) - (len(keystr) // 2) - len(keystr) % 2
            )
        start_y = int((height // 2) - 2)

        # Printing comments
        whstr = menu.comments
        stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(
            height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1)
            )
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(3, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(5, (width // 2) - 2, '-' * 4)

        if menu.step == 4:

            # case of the substituted product
            columns = width-8
            rows = int(ceil(len(subtitle)/columns))
            box = curses.newwin(rows + 2, columns + 2, 7, 1)
            box.box()
            for row in range(1, rows+1):
                box.addstr(
                    row, 1,
                    subtitle[(row*columns)-columns:row*columns]
                    )
                box.refresh()

        else:
            # other cases
            for idx, row in enumerate(subtitle):
                start_y = height//2 - len(subtitle)//2 + idx
                start_x_subtitle = int(
                    (width // 2) - (len(row) // 2) - len(row) % 2
                    )
                stdscr.addstr(start_y - 1, start_x_subtitle, row[:width-1])

        stdscr.addstr(start_y + 5, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 7, start_x_keystr, keystr)

        # Wait for next input
        k = stdscr.getch()
        k = chr(k)
        menu.choice = k
        menu.app_menu()

    # closes mysql connexion
    db.close_cnx()


def main():
    curses.wrapper(draw_menu)


if __name__ == "__main__":

    # creating Menu object before launching app
    db = Database()
    menu = Menu(db)
    main()
