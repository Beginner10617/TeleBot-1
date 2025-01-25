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
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        words = response.json()
        if words:  # If we get a result, the word is valid
            return True
    elif response.status_code == 404:
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
    output = [""] * 5
    Indexes = [i for i in range(5)]
    for i in range(5):
        if guess[i] == word[i]:
            output[i] = 'G'
            Indexes.remove(i)
            letterCount[guess[i]] -= 1
    for i in Indexes:
        if guess[i] in word:
            if letterCount[guess[i]] > 0:
                output[i] = 'Y'
                letterCount[guess[i]] -= 1
            else:
                output[i] = 'R'
        else:
            output[i] = 'R'
    return output

if __name__ == "__main__":
    word = get_random_word()
    while not is_valid_word(word):
        word = get_random_word()
    print("Word:", word)
    Response = True
    while Response:
        guess = input("Enter your guess: ")
        Response = response(word, guess)
        if Response:print(Response)
        else:print("You guessed the word!")
        