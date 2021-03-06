#!/usr/bin/python3

import sys
import os
import random
import math

import numpy as np
import operator

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0


class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior      = np.array([0.5, 0.5])
        self.transition = np.array([[0.999, 0.001], [0.01, 0.99]])
        self.emission   = np.array([{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                                    {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}])

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code
        states = [0,1]
        m = [{}]

        for i, st in enumerate(states):
            m[0][st] = {"P": np.log(self.prior[i]) + np.log(self.emission[i][sequence[0]]), "prev":None}

        for t in range(1, len(sequence)):
            m.append({})
            for i, st in enumerate(states):
                maxProb = max(m[t-1][prevState]["P"] + np.log(self.transition[j][i]) for j, prevState in enumerate(states))

                for k,prev in enumerate(states):
                    if maxProb == m[t-1][prev]["P"] + np.log(self.transition[k][i]):
                        max_prob = maxProb + np.log(self.emission[i][sequence[t]])
                        m[t][st] = {"P":max_prob, "prev":prev}
                        break

        path = []
        max_prob = max(value["P"] for value in m[-1].values())
        previous = None
        for st, data in m[-1].items():
            if data["P"] == max_prob:
                path.append(st)
                previous = st
                break

        for t in range(len(m) - 2, -1, -1):
            path.insert(0, m[t + 1][previous]["prev"])
            previous = m[t + 1][previous]["prev"]

        return path
        # End your code
        ###########################################


    def log_sum(self, factors):
        if abs(min(factors)) > abs(max(factors)):
            a = min(factors)
        else:
            a = max(factors)

        total = 0
        for x in factors:
            total += math.exp(x - a)
        return a + math.log(total)

    # - sequence: String with characters [A,C,T,G]
    # return: posterior distribution. shape should be (len(sequence), 2)
    # Please use log_sum() in posterior computations.
    def posterior(self, sequence):
        ###########################################
        # Start your code
        states = [0,1]

        f = np.zeros([len(sequence), len(states)])
        for i in states:
            f[0][i] = np.log(self.prior[i]) + np.log(self.emission[i][sequence[0]])
        
        for t in range(1,len(sequence)):
            for i in range(len(states)):
                f[t][i] = self.log_sum([ np.log(self.emission[i][sequence[t]]) + np.log(self.transition[j][i]) + f[t-1][j] for j in states])

        #print(f)

        b = np.zeros([len(sequence), len(states)])
        
        for i in states:
            b[-1][i] = np.log(1)
    

        for i in states:
            b[-2][i] = np.log(1) + np.log(self.emission[i][sequence[-1]])

        for t in range(-3,-len(sequence)-1,-1):
            for i in range(len(states)):
                b[t][i] = self.log_sum([ np.log(self.emission[i][sequence[t+1]]) + np.log(self.transition[i][j]) + b[t+1][j] for j in states])


        print(b)

        prob = np.zeros([len(sequence), len(states)])
        alpha = 1/(self.log_sum(f[:][-1]))

        for i in range(len(sequence)):
            for j in states:
                prob[i][j] = f[i][j] * b[i][j] * alpha


        return prob
        # End your code
        ###########################################


    # Output the most likely state for each symbol in an emmision sequence
    # - sequence: posterior probabilities received from posterior()
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def posterior_decode(self, sequence):
        nSamples  = len(sequence)
        post = self.posterior(sequence)
        best_path = np.zeros(nSamples)
        for t in range(nSamples):
            best_path[t], _ = max(enumerate(post[t]), key=operator.itemgetter(1))
        return list(best_path.astype(int))


def read_sequences(filename):
    inputs = []
    with open(filename, "r") as f:
        for line in f:
            inputs.append(line.strip())
    return inputs

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, viterbi, posterior):
    vit_file_name = filename[:-4]+'_viterbi_output.txt' 
    with open(vit_file_name, "a") as f:
        for state in range(2):
            f.write(str(viterbi.count(state)))
            f.write("\n")
        f.write(" ".join(map(str, viterbi)))
        f.write("\n")

    pos_file_name = filename[:-4]+'_posteri_output.txt' 
    with open(pos_file_name, "a") as f:
        for state in range(2):
            f.write(str(posterior.count(state)))
            f.write("\n")
        f.write(" ".join(map(str, posterior)))
        f.write("\n")


def truncate_files(filename):
    vit_file_name = file[:-4]+'_viterbi_output.txt'
    pos_file_name = file[:-4]+'_posteri_output.txt' 
    if os.path.isfile(vit_file_name):
        open(vit_file_name, 'w')
    if os.path.isfile(pos_file_name):
        open(pos_file_name, 'w')


if __name__ == '__main__':

    hmm = HMM()

    file = sys.argv[1]
    truncate_files(file)
    
    sequences  = read_sequences(file)
    for sequence in sequences:
        #viterbi   = hmm.viterbi(sequence)
        #posterior = hmm.posterior_decode(sequence)
        posterior = hmm.posterior(sequence)
        #write_output(file, viterbi, posterior)


