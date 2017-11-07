#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import curses
import unicornhathd

def draw_pixel(x, y, col):
    unicornhathd.set_pixel(x, 16 - 1 - y, *col)

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
            ( 0.0, "wwwhhwwwhhwwwhhwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"),
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

        fx, fy = 8, (9 + 3)

        timer = 0.0
        key = ''
        while key != ord('q'):
            key = stdscr.getch()
            if key == curses.KEY_UP:
                stdscr.addstr(2, 20, "Up")
                fy -= 1
            elif key == curses.KEY_DOWN:
                stdscr.addstr(3, 20, "Down")
                fy += 1
            elif key == curses.KEY_LEFT:
                stdscr.addstr(4, 20, "Left")
                fx -= 1
            elif key == curses.KEY_RIGHT:
                stdscr.addstr(5, 20, "Right")
                fx += 1

            for y, lane in enumerate(lanes):
                start_pos = int(timer * lane[0])
                if start_pos < 0:
                    start_pos = 64 - (abs(start_pos) % 64)
                for i in range(16):
                    draw_pixel(i, y+3, objs[lane[1][(start_pos + i) % 64]])

            # Draw frog
            draw_pixel(fx, fy, (0, 255, 0))

            unicornhathd.show()
            time.sleep(0.01)
            timer += 0.01
    finally:
        term()

main()
