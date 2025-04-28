import random
import pygame as pg
import word as w
import time

# Initialize game
pg.init()
pg.mixer.init()

# Game constants
win_width = 600
win_height = 700
screen = pg.display.set_mode([win_width, win_height])
pg.display.set_caption('Word Challenge')

# Load sounds
win_sound = pg.mixer.Sound('C:\MyFiles\pyproj\pygame_env\ACSP\ACSP5-3\Win.wav')
lose_sound = pg.mixer.Sound('C:\MyFiles\pyproj\pygame_env\ACSP\ACSP5-3\Lose.wav')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)

# Fonts
font = pg.font.Font(None, 50)
small_font = pg.font.Font(None, 30)
timer_font = pg.font.Font(None, 35)

# Game variables
ans = random.choice(w.word_list)
game_board = [[' ']*5 for _ in range(6)]
count = 0
letters = 0
game_over = False
running = True
letter_status = {chr(i): 'dark_gray' for i in range(97, 123)}
start_time = time.time()
time_limit = 60
timer_stopped = False
sound_played = False
color_reveal = [[None]*5 for _ in range(6)]
frozen_remaining_time = None  # Freeze timer after win/loss

def draw_board():
    base_x = (win_width - 500) // 2
    for row in range(6):
        for col in range(5):
            square = pg.Rect(base_x + col * 80 + 10, row * 70 + 50, 65, 55)
            letter = game_board[row][col]
            border_color = color_reveal[row][col] or white
            pg.draw.rect(screen, border_color, square, width=3)
            if letter != ' ':
                letter_text = font.render(letter.upper(), True, white)
                screen.blit(letter_text, (base_x + col*80 + 25, row*70 + 60))

def check_match():
    global game_over, letter_status, timer_stopped, sound_played, color_reveal, frozen_remaining_time

    current_guess = ''.join(game_board[count]).lower()

    if current_guess == ans:
        game_over = True
        timer_stopped = True
        frozen_remaining_time = max(time_limit - int(time.time() - start_time), 0)
        if not sound_played:
            win_sound.play()
            sound_played = True

    for i in range(5):
        letter = current_guess[i]
        if letter == ans[i]:
            color_reveal[count][i] = green
            letter_status[letter] = 'green'
        elif letter in ans:
            color_reveal[count][i] = yellow
            if letter_status[letter] != 'green':
                letter_status[letter] = 'yellow'
        else:
            color_reveal[count][i] = gray
            if letter_status[letter] not in ['green', 'yellow']:
                letter_status[letter] = 'gray'

def draw_keyboard():
    keyboard_layout = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
    base_y = 550
    for row in keyboard_layout:
        base_x = (win_width - len(row)*35 + 5) // 2
        for i, char in enumerate(row):
            key_rect = pg.Rect(base_x + i*35, base_y, 32, 35)
            color = dark_gray
            if letter_status[char] == 'green':
                color = green
            elif letter_status[char] == 'yellow':
                color = yellow
            elif letter_status[char] == 'gray':
                color = gray
            pg.draw.rect(screen, color, key_rect)
            text = small_font.render(char.upper(), True, white)
            screen.blit(text, (base_x + i*35 + 8, base_y + 5))
        base_y += 40

def draw_timer():
    global timer_stopped, frozen_remaining_time
    if not timer_stopped:
        elapsed = time.time() - start_time
        remaining = max(time_limit - int(elapsed), 0)
        if remaining == 0:
            timer_stopped = True
            frozen_remaining_time = 0
    else:
        if frozen_remaining_time is None:
            elapsed = time.time() - start_time
            frozen_remaining_time = max(time_limit - int(elapsed), 0)
        remaining = frozen_remaining_time

    timer_text = timer_font.render(f"Time: {remaining}s", True, white)
    screen.blit(timer_text, (20, 20))
    return remaining == 0

def draw_game_over():
    if game_over:
        result_text = "Winner!" if ''.join(game_board[count]).lower() == ans else "Game Over!"
        text = font.render(result_text, True, white)
        ans_text = small_font.render(f"Answer: {ans.upper()}", True, white)
        screen.blit(text, (200, 450))
        screen.blit(ans_text, (200, 500))

def reset_game():
    global ans, game_board, count, letters, game_over, letter_status, start_time
    global timer_stopped, sound_played, color_reveal, frozen_remaining_time

    ans = random.choice(w.word_list)
    game_board = [[' ']*5 for _ in range(6)]
    color_reveal = [[None]*5 for _ in range(6)]
    count = 0
    letters = 0
    game_over = False
    timer_stopped = False
    sound_played = False
    frozen_remaining_time = None
    letter_status = {chr(i): 'dark_gray' for i in range(97, 123)}
    start_time = time.time()

while running:
    screen.fill(black)
    time_up = draw_timer()

    if time_up and not game_over and not timer_stopped:
        game_over = True
        timer_stopped = True
        frozen_remaining_time = 0
        if not sound_played:
            lose_sound.play()
            sound_played = True

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.TEXTINPUT and letters < 5 and not game_over:
            entry = event.text.lower()
            if entry.isalpha():
                game_board[count][letters] = entry.upper()
                letters += 1

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE and letters > 0:
                game_board[count][letters - 1] = ' '
                letters -= 1

            if event.key == pg.K_RETURN:
                if game_over:
                    reset_game()
                elif letters == 5 and not game_over:
                    check_match()
                    if ''.join(game_board[count]).lower() == ans or count == 5:
                        game_over = True
                        timer_stopped = True
                        if ''.join(game_board[count]).lower() != ans and not sound_played:
                            lose_sound.play()
                            sound_played = True
                        frozen_remaining_time = max(time_limit - int(time.time() - start_time), 0)
                    else:
                        count += 1
                        letters = 0

    draw_board()
    draw_keyboard()
    draw_game_over()
    pg.display.flip()

pg.quit()
