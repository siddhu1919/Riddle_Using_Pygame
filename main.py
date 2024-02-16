import random
import time

# Load riddles from text file
riddles = {}
riddles_ans = {
    "1. Riddle": "An echo",
    "2. Riddle": "Footsteps",
    "3. Riddle": "Pencil lead/graphite",
    "4. Riddle": "A keyboard",
    "5. Riddle": "A coffin",
    "6. Riddle": "Cloud",
    # Fill Yourself till 100
}

used_riddles = set()

with open(r"riddles_dataset_Debug.txt") as f: # Change it to "riddles_dataset" from "riddles_dataset_Debug" when you complete filing all the 100 entries riddles_ans {}.
    for line in f:
        parts = line.strip().split(":")
        if len(parts) == 2:
            riddle, answer = parts
            riddles[riddle] = answer
            
        else:
            # invalid line with no : separator
            continue


def get_random_riddle():
    # Select a random riddle key that hasn't been used yet
    available_riddles = list(set(riddles.keys()) - used_riddles)
    if not available_riddles:
        return None, None  # Return None if there are no more available riddles
    random_riddle_number = random.choice(available_riddles)
    riddle_text = riddles[random_riddle_number]
    used_riddles.add(random_riddle_number)  # Mark this riddle as used
    return random_riddle_number, riddle_text


def get_user_answer():
    user_answer = input("Your answer: ")
    return user_answer


def evaluate_answer(riddle, user_answer):
    correct_answer = riddles_ans.get(riddle)
    # print(riddles[riddle])
    return user_answer.lower() == correct_answer.lower()


score = 0


def update_score(is_correct):
    global score
    if is_correct:
        score += 1
    else:
        score -= 1


def play_game():
    global score
    while True:
        riddle_number, riddle = get_random_riddle()
        # print(riddle_number)
        print(f"{riddle}")
        

        user_answer = get_user_answer()
        is_correct = evaluate_answer(riddle_number, user_answer)

        update_score(is_correct)
        print("Your current score: {}".format(score))

        play_again = input("Do you want to play again? (yes/no): ")
        if play_again.lower() != "yes":
            break


play_game()
