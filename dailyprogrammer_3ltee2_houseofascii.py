'''
Copyright (c) Paulo Pinto <paulo@cod.pt>
Sample solution of the challenge at: reddit.com/3ltee2

In short:
this:
   *
  ***
******
should become this:
              A
             / \
    A     A +---+ A
   / \   / \|   |/ \
  /   \ +---+   +---+ A
 /     \| o         |/ \
+-------+           +---+
|     o      | |      o |
+-----------------------+

Works well with different aspects, and deals with floating/overlapping blocks.
Try, for instance (add a space on the empty line to delay the construction):
   ***
   ***

    *     ******
   ***  ****
 *********    **
'''

import random, sys

aspect = (4, 2) # block size

class Grid(object):
	'Very simple sparce table implementation'
	emptyblock = ' '
	def __init__(self):
		self.data = {}
		self.minx = 0
		self.maxx = 0
		self.miny = 0
		self.maxy = 0

	def __setitem__(self, pair, c):
		x, y = pair
		self.minx = min(self.minx, x)
		self.maxx = max(self.maxx, x)
		self.miny = min(self.miny, y)
		self.maxy = max(self.maxy, y)
		self.data[(x, y)] = c

	def __getitem__(self, pair):
		try: return self.data[pair]
		except KeyError: return Grid.emptyblock

	def empty(self, x, y):
		return self[(x, y)] == Grid.emptyblock

	def normalized(self):
		'return a new translated grid starting on the origin (0,0)'
		newgrid = Grid()
		for x in range(self.minx, self.maxx + 1):
			for y in range(self.miny, self.maxy + 1):
				if not self.empty(x, y):
					newgrid[(x - self.minx, y - self.miny)] = self[(x, y)]
		return newgrid

	def show(self):
		for y in range(self.miny, self.maxy + 1):
			print(''.join(self[(x, y)] for x in range(self.minx, self.maxx + 1)))

def parse(lines):
	'parses an input lines into a grid, trimming the borders'
	g = Grid()
	for y, line in enumerate(lines):
		for x, block in enumerate(line):
			if block == '*':
				g[(x, y)] = '*'
	return g.normalized()

def build_house(lines):
	# parse lines, determine door position
	bw, bh = aspect
	blue = parse(lines) # blueprints: ' ':empty, *:wall, d:door, r:roof
	grid = Grid()
	doory = blue.maxy
	doorx = random.choice([x for x in range(blue.maxx + 1) if not blue.empty(x, doory)])
	blue[(doorx, blue.maxy)] = 'd'

	def puttext(x, y, text):
		for dy, line in enumerate(text.split('\n')):
			for dx, c in enumerate(line):
				grid[(x + dx, y + dy)] = c

	def roof(x, y, width):
		for dx in range(width//2):
			puttext(x + dx, y - dx, '/' + ' ' * (width-dx*2-2) + '\\')
		if width % 2 == 1:
			grid[(x + width//2, y-width//2)] = 'A'

	# draw blocks
	slab = '+' + '-' * (bw - 1) + '+'
	wall = '+' + '\n|' * (bh - 1) + '\n+'
	for y in range(blue.maxy + 1):
		for x in range(blue.maxx + 1):
			if blue[(x,y)] in ('*','d'):
				if not blue[(x,y - 1)] in ('*','d'):
					puttext(x * bw, y * bh, slab)
					# determine roof width, marking tiles
					for roofwidth in range(blue.maxx - x + 2):
						if blue.empty(x + roofwidth, y - 1) and not blue.empty(x + roofwidth, y):
							blue[(x + roofwidth, y - 1)] = 'r'
						else:
							break
					if roofwidth > 0:
						roof(x * bw + 1, y * bh - 1, roofwidth * bw - 1)

				if blue.empty(x,y+1): puttext(x * bw, (y + 1) * bh, slab)
				if blue.empty(x-1,y): puttext(x * bw, y * bh, wall)
				if blue.empty(x+1,y): puttext((x+1) * bw, y * bh, wall)
				if blue[(x, y)] == '*' and random.randint(1, 2) == 1:
					puttext(x * bw + bw//2, y * bh + bh//2, 'o')

	puttext(doorx * bw + 1, doory * bh, '\n|' * (bh - 1))
	puttext((doorx + 1) * bw - 1, doory * bh, '\n|' * (bh - 1))
	grid.show()

print('blueprints (use * for blocks and space for indenting, empty line to build):')
lines = []
while True:
	line = sys.stdin.readline().rstrip('\n')
	if any(c for c in line if c not in ('*', ' ')):
		print('bye')
		break
	elif line:
		lines.append(line)
	elif len(lines):
		build_house(lines)
		lines = []
		print('')
