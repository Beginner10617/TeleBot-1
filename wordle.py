import requests

def get_random_word():
    url = "https://random-word-api.herokuapp.com/word?number=1&length=5"
    response = requests.get(url)
    
    if response.status_code == 200:
        words = response.json()
        if words:
            return words[0]  # Get the first word from the response
    return None

def is_valid_word(word):
    # Not working
    url = f"https://api.datamuse.com/words?sp={word}&max=1"
    response = requests.get(url)
    if response.status_code == 200:
        words = response.json()
        if words:  # If we get a result, the word is valid
            return True
    return False

def response(Word : str, Guess : str):
    guess = Guess.lower()
    word = Word.lower()
    if is_valid_word(guess) == False:
        return "Invalid guess"
    if len(guess) != 5:
        return "Invalid guess"
    if guess == word:
        return False
    letterCount = {}
    for i in set(word):
        letterCount[i] = word.count(i)
    output = ""
    for i in range(5):
        if guess[i] in letterCount:
            if letterCount[guess[i]] > 0:
                letterCount[guess[i]] -= 1
                if guess[i] == word[i]:
                    # If the letter is in the word and in the correct position
                    output += "G"
                elif guess[i] in word:
                    # If the letter is in the word but in the wrong position
                    output += "Y"
            else:
                # If the letter is in the word but already used
                output += "R"
        else:
            # If the letter is not in the word
            output += "R"
    return output

if __name__ == "__main__":
    word = get_random_word()
    print("Word:", word)
    Response = True
    while Response:
        guess = input("Enter your guess: ")
        print(is_valid_word(guess))
        Response = response(word, guess)
        if Response:print(Response)
        else:print("You guessed the word!")