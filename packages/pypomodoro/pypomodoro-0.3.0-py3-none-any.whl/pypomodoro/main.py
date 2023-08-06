#!/usr/bin/env python3
"""
Pomodoro
"""

__author__ = "Andrew Lowe"
__version__ = "0.3.0"
__license__ = "MIT"

import curses
import argparse
import time
import datetime as dt


class Pomodoro:

  def __init__(self,work_time=25,break_time=5):
    self.work_secs=work_time*60
    self.break_secs=break_time*60
    self.pomo_number = 1

  def start(self):
    self.start_time = dt.datetime.now()
    self.pomo_end_time = self.start_time + dt.timedelta(seconds=self.work_secs)
    self.break_end_time = self.start_time + dt.timedelta(seconds=self.work_secs+self.break_secs)
  
  def get_state(self):
    now = dt.datetime.now()

    if now < self.pomo_end_time:
      return "pomo"
    elif now <= self.break_end_time:
      return "break"
    else:
      return "done"

  def restart(self):
    self.pomo_number += 1
    self.start()

def get_time_display(time_text):
  a = "####" 
  b = "#  #"
  c = "#   "
  d = "   #"
  o = "   "
  x = " # "

    
               # 0,1,2,3,4,5,6,7,8,9,:
  templates = [ [a,d,a,a,b,a,a,a,a,a,o],
                [b,d,d,d,b,c,c,d,b,b,x],
                [b,d,a,a,a,a,a,d,a,a,o],
                [b,d,c,d,d,d,b,d,b,d,x],
                [a,d,a,a,d,a,a,d,a,a,o] ]

  out = ""
  for row in templates: 
    for digit in time_text:
      if digit == ":":
        digit = 10
      else:
        digit = int(digit,10)
      out = out + row[digit] + " "
    out = out + "\n"

  return out
  
def print_screen(screen,text):
  x = 0
  y = 0

  num_rows, num_cols = screen.getmaxyx()
  middle_row = int(num_rows / 2)
  middle_col = int(num_cols / 2)
 

  lines = text.rstrip("\n").split("\n")
  longest_line = max(map(len,lines))

  y = middle_row - int(len(lines) / 2)
  x = middle_col - int(longest_line / 2)

  for line in lines:
    screen.addstr(y,x,line + "\n", curses.color_pair(1))
    y = y + 1
  screen.refresh()

def init_args():
  """ This is executed when run from the command line """
  parser = argparse.ArgumentParser()

  parser.add_argument("-w", "--work", default=25, type=float, action="store", dest="work_mins", help="Number of miinutes for work")
  parser.add_argument("-b", "--break", default=5, type=float, action="store", dest="break_mins", help="Number of minutes for break")
  parser.add_argument("-v", "--verbose", action="store_true", help="Move detailed display")
  
  # Specify output of "--version"
  parser.add_argument(
      "--version",
      action="version",
      version="%(prog)s (version {version})".format(version=__version__))

  args = parser.parse_args()
  return args

def handle_screen_input(screen):
  key_pressed = ''
  try:
    key = screen.getkey()
  except curses.error as e:
    if str(e) == 'no input': return ''
    raise e
  return key

def main(screen=None):
  state_text = {
      'pomo' : 'Time to work',
      'break': 'Take a break',
      'done': 'Press space to get back to work'
  }

  args = init_args()
  
  if not screen : curses.wrapper(main)
  else:
    #print(args)
    curses.curs_set(0)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    screen.nodelay(True)

    pomo = Pomodoro(args.work_mins,args.break_mins)
    pomo.start()
    screen.clear()
    while True:
      # Pomodora started
      key_pressed = handle_screen_input(screen)
      if key_pressed == 'q':
        exit(0);

      now = dt.datetime.now()
      pom_end_time = pomo.pomo_end_time
      break_end_time = pomo.break_end_time
      pom_state = pomo.get_state()
      pom_start_time = pomo.start_time

      if pom_state == "pomo":
        time_left = pom_end_time - now
      elif pom_state == "done":
        time_left = "00:00:00"
        if key_pressed == ' ':
          pomo.restart()
          continue
      else :
        time_left = break_end_time - now

      display_info = state_text[pom_state]

      if key_pressed != '':
        display_info = "Press 'q' to quit"
      
      if args.verbose:
        display_info += "\n" + f"Pomo number: {pomo.pomo_number}"
        display_info += "\n" + f"Pomo end time: {pomo.pomo_end_time:%H:%M:%S}"
        display_info += "\n" + f"Break end time: {pomo.break_end_time:%H:%M:%S%z}"
      time_left = str(time_left).split(".")[0]
      time_left = "{:0>8}".format(time_left)
      display_text = get_time_display(time_left)
      display_text = display_text + "\n" + display_info
      print_screen(screen,display_text)
      time.sleep(1)

if __name__ == "__main__": main()
