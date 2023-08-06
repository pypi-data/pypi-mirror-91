import random
import words

def get_easy_tf():
    return random.choice(words.easy)

def get_easy_t():
    return random.choice(get_easy_tf())

print(get_easy_tf())
