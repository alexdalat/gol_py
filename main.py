import pygame
import sys
import copy
import sched, time
s = sched.scheduler(time.time, time.sleep)

BLACK = (0, 0, 0)
WHITE = (204, 204, 204)
RED = (204, 112, 106)
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1000
time = 100 # ms
extraDistKill = 10 # blocks

dirs = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

blockSize = 20
boardSizeX = int(WINDOW_WIDTH / blockSize)
boardSizeY = int(WINDOW_HEIGHT / blockSize)
playing = True

tiles = []
new_tiles = []

def main():
	global SCREEN, CLOCK, tiles, playing, time
	pygame.init()
	SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	CLOCK = pygame.time.Clock()
	SCREEN.fill(BLACK)

	UPDATEEVENT = pygame.USEREVENT+1
	pygame.time.set_timer(UPDATEEVENT, time)

	while True:
		drawGrid()
		for event in pygame.event.get():
			if event.type == UPDATEEVENT: # update loop
				if playing:
					updateBoard()
			if event.type == pygame.KEYDOWN: # KEY PRESSES
				if event.key == pygame.K_SPACE: # pause/play
					playing = not playing
				if event.key == pygame.K_UP: # faster speed
					time /= 2
					time = int(max(time, 10))
					pygame.time.set_timer(UPDATEEVENT, time)
				if event.key == pygame.K_DOWN: # slower speed
					time *= 2
					time = min(time, 5000)
					pygame.time.set_timer(UPDATEEVENT, time)
				if event.key == pygame.K_r: # reset
					tiles = []
			if event.type == pygame.MOUSEBUTTONDOWN: # button click
				pos = pygame.mouse.get_pos()
				if event.button == 1: # left click
					if((int(pos[0]/blockSize), int(pos[1]/blockSize)) not in tiles):
						tiles.append((int(pos[0]/blockSize), int(pos[1]/blockSize)))
					else:
						tiles.remove((int(pos[0]/blockSize), int(pos[1]/blockSize)))
				if event.button == 3: # right click
					pass
			if event.type == pygame.QUIT: # quit
				pygame.quit()
				sys.exit()

		pygame.display.update()


def drawGrid():
	for x in range(0, boardSizeX):
		for y in range(0, boardSizeY):
			col = WHITE
			if((x, y) in tiles):
				col = RED
			rect = pygame.Rect(x*blockSize+1, y*blockSize+1, blockSize-2, blockSize-2)
			pygame.draw.rect(SCREEN, col, rect)

def checkStatus(cellX, cellY):
	if((cellX < -extraDistKill or cellX > boardSizeX+extraDistKill or cellY < -extraDistKill or cellY > boardSizeY+extraDistKill) and ((cellX, cellY) in new_tiles)):
		new_tiles.remove((cellX, cellY))
	alive = ((cellX, cellY) in tiles)
	live_count = 0
	for index, dir in enumerate(dirs):
		checkX = cellX + dir[0]
		checkY = cellY + dir[1]
		#if(checkX < 0 or checkX > boardSizeX or checkY < 0 or checkY > boardSizeY):
		#	continue
		if((checkX, checkY) in tiles):
			live_count += 1
	if(alive and (live_count == 2 or live_count == 3)):
		return 1 # alive
	if(not alive and live_count == 3):
		if((cellX, cellY) not in new_tiles):
			new_tiles.append((cellX, cellY))
		return 1 # alive
	if(((cellX, cellY) in new_tiles)): # if not already dead, kill
		new_tiles.remove((cellX, cellY))
	return 0 # dead

def updateBoard():
	global tiles, new_tiles
	new_tiles = copy.deepcopy(tiles)
	for tile in tiles:
		checkStatus(tile[0], tile[1])
		for index, dir in enumerate(dirs):
			checkStatus(tile[0] + dir[0], tile[1] + dir[1])
	tiles = new_tiles
	#print(tiles)



if __name__ == "__main__":
	main()