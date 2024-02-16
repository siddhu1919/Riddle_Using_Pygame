import pygame
import sys
import random
import time
import json


# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Riddle Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font settings
font = pygame.font.Font(None, 32)
popup_font = pygame.font.Font(None, 48)


riddles = None
# Assuming your corrected JSON is saved in 'dataset.json'
with open("riddle_gui.json", "r") as file:
    riddles = json.load(file)


# Load riddles and answers
# riddles = [
#     {"riddle": "What has keys but can't open locks?", "answer": "keyboard"},
#     {"riddle": "What has words, but never speaks?", "answer": "book"},
#     # Add your riddles here. Ensure there are at least 10 for this example.
# ]
# print(riddles)


random.shuffle(riddles)  # Shuffle riddles to get them in random order

# Limit to 10 riddles
riddles = riddles[:10]

# Game variables
current_riddle_index = 0
user_answer = ""
score = 0
total_questions = len(riddles)
answers_submitted = [False] * total_questions
start_time = time.time()
game_duration = 600  # 10 minutes in seconds

# Button variables
button_font = pygame.font.Font(None, 24)
next_button = pygame.Rect(screen_width - 150, screen_height - 40, 100, 30)
previous_button = pygame.Rect(50, screen_height - 40, 100, 30)  # Previous button
submit_button = pygame.Rect(screen_width / 2 - 50, screen_height - 40, 100, 30)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def draw_button(button, text, surface):
    pygame.draw.rect(surface, GRAY, button)
    draw_text(text, button_font, BLACK, surface, button.x + 5, button.y + 5)


def show_popup_message(message, color, duration=1000):
    surface = pygame.Surface((screen_width, screen_height))
    surface.set_alpha(128)  # Transparency value
    surface.fill(BLACK)
    screen.blit(surface, (0, 0))
    draw_text(message, popup_font, color, screen, 325, screen_height / 2 - 20)
    pygame.display.flip()
    pygame.time.delay(duration)


def game_ended():
    show_popup_message(f"Final Score: {score}", WHITE, 5000)
    pygame.quit()
    sys.exit()


def game_loop():
    global current_riddle_index, user_answer, score

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time > game_duration or all(answers_submitted):
            game_ended()

        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (
                event.type == pygame.KEYDOWN
                and not answers_submitted[current_riddle_index]
            ):
                if event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    user_answer += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if (
                    check_button_click(mouse_pos, next_button)
                    and current_riddle_index < total_questions - 1
                ):
                    current_riddle_index += 1
                    user_answer = ""
                elif (
                    check_button_click(mouse_pos, previous_button)
                    and current_riddle_index > 0
                ):
                    current_riddle_index -= 1
                    user_answer = ""
                elif (
                    check_button_click(mouse_pos, submit_button)
                    and not answers_submitted[current_riddle_index]
                ):
                    answers_submitted[current_riddle_index] = True
                    correct = (
                        riddles[current_riddle_index]["answer"].lower()
                        == user_answer.lower()
                    )
                    if correct:
                        score += 1
                        show_popup_message("Correct!", GREEN)
                    else:
                        score -= 1
                        show_popup_message("Wrong!", RED)
                    user_answer = ""

        remaining_time = game_duration - elapsed_time
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        # Display riddle, user answer, score, and timer
        draw_text(
            f"Riddle {current_riddle_index + 1}/{total_questions} :",
            font,
            WHITE,
            screen,
            20,
            40,
        )
        draw_text(
            f"{riddles[current_riddle_index]['riddle']}", font, WHITE, screen, 20, 90
        )
        draw_text(f"Your answer: {user_answer}", font, WHITE, screen, 20, 150)
        draw_text(f"Score: {score}", font, WHITE, screen, screen_width - 200, 50)
        draw_text(
            f"Time left: {minutes}:{seconds:02}",
            font,
            WHITE,
            screen,
            screen_width - 200,
            20,
        )

        # Draw buttons
        if not answers_submitted[current_riddle_index]:
            draw_button(submit_button, "Submit", screen)
        if current_riddle_index < total_questions - 1:
            draw_button(next_button, "Next", screen)
        if current_riddle_index > 0:
            draw_button(previous_button, "Previous", screen)

        pygame.display.flip()


def check_button_click(mouse_pos, button):
    if button.collidepoint(mouse_pos):
        return True
    return False


game_loop()
