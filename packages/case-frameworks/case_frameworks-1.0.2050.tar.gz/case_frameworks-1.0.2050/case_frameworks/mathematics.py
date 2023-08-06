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
    def arithmetic_practise(self, questions, answers, max_figures,
                            max_decimals, arithmetic_type):
        """Generates problems to practise arithmetric

        Args:
            questions (dict): Dictionary of mental math questions
            answers (dict): Dictionary of mental math answers
            max_figures (int): Maximum randomly generated number, expressed in multiples of 10 (10,100,1000 etc.)
            max_decimals (int): Maximum number of decimal places (1,2,3 etc.)
            arithmetic_type (str): Type of operation to be applied (addition, subtraction, multiplication or division)

        Returns:
            questions (dict): Updated dictionary of mental math questions
            answers (dict): Updated dictionary of mental math answers 
        """
        # loops through the questions dictionary
        for key in questions:
            # Generates random values to practise
            num_1 = round(rd.random() * max_figures,
                          round(rd.random() * max_decimals))
            print(num_1)
            num_2 = round(rd.random() * max_figures,
                          round(rd.random() * max_decimals))
            # Set questions and answers if multiplication
            if arithmetic_type == 'multiplication':
                #Calculates the answers from the numbers generated
                answers[key] = num_1 * num_2
                # Stores the question in the question string
                questions[key] = str(num_1) + ' x ' + str(num_2)
            # Set questions and answers if division
            elif arithmetic_type == 'division':
                #Calculates the answers from the numbers generated
                answers[key] = num_1 / num_2
                # Stores the question in the question string
                questions[key] = str(num_1) + ' / ' + str(num_2)
            # Set questions and answers if addition
            elif arithmetic_type == 'addition':
                #Calculates the answers from the numbers generated
                answers[key] = num_1 + num_2
                # Stores the question in the question string
                questions[key] = str(num_1) + ' + ' + str(num_2)
            # Set questions and answers if subtraction
            elif arithmetic_type == 'subtraction':
                #Calculates the answers from the numbers generated
                answers[key] = num_1 - num_2
                # Stores the question in the question string
                questions[key] = str(num_1) + ' - ' + str(num_2)
            else:
                # Sets a no operation appplied
                questions[key] = 'No operation applied!'
        # Returns the answers
        return questions, answers

    def quiz(self, questions, answers):
        """Generates a quiz to ask mental math questions

        Args:
            questions (dict): Dictionary of mental math questions
            answers (dict): Dictionary of mental math answers
        """