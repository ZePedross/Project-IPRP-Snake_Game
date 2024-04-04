import time
import random
import functools
import turtle

MAX_X = 600
MAX_Y = 800
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'high_scores.txt'
# Controla a velocidade da cobra. Quanto menor o valor, mais rápido é o movimento da cobra.
SPEED = 0.1


def load_high_score(state):
    # se já existir um high score devem guardar o valor em state['high_score']
    l=[]
    f = open(HIGH_SCORES_FILE_PATH,'r')
    for i in f:
        l.append(i)
    if len(l)>0:
        a = int(max(l))
        state['high_score'] = a
    
def write_high_score_to_file(state):
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    f= open(HIGH_SCORES_FILE_PATH,'a')   
    f.write(str(state['high_score']) + "\n")
    f.close()

def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.2)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)

def update_score_board(state):
    if (state['score']) >= (state['high_score']):
        state['new_high_score'] = True
    state['score_board'].clear()
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], state['high_score']), align="center", font=("Helvetica", 24, "normal"))

def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'

def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'

def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'

def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'

def init_state():
    state = {}
    # Informação necessária para a criação do score board
    state['score_board'] = None
    state['new_high_score'] = False
    state['high_score'] = 0
    state['score'] = 0
    # Para gerar a comida deverá criar um nova tartaruga e colocar a mesma numa posição aleatória do campo
    state['food'] = None
    state['window'] = None
    snake = {
        'head': None,                  # Variável que corresponde à cabeça da cobra
        'current_direction': None,     # Indicação da direcção atual do movimento da cobra
        'body':[]
    }
    state['snake'] = snake
    return state

def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)
    state['window'] = window
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('green')
    create_score_board(state)
    create_food(state)
    

def move(state):
    ''' 
    Função responsável pelo movimento da cobra no ambiente.
    '''
    snake = state['snake']
    
        
    for i in range(len(snake['body'])-1,0,-1):
        snake['body'][i].goto(snake['body'][i-1].position())
    if len(snake['body']) > 0:    
        snake['body'][0].goto(snake["head"].position())
        
       
    if state['snake']['current_direction'] =='up':
        snake=state["snake"]
        snake["head"].seth(90)
        snake["head"].fd(DEFAULT_SIZE)
    
    elif state['snake']['current_direction'] =='down':
        snake=state["snake"]
        snake["head"].seth(-90)
        snake["head"].fd(DEFAULT_SIZE)        
  
    elif state['snake']['current_direction'] =='left':
        snake=state["snake"]
        snake["head"].seth(180)
        snake["head"].fd(DEFAULT_SIZE)        
        
    elif state['snake']['current_direction'] =='right':
        snake=state["snake"]
        snake["head"].seth(0)
        snake["head"].fd(DEFAULT_SIZE)     

    

def create_food(state):
    ''' 
        Função responsável pela criação da comida. Note que elas deverão ser colocadas em posições aleatórias, mas dentro dos limites do ambiente.
    '''
    # a informação sobre a comida deve ser guardada em state['food']
    snake=state["snake"]
    
    x=random.randint(-280,280)
    y=random.randint(-280,280)
        
    for i in range(len(snake["body"])-1):
        if (snake["body"][i].xcor()== x or snake["body"][i].ycor()== y or snake["head"].xcor()== x or snake["head"].ycor()== y):
            x=random.randint(-280,280)
            y=random.randint(-280,280)
            
    snake=state["snake"]
    food=turtle.Turtle()
    food.shape("circle")
    food.color("red")
    food.up()
    food.goto(x,y)        
    food.down()
    state["food"]=food
    move(state)
    
def body_grow(state):
    snake=state['snake']
    bodyp=turtle.Turtle()
    bodyp.shape("square")
    bodyp.color("black")
    bodyp.pu()
    snake['body'].append(bodyp) 

def check_if_food_to_eat(state):
    ''' 
        Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida estiver a uma distância inferior a 15 pixels a cobra pode comer a peça de comida. 
    '''
    snake=state['snake']
    food =state['food']
    if (snake['head'].distance(food)<=15):
        food.ht()
        state['score']=state['score']+10
        if state['score'] > state['high_score']:
            state['high_score'] = state['score']
        update_score_board(state)
        create_food(state)
        body_grow(state)
        
             
        
    # para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do state: state['high_score'], state['score'] e state['new_high_score']

def boundaries_collision(state):
    ''' 
        Função responsável por verificar se a cobra colidiu com os limites do ambiente. Sempre que isto acontecer a função deverá returnar o valor booleano True, caso contrário retorna False.
    '''
    snake=state["snake"] 
    if (snake["head"].xcor()>300 or snake["head"].xcor()<-300):
        return True
    elif (snake["head"].ycor()>400 or snake["head"].ycor()<-400):
        return True    
    for i in range(len(snake["body"])-1):     
        if (snake["body"][i].xcor()>300 or snake["body"][i].xcor()<-300):  
            return True
        elif (snake["body"][i].ycor()>400 or snake["body"][i].ycor()<-400):
            return True
        
        
def check_collisions(state):
    '''
        Função responsável por avaliar se há colisões. Atualmente apenas chama a função que verifica se há colisões com os limites do ambiente. No entanto deverá escrever o código para verificar quando é que a tartaruga choca com uma parede ou com o seu corpo.
    '''
    snake = state['snake']
    for i in range(len(snake["body"])-1):
        if (snake['head'].distance(snake["body"][i])<=5):
            return True
             
    return boundaries_collision(state)

def main():
    state = init_state()
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        move(state)
        time.sleep(SPEED) 
    print("YOU LOSE!")
    if state['new_high_score']:
        write_high_score_to_file(state)
        
main()

turtle.exitonclick()