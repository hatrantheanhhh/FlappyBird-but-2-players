import pygame, sys, random
from screeninfo import get_monitors
monitors = get_monitors()
print(monitors)

random_pipe_position=500

if monitors:
    first_monitor = monitors[0]
    screen_width, screen_height = first_monitor.width, first_monitor.height
    print("Kích thước màn hình: {}x{}".format(screen_width, screen_height))

def draw_floor():
	screen.blit(floor_surface,(floor_x_position,900))
	screen.blit(floor_surface,(floor_x_position + 576,900))

def create_pipe():
	global random_pipe_position
	random_pipe_position = random.randint(400, 800)
	bottom_pipe = pipe_surface.get_rect(midtop = (900,random_pipe_position))
	top_pipe = pipe_surface.get_rect(midbottom = (900,random_pipe_position-270))
	return bottom_pipe, top_pipe
 
def create_powerup():
	random_number =random.randint(1, 10)
	if random_number == 2:
		speedup = arrow_speedup_surface.get_rect(center = (900, random_pipe_position - 20))
		return [speedup, 'fast']
	# else: 
	elif random_number==3: 
		speedup = arrow_slow_surface.get_rect(center = (900, random_pipe_position - 20))
		return [speedup, 'slow']
	return 0 

def move_pipes(pipes):
	# print(pipes)
	for pipe in pipes:
		pipe.centerx -= speed
	return pipes

def move_pws(pws):
	for powerup in pws:
		powerup[0].centerx -= speed
	return pws

def draw_pipes_powerup(pipes, pws):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)
	for power in pws:
		if power[1]=='slow':
			screen.blit(arrow_slow_surface, power[0])
		else:
			screen.blit(arrow_speedup_surface, power[0])

def draw_pws(pws):
	for power in pws:
		if power.bottom >= 1024:
			screen.blit(arrow_slow_surface, power)
		
def check_collision(pipes):
	# return True
	for pipe in pipes:
		if bird2_rectangle.centerx == pipe.centerx:
			score_sound.play()
		if bird1_rectangle.colliderect(pipe):
			death_sound.play()
			return False
	if bird1_rectangle.top <= -100 or bird1_rectangle.bottom >= 900:
		death_sound.play()
		return False
	for pipe in pipes:
		if bird2_rectangle.colliderect(pipe):
			death_sound.play()
			return False
	if bird2_rectangle.top <= -100 or bird2_rectangle.bottom >= 900:
		death_sound.play()
		return False
	return True

def check_collision_powerups(pws):
	global speed 
	i=0
	while i < len(pws):
		if bird1_rectangle.colliderect(pws[i][0]) or bird2_rectangle.colliderect(pws[i][0]):
			if pws[i][1]=='fast':
				speed = min(speed+1, 10)
				powerup_faster_sound.play()
				pws.pop(i)
			else:
				speed = max(speed-1, 3)
				powerup_slower_sound.play()
				pws.pop(i)
		i+=1

def rotate_bird(bird, index):
	if index==1:
		new_bird = pygame.transform.rotate(bird, -bird1_speed*3)
		return new_bird
	else: 
		new_bird = pygame.transform.rotate(bird, -bird2_speed*3)
		return new_bird
        
def score_display(game_state):
	if game_state == 'main_game':
		score_surface = font.render(str(int(score)), True, (255,255,255))
		score_rectangle = score_surface.get_rect(center = (width_game//2, 100))
		screen.blit(score_surface, score_rectangle)

	if game_state == 'game_over':
		score_surface = font.render(f'Score: {int(score)}', True, (255,255,255))
		score_rectangle = score_surface.get_rect(center = (width_game//2, 100))
		screen.blit(score_surface, score_rectangle)

		high_score_surface = font.render(f'High Score: {int(high_score)}', True, (255,255,255))
		high_score_rectangle = high_score_surface.get_rect(center = (288, 185))
		screen.blit(high_score_surface, high_score_rectangle)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score


#function to initialize (init()) pygame
# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
width_game=800
height_game=1024
pygame.init()
screen = pygame.display.set_mode((800,1024))
clock = pygame.time.Clock()
font = pygame.font.Font('./assets/04B_19.TTF',40)

# variables for the game
gravity = 0.6
bird1_speed = 0
bird2_speed = 0
game_active = False
score = 0
high_score = 0
speed=5

background_list=[]
background_list.append(pygame.image.load('assets/background-day_5.png'))
background_list.append(pygame.image.load('assets/background-day_5.png'))
background_list.append(pygame.image.load('assets/background-day_4.png'))
background_list.append(pygame.image.load('assets/background-day_3.png'))
background_list.append(pygame.image.load('assets/background-day_2.png'))
background_list.append(pygame.image.load('assets/background-day.png'))

background_surface = background_list[0]

floor_surface = pygame.image.load('assets/base2x.png')
floor_x_position = 0

bird1_surface = pygame.image.load('assets/bluebird-midflap2x.png')
bird1_rectangle = bird1_surface.get_rect(center = (100,height_game//2))

bird2_surface = pygame.image.load('assets/yellowbird-midflap2x.png')
bird2_rectangle = bird2_surface.get_rect(center = (200, height_game//2))

arrow_slow_surface=pygame.image.load('assets/arrow_reverse.png')
arrow_speedup_surface=pygame.image.load('assets/arrow.png')
arrow_rect=arrow_speedup_surface.get_rect(center = (300, height_game//2))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
print(arrow_slow_surface, pipe_surface)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
SPAWNPWS = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1600)
pygame.time.set_timer(SPAWNPWS, 1600)
pipe_height = [400, 600, 800]

powerup_list=[]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png'))
game_over_rectangle = game_over_surface.get_rect(center = (288, height_game//2))

flap_sound = pygame.mixer.Sound('assets/wing.wav')
death_sound = pygame.mixer.Sound('assets/hit.wav')
score_sound = pygame.mixer.Sound('assets/point.wav')
powerup_faster_sound = pygame.mixer.Sound('assets/faster.mp3')
powerup_slower_sound = pygame.mixer.Sound('assets/slower.mp3')
# score_sound_countdown = 100


while True:
	for event in pygame.event.get():
		print(speed)
		if event.type == pygame.K_0:
			print(1)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		# keys = pygame.key.get_pressed()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == pygame.K_SPACE and game_active:
				# print
				bird1_speed = 0
				bird1_speed -= 12  
				flap_sound.play()
			if event.key == pygame.K_UP and game_active:
				flap_sound.play()
				bird2_speed = 0
				bird2_speed -= 12
 
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				powerup_list.clear()
				bird1_rectangle.center = (100, height_game//2)
				bird1_speed = 0
				bird2_rectangle.center = (200, height_game//2)
				bird2_speed = 0
				score = 0


		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())
		if event.type == SPAWNPWS:
			tmp = create_powerup()
			if tmp!=0:
				powerup_list.append(tmp)

	screen.blit(background_surface,(0,0))

	if game_active:
		# bird movement
		bird1_speed += gravity
		bird2_speed += gravity
		rotated_bird1 = rotate_bird(bird1_surface, 1)
		rotated_bird2 = rotate_bird(bird2_surface, 2)
		bird1_rectangle.centery += bird1_speed
		bird2_rectangle.centery += bird2_speed
		screen.blit(rotated_bird1, bird1_rectangle)
		screen.blit(rotated_bird2, bird2_rectangle)
		# screen.blit(arrow_speedup_surface, arrow_rect) 
		game_active = check_collision(pipe_list)
		check_collision_powerups(powerup_list)

		# pipes
		pipe_list = move_pipes(pipe_list)
		powerup_list = move_pws(powerup_list)
		draw_pipes_powerup(pipe_list, powerup_list)
        # draw_pws(powerup_list)
	
		score += 0.01
		score_display('main_game')
		# score_sound_countdown -= 1
		# if score_sound_countdown <= 0:
		# 	score_sound.play()
		# 	score_sound_countdown = 100

	else:
		screen.blit(game_over_surface, game_over_rectangle)
		high_score = update_score(score, high_score)
		score_display('game_over')


	#Floor
	floor_x_position -= 1.
	draw_floor()
	if floor_x_position <= -376:
		floor_x_position = 0

	pygame.display.update()
	clock.tick(60)
