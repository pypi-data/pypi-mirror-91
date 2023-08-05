from PyInquirer import style_from_dict, Token, prompt, Separator
from pyfiglet import Figlet
import argparse
import os
import csv
import json
from logic import Choice1

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'checkbox',
        'message': 'Select function:',
        'name': 'function',
        'choices': [
            Separator('= Functions ='),
            {
                'key': 'a',
                'name': 'Convert CSV to JSON',
                'value': 'ConvertToJSON'
            },
            {
                'key': 'b',
                'name': 'Present a data summary',
                'value': 'DataSummary'
            },
            {
                'key': 'c',
                'name': 'Generate a SQL insert statement for all rows in the input',
                'value': 'SQLInsert'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer['function']) == 0 else True
    }
]

def main():
    
    # CLI argument parser
    parser = argparse.ArgumentParser()

    # adding a mutually exclusive group
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v',"--verbose", action="store_true")
    group.add_argument('-q','--quit', action="store_true")

     # adding an argument of type int and saving it in num variable place holder
    parser.add_argument(
        "filepath", help="The CSV File path the contain that data to be transformed", type=str)

    # adding an option to output the result in a file
    parser.add_argument(
        "-o", "--output", help="output result to a file", action="store_true")

     
    # Grabbing the argument from the command line
    args = parser.parse_args()
    
    filepath = args.filepath
    # CLI choose option using PyInquirer
    chooseOption(filepath)

    
def chooseOption(filepath):
    while True:
        # converting strings into ASCII Text with arts fonts using Pyfiglet
        f = Figlet(font='slant')
        print(f.renderText('Python CLI Appliction'))
        answers = prompt(questions, style=style)
        # if no choice entered by the user loop over
        if  len(answers['function']) == 0:
            os. system('cls')
            print('-------------------- You have to choose atleast one! --------------------\n\n')
        else: # if atleat one choice was entered
            # Enter logic for choice here
            print(answers)
            choiceLogic(answers, filepath)
            break


def choiceLogic(answers, filepath):
    print("Inside the choiceLogic")
    convertjson = Choice1()
    for x in answers['function']:
        if x == 'ConvertToJSON':
            print("The choice is "+str(x))
            convertjson.convertToJson(filepath)
        elif x == 'DataSummary':
            print("The choice is "+str(x))
            getDataSummary()
        elif x == 'SQLInsert':
            print("The choice is "+str(x))
            geSQLInsert()
        else:
            print('Error: Choice feild is incorrect')




def getDataSummary():
    result = "Function to covert CVS to JSON of CSV"
    createFile(result)

def geSQLInsert():
    result = "Function to generate a SQL insert statement for all rows in the input CSV"
    createFile(result)



def createFile(result):
    f = open("./result.txt", "w")
    f.write(result+'\n')
    f.close()



main()
