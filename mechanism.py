import numpy as np


class ENVIRONMENT:
    def __init__(self, size):
        length = size[0]
        width = size[1]
        self.length = length
        self.width = width
        self.table = np.ones([length, width], dtype=int)
        self.table[2:-2, 2:-2] = 0
        self.snake = SNAKE([5, 5])
        self.prey_location = [5, 6]
        self.env = self.table
        self.renew_env()
        self.prey_renew()
        self.snake_renew()
        self.count = 0


    def step(self, action):
        self.count += 1
        tile_temp = self.snake.move(action)
        reward = 0
        if self.snake.alive:
            self.snake.alive = self.if_alive()
        if self.snake.eat_success(self.prey_location):
            self.prey_renew()
            self.snake.grow(tile_temp)
            self.count = 0
            reward = 30
        self.renew_env()

        if not self.snake.eat_success(self.prey_location):
            # reward = reward-1
            pass
        if not self.snake.alive:
            self.count = 0
            reward = reward-100

        return self.snake.alive, reward

    def prey_renew(self):
        loc = np.where(self.env == 0)
        loc = np.transpose(loc)
        index = np.random.randint(0, len(loc))
        self.prey_location = loc[index]
    def snake_renew(self):
        loc = np.where(self.env == 0)
        loc = np.transpose(loc)
        index = np.random.randint(0, len(loc))
        self.snake.body_location[0] = loc[index]

    def renew_env(self):
        table = np.copy(self.table)
        for i in range(self.snake.length):
            table[tuple(self.snake.body_location[i])] = 1
        table[tuple(self.prey_location)] = 3
        self.env = table

    def if_alive(self):
        if self.snake.bite_self():
            return False
        for i in range(self.snake.length):
            if self.table[tuple(self.snake.body_location[i])] == 1:
                return False
        else:
            return True

    def show_env(self):
        # table = np.copy(self.table)
        # for i in range(self.snake.length):
        #     table[tuple(self.snake.body_location[i])] = 2
        # table[tuple(self.prey_location)] = 3
        print(self.env)

    def get_s(self):
        loc = self.snake.body_location[0]
        loc_up = (loc[0]-1,loc[1])
        loc_down = (loc[0]+1,loc[1])
        loc_left = (loc[0],loc[1]-1)
        loc_right = (loc[0],loc[1]+1)
        s1=0
        s2=0
        s3=0
        s4=0
        if self.env[loc_up] ==1:s1=1
        if self.env[loc_down] ==1:s2=1
        if self.env[loc_left] ==1:s3=1
        if self.env[loc_right] ==1:s4=1
        loc_prey = self.prey_location
        x_dir = loc_prey[0]-loc[0]
        y_dir = loc_prey[1]-loc[1]
        if abs(x_dir)>abs(y_dir):
            if x_dir <0:
                s5=0
            else:
                s5=1
        else:
            if y_dir <0:
                s5=2
            else:
                s5=3
        return (s1,s2,s3,s4,s5)


class SNAKE:
    # location: example (5,6)
    def __init__(self, location):
        self.length = 1
        self.body_location = [location]  # example:[(1,3),(1,2),(1,1)]
        self.alive = True

    # up:8 down:2 right:4 left:6
    # return tile location befor move
    def move(self, action):
        tile_location_before_move = self.body_location[-1]
        action = int(action)
        next_location = np.copy(self.body_location[0])
        if action == 0:
            next_location[0] -= 1
        if action == 1:
            next_location[0] += 1
        if action == 2:
            next_location[1] -= 1
        if action == 3:
            next_location[1] += 1

        if self.length > 1:
            if all(self.body_location[1] == next_location):
                self.alive = False

        for i in range(1, self.length):
            self.body_location[-i] = np.copy(self.body_location[-(i + 1)])
        self.body_location[0] = next_location
        return tile_location_before_move

    def grow(self, grow_location):
        self.length += 1
        self.body_location.append(grow_location)

    def eat_success(self, prey_location):
        if all(self.body_location[0] == prey_location):
            return True
        else:
            return False

    def bite_self(self):
        for i in range(1, self.length):
            if all(self.body_location[0] == self.body_location[i]):
                return True
        else:
            return False


if __name__ == '__main__':
    env = ENVIRONMENT(10, 10)
    while True:

        env.show_env()
        action = int(input())
        alive = env.step(action)
        if not alive:
            break
