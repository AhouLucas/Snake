import pygame as pg
import random as rd

pg.init()
width,height = 600,600
win = pg.display.set_mode((width,height))
running = True
FPS = 15
pg.display.update()
pg.display.set_caption("Snake")
scale = 20

score = 0   #Score text
highScore = 0
scoreFont = pg.font.Font(None, 30)
scoreText = scoreFont.render('Score ' + str(score), True,(255,255,255),(0))
scoreTextRect = scoreText.get_rect()
scoreTextRect.center = (50,50)
highScoreText = scoreFont.render('HIGH SCORE ' + str(highScore), True, (255,0,0),(0))
highScoreTextRect = highScoreText.get_rect()
highScoreTextRect.center = (width/2, height/2 + 100)

end = False #Restart Text
restartFont = pg.font.Font(None, 45)
restartText = restartFont.render("'Press any key to restart'", True,(255,255,255),(0))
restartTextRect = restartText.get_rect()
restartTextRect.center = (width/2,height/2)


class square():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        return

    def display(self):
        pg.draw.rect(win, (255,255,255), pg.Rect(self.x, self.y, scale, scale))


Left, Right, Up, Down = False, True, False, False

snake = [square(width/2, height/2), square(width/2 + scale, height/2), square(width/2 + 2*scale, height/2)]  #The actual snake, the head is the last element from the array of square
appleX, appleY = rd.randint(5, (width-40)/scale)*scale, rd.randint(5, (height-20)/scale)*scale

def move():
    global Left, Right, Up, Down
    keysPressed = pg.key.get_pressed()
    if keysPressed[pg.K_z] and Down == False:     #Going Up if 'z' is pressed
        Left = False
        Right = False
        Down = False
        Up = True
    if keysPressed[pg.K_d] and Left == False:     #Going Right if 'd' is pressed
        Left = False
        Up = False
        Down = False
        Right = True
    if keysPressed[pg.K_s] and Up == False:     #Going Down if 's' is pressed
        Left = False
        Right = False
        Up = False
        Down = True
    if keysPressed[pg.K_q] and Right == False:     #Going Left if 'q' is pressed
        Up = False
        Right = False
        Down = False
        Left = True

    if Up:
        snake.append(square(snake[len(snake)-1].x, snake[len(snake)-1].y - scale))  #add a new square above the previous head
    if Down:
        snake.append(square(snake[len(snake)-1].x, snake[len(snake)-1].y + scale))  #add a new square below the previous head
    if Right:
        snake.append(square(snake[len(snake)-1].x + scale, snake[len(snake)-1].y))  #add a new square on the right of the previous head
    if Left:
        snake.append(square(snake[len(snake)-1].x - scale, snake[len(snake)-1].y)) #add a new square on the left of the previous head
    snake.pop(0)

def collision():
    global running, appleX, appleY, Left, Right, Up, Down,score, highScore, end

    if snake[len(snake)-1].x <= 0 or snake[len(snake)-1].x >= width or snake[len(snake)-1].y <= 0 or snake[len(snake)-1].y >= height:   #End the game if you collide into the wall
        end = True 

    if snake[len(snake)-1].x == appleX and snake[len(snake)-1].y == appleY: #Eating an apple makes the snake one square bigger
        score += 1
        if score > highScore:
            highScore = score
        for i in snake:
            if appleX == i.x and appleY == i.y:
                appleX = rd.randint(5, (width-40)/scale)*scale
                appleY = rd.randint(5, (height-40)/scale)*scale
        if Left:
            snake.insert(0, square(snake[0].x + scale, snake[0].y))
        if Right:
            snake.insert(0, square(snake[0].x - scale, snake[0].y))
        if Up:
            snake.insert(0, square(snake[0].x, snake[0].y + scale))
        if Left:
            snake.insert(0, square(snake[0].x, snake[0].y - scale))
    for i in snake:
            if appleX == i.x and appleY == i.y:
                appleX = rd.randint(5, (width-40)/scale)*scale
                appleY = rd.randint(5, (height-40)/scale)*scale
    for i in range(len(snake)-1):
        if snake[len(snake)-1].x == snake[i].x and snake[len(snake)-1].y == snake[i].y:
            end = True 

def show():
    scoreText = scoreFont.render('Score ' + str(score), True,(255,255,255),(0))
    win.fill((0))
    win.blit(scoreText, scoreTextRect)
    pg.draw.rect(win, (255,0,0), pg.Rect(appleX, appleY, scale, scale)) #Draws the apple
    for i in snake:
        i.display()
    pg.display.update()


def restartGame():
    global end, score, snake, appleX, appleY, Left, Right, Up, Down
    if(end == True):
        pg.time.delay(500)
        highScoreText = scoreFont.render('HIGH SCORE ' + str(highScore), True, (255,0,0),(0))
        win.fill((0))
        win.blit(restartText, restartTextRect)
        win.blit(highScoreText, highScoreTextRect)

        pg.display.update()
        event = pg.event.wait()
        if event.type == pg.KEYDOWN:
            score = 0
            snake = [square(width/2, height/2), square(width/2 + scale, height/2), square(width/2 + 2*scale, height/2)]  
            appleX = rd.randint(5, (width-40)/scale)*scale
            appleY = rd.randint(5, (height-20)/scale)*scale
            Left = False
            Right = True
            Up = False 
            Down = False 
            pg.time.delay(200)
            end = False

def main():
    global running,end 
    clock = pg.time.Clock()
    while running:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                 running = False
        restartGame()
        if end == False: 
            move()
            show()
            collision()
        
    if running == False:
        pg.quit()



if __name__ == '__main__':
    main()