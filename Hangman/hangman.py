import pygame
import math
import random
import words

pygame.init()
WIDTH, HEIGHT = 800, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")
WINDOW_COLOR = (187, 151, 201)
BLACK = (0, 0, 0)
LIGHTBLUE = (61, 94, 78)
WHITE = (255, 255, 255)
FPS = 60

#fonts
LETTER_FONT = pygame.font.SysFont('comicSans', 18)
LETTER_FONT2 = pygame.font.SysFont('comicSans', 30)

#load images
images = []
for i in range(7):
    image = pygame.image.load(str(i) + ".jpg")
    image = pygame.transform.smoothscale(image, (110, 175))
    images.append(image); 
print(images)

# game variables
hangman_status = 0
guessed = []

#button variables
RADIUS = 15
GAP = 15
A = 65
letters_conso = []
letters_vowels = []
startxConso = round(WIDTH * .02)
startyConso = HEIGHT - 150
startxVowel = round(WIDTH * .7)
counterC = 1
counterV = 1
for i in range(26):
    if A + i == 65 or A + i == 69 or A + i == 73 or A + i == 79 or A + i == 85:
        x = startxVowel + ((2 * RADIUS + GAP) * (counterV % 3))
        y = startyConso + (counterV // 3) * (2 * GAP + RADIUS)
        letters_vowels.append([x, y, chr(A + i), True])
        counterV += 1

    else:
        x = startxConso + ((2 * RADIUS + GAP) * (counterC % 11))
        y = startyConso + (counterC // 11) * (2 * GAP + RADIUS)
        letters_conso.append([x, y, chr(A + i), True])
        counterC += 1


def get_valid_word(words):
    word = random.choice(words)
    while "-" in word or ' ' in word:
        word = random.choice(words)
    return word


word = get_valid_word(words.word3)

def drawWindow(): 
    WINDOW.fill(WINDOW_COLOR)

    #draw title
    text = LETTER_FONT2.render("HANGING WITH HANGMAN", 1, BLACK)
    WINDOW.blit(text, (150, 20))

    #draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = LETTER_FONT2.render(display_word, 1, BLACK)
    WINDOW.blit(text, (50, 150))



    text = LETTER_FONT.render("CONSONANTS", 1, BLACK)
    WINDOW.blit(text, (startxConso * 10 ,HEIGHT - 220))
    text = LETTER_FONT.render("VOWELS", 1, BLACK)
    WINDOW.blit(text, (startxVowel + 20 ,HEIGHT - 220))
    for letter in letters_conso:
        x, y, let, visible = letter
        if visible:
            pygame.draw.circle(WINDOW, BLACK, (x + RADIUS/2, y + RADIUS), RADIUS, 2)
            text = LETTER_FONT.render(let, 1, BLACK)
            WINDOW.blit(text, (x, y))
    for letter in letters_vowels:
        x, y, let, visible = letter
        if visible: 
            pygame.draw.circle(WINDOW, LIGHTBLUE, (x + RADIUS/2, y + RADIUS), RADIUS, 2)
            text = LETTER_FONT.render(let, 1, BLACK)
            WINDOW.blit(text, (x, y))
    WINDOW.blit(images[hangman_status], (450, 70))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    WINDOW.fill(WHITE)
    text = LETTER_FONT2.render(message, 1, BLACK)
    WINDOW.blit(text, (WIDTH / 2 - 100, HEIGHT / 2 - 50))
    text = LETTER_FONT.render(word, 1, BLACK)
    WINDOW.blit(text, (WIDTH / 2 - 50 , HEIGHT / 2 + 50))
    pygame.display.update()
    pygame.time.delay(3000)



def main():
    clock = pygame.time.Clock();
    run = True
    global hangman_status
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters_conso:
                    x, y, let, visible = letter
                    if visible: 
                        dis = math.sqrt((x+ RADIUS/2 - m_x) ** 2 + (y + RADIUS - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(let)
                            if let not in word:
                                hangman_status += 1
                for letter in letters_vowels:
                    x, y, let, visible = letter
                    if visible: 
                        dis = math.sqrt((x+ RADIUS/2 - m_x) ** 2 + (y + RADIUS - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(let)
                            if let not in word:
                                hangman_status += 1
        drawWindow()

        winner = True
        for letter in word:
            if letter not in guessed:
                winner = False
                break
        
        if winner:
            display_message("YOU WON!")
            break
        
        if hangman_status == 6:
            display_message("YOU LOST")

            break

            
    pygame.quit()

if __name__ == "__main__":
    main()
