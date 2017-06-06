import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
import random
from pylab import *
from mpl_toolkits.mplot3d import Axes3D

def load_data(filename):
    #load data
    reader = csv.reader(open(filename, "rb"), delimiter=",")
    d = list(reader)

    data = np.array(d)
    X = data[:,0:23]
    y = data[:,23]
    y = np.delete(y, 0, 0)
    X = np.delete(X, 0, 0)
    y.shape = (len(y), 1)
    y = y.astype("float")

    # biasone = np.ones((np.shape(X)[0], 1))
    # X = np.concatenate((biasone, X), axis=1)
    return X, y

# <= 300 F
# 300 < score <= 400 D
# 400 < score <= 500 C
# 500 < score <= 600 B
# score > 600 A
def classify(y):
    length = len(y)
    Y = np.copy(y)
    Y = Y.astype("string")
    for i in range(length):
        if y[i][0] < 450:
            Y[i][0] = "c"
        elif y[i][0] >= 450 and y[i][0] < 580:
            Y[i][0] = "b"
        elif y[i][0] >= 580:
            Y[i][0] = "a"
        # elif y[i][0] > 600:
        #     Y[i][0] = "a"

    return Y

def maximum(X, col):
    rownum = X.shape[0]
    maxi = -1000
    for i in range(rownum):
        if X[i][col] >= maxi:
            maxi = X[i][col]

    return maxi

def minimum(X, col):
    rownum = X.shape[0]
    mini = 1000000
    for i in range(rownum):
        if X[i][col] <= mini:
            mini = X[i][col]

    return mini

# normalize certain attributes after removing NA
def normalize(X):
    rownum = np.shape(X)[0]
    max0 = maximum(X, 0)
    min0 = minimum(X, 0)
    print max0, min0
    max17 = maximum(X, 17)
    min17 = minimum(X, 17)
    max18 = maximum(X, 18)
    min18 = minimum(X, 18)
    max22 = maximum(X, 22)
    min22 = minimum(X, 22)
    min2 = 0.0
    max2 = 6.0
    for i in range(rownum):
        X[i][0] = (X[i][0] - min0) / (max0 - min0)

        X[i][2] = (X[i][2] - min2) / (max2 - min2)
        X[i][17] = (X[i][17] - min17) / (max17 - min17)
        X[i][18] = (X[i][18] - min18) / (max18 - min18)
        X[i][22] = (X[i][22] - min22) / (max22 - min22)


# write the processed data into a new csv
def writeFile(X, y, train):
    if train == True:
        with open('train_processed.csv', 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            data = []
            data.append(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'Grade'])
            for i in range(X.shape[0]):
                temp = []
                for j in range(X.shape[1]):
                    temp.append(X[i][j])
                temp.append(y[i][0])
                data.append(temp)

            a.writerows(data)
    else:
        with open('test_processed.csv', 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            data = []
            data.append(['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', 'x10', 'x11', 'x12', 'x13', 'x14', 'x15', 'x16', 'x17', 'x18', 'x19', 'x20', 'x21', 'x22', 'x23', 'Grade'])
            for i in range(X.shape[0]):
                temp = []
                for j in range(X.shape[1]):
                    temp.append(X[i][j])
                temp.append(y[i][0])
                data.append(temp)

            a.writerows(data)

def replace_NA(X, col):
    rownum = np.shape(X)[0]
    a = []
    for i in range(rownum):
        if X[i][col] != 'NA':
            a.append(float(X[i][col]))

    a = np.asarray(a)
    # print a
    return np.mean(a)

def delete_NA(X, y):
    X_copy = np.copy(X)
    y_copy = np.copy(y)
    rownum = np.shape(X)[0]
    colnum = np.shape(X)[1]
    delete_lines = []
    for i in range(rownum):
        for j in range(colnum):
            if X[i][j] == 'NA':
                delete_lines.append(i)
                break

    X_copy = np.delete(X_copy, delete_lines, 0)
    y_copy = np.delete(y_copy, delete_lines, 0)
    # X_copy = X_copy.astype("float")
    return X_copy, y_copy


def preprocess_data(X):
    # Race: white, hispanic, asian, black, american indian/alaska, other pacific islanders, more than one race
    # Race: 0, 1, 2, 3, 4, 5, 6
    rownum = np.shape(X)[0]
    colnum = np.shape(X)[1]
    median18 = replace_NA(X, 17)
    print median18
    median19 = replace_NA(X, 18)
    print median19
    median23 = replace_NA(X, 22)
    print median23
    for i in range(rownum):
        for j in range(colnum):
            if j == 2:
                if X[i][j] == 'NA':
                    X[i][j] = str(float(randint(0, 6)))
                elif X[i][j] == 'White':
                    X[i][j] = '0.0'
                elif X[i][j] == 'Hispanic':
                    X[i][j] = '1.0'
                elif X[i][j] == 'Asian':
                    X[i][j] = '2.0'
                elif X[i][j] == 'Black':
                    X[i][j] = '3.0'
                elif X[i][j] == 'American Indian/Alaska Native':
                    X[i][j] = '4.0'
                elif X[i][j] == 'Native Hawaiian/Other Pacific Islander':
                    X[i][j] = '5.0'
                elif X[i][j] == 'More than one race':
                    X[i][j] = '6.0'
            elif j == 17:
                if X[i][j] == 'NA':
                    X[i][j] = str(median18)
            elif j == 18:
                if X[i][j] == 'NA':
                    X[i][j] = str(median19)
            elif j == 22:
                if X[i][j] == 'NA':
                    X[i][j] = str(median23)
            else:
                if X[i][j] == 'NA':
                    X[i][j] = str(float(randint(0, 1)))
                    # X[i][j] = 0.0
                else:
                    X[i][j] = str(float(X[i][j]))

    X = X.astype("float")
    return X

def calculate_w(X, y):
    print "Calculating w"
    w = np.dot(np.linalg.pinv(np.dot(X.T, X)), np.dot(X.T, y))
    print "done"
    return w

def testError(Y_train, Y):
    length = len(Y)
    count_error = 0
    for i in range(length):
        if Y_train[i][0] != Y[i][0]:
            count_error += 1

    print 1.0 - float(count_error) / float(length)


def count_NA(X):
    rownum = np.shape(X)[0]
    colnum = np.shape(X)[1]
    count = 0
    for i in range(rownum):
        for j in range(colnum):
            if X[i][j] == 'NA':
                count += 1

    print count

def convert_race(X):
    rownum = np.shape(X)[0]
    colnum = np.shape(X)[1]
    for i in range(rownum):
        for j in range(colnum):
            if j == 2:
                if X[i][j] == 'White':
                    X[i][j] = '0.0'
                elif X[i][j] == 'Hispanic':
                    X[i][j] = '1.0'
                elif X[i][j] == 'Asian':
                    X[i][j] = '2.0'
                elif X[i][j] == 'Black':
                    X[i][j] = '3.0'
                elif X[i][j] == 'American Indian/Alaska Native':
                    X[i][j] = '4.0'
                elif X[i][j] == 'Native Hawaiian/Other Pacific Islander':
                    X[i][j] = '5.0'
                elif X[i][j] == 'More than one race':
                    X[i][j] = '6.0'

    X = X.astype("float")


X, y = load_data("pisa2009train.csv")
#train weight using linear regression

X = preprocess_data(X)
# X, y = delete_NA(X, y)
# convert_race(X)
# X = X.astype("float")
normalize(X)
Y = classify(y)

# testError(Y_train, Y)
# print Y_train
# print Y
writeFile(X, Y, True)

#-----------------------------------------

X_test, y_test = load_data("pisa2009test.csv")
X_test = preprocess_data(X_test)
# X_test, y_test = delete_NA(X_test, y_test)
# convert_race(X_test)
# X_test = X_test.astype("float")
normalize(X_test)
Y_test = classify(y_test)
writeFile(X_test, Y_test, False)
