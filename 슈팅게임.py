import pygame
from pygame.rect import*
import random

def restart(): #재시작 함수
    global GameOver, score
    GameOver = False
    score = 0 #점수 초기화
    for i in range(len(ufo)): #적 초기화
        recUfo[i].y = -1
    for i in range(len(atk)): #공격 초기화
        recAtk[i].y = -1
    pass

def eventProcess(): #키 이동에 대한 함수 생성
    for event in pygame.event.get(): #키를 누를 때 여러개 쌓여도 받으려고 for문
        if event.type == pygame.KEYDOWN: #키를 누르면 down 키를 떼면 up
            if event.key == pygame.K_ESCAPE: #esc누르면 게임 종료
                pygame.quit() 
            if event.key == pygame.K_LEFT:
                move.x = -1
            if event.key == pygame.K_RIGHT:
                move.x = +1
            if event.key == pygame.K_UP:
                move.y = -1
            if event.key == pygame.K_DOWN:
                move.y = +1
            if event.key == pygame.K_r:
                restart()
            if event.key == pygame.K_SPACE:
                makeAtk()

def movePlayer(): #플레이어 이동 함수
    if not GameOver: #게임오버이면 중지
        recPlayer.x += move.x
        recPlayer.y += move.y

    if recPlayer.x < 0: #화면 밖으로 넘어가지 않게 제한 설정
        recPlayer.x = 0
    if recPlayer.x > SCREEN_WIDTH - recPlayer.width:
        recPlayer.x = SCREEN_WIDTH - recPlayer.width
    
    if recPlayer.y < 0:
        recPlayer.y = 0
    if recPlayer.y > SCREEN_HEIGHT - recPlayer.height:
        recPlayer.y = SCREEN_HEIGHT - recPlayer.height
    
        
    SCREEN.blit(player, recPlayer)

def timeDelay500ms(): #적 생성 딜레이 생성 -> 적들이 퍼져서 생성
    global time_delay_500ms
    if time_delay_500ms > 5:
        time_delay_500ms = 0
        return True
    
    time_delay_500ms += 1
    return False

def makeUfo():  #적 랜덤 생성
    if GameOver: #게임오버이면 생성 중지
        return
    if timeDelay500ms():
        index = random.randint(0, len(ufo) - 1)
        if recUfo[index].y == -1:
            recUfo[index].x = random.randint(0, SCREEN_WIDTH)
            recUfo[index].y = 0


def moveUfo(): #적 이동 함수
    makeUfo()

    for i in range(len(ufo)):
        if recUfo[i].y == -1:
            continue

        if not GameOver: #게임오버이면 중지
            recUfo[i].y += 1
        if recUfo[i].y > SCREEN_HEIGHT:
            recUfo[i].y = 0

        SCREEN.blit(ufo[i], recUfo[i])

#적과 공격 충돌
def CheckCollisionAtk():
    global score, GameOver, recAtk
    if GameOver:
        return
    for rec in recUfo:
        if rec.y == -1:
            continue
        for recA in recAtk:

            if rec.top < recA.bottom \
                    and recA.top < rec.bottom \
                    and rec. left < recA.right \
                    and recA.left < rec.right: # 충돌 알고리즘
                rec.y = -1
                recA.y = -1
                score += 100 #상대 맞추면 점수 증가
                break


#공격함수
def makeAtk():  #공격 생성
    if GameOver: #게임오버이면 생성 중지
        return
    for i in range(len(atk)):
        if recAtk[i].y == -1:
            recAtk[i].x = recPlayer.x
            recAtk[i].y = recPlayer.y
            break

def moveAtk(): #공격 이동 함수

    for i in range(len(atk)):
        if recAtk[i].y == -1:
            continue

        if not GameOver: #게임오버이면 중지
            recAtk[i].y -= 1
        if recAtk[i].y < 0:
            recAtk[i].y = -1

        SCREEN.blit(atk[i], recAtk[i])

def CheckCollision(): #게임오버
    global score, GameOver
    if GameOver:
        return
    for rec in recUfo:
        if rec.y == -1:
            continue
        if rec.top < recPlayer.bottom \
            and recPlayer.top < rec.bottom \
            and rec. left < recPlayer.right \
            and recPlayer.left < rec.right: # 충돌 알고리즘
            print('충돌')
            GameOver = True
            break
    score += 1 #점수 초당 증가

def blink(): #게임오버시 텍스트 깜빡깜빡
    global time_delay_4sec, toggle
    time_delay_4sec += 1
    if time_delay_4sec > 40: #4초마다 깜빡임
        time_delay_4sec = 0
        toggle = ~toggle
    return toggle


def setText(): #좌상단 텍스트
    mFont = pygame.font.SysFont("arial", 17, True, False) #폰트 설정
    SCREEN.blit(mFont.render(f'SCORE : {score}', True, 'red'), (10, 10, 0, 0)) #텍스트 내용, 색, 위치 설정
    if GameOver and blink(): #게임오버시 텍스트 띄움
        mFont = pygame.font.SysFont("arial", 25, True, False)
        SCREEN.blit(mFont.render('!!!Game Over!!!', True, 'red'), (110, 280, 0, 0))
        SCREEN.blit(mFont.render('Press "R" to Restart', True, 'white'), (80, 300, 0, 0))

#변수 초기화
isActive = True
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
move = Rect(0, 0, 0, 0) #상하좌우 값
time_delay_500ms = 0
score = 0
GameOver = False
time_delay_4sec = 0 #blink에 쓸 변수
toggle = False

#스크린 생성
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #스크린 사이즈 설정
pygame.display.set_caption('Shooting Game!!') #맨위 타이틀 문자열 설정

#플레이어 생성
player = pygame.image.load('aeroplane.png') #플레이어 이미지 설정
player = pygame.transform.scale(player,(20, 30)) #플레이어 이미지 크기설정
recPlayer = player.get_rect()
recPlayer.centerx = (SCREEN_WIDTH/2) #플레이어 중앙 설정 x값
recPlayer.centery = (SCREEN_HEIGHT/2) #플레이어 중앙 설정 y값

#적 생성
ufo = [pygame.image.load('ufo.png') for i in range(45)] #적 이미지 설정과 갯수 설정
recUfo = [None for i in range(len(ufo))]
for i in range(len(ufo)):
    ufo[i] = pygame.transform.scale(ufo[i],(30, 30)) #적 이미지 크기설정
    recUfo[i] = ufo[i].get_rect()
    recUfo[i].y = -1

#공격 생성
atk = [pygame.image.load('missile.png') for i in range(3)] #플레이어 이미지 설정과 갯수 설정
recAtk = [None for i in range(len(atk))]
for i in range(len(atk)):
    atk[i] = pygame.transform.scale(atk[i],(10, 15)) #플레이어 이미지 크기설정
    recAtk[i] = atk[i].get_rect()
    recAtk[i].y = -1

#기타(이동)
clock = pygame.time.Clock() #화면 이동이 너무 빠르기 때문에 딜레이 생성

###반복
while isActive:
    #화면지움 (잔상이 남음)
    SCREEN.fill((0, 0, 0))
    #이벤트처리
    eventProcess()
    #플레이어 이동
    movePlayer()
    #적 생성 및 이동
    moveUfo()
    #공격 생성
    moveAtk()
    #적과 공격 충돌
    CheckCollisionAtk()
    #충돌 확인
    CheckCollision()
    #텍스트 업데이트(점수)
    setText()
    #화면 갱신
    pygame.display.flip() #창 띄우기
    clock.tick(100) #화면 이동이 너무 빠르기 때문에 딜레이 생성 밀리sec 단위