#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This demonstrates a simple version of Frogger using the Unicorn Hat HD for
the Raspberry Pi.
It is based on a Windows console version written by the One Lone Coder see:
https://github.com/OneLoneCoder/videos/blob/master/OneLoneCoder_Frogger.cpp
"""
import time
import curses
import unicornhathd
import math

danger_buffer = [False] * 16 * 16

def draw_pixel(x, y, col):
    """ Write pixel to the Unicorn Hat HD"""
    unicornhathd.set_pixel(x, 12 - y, col[0], col[1], col[2])

def set_danger(x, y, char):
    """
    Set the x,y location of the map as dangerous or not based on the
    character passed in.
    """
    danger = False
    if char not in ".jklph":
        danger = True
    danger_buffer[y * 16 + x] = danger

def get_danger(x, y):
    """ Is the x,y location dangerous for the frog? """
    return danger_buffer[y * 16 + x]

def init():
    """ Initialize the Unicorn Hat HD and keyboard"""
    unicornhathd.rotation(270)
    unicornhathd.brightness(1.0)

    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.nodelay(1)
    stdscr.keypad(1)

    return stdscr

def term():
    """ Clean up resource used by the program before exiting"""
    curses.endwin()
    unicornhathd.off()

def get_log_pos(timer, lane_speed):
    """ Helper function to calculate the floating point log position"""
    log_pos = timer * lane_speed
    if log_pos < 0:
        log_pos = 64 - (abs(log_pos) % 64)
    return log_pos

def main():
    """ Main entry point for the game"""
    try:
        stdscr = init()

        lanes = [
            (0.0, "wwhhwwwhhwwwhhwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"),
            (-3.0,",,,jllk,,jllllk,,,,,,,jllk,,,,,jk,,,jlllk,,,,jllllk,,,,jlllk,,,,"),
            (3.0, ",,,,jllk,,,,,jllk,,,,jllk,,,,,,,,,jllk,,,,,jk,,,,,,jllllk,,,,,,,"),
            (2.0, ",,jlk,,,,,jlk,,,,,jk,,,,,jlk,,,jlk,,,,jk,,,,jllk,,,,jk,,,,,,jk,,"),
            (0.0, "pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp"),
            (-3.0,"....asdf.......asdf....asdf..........asdf........asdf....asdf..."),
            (3.0, ".....ty..ty....ty....ty.....ty........ty..ty.ty......ty.......ty"),
            (-4.0,"..zx.....zx.........zx..zx........zx...zx...zx....zx...zx...zx.."),
            (2.0, "..ty.....ty.......ty.....ty......ty..ty.ty.......ty....ty......."),
            (0.0, "pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
            ]

        objs = {
            # Bus
            "a": (64, 16, 0),
            "s": (64, 16, 0),
            "d": (64, 16, 0),
            "f": (64, 16, 0),
            # Log
            "j": (64, 32, 8),
            "l": (64, 32, 8),
            "k": (64, 32, 8),
            # Car 1
            "z": (64, 64, 0),
            "x": (64, 64, 0),
            # Car 2
            "t": (0, 0, 64),
            "y": (0, 0, 64),
            # Wall
            "w": (64, 0, 0),
            # Home
            "h": (0, 32, 0),
            # Water
            ",": (16, 32, 64),
            # Pavement
            "p": (16, 16, 16),
            # Road
            ".": (0, 0, 0)
            }

        frog_x, frog_y = 8.0, 9.0

        timer = 0.0
        key = ''
        while key != ord('q'):
            # Is frog in danger?
            if get_danger(int(frog_x), int(frog_y)):
                frog_x, frog_y = 8.0, 9.0

            key = stdscr.getch()
            if key == curses.KEY_UP and frog_y > 0.0:
                frog_y -= 1.0
            elif key == curses.KEY_DOWN and frog_y < 9.0:
                frog_y += 1.0
            elif key == curses.KEY_LEFT:
                frog_x -= 1.0
            elif key == curses.KEY_RIGHT:
                frog_x += 1.0

            if frog_x < 0.0:
                frog_x = 0.0
            if frog_x > 15:
                frog_x = 15.0

            # Deal with movement of logs
            if frog_y <= 3.0:
                # Because the game is working purely in an integer display but
                # using fractions to control the speed of moving objects, we
                # have to sync the frog with the log its landing on. Otherwise,
                # the frog might die due to the log moving slightly ahead of the frog.
                # This could be considered a feature but I'd prefer it to be turned off
                log_pos = get_log_pos(timer, lanes[int(frog_y)][0])
                log_denom, _ = math.modf(log_pos)
                _, frog_numer = math.modf(frog_x)
                frog_x = frog_numer + log_denom
                # Now factor in log movement - as we're abount to move these
                frog_x -= 0.01 * lanes[int(frog_y)][0]

            for y, lane in enumerate(lanes):
                start_pos = int(get_log_pos(timer, lane[0]))
                for i in range(16):
                    obj = lane[1][(start_pos + i) % 64]
                    draw_pixel(i, y, objs[obj])
                    set_danger(i, y, obj)

            # Draw frog
            draw_pixel(int(frog_x), int(frog_y), (64, 128, 64))

            unicornhathd.show()
            time.sleep(0.01)
            timer += 0.01
    finally:
        term()

if __name__ == "__main__":
    main()
