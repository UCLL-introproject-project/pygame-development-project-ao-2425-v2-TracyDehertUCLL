import copy;
import random;
import pygame;
pygame.init()

#added suits to my cards:
suits = ['\u2663', '\u2665', '\u2666', '\u2660']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
cards = []

for suit in suits:
    for rank in ranks:
        cards.append([suit, rank])

card_value = cards[0]
decks = 2
WIDTH = 800
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack!')
fps = 60
timer = pygame.time.Clock()
font = pygame.font.SysFont('segoeui', 44)
small_font = pygame.font.SysFont('segoeui', 36)
active = False
#win, loss, draw
records = [0,0,0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False
results = ['', 'Player loses', 'Player wins', 'Dealer wins', 'Game tied']

#added sounds for victory, tie and loss into usable global variable
victory_sound = pygame.mixer.Sound('Project work/Victory.mp3')
tied_sound = pygame.mixer.Sound('Project work/Tied.mp3')
loss_sound = pygame.mixer.Sound('Project work/Loss.mp3')

#All the screen sizing has been adjusted for a bigger width and smaller heighth and also to look nice on my pc screen(might look wonky on other sizes)
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return(current_hand, current_deck)

def draw_scores(player, dealer):
    screen.blit(font.render(f'score[{player}]', True, 'white'), (500, 450))
    if reveal_dealer:
        screen.blit(font.render(f'score[{dealer}]', True, 'white'), (500, 170))

def draw_cards(player, dealer, reveal):
#added a string to be able to display both the suit and rank of my card
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [60 + (65 * i), 360 + (3 * i), 180, 270], 0, 5)
        screen.blit(font.render(f"{player[i][0]}{player[i][1]}", True, 'black'), (68 + 65 * i, 360 + 3 * i))
        screen.blit(font.render(f"{player[i][0]}{player[i][1]}", True, 'black'), (68 + 65 * i, 570 + 3 * i))
        pygame.draw.rect(screen, 'red', [60 + (65 * i), 360 + (3 * i), 180, 270], 5, 5)

    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [60 + (65 * i), 70 + (3 * i), 180, 270], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(f"{dealer[i][0]}{dealer[i][1]}", True, 'black'), (68 + 65 * i, 70 + 3 * i))
            screen.blit(font.render(f"{dealer[i][0]}{dealer[i][1]}", True, 'black'), (68 + 65 * i, 275 + 3 * i))
        else:
            screen.blit(font.render('?', True, 'black'), (70 + 65 * i, 70 + 3 * i))
            screen.blit(font.render('?', True, 'black'), (70 + 65 * i, 275 + 3 * i))
        pygame.draw.rect(screen, 'blue', [60 + (65 * i), 70 + (3 * i), 180, 270], 5, 5)

#adjusted entire code to accept my cards list and look at only the card rank for scoring
def calculate_score(hand):
    hand_score = 0
    aces_count = hand[1].count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i][1] == cards[j][1]:
                hand_score += int(hand[i][1])

        if hand[i][1] in ['10', 'J', 'Q', 'K']:
            hand_score += 10
        elif hand[i][1] == 'A':
            hand_score += 11

    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score     

def draw_game(act, record, result):
    button_list = []
    if not act:
        deal = pygame.draw.rect(screen, 'white', [225, 20, 350, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [225, 20, 350, 100], 3, 5)
        deal_text = font.render('Deal Hand', True, 'black')
        screen.blit(deal_text, (300, 40))
        button_list.append(deal)
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 650, 400, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 650, 400, 100], 3, 5)
        hit_text = font.render('Hit Me', True, 'black')
        screen.blit(hit_text, (140, 670))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [400, 650, 400, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [400, 650, 400, 100], 3, 5)
        stand_text = font.render('Stand', True, 'black')
        screen.blit(stand_text, (550, 670))
        button_list.append(stand)
        score_text = small_font.render(f'Wins:{record[0]}      Losses: {record[1]}    Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (150, 750))
        exit = pygame.draw.rect(screen, 'white', [500, 20, 200, 80], 0, 5)
        pygame.draw.rect(screen, 'green', [500, 20, 200, 80], 3, 5)
        #added exit button to game
        exit_text = small_font.render('Exit game', True, 'black')
        screen.blit(exit_text, (525, 35))
        button_list.append(exit)
    if result != 0:
        screen.blit(font.render(results[result], True, 'white'), (35, 1))
        deal = pygame.draw.rect(screen, 'white', [225, 280, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [225, 280, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [228, 283, 294, 94], 3, 5)
        deal_text = font.render('New Hand', True, 'black')
        screen.blit(deal_text, (275, 295))
        button_list.append(deal)
    return button_list    

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4
        if add:
            if result == 1 or result == 3:
                totals[1] += 1
                #added loss sound here
                loss_sound.play()
            if result == 2:
                totals[0] += 1
                #added victory sound here
                victory_sound.play()
            if result == 4:
                totals[2] += 1
                #added tied sound here
                tied_sound.play()
        add = False
    return result, totals, add


run = True
while run:
    timer.tick(fps)
    screen.fill('black')

    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * cards)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif buttons[2].collidepoint(event.pos):
                    pygame.quit()
                elif len(buttons) == 4:
                    if buttons[3].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * cards)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()