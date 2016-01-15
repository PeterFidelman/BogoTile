import curses

tileheight=16
data = [0]*(8*tileheight)
formatstrs = ['%{:08b}','      ${:02x}']

def main():
	curx = 0
	cury = 0
	key = None
	prev = None
	fs = 0
	while(True):
		# Rendering
		for tiley in range(tileheight):
			for tilex in range(8):
				lincrt.stdscr.addstr(tiley, 25+tilex*2, shades[data[tiley*8 + tilex]])
			lincrt.stdscr.addstr(tiley, 26+8*2, ";")
			lincrt.stdscr.addstr(tiley, 28+8*2, str(tiley))
		lincrt.stdscr.addstr(17, 0, 'Arrows to Move! :: QWER to Draw! :: Shift-C to Clear! :: Shift-Q to Quit!')

		# Binary
		for tiley in range(tileheight):
			line = data[tiley*8 : tiley*8+8]

			combine = ((line[0]&0x1)<<7) + ((line[1]&0x1)<<6) + ((line[2]&0x1)<<5) + ((line[3]&0x1)<<4) + ((line[4]&0x1)<<3) + ((line[5]&0x1)<<2) + ((line[6]&0x1)<<1) + ((line[7]&0x1))
			lincrt.stdscr.addstr(tiley, 0, "db %s," % formatstrs[fs].format(combine))
			combine = ((line[0]&0x2)<<6) + ((line[1]&0x2)<<5) + ((line[2]&0x2)<<4) + ((line[3]&0x2)<<3) + ((line[4]&0x2)<<2) + ((line[5]&0x2)<<1) + ((line[6]&0x2)   ) + ((line[7]&0x2)>>1)
			lincrt.stdscr.addstr(tiley, 13, "%s ; " % formatstrs[fs].format(combine))

		lincrt.stdscr.move(cury, 25+curx*2)
		lincrt.stdscr.refresh()
		# Control
		prev=key
		key = lincrt.stdscr.getch()
		if key == curses.KEY_UP:
			cury = max(0, cury-1)
		elif key == curses.KEY_DOWN:
			cury = min(tileheight-1, cury+1)
		elif key == curses.KEY_LEFT:
			curx = max(0, curx-1)
		elif key == curses.KEY_RIGHT:
			curx = min(7, curx+1)
		elif key == ord('B'):
			fs ^= 1
		elif key == ord('C'):
			(curx, cury) = (0, 0)
			for i in range(len(data)):
				data[i]=0
		elif key == ord('Q'):
			return
		elif key == ord('q'):
			data[cury*8 + curx] = 0
		elif key == ord('w'):
			data[cury*8 + curx] = 1
		elif key == ord('e'):
			data[cury*8 + curx] = 2
		elif key == ord('r'):
			data[cury*8 + curx] = 3
		elif key == ord(' ') and prev == key:
			key=None
			data[cury*8 + curx] = 0
			curx = min(7, curx+1)
		elif key == ord(',') and prev == ord('`'):
			key=None
			data[cury*8 + curx] = 1
			curx = min(7, curx+1)
		elif key == ord(':') and prev == key:
			key=None
			data[cury*8 + curx] = 2
			curx = min(7, curx+1)
		elif key == ord('#') and prev == key:
			key=None
			data[cury*8 + curx] = 3
			curx = min(7, curx+1)
		elif key == ord('\n'):
			curx = 0
			cury = min(tileheight-1, cury+1)

class MiniCRT:
	def __init__(self):
		self.stdscr = curses.initscr()
		curses.noecho()
		curses.cbreak()
		self.stdscr.keypad(1)

	def wrapper(self, function):
		try:
			function()
		finally:
			self.stdscr.keypad(0)
			curses.nocbreak()
			curses.echo()
			curses.endwin()

lincrt = MiniCRT()
shades = ['  ', '`,', '::', '##']
lincrt.wrapper(main)
