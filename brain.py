from collections import Iterable

import numpy as np


#  discrete action, 2 continuous state
class Brain:
    def __init__(self,action_n):
        self.action_n = action_n
        self.greedy = 0.0
        self.q = QTable()

    def pi(self, s):
        s = list(s)
        if self.greedy < np.random.rand():
            q_value = np.zeros(shape=[self.action_n])
            for a in range(self.action_n):
                s_a = s+[a]
                s_a = tuple(s_a)
                q_value[a] = self.q.q(s_a)

            a = np.argmax(q_value)
            # print('s ', s, ' a ', a, ' q_value ', q_value)
            bool_arr = (q_value == q_value[a])
            if np.sum(bool_arr) > 1:
                a = np.random.choice(range(self.action_n))
            else:
                pass
        else:
            a = np.random.choice(range(self.action_n))
        # print(a)
        return int(a)


class QTable:
    def __init__(self):
        # state: up down left right apple_dir action
        #         2*   2*   2*    2*        4*     4
        self.q_table = np.zeros([2, 2, 2, 2, 4, 4])

    def q(self, s_a):

        return self.q_table[s_a]

    def q_improve(self, s_a, r, s_a_):
        alpha = 0.001
        gamma = 1.0

        q_ = self.q(s_a) + alpha * (r + gamma * self.q(s_a_) - self.q(s_a))
        self.q_table[s_a] = q_
