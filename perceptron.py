# -*- coding: utf-8 -*-
__author__ = 'wangjz'

import random
import numpy as np

"""
Learning From Data
HW 1
The Perceptron Learning Algorithm
目前本目录下的main函数不能使用

In this problem, you will create your own target function f and data set D to see how the
Perceptron Learning Algorithm works.Take d = 2 so you can visualize the problem,
and assume X = [−1, 1] × [−1, 1] with uniform probability of picking each x∈X.
In each run, choose a random line in the plane as your target function f
(do this by taking two random, uniformly distributed points in [−1, 1] × [−1, 1] and
taking the line passing through them), where one side of the line maps to +1 and the other maps to −1.
Choose the inputs xn of the data set as random points (uniformly in X ), and evaluate the target function on each xn
to get the corresponding output yn.Now, in each run, use the Perceptron Learning Algorithm to find g.
Start the PLA with the weight vector w being all zeros, and at each iteration have the algorithm
choose a point randomly from the set of misclassified points. We are interested in two quantities:
the number of iterations that PLA takes to converge to g, and the disagreement between f and g which is
P[f(x) ̸= g(x)] (the probability that f and g will disagree on their classification of a random point).
You can either calculate this probability exactly, or approximate it by generating a sufficiently large,
separate set of points to estimate it.In order to get a reliable estimate for these two quantities, you should
repeat the experiment for 1000 runs (each run as specified above) and take the average over these runs.
"""


def update_w(w, item):
    x, y = item[0], item[1]
    x.shape = 3,1
    w = w + y * x
    return w


def dot_prodcut(a1, a2):
    """dot product"""
    res = 0
    for i in range(len(a1)):
        res += a1[i] * a2[i]
    return res


def sign(a1, a2):
    #element-wise multiply
    return 1 if np.dot(a1, a2) >= 0 else -1


class Perceptron:
    def __init__(self, training_X, training_Y, init_w=[]):
        self.__N = training_X.shape[0]
        self.__training_X = training_X
        self.__training_Y = training_Y
        self.num_iterations = 0
        self.w = init_w

    def gd_algorithm(self):
        weights = self.w
        num_iteration = 0
        while True:
            #find misclassified points
            mis_classify = []
            for index in range(self.__N):
                x = self.__training_X[index, :]
                y = self.__training_Y[index, 0]
                if sign(x, weights) != y:
                    mis_classify.append((x, y))
            if len(mis_classify) == 0:
                break
            num_iteration += 1

            #randomly choose a misclassified point and apply gradient descent
            mis_item = random.choice(mis_classify)
            weights = update_w(weights, mis_item)

        self.num_iterations = num_iteration
        self.w = weights


def generate_training_date(n):
    #generate target function (represented by vector w)
    p1 = [random.uniform(-1, 1), random.uniform(-1, 1)]
    p2 = [random.uniform(-1, 1), random.uniform(-1, 1)]
    w = [1, 0, 0]
    w[1] = (p2[0] - p1[0]) / (p1[1] - p2[1])
    w[2] = - (p1[0] * w[0] + p1[1] * w[1])

    #generate n random points between [-1,1]X[-1,1]
    training_data = []
    for i in range(n):
        p = [random.uniform(-1, 1), random.uniform(-1, 1), 1]
        p = [sign(w, p)] + p #set label
        training_data.append(p)

    return training_data, w


def main():
    #Let's do the experiment
    num_points = 100
    num_random_test = 100
    iterations = 1000
    iter_list = []
    p_agree = []

    for i in range(iterations):
        td, f = generate_training_date(num_points)
        perce = Perceptron(td)
        perce.gd_algorithm()
        iter_list.append(perce.num_iterations)
        g = perce.w

        agree = 0
        for _ in range(num_random_test):
            ran_p = [random.uniform(-1, 1), random.uniform(-1, 1), 1]
            if sign(ran_p, f) == sign(ran_p, g):
                agree += 1

        p_agree.append(1.0 * agree / num_random_test)

    print max(iter_list)
    print min(iter_list)
    print 1.0 * sum(iter_list) / len(iter_list)

    print max(p_agree)
    print min(p_agree)
    print 1.0 * sum(p_agree) / len(p_agree)

if __name__ == "__main__":
    main()

