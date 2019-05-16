#!/usr/bin/env python 
# -*- coding:utf-8 -*-
##############################################
##initial data
###########################
import pandas as pd
import random

content = pd.read_csv( 'D:/doct/leason/NLP/leason3/Kaggle_Titanic-master/Kaggle_Titanic-master/train.csv')
content = content.dropna()
age_with_fares = content[
    (content['Age'] > 22) & (content['Fare'] < 400) & (content['Fare'] > 130)
]
sub_fare = age_with_fares['Fare']
sub_age = age_with_fares['Age']
#######################################################################
#forword:k/age+b=price
#loss:abs(y - yhat)=loss
#########################################################################

def func(age, k, b): return k * age + b
import numpy as np
def loss(y, yhat):
    return np.mean(np.abs(y - yhat))
#################################################
#func of forward、loss
##################################################################3
min_error_rate = float('inf')
loop_times = 10000
losses = []

change_directions = [
    # (k, b)
    (+1, -1), # k increase, b decrease
    (+1, +1),
    (-1, +1),
    (-1, -1)  # k decrease, b decrease
]
k_hat = random.random() * 20 - 10#initial k
b_hat = random.random() * 20 - 10#initial b

best_k, best_b = k_hat, b_hat

best_direction = None


def step(): return random.random() * 1


direction = random.choice(change_directions)

#######################################################################################
#反向系数k，b 更新
##########################################################################################
def derivate_k(y, yhat, x):
    abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i, yhat_i in zip(y, yhat)]
    return np.mean([a * -x_i for a, x_i in zip(abs_values, x)])

def derivate_b(y, yhat):
    abs_values = [1 if (y_i - yhat_i) > 0 else -1 for y_i, yhat_i in zip(y, yhat)]
    return np.mean([a * -1 for a in abs_values])

learing_rate = 1e-1

##########################################################################################
#main，loop time<
#####################################################
while loop_times > 0:
    k_delta = -1 * learing_rate * derivate_k(sub_fare, func(sub_age, k_hat, b_hat), sub_age)
    b_delta = -1 * learing_rate * derivate_b(sub_fare, func(sub_age, k_hat, b_hat))

    k_hat += k_delta
    b_hat += b_delta

    estimated_fares = func(sub_age, k_hat, b_hat)
    error_rate = loss(y=sub_fare, yhat=estimated_fares)

    print('loop == {}'.format(loop_times))#show loop time
        # losses.append(min_error_rate)
    print('f(age) = {} * age + {}, with error rate: {}'.format(best_k, best_b, error_rate))       #show
    losses.append(error_rate)
    loop_times -= 1
##################################################
#show
#######################################
import matplotlib.pyplot as plt
plt.plot(range(len(losses)), losses)
plt.show()