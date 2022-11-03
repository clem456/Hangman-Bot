from hanging import Hanging

def check_letter(lives, letter, word):
    returned_string = ""

    if letter in word:
        pass
    else:
        lives -= 1

    return lives, returned_string
