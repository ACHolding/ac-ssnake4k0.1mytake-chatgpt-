
# AC's Snake: My Take 0.2
# Atari-inspired menu, futuristic UI, no external files required.

import pygame, random, sys, math

pygame.init()

W,H=1280,720
screen=pygame.display.set_mode((W,H))
pygame.display.set_caption("AC's Snake: My Take 0.2")
clock=pygame.time.Clock()

BLACK=(8,10,18)
CYAN=(0,220,255)
WHITE=(255,255,255)
GREEN=(0,255,120)
RED=(255,80,80)

FONT_BIG=pygame.font.SysFont(None,80)
FONT_MED=pygame.font.SysFont(None,42)

menu=["START GAME","ABOUT","SETTINGS","EXIT"]
sel=0
state="menu"

GRID=20
snake=[(W//2,H//2)]
direction=(GRID,0)
food=(200,200)
score=0
snake_speed=8
timer=0
sound_on=True

def spawn_food():
    global food
    food=(random.randrange(0,W,GRID),random.randrange(0,H,GRID))

def reset():
    global snake,direction,score
    snake=[(W//2,H//2)]
    direction=(GRID,0)
    score=0
    spawn_food()

reset()

running=True
while running:
    dt=clock.tick(60)
    timer+=dt

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False

        if e.type==pygame.KEYDOWN:
            if state=="menu":
                if e.key==pygame.K_UP: sel=(sel-1)%len(menu)
                if e.key==pygame.K_DOWN: sel=(sel+1)%len(menu)
                if e.key==pygame.K_RETURN:
                    if sel==0:
                        reset()
                        state="game"
                    elif sel==1:
                        state="about"
                    elif sel==2:
                        state="settings"
                    else:
                        running=False

            elif state=="game":
                if e.key==pygame.K_ESCAPE: state="menu"
                if e.key==pygame.K_UP and direction!=(0,GRID): direction=(0,-GRID)
                if e.key==pygame.K_DOWN and direction!=(0,-GRID): direction=(0,GRID)
                if e.key==pygame.K_LEFT and direction!=(GRID,0): direction=(-GRID,0)
                if e.key==pygame.K_RIGHT and direction!=(-GRID,0): direction=(GRID,0)

            else:
                if e.key==pygame.K_ESCAPE: state="menu"
                if state=="settings" and e.key==pygame.K_SPACE:
                    sound_on=not sound_on

    screen.fill(BLACK)

    # futuristic background
    for x in range(0,W,40):
        pygame.draw.line(screen,(20,30,50),(x,0),(x,H))
    for y in range(0,H,40):
        pygame.draw.line(screen,(20,30,50),(0,y),(W,y))

    if state=="menu":
        title=FONT_BIG.render("AC'S SNAKE",True,CYAN)
        screen.blit(title,(W//2-title.get_width()//2,90))

        sub=FONT_MED.render("MY TAKE 0.2",True,WHITE)
        screen.blit(sub,(W//2-sub.get_width()//2,170))

        for i,item in enumerate(menu):
            color=CYAN if i==sel else WHITE
            txt=FONT_MED.render(("> " if i==sel else "  ")+item,True,color)
            screen.blit(txt,(W//2-150,280+i*60))

    elif state=="game":
        if timer>=1000//snake_speed:
            timer=0
            hx,hy=snake[0]
            nh=(hx+direction[0],hy+direction[1])

            if nh[0]<0 or nh[0]>=W or nh[1]<0 or nh[1]>=H or nh in snake:
                state="menu"
            else:
                snake.insert(0,nh)
                if nh==food:
                    score+=1
                    spawn_food()
                else:
                    snake.pop()

        pygame.draw.rect(screen,RED,(*food,GRID,GRID))
        for s in snake:
            pygame.draw.rect(screen,GREEN,(*s,GRID,GRID))

        screen.blit(FONT_MED.render(f"SCORE {score}",True,WHITE),(20,20))

    elif state=="about":
        lines=[
            "ATARI-STYLE MENU",
            "FUTURISTIC PS5-INSPIRED UI LOOK",
            "NO EXTERNAL FILES",
            "ESC TO RETURN"
        ]
        for i,l in enumerate(lines):
            screen.blit(FONT_MED.render(l,True,WHITE),(80,140+i*60))

    elif state=="settings":
        txt=f"SOUND: {'ON' if sound_on else 'OFF'}"
        screen.blit(FONT_MED.render(txt,True,WHITE),(80,140))
        screen.blit(FONT_MED.render("SPACE = TOGGLE",True,CYAN),(80,200))
        screen.blit(FONT_MED.render("ESC = BACK",True,WHITE),(80,260))

    pygame.display.flip()

pygame.quit()
