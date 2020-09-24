from mechanism import ENVIRONMENT
from brain import Brain
import pygame
import time


pygame.init()
window_size = [800, 800]
win = pygame.display.set_mode(tuple(window_size))
pygame.display.set_caption("greedy snake Game")
DRAW = True

agent = Brain(4)


for i_episode in range(999999):

    max_len=0

    env_size = [20, 20]
    env = ENVIRONMENT(tuple(env_size))
    x_scaling = window_size[0] / env_size[0]
    y_scaling = window_size[1] / env_size[1]
    for i_step in range(999999):

        if i_episode % 100 == 0:
            DRAW = True
        if DRAW:
            time.sleep(0.01)
            pygame.event.get()

            width = x_scaling
            height = y_scaling

            win.fill((0, 0, 0))  # Fills the screen with black
            for i in range(env_size[0]):
                for j in range(env_size[1]):
                    x = i*x_scaling
                    y = j*x_scaling
                    if env.env[i, j] == 1:
                        pygame.draw.rect(win, (128, 128, 125), (y, x, width, height))
                    if env.env[i, j] == 0:
                        pygame.draw.rect(win, (0, 0, 0), (y, x, width, height))
                    if env.env[i, j] == 2:
                        pygame.draw.rect(win, (255, 0, 0), (y, x, width, height))
                    if env.env[i, j] == 3:
                        pygame.draw.rect(win, (0, 255, 0), (y, x, width, height))
            pygame.display.update()



        # env.show_env()
        s=env.get_s()
        a = agent.pi(s)
        alive,r = env.step(a)
        if env.snake.length > max_len:
            max_len = env.snake.length
        # print('reward',r)
        s_=env.get_s()
        a_=agent.pi(s_)
        if not alive or env.count>=100 :
            env = ENVIRONMENT(tuple(env_size))
            s_ = env.get_s()
            a_ = agent.pi(s_)

        s_a = list(s)+[a]
        s_a = tuple(s_a)
        s_a_ = list(s_)+[a_]
        s_a_ = tuple(s_a_)
        agent.q.q_improve(s_a,r,s_a_)

        if not alive or env.count>=100:
            break
    if i_episode % 10 == 0:
        print('episode ',i_episode,' max length',max_len)

    DRAW = False