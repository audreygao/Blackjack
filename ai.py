import copy
import random

from game import Game, states

HIT = 0
STAND = 1
DISCOUNT = 0.95 #This is the gamma value for all value calculations

class Agent:
    def __init__(self):

        # For MC values
        self.MC_values = {} # Dictionary: Store the MC value of each state
        self.S_MC = {}      # Dictionary: Store the sum of returns in each state
        self.N_MC = {}      # Dictionary: Store the number of samples of each state
        # MC_values should be equal to S_MC divided by N_MC on each state 

        # For TD values
        self.TD_values = {}  # Dictionary: Store the TD value of each state
        self.N_TD = {}       # Dictionary: Store the number of samples of each state

        # For Q-learning values
        self.Q_values = {}   # Dictionary: Store the Q-Learning value of each state and action
        self.N_Q = {}        # Dictionary: Store the number of samples of each state for each action

        # Initialization of the values
        for s in states:
            self.MC_values[s] = 0
            self.S_MC[s] = 0
            self.N_MC[s] = 0
            self.TD_values[s] = 0
            self.N_TD[s] = 0
            self.Q_values[s] = [0,0] # First element is the Q value of "Hit", second element is the Q value of "Stand"
            self.N_Q[s] = [0,0] # First element is the number of visits of "Hit" at state s, second element is the Q value of "Stand" at s

        # Game simulator
        self.simulator = Game()

    # fixed policy, need to perform MC and TD policy evaluation. 
    @staticmethod
    def default_policy(state):
        user_sum = state[0]
        user_A_active = state[1]
        actual_user_sum = user_sum + user_A_active * 10
        if actual_user_sum < 14:
            return 0
        else:
            return 1

    @staticmethod
    def alpha(n):
        return 10.0/(9 + n)
   
    def make_one_transition(self, action):
        if self.simulator.game_over():
            return None, None
        
        if action == HIT:
            self.simulator.act_hit()
        elif action == STAND:
            self.simulator.act_stand()
        return self.simulator.state, self.simulator.check_reward()
    
    # return the full trajectory in a list of (state, reward) pairs
    def make_full_trajectory(self):
        trajectory = []
        trajectory.append((self.simulator.state, self.simulator.check_reward()))

        while not self.simulator.game_over():
            action = self.default_policy(self.simulator.state)
            state, reward = self.make_one_transition(action)
            trajectory.append((state, reward))
        return trajectory

    # MC policy evaluation
    def MC_run(self, num_simulation, tester=False):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):

            if tester:
                self.tester_print(simulation, num_simulation, "MC")
            self.simulator.reset()  # The simulator is already reset for you for each new trajectory

            trajectory = self.make_full_trajectory()
            _, final_reward = trajectory[len(trajectory)-1]
            for i in range(len(trajectory)):
                state, _ = trajectory[i]
                reward_to_go = DISCOUNT**(len(trajectory)-i-1) * final_reward
                self.S_MC[state] += reward_to_go
                self.N_MC[state] += 1
                self.MC_values[state] = self.S_MC[state] / self.N_MC[state]
    
    # TD policy evaluation
    def TD_run(self, num_simulation, tester=False):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):

            if tester:
                self.tester_print(simulation, num_simulation, "TD")
            self.simulator.reset()

            curr_state = self.simulator.state
            curr_reward = self.simulator.check_reward()
            while curr_state is not None:
                action = self.default_policy(self.simulator.state)
                next_state, next_reward = self.make_one_transition(action)
                next_td = 0 if next_state is None else self.TD_values[next_state]
                self.TD_values[curr_state] += self.alpha(self.N_TD[curr_state]) * (curr_reward + DISCOUNT * next_td - self.TD_values[curr_state])
                self.N_TD[curr_state] += 1
                curr_reward = next_reward
                curr_state = next_state
                
    # Q-learning
    def Q_run(self, num_simulation, tester=False, epsilon=0.4):

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):

            if tester:
                self.tester_print(simulation, num_simulation, "Q")
            self.simulator.reset()

            curr_state = self.simulator.state
            curr_reward = self.simulator.check_reward()
            while curr_state is not None:
                action = self.pick_action(curr_state, epsilon)
                next_state, next_reward = self.make_one_transition(action)
                if next_state is None:
                    max_next_sa = 0
                else:
                    max_next_sa = max(self.Q_values[next_state])
                self.Q_values[curr_state][action] += self.alpha(self.N_Q[curr_state][action]) * (curr_reward + DISCOUNT * max_next_sa - self.Q_values[curr_state][action])
                self.N_Q[curr_state][action] += 1
                curr_reward = next_reward
                curr_state = next_state

    # epsilon-greedy policy
    def pick_action(self, s, epsilon):
        if random.uniform(0,1) < epsilon:
            return random.randint(0, 1)
        else:
            q_hit, q_stand = self.Q_values[s]
            return 0 if q_hit >= q_stand else 1

    def autoplay_decision(self, state):
        hitQ, standQ = self.Q_values[state][HIT], self.Q_values[state][STAND]
        if hitQ > standQ:
            return HIT
        if standQ > hitQ:
            return STAND
        return HIT #Before Q-learning takes effect, just always HIT

    def save(self, filename):
        with open(filename, "w") as file:
            for table in [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q]:
                for key in table:
                    key_str = str(key).replace(" ", "")
                    entry_str = str(table[key]).replace(" ", "")
                    file.write(f"{key_str} {entry_str}\n")
                file.write("\n")

    def load(self, filename):
        with open(filename) as file:
            text = file.read()
            MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text, _  = text.split("\n\n")
            
            def extract_key(key_str):
                return tuple([int(x) for x in key_str[1:-1].split(",")])
            
            for table, text in zip(
                [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q], 
                [MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text]
            ):
                for line in text.split("\n"):
                    key_str, entry_str = line.split(" ")
                    key = extract_key(key_str)
                    table[key] = eval(entry_str)

    @staticmethod
    def tester_print(i, n, name):
        print(f"\r  {name} {i + 1}/{n}", end="")
        if i == n - 1:
            print()
