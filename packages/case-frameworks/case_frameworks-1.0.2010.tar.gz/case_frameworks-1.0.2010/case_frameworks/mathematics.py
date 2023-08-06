# This python script creates a set of long multiplication and divison problems to solve.
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


class mathematics:
    # Defines long_multiplication
    def long_multiplication(self, questions, answers, max_decimals):
        """Generates long multiplication problems

        Args:
            questions (dict): Dictionary of mental math questions
            answers (dict): Dictionary of mental math answers
            max_decimals (int): Maximum number of decimals for rounded numbers

        Returns:
            questions (dict): Dictionary of updated mental math questions
            answers (dict): Dictionary of updated mental math answers
        """
        # loops through the questions dictionary
        for key in questions[key]:
            # Generates random values to practise
            num_1 = round(rd.random() * 1000), round(rd.random() *
                                                     max_decimals)
            num_2 = round(rd.random() * 1000), round(rd.random() *
                                                     max_decimals)
            #Calculates the answers from the numbers generated
            answers[key] = num_1 * num_2
            # Stores the question in the question string
            questions[key] = str(num_1) + 'x' + str(num_2)
        # Returns the answers
        return questions, answers

    def long_division(self, questions, answers, num_array):
        """Generates long division problems

        Args:
            questions ([type]): [description]
            answers ([type]): [description]
            num_array ([type]): [description]
        """

    def long_addition(self, questions, answers, num_array):
        """[summary]

        Args:
            questions ([type]): [description]
            answers ([type]): [description]
            num_array ([type]): [description]
        """

    def long_subtraction(self, questions, answers, num_array):
        """[summary]

        Args:
            questions ([type]): [description]
            answers ([type]): [description]
            num_array ([type]): [description]
        """