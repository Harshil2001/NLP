import sys
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

# Pre-Process the Text 
def preprocess(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens  = [t for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t)>5]
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))
    tags = nltk.pos_tag(lemmas_unique)
    print("_________________________________________________________________")
    print(tags[:20],"\n")
    
    nouns  = [word for word, tag in tags if tag.startswith('NN' or 'NNS' or 'NNP' or 'NNPS')]
    print("Number of Tokens are : ")
    print(len(tokens))
    print("Number of Nouns are : ")
    print(len(nouns))
    return tokens, nouns

# Guessig Game Function
def Guessing_game(list):
    score = 5
    seed(1234)
    # Generate a random index to select a word
    random_index = randint(0, 49)  # Indices range from 0 to 49 for a list of 50 items
    # Select the word using the random index
    word = list[random_index]
    print(len(word))
    display = ['_'] * len(word)
    print(" ".join(display))

    while score >= 0:  # The game continues as long as the score is positive
        guess = input(" Guess a letter or '!' to quit: ").lower()
        if guess == '!':
            print("Game over. Your final score is:", score)
            break

        if guess == '':
            print("You didn't enter anything, Please Try Again !!!")

        elif guess in word:
            print("Right!")
            score += 1
            if guess == word:
                print("Congratulations, you've solved it!")
                print("Your Current Score is : ",score, '\n')
                print('Guess the another word')
                Guessing_game(list)
                break
                
            # Reveal the guessed letters
            for i, letter in enumerate(word):
                if letter == guess:
                    display[i] = guess
        else:
            print("Sorry, guess again.")
            score -= 1

        print(" ".join(display))
        print(f"Your score: {score}")

        # Check if the word has been fully guessed
        if '_' not in display:
            print("Congratulations, you've solved it!")

            print("Your Current Score is : ",score, '\n')
            print('Guess the another word')
            Guessing_game(list)
            break

        # End the game if the score is negative
        if score < 0:
            print("Game over. Your final score is:", score)
            break

def main(filename):
    
    # Main Function
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            
            # Open and Read the file
            raw_text = file.read()

            # Calculating the Lexical Diversity
            tokens = word_tokenize(raw_text)
            unique_tokens = set(tokens)                            # Unique Tokens
            lexical_diversity = len(unique_tokens) / len(tokens)   # Lexical Diversity 
    
            # Printing the result to 2 decimal points
            print(f"Lexical Diversity: {lexical_diversity:.2f}")
            
            # Pre-Process the Raw_text
            tokens, nouns = preprocess(raw_text)
            
            # Creating a Dictionary 
            Dict = {}
            for noun in set(nouns):
                Dict[noun] = tokens.count(noun)
            sorted_dict = sorted(Dict.items(), key=lambda x: x[1], reverse=True)[:50]

            # Printing 50 most common nouns and their respective counts
            for noun, count in sorted_dict:
                print(f"{noun}: {count}")
            sorted_list = [word for word, count in sorted_dict]
       
            # Guessing Game
            Guessing_game(sorted_list)
            
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No filename provided.")
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)