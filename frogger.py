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
    if char not in ".lph":
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
            (-3.0,",,,llll,,llllll,,,,,,,llll,,,,,ll,,,lllll,,,,llllll,,,,lllll,,,,"),
            (3.0, ",,,,llll,,,,,llll,,,,llll,,,,,,,,,llll,,,,,ll,,,,,,llllll,,,,,,,"),
            (2.0, ",,lll,,,,,lll,,,,,ll,,,,,lll,,,lll,,,,ll,,,,llll,,,,ll,,,,,,ll,,"),
            (0.0, "pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp"),
            (-3.0,"....bbbb.......bbbb....bbbb..........bbbb........bbbb....bbbb..."),
            (3.0, ".....yy..yy....yy....yy.....yy........yy..yy.yy......yy.......yy"),
            (-4.0,"..xx.....xx.........xx..xx........xx...xx...xx....xx...xx...xx.."),
            (2.0, "..yy.....yy.......yy.....yy......yy..yy.yy.......yy....yy......."),
            (0.0, "pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
            ]

        objs = {
            # Bus
            "b": (64, 16, 0),
            # Log
            "l": (64, 32, 8),
            # Car 1
            "x": (64, 64, 0),
            # Car 2
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
                # The game is using fractions to control the speed of moving objects.
                # This can cause problems for the sideways movement of the frog
                # as it is not quite in sync (fractionally speaking). The worst
                # case is that the frog may die after seemingly landing on the end of
                # the log (because the log moves slightly ahead of the frog).
                # The solution here is to give the frog the same fractional value as
                # the log row it has landed on:
                log_pos = get_log_pos(timer, lanes[int(frog_y)][0])
                log_denom, _ = math.modf(log_pos)
                _, frog_numer = math.modf(frog_x)
                frog_x = frog_numer + log_denom
                # Now factor in log movement - as we're about to move these
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
