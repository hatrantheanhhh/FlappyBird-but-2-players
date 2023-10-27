import pygame, sys, random
from screeninfo import get_monitors
monitors = get_monitors()

random_pipe_position=500 #biến này là vị trí của ống

def draw_floor():
	screen.blit(floor_surface,(floor_x_position,900))
	screen.blit(floor_surface,(floor_x_position + 576,900))

def create_pipe(): #hàm này để sinh các chướng ngại vật (ống)
	global random_pipe_position
	random_pipe_position = random.randint(400, 800) #mỗi lần tạo ra ống mới tại 1 vị trí ngẫu nhiên
	#sinh ra 2 ống trên và dưới và return chúng 
	bottom_pipe = pipe_surface.get_rect(midtop = (900,random_pipe_position)) 
	top_pipe = pipe_surface.get_rect(midbottom = (900,random_pipe_position-270))
	return bottom_pipe, top_pipe
 
def create_powerup(): #hàm này tạo ra các powerup là tăng tốc và giảm tốc
	random_number =random.randint(1, 10)
	#lấy 1 số ngẫu nhiên từ 1 đến 10
	#nếu là số 2 thì tạo ra powerup tăng tốc
	#nếu là 3 thì tạo ra speedup giảm tốc
	#còn là những số khác thì không tạo powerup
	#return vị trí của powerup và mô tả của chúng: 'fast' hoặc 'slow' hoặc return 0 nếu không tạo powerup
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
	#di chuyển tất cả các ống trên mỗi khung hình với tốc độ được thể hiện bằng biến speed và return về list các ống đó để in ra
	#speed mặc định là 5  #với mỗi powerup tăng tốc thì speed tăng lên 1 đơn vị, tối đa là 
	for pipe in pipes:
		pipe.centerx -= speed
	return pipes

def move_pws(pws):
	#cũng tương tự hàm move_pipes(), di chuyển các powerup với cùng tốc độ
	for powerup in pws:
		powerup[0].centerx -= speed
	return pws

def draw_pipes_powerup(pipes, pws):
	#vẽ lên màn hình list các ống và list các powerup bằng screen.blit()
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

def check_collision(pipes):
	global score
	'''
	hàm này để kiểm tra sự va chạm của bird với các chướng ngại vật (bản chất là các hình chữ nhật) bằng hàm colliderect
	duyệt tất cả các ống trong list và kiểm tra sự va chạm giữa 2 con chim và các ống đó
	ngoài ra cũng cần kiểm tra xem có con chim nào đã bay lên quá cao hoặc đã rơi xuống đất chưa (tức là chạm vào rìa trên hoặc rìa dưới)
	nếu có va chạm, game kết thúc
	
	'''
	# return True
	for pipe in pipes: 
		#vòng for này để tính điểm và phát âm thanh mỗi khi chim đi trước đã vượt được qua 1 chướng ngại vật
		if bird2_rectangle.centerx == pipe.centerx:
			score_sound.play()
			score+=0.5
	
	# 2 vòng for tới này sẽ kiểm tra lần lượt chim số 1 và chim số 2 xem đã bị va chạm với ống nước chưa?
	for pipe in pipes:
		if bird1_rectangle.colliderect(pipe):
			death_sound.play()
			return False
	for pipe in pipes:
		if bird2_rectangle.colliderect(pipe):
			death_sound.play()
			return False
		
	# cuối cùng là kiểm tra xem có con chim nào đã chạm tới rìa trên hoặc rìa dưới của màn hình chưa?
	if bird1_rectangle.top <= -100 or bird1_rectangle.bottom >= 900:
		death_sound.play()
		return False
	if bird2_rectangle.top <= -100 or bird2_rectangle.bottom >= 900:
		death_sound.play()
		return False
	return True

def check_collision_powerups(pws):
	'''
	hàm này để kiểm tra xem các con chim có chạm vào được các powerups
	nguyên lý hoạt động tương tự hàm kiểm tra va chạm với ống check_collision():
	là duyệt qua tất cả các powerups có trong list các powerups được truyền vào hàm này và kiểm tra xem chim có va chạm với chúng không
	'''
	global speed 
	i=0
	while i < len(pws):
		if bird1_rectangle.colliderect(pws[i][0]) or bird2_rectangle.colliderect(pws[i][0]):
			if pws[i][1]=='fast': #nếu có sự va chạm với powerup tăng tốc, tốc độ (speed) sẽ tăng 1 đơn vị, tối đa là 10
				speed = min(speed+1, 10)
				powerup_faster_sound.play()
				pws.pop(i)
			else: #nếu có sự va chạm với powerup giảm tốc, tốc độ (speed) sẽ giảm 1 đơn vị, tối thiểu là 3
				speed = max(speed-1, 3)
				powerup_slower_sound.play()
				pws.pop(i)
		i+=1

def rotate_bird(bird, index):
	'''
	hàm này trả về hình ảnh con chim bị xoay trong lúc di chuyển
	'''
	if index==1:
		new_bird = pygame.transform.rotate(bird, -bird1_speed*3)
		return new_bird
	else: 
		new_bird = pygame.transform.rotate(bird, -bird2_speed*3)
		return new_bird
        
def score_display(game_state):
	'''
	game_state là biến lưu trạng thái hiện tại của trò chơi
	'main_game' tương ứng với đang chơi, 'game_over' tương ứng với lúc game đã kết thúc và đang trong trạng thái chờ kích hoạt game mới
	'''
	#tạo số điểm bằng font chữ của game và in ra màn hình
	if game_state == 'main_game':
		score_surface = font.render(str(int(score)), True, (255,255,255))
		screen.blit(score_surface, (width_game//2, 100))
	#nếu game đã kết thúc, in ra điểm đã đạt được và cả high_score ở phía dưới của điểm hiện tại nữa
	if game_state == 'game_over':
		score_surface = font.render(f'Score: {int(score)}', True, (255,255,255))
		screen.blit(score_surface, (width_game//3, 100))

		high_score_surface = font.render(f'High Score: {int(high_score)}', True, (255,255,255))
		screen.blit(high_score_surface, (width_game//3, 185))

def update_score(score, high_score): #cập nhật kỷ lục mới
	high_score = max(high_score, score)
	return high_score


'''
khởi tạo cửa sổ trò chơi
chiều rộng 800px, dài 1024px
'''
width_game=800
height_game=1024
pygame.init()
screen = pygame.display.set_mode((800,1024))        #màn hình chính của game
clock = pygame.time.Clock()                         #tạo 1 clock để quản lý tốc độ khung hình (fps) 
font = pygame.font.Font('./assets/04B_19.TTF',40)   #font chữ cho game

gravity = 0.6			#trọng lực là 0.6 pixel, với mỗi khung hình thì con chim sẽ bị rơi xuống thêm 0.6 pixel
bird1_speed = 0			#tốc độ của chim số 1
bird2_speed = 0			#tốc độ của chim số 2
game_active = False		#thể hiện game có đang được chơi hay không, khởi tạo False nghĩa là chưa được chơi
score = 0				#điểm xuất phát từ 0
high_score = 0			#lưu lại kỷ lục cao nhất
speed=5					#tốc độ khởi tạo là 5, có thể dao động từ 3 đến 10 thông qua các powerup

background_list=[]		#list các background để chọn
background_list.append(pygame.image.load('assets/background-day_5.png'))
background_list.append(pygame.image.load('assets/background-day_5.png'))
background_list.append(pygame.image.load('assets/background-day_4.png'))
background_list.append(pygame.image.load('assets/background-day_3.png'))
background_list.append(pygame.image.load('assets/background-day_2.png'))
background_list.append(pygame.image.load('assets/background-day.png'))

pipes_image_list=[pygame.image.load('assets/pipe-green2x.png'), pygame.image.load('assets/pipe-red2x.png')	]

background_surface = background_list[0]

#một vài hình ảnh các vật trong game

floor_surface = pygame.image.load('assets/base2x.png')						#nền đất
floor_x_position = 0														#vị trí ban đầu của nền đất
bird1_surface = pygame.image.load('assets/bluebird-midflap2x.png')			#hình con chim số 1
bird1_rectangle = bird1_surface.get_rect(center = (100,height_game//2))		#vị trí chim số 1
bird2_surface = pygame.image.load('assets/yellowbird-midflap2x.png')		#hình con chim số 2
bird2_rectangle = bird2_surface.get_rect(center = (200, height_game//2))	#vị trí chim số 2
arrow_slow_surface=pygame.image.load('assets/arrow_reverse.png')			#hình powerup giảm tốc
arrow_speedup_surface=pygame.image.load('assets/arrow.png')					#hình powerup tăng tốc
pipe_surface = pygame.image.load('assets/pipe-green2x.png')					#hình cái ống
get_ready_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png'))	#màn hình get_ready
get_ready_rectangle = get_ready_surface.get_rect(center = (width_game//2, height_game//2)) 

#2 list chứa các ống và các powerups
pipe_list = []																
powerup_list=[]

#tạo USEREVENT mới là SPAWN
#dùng hàm set_timer để kích hoạt chúng mỗi 1.6 giây 1 lần
SPAWN = pygame.USEREVENT
pygame.time.set_timer(SPAWN, 1600)


#nguồn âm thanh của game
flap_sound = pygame.mixer.Sound('assets/wing.wav')
death_sound = pygame.mixer.Sound('assets/hit.wav')
score_sound = pygame.mixer.Sound('assets/point.wav')
powerup_faster_sound = pygame.mixer.Sound('assets/faster.mp3')
powerup_slower_sound = pygame.mixer.Sound('assets/slower.mp3')

#vòng lặp chính của game
while True:
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit() #cài đặt tắt trò chơi khi bấm dấu X trên góc cửa sổ trò chơi
			sys.exit()

		#nếu có phím được bấm, chạy đoạn code này để xử lý với từng phím được ấn
		if event.type == pygame.KEYDOWN:     
			if event.key == pygame.K_ESCAPE: #cũng có thể thoát găm bằng cách ấn phím Esc
				pygame.quit()
				sys.exit()
			
			if event.key == pygame.K_SPACE and game_active:  
				# phím SPACE để điều khiển con chim số 1, reset tốc độ rơi của nó về 0 và giảm 12 đơn vị mỗi khung hình
				# tức là mỗi khung hình thì con chim sẽ bay lên 12 pixel và có chịu ảnh hưởng rơi dần của biến gravity
				# print
				bird1_speed = 0
				bird1_speed -= 12  
				flap_sound.play()
			if event.key == pygame.K_UP and game_active:
				#tương tự chim số 1, người chơi thứ 2 bấm phím UP trên bàn phím để điều khiển chim số 2
				flap_sound.play()
				bird2_speed = 0
				bird2_speed -= 12
 

			if event.key == pygame.K_SPACE and game_active == False:
				'''
				nếu game chưa bắt đầu thì bấm SPACE để khởi động game mới và làm 1 số việc:
				xóa sạch các ống và các powerups trong list
				reset độ cao về giữa màn hình và tốc độ rơi của 2 con chim
				reset điểm về 0
				ống nước sẽ có màu ngẫu nhiên
				'''
				pipe_surface=random.choice(pipes_image_list)
				# background_surface=random.choice(background_list)
				game_active = True
				pipe_list.clear()
				powerup_list.clear()
				bird1_rectangle.center = (100, height_game//2)
				bird1_speed = 0
				bird2_rectangle.center = (200, height_game//2)
				bird2_speed = 0
				score = 0

		#nếu event hiện tại là SPAWN (sinh ra mỗi 1.6 giây) thì gọi hàm sinh ống nước và powerup mới
		#sau đó lưu chúng vào trong 2 list chính chứa các object trong game là pipe_list và powerup_list
		if event.type == SPAWN:
			pipe_list.extend(create_pipe())
			tmp = create_powerup()
			if tmp!=0:
				powerup_list.append(tmp)

	#Phần in ra màn hình
	#in ra background đầu tiên
	screen.blit(background_surface,(0,0))

	if game_active:
		# bird movement
		#với mỗi khung hình thì bọn chim phải chịu thêm 1 lực gravity được cộng dồn vào tốc độ rơi của nó bird_speed
		bird1_speed += gravity
		bird2_speed += gravity

		#xoay con chim
		rotated_bird1 = rotate_bird(bird1_surface, 1)
		rotated_bird2 = rotate_bird(bird2_surface, 2)

		#vị trí (theo trục y) sẽ thay đổi theo tốc độ rơi của nó bằng cách cộng tốc độ rơi vào vị trí y hiện tại của chúng
		bird1_rectangle.centery += bird1_speed
		bird2_rectangle.centery += bird2_speed

		#vẽ ra màn hình hình ảnh với vị trí mới cập nhật
		screen.blit(rotated_bird1, bird1_rectangle)
		screen.blit(rotated_bird2, bird2_rectangle)

		#gọi hàm kiểm tra sự va chạm với các object
		game_active = check_collision(pipe_list)
		check_collision_powerups(powerup_list)

		# di chuyển các ống nước và powerups trên mỗi khung hình, sau đó in ra màn hình
		pipe_list = move_pipes(pipe_list)
		powerup_list = move_pws(powerup_list)
		draw_pipes_powerup(pipe_list, powerup_list)
	
		# in điểm hiện tại ra màn hình
		score_display('main_game')

	else: #cập nhật và in ra thông báo game over, điểm hiện tại, kỷ lục
		screen.blit(get_ready_surface, get_ready_rectangle)
		high_score = update_score(score, high_score)
		score_display('game_over')


	# mỗi khung hình thì nền đất sẽ di chuyển lùi 1 pixel
	# nếu hình nền đất đã lùi quá sâu (sắp ra khỏi màn hình) thì sẽ reset về vị trí ban đầu và tiếp tục di chuyển
	floor_x_position -= 1
	draw_floor()
	if floor_x_position <= -376:
		floor_x_position = 0

	#update những gì xuất hiện trên màn hình và kiểm soát tốc độ khung hình ở mức 60 FPS
	pygame.display.update()
	clock.tick(60)
