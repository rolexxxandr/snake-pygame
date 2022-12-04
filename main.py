import pygame
from random import randrange

RES = 600 #розмір екрану
SIZE = 30 #розмір 1 блоку змійки

x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE) #вибираємо рандомну точку, де заспавниться змія(старт, кінець, крок)
apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE) #вибираємо рандомну точку, де заспавниться яблуко(старт, кінець, крок)
stone = randrange(0, RES, SIZE), randrange(0, RES, SIZE) #вибираємо рандомну точку, де заспавниться камінь(старт, кінець, крок)
dirs = {'W' : True, 'A' : True, 'S' : True, 'D' : True}
length = 1 #довжина змійки
snake = [(x, y)] #оприділяємо змійку в вгляді списку координат, зараз вона має тільки координати голови
dx, dy = 0, 0 #напрямки руху
score = 0 #рахунок
fps = 10 #швидкість змійки

pygame.init() #ініціалізуємо модулі pygame
sc = pygame.display.set_mode([RES, RES]) #створюємо квадратне вікно 600х600 sc = screen
clock = pygame.time.Clock() #створюємо об'єкт класу Clock, шоб регулювати швидкість змійки
font_score = pygame.font.SysFont("Arial", 20, bold=True) #шрифт рахунку
font_speed = pygame.font.SysFont("Arial", 16, bold=False) #шрифт швидкостіa

while True:
    sc.fill(pygame.Color("black")) #на кожній ітерації будемо замальовувати фон чорним кольором
    #drawing snake, apple
    #намалюємо всі секції змійки, як квадрати зеленого кольору
    #викоритовуючи спискове включення(list comprehension) для короткого запису
    #в якому пройдемся по всім її координатам
    [(pygame.draw.rect(sc, pygame.Color("black"), (i, j, SIZE, SIZE))) for i, j in snake] #відображає контур
    [(pygame.draw.rect(sc, pygame.Color("green"), (i, j, SIZE-1, SIZE-1))) for i, j in snake] #відображає внутрішній квадрат
    #яблуко і камінь це такі ж самі квадрати, тільки червоного і сірого кольору
    pygame.draw.rect(sc, pygame.Color("red"), (*apple, SIZE, SIZE))
    pygame.draw.rect(sc, pygame.Color("grey"), (*stone, SIZE, SIZE))

    #show score
    render_score = font_score.render(f"SCORE: {score}", 1, pygame.Color("purple"))
    sc.blit(render_score, (5, 5)) #координати показника рахунку

    #show speed
    render_speed = font_speed.render(f"FPS: {fps}", 1, pygame.Color("orange"))
    sc.blit(render_speed, (5, 25)) #координати показника швидкості

    #snake movement
    x += dx * SIZE #її крок дорівнює відстані розміру її голови
    y += dy * SIZE
    snake.append((x, y)) #кожен крок змійки будемо добавляти в її список координат
    snake = snake[-length:] #робимо зріз, шоб змія не було бескінечна

    #eatting apple
    if snake[-1] == apple: #голова, це крайній елемент, коли вона = координатам яблука - змія з'їла яблуко
        apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE) #заново розіщаємо яблуко
        stone = randrange(0, RES, SIZE), randrange(0, RES, SIZE)  # заново розіщаємо камінь
        length += 1 #збільшуємо довжину змійки
        score += 1 #збільшуємо рахунок
        fps += 1 #підвищуємо швидкість змійки

    #eatting stone
    if snake[-1] == stone: #голова, це крайній елемент, коли вона = координатам яблука - змія з'їла яблуко
        if len(snake) == 1: #якшо змія має тільки голову і з'їла камінь - кінець гри
            break

        stone = randrange(0, RES, SIZE), randrange(0, RES, SIZE)  # заново розіщаємо камінь
        apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE) #заново розіщаємо яблуко
        length -= 1 #збільшуємо довжину змійки
        fps -= 1 #підвищуємо швидкість змійки
    #game over
    if x + SIZE < 0 or x > RES or y + SIZE < 0 or y > RES: #коли вийшли за границі
        break
    if len(snake) != len(set(snake)): #коли стукнулись в себе
        break

    pygame.display.flip() #обновляємо поверхність
    clock.tick(fps) #задаємо затримку для фпс

    #провірка на закриття
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    #control
    #необхідно получити інформацію, про всі нажаті клавіші
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and dirs['W']:
        dx, dy = 0, -1
        dirs = {'W': True, 'A': True, 'S': False, 'D': True} #не позволяє нажимати кнопку S
    elif key[pygame.K_a] and dirs['A']:
        dx, dy = -1, 0
        dirs = {'W': True, 'A': True, 'S': True, 'D': False} #не позволяє нажимати кнопку D
    elif key[pygame.K_s] and dirs['S']:
        dx, dy = 0, 1
        dirs = {'W': False, 'A': True, 'S': True, 'D': True} #не позволяє нажимати кнопку W
    elif key[pygame.K_d] and dirs['D']:
        dx, dy = 1, 0
        dirs = {'W': True, 'A': False, 'S': True, 'D': True} #не позволяє нажимати кнопку A
