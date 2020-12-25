#!/usr/bin/env python3
import os
from termcolor import colored
import time

# https://pypi.org/project/termcolor/
# https://textart.io/art/tag/pirate/1

SHIP_UPPER = 34
MAX_NAME_LEN = 7
COUNTRY_LEN = 3
MAX_NUM_LEN = 3
directions_to_moves = {"north": "n", "south": "s", "east": "e", "west": "w"}
SHIP_COLOR = "cyan"
CANON_COLOR = "cyan"
ALIVE_COLOR = "green"
DEAD_COLOR = "red"
SMOKE_COLOR = "white"
MESSAGE_OFFSET = 76


def convert_num_to_string(num, max_num_len):
    if num == "XXX":
        return num
    cur_num = num
    num_string = ""
    if cur_num < 100:
        num_string += " "
    else:
        num_string += "{}".format(int(cur_num / 100))
        cur_num = cur_num % 100
    if cur_num < 10:
        if num >= 100:
            num_string += "0"
        else:
            num_string += " "
    else:
        num_string += "{}".format(int(cur_num / 10))
        cur_num = cur_num % 10
    num_string += "{}".format(cur_num)
    return num_string


def canon_or_board(index, ship_color=SHIP_COLOR, canon_color=CANON_COLOR):
    if 2 <= index < SHIP_UPPER - 2 and (index % 4 == 0 or index % 4 == 1):
        return colored("|", canon_color)
    return colored("-", ship_color)


class Board:
    def __init__(self, length=126, width=30):
        self.length = length
        self.width = width
        self.ships = {}
        self.render_string = ""
        self.hostile_ship_directions = ["north", "south", "east", "west"]

    def update_health(self, attack=None):
        if attack:
            for ship_direction in self.hostile_ship_directions:
                if getattr(attack, ship_direction):
                    self.ships["center"].hitpoints -= self.ships[
                        ship_direction].attack
            if attack.center is not None:
                if attack.center == "n":
                    self.ships["north"].hitpoints -= self.ships[
                        "center"].attack
                elif attack.center == "s":
                    self.ships["south"].hitpoints -= self.ships[
                        "center"].attack
                elif attack.center == "e":
                    self.ships["east"].hitpoints -= self.ships["center"].attack
                elif attack.center == "w":
                    self.ships["west"].hitpoints -= self.ships["center"].attack

    def update_render_string(self, attack=None):
        self.render_string = "\n\n"

        self.render_string += "".join([" " for i in range(MESSAGE_OFFSET)]) + "Historic battle in sea bursts out,\n"
        self.render_string += "".join([" " for i in range(MESSAGE_OFFSET)]) + "'tis total war, not just a bout.\n"
        self.render_string += "".join([" " for i in range(MESSAGE_OFFSET)]) + "The Lady's cannons will unlease hell,\n"
        self.render_string += "".join([" " for i in range(MESSAGE_OFFSET)]) + "but who survives, ye cannot tell.\n\n\n\n"

        # North ship
        north_letter_color = ALIVE_COLOR
        if "north" not in self.hostile_ship_directions:
            north_letter_color = DEAD_COLOR
        ## Line 0
        self.render_string += "    Boat's hitpoints are HTP," +\
            "".join([" " for i in range(51)]) + \
            "".join([canon_or_board(i) for i in range(SHIP_UPPER)]) + "".join(
            [" " for i in range(58)]) + "N" + "\n"
        ## Line 1
        self.render_string += "    when they're zero, ye cease to be! " + \
            "".join([" " for i in range(39)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", north_letter_color) + \
                              "".join(
            [" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   |", SHIP_COLOR) + "".join(
            [" " for i in range(57)]) + "|" + "\n"
        ## Line 2
        self.render_string += "    Cannon power is shown by ATT," +\
            "".join([" " for i in range(44)]) + colored("=", SHIP_COLOR) + "".join(
            [" " for i in range(13)]) + colored("CAP: ", north_letter_color) + \
                              colored(self.ships["north"].captain, north_letter_color) + "".join(
            [" " for i in range(MAX_NAME_LEN - len(self.ships["north"].captain))]) + \
                              "".join([" " for i in range(4)]) + colored("[[[    =", SHIP_COLOR) + "".join(
            [" " for i in range(53)]) + "W --+-- E" + "\n"
        ## Line 3
        self.render_string += "    when they hit ye, remember that." +\
            "".join([" " for i in range(40)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("HTP: ", north_letter_color) + \
                              colored(convert_num_to_string(self.ships["north"].hitpoints, MAX_NUM_LEN),
                                      north_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| ", SHIP_COLOR) + \
                              colored(self.ships["north"].captain[0], north_letter_color) + colored(" |", SHIP_COLOR) + \
                              "".join([" " for i in range(57)]) + "|" + "\n"
        ## Line 4
        self.render_string += "    RTH counts rounds till hit," +\
            "".join([" " for i in range(45)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("ATT: ", north_letter_color) + \
                              colored(convert_num_to_string(self.ships["north"].attack, MAX_NUM_LEN),
                                      north_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| * |", SHIP_COLOR) + "".join(
            [" " for i in range(57)]) + "S" + "\n"
        ## Line 5
        self.render_string += "    reloading canons takes a bit!" + \
            "".join([" " for i in range(44)]) + colored("=", SHIP_COLOR) + "".join(
            [" " for i in range(13)]) + colored("RTH: ", north_letter_color) + \
                              colored(convert_num_to_string(self.ships["north"].time_to_hit, MAX_NUM_LEN),
                                      north_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(4)]) + colored("[[[    =", SHIP_COLOR) + "\n"
        ## Line 6
        self.render_string += "".join([" " for i in range(78)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", north_letter_color) + \
                              "".join([" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   |", SHIP_COLOR) + "\n"
        ## Line 7
        self.render_string += "".join([" " for i in range(80)]) + "".join(
            [canon_or_board(i) for i in range(SHIP_UPPER)]) + "\n"
        ## Line 8, 9
        if attack and attack.north:
            self.render_string += colored(
                "".join([" " for i in range(84)]) + "/\\" + "  /\\" + "  /\\" +
                "  /\\" + "  /\\" + "  /\\" + "  /\\", SMOKE_COLOR) + "\n\n"
        else:
            self.render_string += "\n\n"
        if attack and attack.center == "n":
            self.render_string += colored(
                "".join([" " for i in range(84)]) + "\\/" + "  \\/" + "  \\/" +
                "  \\/" + "  \\/" + "  \\/" + "  \\/", SMOKE_COLOR) + "\n"
        else:
            self.render_string += "\n"

        # West, center and east ship
        east_letter_color = ALIVE_COLOR
        if "east" not in self.hostile_ship_directions:
            east_letter_color = DEAD_COLOR
        west_letter_color = ALIVE_COLOR
        if "west" not in self.hostile_ship_directions:
            west_letter_color = DEAD_COLOR
        center_letter_color = ALIVE_COLOR
        if self.ships["center"].hitpoints == "XXX":
            center_letter_color = DEAD_COLOR
        ## Line 10
        self.render_string += "".join([" " for i in range(4)]) + \
            "".join([canon_or_board(i) for i in range(SHIP_UPPER)])
        self.render_string += "".join([" " for i in range(42)]) + "".join(
            [canon_or_board(i) for i in range(SHIP_UPPER)])
        self.render_string += "".join([" " for i in range(42)]) + \
            "".join([canon_or_board(i) for i in range(SHIP_UPPER)]) + " \n"
        ## Line 11
        self.render_string += "".join([" " for i in range(2)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", west_letter_color) + "".join(
            [" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   |", SHIP_COLOR) + \
                              "".join([" " for i in range(39)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", center_letter_color) + \
                              "".join(
            [" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   |", SHIP_COLOR) + \
                              "".join([" " for i in range(39)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", east_letter_color) + \
                              "".join(
            [" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   |", SHIP_COLOR) + "\n"
        ## Line 12
        west_east = " "
        if attack and attack.west:
            west_east = "<"
        east_west = " "
        if attack and attack.east:
            east_west = ">"
        center_west = " "
        if attack and attack.center == "w":
            center_west = ">"
        center_east = " "
        if attack and attack.center == "e":
            center_east = "<"
        self.render_string += "".join([" " for i in range(1)]) + colored("=", SHIP_COLOR) + "".join(
            [" " for i in range(13)]) + colored("CAP: ", west_letter_color) + \
                              colored(self.ships["west"].captain, west_letter_color) + "".join(
            [" " for i in range(MAX_NAME_LEN - len(self.ships["west"].captain) + 1)]) + \
                              "".join([" " for i in range(6)]) + colored("|   ", SHIP_COLOR) + colored("=", CANON_COLOR) + colored(west_east,
                                                                                                      SMOKE_COLOR) + \
                              "".join([" " for i in range(36)]) + colored(center_west, SMOKE_COLOR) + colored("=",
                                                                                                             CANON_COLOR) + "".join(
            [" " for i in range(13)]) + colored("CAP: ", center_letter_color) + \
                              colored(self.ships["center"].captain, center_letter_color) + "".join(
            [" " for i in range(MAX_NAME_LEN - len(self.ships["center"].captain) + 1)]) + \
                              "".join([" " for i in range(3)]) + colored("[[[    ", SHIP_COLOR) + colored("=", CANON_COLOR) + colored(center_east,
                                                                                                      SMOKE_COLOR) + \
                              "".join([" " for i in range(36)]) + colored(east_west, SMOKE_COLOR) + colored("=",
                                                                                                           CANON_COLOR) + "".join(
            [" " for i in range(13)]) + colored("CAP: ", east_letter_color) + \
                              colored(self.ships["east"].captain, east_letter_color) + "".join(
            [" " for i in range(MAX_NAME_LEN - len(self.ships["east"].captain))]) + \
                              "".join([" " for i in range(7)]) + colored("|   =", SHIP_COLOR) + "\n"
        ## Line 13
        self.render_string += colored("/", SHIP_COLOR) + "".join([" " for i in range(14)]) + colored("HTP: ",
                                                                                                     west_letter_color) + \
                              colored(convert_num_to_string(self.ships["west"].hitpoints, MAX_NUM_LEN),
                                      west_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(4)]) + colored("[[[  ", SHIP_COLOR) + \
                              colored(self.ships["west"].captain[0], west_letter_color) + colored(" |", SHIP_COLOR) + \
                              "".join([" " for i in range(37)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("HTP: ", center_letter_color) + \
                              colored(convert_num_to_string(self.ships["center"].hitpoints, MAX_NUM_LEN),
                                      center_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| ", SHIP_COLOR) + \
                              colored(self.ships["center"].captain[0], center_letter_color) + colored(" |", SHIP_COLOR) + \
                              "".join([" " for i in range(37)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("HTP: ", east_letter_color) + \
                              colored(convert_num_to_string(self.ships["east"].hitpoints, MAX_NUM_LEN),
                                      east_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| ", SHIP_COLOR) +\
                              colored(self.ships["east"].captain[0], east_letter_color) + colored(" |", SHIP_COLOR) + "\n"
        ## Line 14
        self.render_string += colored("\\", SHIP_COLOR) + "".join([" " for i in range(14)]) + colored("ATT: ",
                                                                                                      west_letter_color) + \
                              colored(convert_num_to_string(self.ships["west"].attack, MAX_NUM_LEN),
                                      west_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| * |", SHIP_COLOR) + \
                              "".join([" " for i in range(37)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("ATT: ", center_letter_color) + \
                              colored(convert_num_to_string(self.ships["center"].attack, MAX_NUM_LEN),
                                      center_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| * |", SHIP_COLOR) + \
                              "".join([" " for i in range(37)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("ATT: ", east_letter_color) + \
                              colored(convert_num_to_string(self.ships["east"].attack, MAX_NUM_LEN),
                                      east_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| * |", SHIP_COLOR) + "\n"
        ## Line 15
        self.render_string += "".join([" " for i in range(1)]) + colored("=", SHIP_COLOR) + "".join(
            [" " for i in range(13)]) + colored("RTH: ", west_letter_color) + \
                              colored(convert_num_to_string(self.ships["west"].time_to_hit, MAX_NUM_LEN),
                                      west_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   ", SHIP_COLOR) + colored("=", CANON_COLOR) + colored(west_east,
                                                                                                      SMOKE_COLOR) + \
                              "".join([" " for i in range(36)]) + colored(center_west, SMOKE_COLOR) + colored("=",
                                                                                                             CANON_COLOR) + "".join(
            [" " for i in range(13)]) + colored("RTH: ", center_letter_color) + \
                              colored(convert_num_to_string(self.ships["center"].time_to_hit, MAX_NUM_LEN),
                                      center_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(4)]) + colored("[[[    ", SHIP_COLOR) + colored("=", CANON_COLOR) + colored(center_east,
                                                                                                      SMOKE_COLOR) + \
                              "".join([" " for i in range(36)]) + colored(east_west, SMOKE_COLOR) + colored("=",
                                                                                                           CANON_COLOR) + "".join(
            [" " for i in range(13)]) + colored("RTH: ", east_letter_color) + \
                              colored(convert_num_to_string(self.ships["east"].time_to_hit, MAX_NUM_LEN),
                                      east_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(4)]) + colored("[[[    ", SHIP_COLOR) + colored("=", SHIP_COLOR) + "\n"
        ## Line 16
        self.render_string += "".join([" " for i in range(2)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + \
                              "".join([" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(12)]) + colored("|   |", SHIP_COLOR) + \
                              "".join([" " for i in range(39)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", center_letter_color) + \
                              "".join([" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   ", SHIP_COLOR) + colored("|", SHIP_COLOR) + \
                              "".join([" " for i in range(39)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", east_letter_color) + \
                              "".join([" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   |", SHIP_COLOR) + "\n"
        ## Line 17
        self.render_string += "".join([" " for i in range(4)]) + \
            "".join([canon_or_board(i) for i in range(SHIP_UPPER)])
        self.render_string += "".join([" " for i in range(42)]) + "".join(
            [canon_or_board(i) for i in range(SHIP_UPPER)])
        self.render_string += "".join([" " for i in range(42)]) + \
            "".join([canon_or_board(i) for i in range(SHIP_UPPER)]) + " \n"
        ## Line 18, 19
        if attack and attack.center == "s":
            self.render_string += colored(
                "".join([" " for i in range(84)]) + "/\\" + "  /\\" + "  /\\" +
                "  /\\" + "  /\\" + "  /\\" + "  /\\", SMOKE_COLOR) + "\n\n"
        else:
            self.render_string += "\n\n"
        if attack and attack.south:
            self.render_string += colored(
                "".join([" " for i in range(84)]) + "\\/" + "  \\/" + "  \\/" +
                "  \\/" + "  \\/" + "  \\/" + "  \\/", SMOKE_COLOR) + "\n"
        else:
            self.render_string += "\n"

        # South ship
        south_letter_color = ALIVE_COLOR
        if "south" not in self.hostile_ship_directions:
            south_letter_color = DEAD_COLOR
        ## Line 20
        self.render_string += "".join([" " for i in range(80)]) + "".join(
            [canon_or_board(i) for i in range(SHIP_UPPER)]) + "\n"
        ## Line 21
        self.render_string += "".join([" " for i in range(78)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", south_letter_color) + \
                            "".join(
            [" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   ", SHIP_COLOR)+ colored("|", SHIP_COLOR) + "\n"
        ## Line 22
        self.render_string += "".join([" " for i in range(77)]) + colored("=", SHIP_COLOR) + "".join(
            [" " for i in range(13)]) + colored("CAP: ", south_letter_color) + \
                              colored(self.ships["south"].captain, south_letter_color) + "".join(
            [" " for i in range(MAX_NAME_LEN - len(self.ships["south"].captain))]) + \
                              "".join([" " for i in range(4)]) + colored("[[[    ", SHIP_COLOR) + colored("=", SHIP_COLOR) + "\n"
        ## Line 23
        self.render_string += "".join([" " for i in range(76)]) + colored("/", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("HTP: ", south_letter_color) + \
                              colored(convert_num_to_string(self.ships["south"].hitpoints, MAX_NUM_LEN),
                                      south_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| ", SHIP_COLOR) + \
                              colored(self.ships["south"].captain[0], south_letter_color) + colored(" |", SHIP_COLOR) + "\n"
        ## Line 24
        self.render_string += "".join([" " for i in range(76)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(14)]) + colored("ATT: ", south_letter_color) + \
                              colored(convert_num_to_string(self.ships["south"].attack, MAX_NUM_LEN),
                                      south_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("| * |", SHIP_COLOR) + "\n"
        ## Line 25
        self.render_string += "".join([" " for i in range(77)]) + colored("=", SHIP_COLOR) + "".join(
            [" " for i in range(13)]) + colored("RTH: ", south_letter_color) + \
                              colored(convert_num_to_string(self.ships["south"].time_to_hit, MAX_NUM_LEN),
                                      south_letter_color) + "".join([" " for i in range(MAX_NAME_LEN - MAX_NUM_LEN)]) + \
                              "".join([" " for i in range(4)]) + colored("[[[    =", SHIP_COLOR) + "\n"
        ## Line 26
        self.render_string += "".join([" " for i in range(78)]) + colored("\\", SHIP_COLOR) + "".join(
            [" " for i in range(12)]) + colored("     ", south_letter_color) + \
                              "".join([" " for i in range(MAX_NAME_LEN)]) + \
                              "".join([" " for i in range(7)]) + colored("|   |", SHIP_COLOR) + "\n"
        ## Line 27
        self.render_string += "".join([" " for i in range(80)]) + \
            "".join([canon_or_board(i) for i in range(SHIP_UPPER)]) + "\n\n\n"


class Ship:
    def __init__(self, country, captain, people, hitpoints, attack,
                 time_to_hit, cooldown_period):
        self.country = country
        self.captain = captain
        self.people = people
        self.hitpoints = hitpoints
        self.attack = attack
        self.time_to_hit = time_to_hit
        self.cooldown_period = cooldown_period


class Attack:
    def __init__(self,
                 center=None,
                 north=False,
                 south=False,
                 west=False,
                 east=False):
        self.center = center
        self.north = north
        self.south = south
        self.east = east
        self.west = west


def win_string():
    return """


                                                                                 ___
                                                                                 \_/
                                                                                  |._
                                                                                  |'."-._.-""--.-"-.__.-'/
                                                                                  |  \\       .-.        (
                                                                                  |   |     (@.@)        )
                                                                                  |   |   '=.|m|.='     /
                                                                                  |  /    .='`"``=.    /
                                                                                  |.'                 (
                                                                                  |.-"-.__.-""-.__.-"-.)
                                                                                  |
                                                                                  |
                                                                                  |
                            
                                                                                        ______
                                                                                   _.-':::::::`.
                                                                                   \\::::::::::::`.-._
                                                                                    \\:::''   `::::`-.`.
                                                                                     \\         `:::::`.\\
                                                                                      \\          `-::::`:
                                                                                       \\______       `:::`.
                                                                                       .|_.-'__`._     `:::\\
                                                                                      ,'`|:::|  )/`.     \\:::
                                                                                     /. -.`--'  : /.\\     ::|
                                                                                     `-,-'  _,'/| \\|\\\\    |:|
                                                                                      ,'`::.    |/>`;'\\   |:|
                                                                                      (_\\ \\:.:.:`((_));`. ;:|
                                                                                      \\.:\\ ::_:_:_`-','  `-:|
                                                                                       `:\\\\|        :
                                                                                          )`__...---'
            

    """


def die_string():
    return """
            
            
                                                                                        _.--'''''''-.
                                                                                      .-'            '.
                                                                                    .'                 '.
                                                                                   /            .        )
                                                                                  |                   _  (
                                                                                  |          .       / \\  \\
                                                                                  \         .     .  \\_/  |
                                                                                   \    .--' .  '         /
                                                                                    \  /  .'____ _       /,
                                                                                     '/   (\    `)\\       |
                                                                                     ||\__||    |;-.-.-,-,|
                                                                                     \\\\___//|   \\--'-'-'-'|
                                                                                      '---' \\             |
                                                                               .--.          '---------.__)   .-.
                                                                              .'   \                         /  '.
                                                                             (      '.                    _.'     )
                                                                              '---.   '.              _.-'    .--'
                                                                                   `.   `-._      _.-'   _.-'`
                                                                                     `-._   '-.,-'   _.-'
                                                                                         `-._   `'.-'
                                                                                       _.-'` `;.   '-._
                                                                                .--.-'`  _.-'`  `'-._  `'-.--.
                                                                               (       .'            '.       )
                                                                                `,  _.'                '._  ,'
            

    """


def initialize_board():
    # initialize board
    board = Board()

    # initialize ships
    board.ships["south"] = Ship(
        country="GB",
        captain="Sean",
        people=60,
        hitpoints=100,
        attack=20,
        time_to_hit=5,
        cooldown_period=5)
    board.ships["north"] = Ship(
        country="GB",
        captain="Nelson",
        people=60,
        hitpoints=100,
        attack=20,
        time_to_hit=4,
        cooldown_period=4)
    board.ships["east"] = Ship(
        country="GB",
        captain="Ethan",
        people=60,
        hitpoints=50,
        attack=10,
        time_to_hit=3,
        cooldown_period=3)
    board.ships["west"] = Ship(
        country="GB",
        captain="William",
        people=60,
        hitpoints=50,
        attack=10,
        time_to_hit=2,
        cooldown_period=2)
    board.ships["center"] = Ship(
        country="??",
        captain="Sparrow",
        people=60,
        hitpoints=200,
        attack=30,
        time_to_hit=2,
        cooldown_period=2)

    return board


def main():
    # initialize board
    os.system("clear")
    board = initialize_board()
    board.update_render_string()
    print(board.render_string)

    first_strike = True
    while True:
        attack = Attack()

        # if first strike, all hostiles hit
        if first_strike:
            for ship_direction in board.hostile_ship_directions:
                setattr(attack, ship_direction, True)
        # otherwise, we update all times to hit
        else:
            for ship_direction in board.hostile_ship_directions + ["center"]:
                board.ships[ship_direction].time_to_hit -= 1
        # check if time to hit expired for hostiles
        for ship_direction in board.hostile_ship_directions:
            if board.ships[ship_direction].time_to_hit == 0:
                setattr(attack, ship_direction, True)
                board.ships[ship_direction].time_to_hit = board.ships[
                    ship_direction].cooldown_period

        # check if time to hit expired for player
        if first_strike or board.ships["center"].time_to_hit == 0:
            board.ships["center"].time_to_hit = board.ships[
                "center"].cooldown_period
            valid_moves = list(
                map(lambda x: directions_to_moves[x],
                    board.hostile_ship_directions))
            if first_strike:
                print("".join([" " for i in range(MESSAGE_OFFSET)]) + "Alas! The entire armada starts firing!")
            my_move = input("".join([" " for i in range(MESSAGE_OFFSET)]) + "Who are we hitting, Captain? {} ".format(valid_moves))
            while my_move not in valid_moves:
                print("".join([" " for i in range(MESSAGE_OFFSET)]) + "Look at our enemies Captain! {}".format(valid_moves))
                my_move = input("".join([" " for i in range(MESSAGE_OFFSET)]) + "Who are we hitting, Captain? {} ".format(valid_moves))
            setattr(attack, "center", my_move)
        else:
            input(
                "".join([" " for i in range(MESSAGE_OFFSET)]) + "Cannons are hot Captain! Any moment now..."
            )

        # cancel first strike for the following
        if first_strike:
            first_strike = False

        # determine if any attack happened during this round
        at_least_one_attack = False
        for ship_direction in board.hostile_ship_directions:
            at_least_one_attack = at_least_one_attack or getattr(
                attack, ship_direction)
        if attack.center is not None:
            at_least_one_attack = True

        # render attack moves
        if at_least_one_attack:
            for i in range(3):
                if i % 2 == 0:
                    board.update_render_string(attack)
                else:
                    board.update_render_string()
                os.system("clear")
                print(board.render_string)
                time.sleep(1)

            # now perform health updates
            board.update_health(attack)
            dead_ship_directions = set()
            for ship_direction in board.hostile_ship_directions:
                if board.ships[ship_direction].hitpoints <= 0:
                    board.ships[ship_direction].people = "XXX"
                    board.ships[ship_direction].hitpoints = "XXX"
                    board.ships[ship_direction].attack = "XXX"
                    board.ships[ship_direction].time_to_hit = "XXX"
                    dead_ship_directions.add(ship_direction)
            for ship_direction in dead_ship_directions:
                board.hostile_ship_directions.remove(ship_direction)
            if board.ships["center"].hitpoints <= 0:
                board.ships["center"].people = "XXX"
                board.ships["center"].hitpoints = "XXX"
                board.ships["center"].attack = "XXX"
                board.ships["center"].time_to_hit = "XXX"

        # render new state
        board.update_render_string()
        os.system("clear")
        print(board.render_string)
        time.sleep(1)

        if board.ships["center"].hitpoints == "XXX":
            print(die_string())
            print("".join([" " for i in range(MESSAGE_OFFSET)]) + "Alas! Abandon ship! 'Tis an honor to die by yer side!")
            input("")
            board = initialize_board()
            first_strike = True
            board.update_render_string()
            os.system("clear")
            print(board.render_string)
        elif len(board.hostile_ship_directions) == 0:
            print(win_string())
            print("".join([" " for i in range(MESSAGE_OFFSET)]) + "Captain, we are free to roam the seven seas once more!")
            input("")
            board = initialize_board()
            first_strike = True
            board.update_render_string()
            os.system("clear")
            print(board.render_string)


if __name__ == '__main__':
    main()
