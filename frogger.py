#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import curses
import unicornhathd
import math

danger_buffer = [False] * 16 * 16

def draw_pixel(x, y, col):
    unicornhathd.set_pixel(x, 12 - y, *col)

def set_danger(x, y, char):
    danger = False
    if char not in ".jklph":
        danger = True
    danger_buffer[y * 16 + x] = danger

def get_danger(x, y):
    return danger_buffer[y * 16 + x]

def init():
    unicornhathd.rotation(270)
    unicornhathd.brightness(1.0)

    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.nodelay(1)
    stdscr.keypad(1)

    return stdscr

def term():
    curses.endwin()
    unicornhathd.off()

def main():
    try:
        stdscr = init()

        lanes = [
            ( 0.0, "wwhhwwwhhwwwhhwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"),
            (-3.0, ",,,jllk,,jllllk,,,,,,,jllk,,,,,jk,,,jlllk,,,,jllllk,,,,jlllk,,,,"),
            ( 3.0, ",,,,jllk,,,,,jllk,,,,jllk,,,,,,,,,jllk,,,,,jk,,,,,,jllllk,,,,,,,"),
            ( 2.0, ",,jlk,,,,,jlk,,,,,jk,,,,,jlk,,,jlk,,,,jk,,,,jllk,,,,jk,,,,,,jk,,"),
            ( 0.0, "pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp"),
            (-3.0, "....asdf.......asdf....asdf..........asdf........asdf....asdf..."),
            ( 3.0, ".....ty..ty....ty....ty.....ty........ty..ty.ty......ty.......ty"),
            (-4.0, "..zx.....zx.........zx..zx........zx...zx...zx....zx...zx...zx.."),
            ( 2.0, "..ty.....ty.......ty.....ty......ty..ty.ty.......ty....ty......."),
            ( 0.0, "pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
            ]

        objs = {
            # Bus
            "a": (255, 128, 0),
            "s": (255, 128, 0),
            "d": (255, 128, 0),
            "f": (255, 128, 0),
            # Log
            "j": (128, 64, 0),
            "l": (128, 64, 0),
            "k": (128, 64, 0),
            # Car 1
            "z": (255, 255, 0),
            "x": (255, 255, 0),
            # Car 2
            "t": (0, 0, 255),
            "y": (0, 0, 255),
            # Wall
            "w": (255, 0, 0),
            # Home
            "h": (0, 64, 0),
            # Water
            ",": (0, 128, 255),
            # Pavement
            "p": (64, 64, 64),
            # Road
            ".": (0, 0, 0)
            }

        fx, fy = 8.0, 9.0

        timer = 0.0
        key = ''
        while key != ord('q'):
            # Is frog in danger?
            if get_danger(int(fx), int(fy)):
                fx, fy = 8.0, 9.0                

            key = stdscr.getch()
            if key == curses.KEY_UP and fy > 0.0:
                fy -= 1.0
            elif key == curses.KEY_DOWN and fy < 9.0:
                fy += 1.0
            elif key == curses.KEY_LEFT:
                fx -= 1.0
            elif key == curses.KEY_RIGHT:
                fx += 1.0

            if fx < 0.0:
                fx = 0.0
            if fx > 15:
                fx = 15.0

            # Deal with movement of logs
            if fy <= 3.0:
                # Because the game is working purely in an integer display but
                # using fractions to control the speed of moving objects, we
                # have to sync the frog with the log its landing on. Otherwise,
                # the frog might die due to the log moving slightly ahead of the frog.
                # This could be considered a feature but I'd prefer it to be turned off
                log_pos = timer * lanes[int(fy)][0]
                log_denom, log_numer = math.modf(pos)
                frog_denom, frog_numer = math.modf(fx)
                fx = frog_numer + log_denom
                # Now factor in log movement - as we're abount to move these
                fx -= 0.01 * lanes[int(fy)][0]

            for y, lane in enumerate(lanes):
                start_pos = int(timer * lane[0])
                if start_pos < 0:
                    start_pos = 64 - (abs(start_pos) % 64)
                for i in range(16):
                    obj = lane[1][(start_pos + i) % 64]
                    draw_pixel(i, y, objs[obj])
                    set_danger(i, y, obj)

            # Draw frog
            draw_pixel(int(fx), int(fy), (0, 255, 0))

            unicornhathd.show()
            time.sleep(0.01)
            timer += 0.01
    finally:
        term()

main()
