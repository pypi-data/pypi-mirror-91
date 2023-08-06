# This python scrips creates a set of long multiplication and divison problems to solve.
# A dictionary of randomly generated long addition, subtraction, mulitplication and division is printed out to the user.
# When the user answers all questions, they can request the answers.

# Imports useful python packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sc
import sklearn as skl
import csv as csv
import openpyxl as pyxl
import pathlib
import os
import pydrive
import random as rd


# Defines long_multiplication
def long_multiplication(questions, answers, num_array):
    """Generates several random long division  problems

    Args:
        questions (dict): Dictionary of mental math questions
        answers (dict): Dictionary of mental math answers
        num_array: Array 

    Returns:
        questions (dict): Dictionary of updated mental math questions
        answers (dict): Dictionary of upted mental math answers
    """
    num = round(rd.random() * 1000)
    print(num)
    return num


# Sets up the questions and answers dictionaries
questions = {
    1: 'NA',
    2: 'NA',
    3: 'NA',
    4: 'NA',
    5: 'NA',
    6: 'NA',
    7: 'NA',
    8: 'NA',
    9: 'NA',
    10: 'NA',
    11: 'NA',
    12: 'NA',
    13: 'NA',
    14: 'NA',
    15: 'NA',
    16: 'NA',
    17: 'NA',
    18: 'NA',
    19: 'NA',
    20: 'NA',
}
answers = {
    1: 'NA',
    2: 'NA',
    3: 'NA',
    4: 'NA',
    5: 'NA',
    6: 'NA',
    7: 'NA',
    8: 'NA',
    9: 'NA',
    10: 'NA',
    11: 'NA',
    12: 'NA',
    13: 'NA',
    14: 'NA',
    15: 'NA',
    16: 'NA',
    17: 'NA',
    18: 'NA',
    19: 'NA',
    20: 'NA',
}
# Test the long multiplication function
num = long_multiplication_whole()
print(num)
