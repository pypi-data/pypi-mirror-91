
""" Halfbricks Graduate Analyst Programmer Code Test
Python CLI application that performs the following functions:

    Input a CSV file and convert it to JSON
    Input a CSV file and present a data summary
    Input a CSV file and generate a SQL insert statement for all rows in the input

    Created: 2021
    Author: Omar Jarkas
"""
from PyInquirer import style_from_dict, Token, prompt, Separator
from pyfiglet import Figlet
import argparse
import os
import csv
import json
import pandas as pd
import matplotlib.pyplot as plt

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

def plotCountriesCount(countries_os_and, countries_os_ios, india_IOS, indiaAnd, states, brands, top_countries, apple, samsung, huawei):


    
    top_3_brands = ['Apple','Samsung','Huawei']
    plt.style.use('seaborn-dark-palette')
    fig = plt.figure()

    # Plot 1
    plt.subplot(2, 2, 1)
    # Setting the positions and width for the bars
    width = 0.25 
    pos_and = list(range(len(countries_os_and.keys())))
    pos_ios = [p - width for p in pos_and]
    
    # # Create a bar with andriod,
    # # in position pos,
    plt.bar(pos_and, list(countries_os_and.values()), width, alpha=0.5, color='red',
            label='andriod') 

    # Create a bar with ios,
    # in position pos,
    plt.bar(pos_ios, list(countries_os_ios.values()), width, alpha=0.5, color='blue', label='IOS') 
    # Placing the name in the plot
    plt.legend(loc='upper right')
    plt.xticks(pos_ios,countries_os_and.keys(), rotation=90)
    plt.xlabel('Countries', fontsize=12)
    plt.ylabel('OS', fontsize=12)
    plt.title('ANDRIOD vs IOS in top frequent countries', fontsize=12)


    # Plot 2
    plt.subplot(2, 2, 2)
    pos_india_and = list(range(len(india_IOS)))
    pos_india_ios = [p - width for p in pos_india_and]
    width = 0.25 

    plt.bar(pos_india_and, list(indiaAnd.values()), width, alpha=0.5, color='green',
        label='ANDROID') 
    plt.bar(pos_india_ios, list(india_IOS.values()), width, alpha=0.5, color='blue',
        label='IOS') 
    # Placing the name in the plot
    plt.legend(loc='upper right')
    plt.xlabel('States', fontsize=12)
    plt.ylabel('OS', fontsize=12)
    plt.title('ANDRIOD vs IOS accross different states in India', fontsize=12)
    plt.xticks(pos_india_and,states, rotation=90)


    # Plot 3
    plt.subplot(2, 2, 3)
    plt.pie(brands.values(), labels = brands.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title('Percentage of Phone Brands Accross different Countries', fontsize=12)

    # Plot 4
    plt.subplot(2, 2, 4)
    pos = list(range(len(top_countries.keys()))) 
    width = 0.25 

    plt.bar(pos,  apple, width,  alpha=0.5,  color='#EE3224', label=top_3_brands[0]) 

    plt.bar([p + width for p in pos], samsung,width, alpha=0.5, color='#F78F1E', label=top_3_brands[1]) 

    plt.bar([p + width*2 for p in pos], huawei, width, alpha=0.5, color='#FFC222', label=top_3_brands[2]) 
    plt.grid()
    plt.xlabel('Countries', fontsize=12)
    plt.ylabel('Number of Phones', fontsize=12)
    plt.title('Top Phone Brands in top frequent countries', fontsize=12)
    plt.legend(top_3_brands, loc='upper right')
    plt.xticks([p + width for p in pos],top_countries.keys())
    

    plt.tight_layout()
    fig.set_constrained_layout_pads(wspace=0, hspace=0, w_pad=0, h_pad=0)
    fig.savefig("Summary.png")

    plt.show()

    print('==================================')
    print('Summary.png has been saved under this directory')
    print('===================================')

def getUniqOS(df):
    """ Based on the df if it contains a columns named devices os it will return unique attributes of the column
    >>> df = pd.read_csv(r"../data.csv")
    >>> getUniqOS(df)
    ['ANDROID', 'IOS']
    """
    # getting a unique list of the countries
    os = df.device_os.unique().tolist()
    # sort list alphabatically
    return sorted(os)

def getUniqCountries(df):
    """
    >>> df = pd.read_csv(r'../data.csv')
    >>> getUniqCountries(df)
    ['Angola', 'Aruba', 'Belize', 'Benin', 'Bhutan', 'Brazil', 'Chad', 'Chile', 'China', 'Cuba', 'Egypt', 'Fiji', 'Gabon', 'Ghana', 'Guam', 'Haiti', 'India', 'Iran', 'Iraq', 'Italy', 'Japan', 'Kenya', 'Laos', 'Libya', 'Macao', 'Mali', 'Malta', 'Nepal', 'Niger', 'Oman', 'Peru', 'Qatar', 'Spain', 'Sudan', 'Syria', 'Togo', 'Yemen']

    """
    # getting a unique list of the countries
    countries_uniq_list = df.geo_country.unique().tolist()
    # delete the "nan"
    del countries_uniq_list[0]
    # sort list alphabatically
    return sorted(countries_uniq_list)


def getCountriesCountOSDictionary(countries_count_per_os, countries_uniq_list, os):
    countries_os_count = countries_count_per_os.loc[:, os]
    dict1 = {}
    for x in countries_uniq_list:
        if x in countries_os_count:
            dict1[x] = countries_os_count[x]
        else:
            dict1[x] = 0
    return dict1


def getMobileCountAccoutOSAccrossStates(countries_count_per_os, countries_uniq_list):
    dict1 = {}
    for x in countries_uniq_list:
        if x in countries_count_per_os:
            dict1[x] = countries_count_per_os[x]
        else:
            dict1[x] = 0
    return dict1

def indiaStates(df):
    """
    >>> import pandas as pd
    >>> df = pd.read_csv(r'../data.csv')
    >>> indiaStates(df)
    ({'Telangana': 13, 'Maharashtra': 24, 'Uttar Pradesh': 3, 'Gujarat': 16, 'Tamil Nadu': 18, 'Chandigarh': 8, 'West Bengal': 5, 'Kerala': 5, 'Haryana': 3, 'Rajasthan': 4, 'Madhya Pradesh': 1, 'Assam': 0, 'Jammu and Kashmir': 0, 'Uttarakhand': 1, 'Delhi': 22, 'Odisha': 0, 'Himachal Pradesh': 0, 'Punjab': 2, 'Bihar': 2, 'Chhattisgarh': 0, 'Karnataka': 11, 'Andhra Pradesh': 4, 'Goa': 0, 'Sikkim': 0, 'Jharkhand': 0, 'Tripura': 0, 'Puducherry': 0, 'Manipur': 0, 'Meghalaya': 0}, {'Telangana': 413, 'Maharashtra': 459, 'Uttar Pradesh': 225, 'Gujarat': 322, 'Tamil Nadu': 482, 'Chandigarh': 102, 'West Bengal': 142, 'Kerala': 94, 'Haryana': 54, 'Rajasthan': 116, 'Madhya Pradesh': 125, 'Assam': 40, 'Jammu and Kashmir': 6, 'Uttarakhand': 22, 'Delhi': 369, 'Odisha': 45, 'Himachal Pradesh': 9, 'Punjab': 46, 'Bihar': 76, 'Chhattisgarh': 9, 'Karnataka': 222, 'Andhra Pradesh': 73, 'Goa': 3, 'Sikkim': 0, 'Jharkhand': 13, 'Tripura': 11, 'Puducherry': 4, 'Manipur': 1, 'Meghalaya': 1}, ['Telangana', 'Maharashtra', 'Uttar Pradesh', 'Gujarat', 'Tamil Nadu', 'Chandigarh', 'West Bengal', 'Kerala', 'Haryana', 'Rajasthan', 'Madhya Pradesh', 'Assam', 'Jammu and Kashmir', 'Uttarakhand', 'Delhi', 'Odisha', 'Himachal Pradesh', 'Punjab', 'Bihar', 'Chhattisgarh', 'Karnataka', 'Andhra Pradesh', 'Goa', 'Sikkim', 'Jharkhand', 'Tripura', 'Puducherry', 'Manipur', 'Meghalaya'])
    
    """
    india_df = df[df.geo_country=="India"]
    india_df.groupby(['device_category','geo_region']).device_brand_name.count()
    
    # Andriod moblie count accross different states in india
    india_mobile_andriod = india_df[india_df.device_category=="mobile"][india_df.device_os=="ANDROID"]
    india_mobile_and_count = india_mobile_andriod.groupby(['geo_region']).device_brand_name.count()

    # IOS mobile count accross different state in india
    india_mobile_ios = india_df[india_df.device_category=="mobile"][india_df.device_os=="IOS"]
    india_mobile_ios_count = india_mobile_ios.groupby(['geo_region']).device_brand_name.count()

    india_uniq_states = india_df.geo_region.unique().tolist()
    del india_uniq_states[-3]

    ios_india_state_count = getMobileCountAccoutOSAccrossStates(india_mobile_ios_count,india_uniq_states)
    and_india_state_count = getMobileCountAccoutOSAccrossStates(india_mobile_and_count,india_uniq_states)

    return ios_india_state_count, and_india_state_count, india_uniq_states


def phone_brands(df):
    """
    >>> import pandas as pd
    >>> df = pd.read_csv(r'../data.csv')
    >>> phone_brands(df)
    {'others': 1912, 'Huawei': 1977, 'LG': 622, 'Apple': 2910, 'Xiaomi': 1491, 'Samsung': 4738, 'Motorola': 584, 'OPPO': 542, 'Vivo': 575}
    """
    brands = {}
    brands['others'] = 0
    # get unique devices
    uniq_phone_brands = df.device_brand_name.unique().tolist()

    for x in uniq_phone_brands:
        if df[df.device_brand_name==x].device_brand_name.count() > 300:
            brands[x] = df[df.device_brand_name==x].device_brand_name.count()
        else:
            brands['others'] = brands['others'] + df[df.device_brand_name==x].device_brand_name.count()
        
    return brands

def topBrandsandCountries(df, countries_unique):
    """
    >>> import pandas as pd
    >>> df = pd.read_csv(r'../data.csv')
    >>> topBrandsandCountries(df, ['Angola', 'Aruba', 'Belize', 'Benin', 'Bhutan', 'Brazil', 'Chad', 'Chile', 'China', 'Cuba', 'Egypt', 'Fiji', 'Gabon', 'Ghana', 'Guam', 'Haiti', 'India', 'Iran', 'Iraq', 'Italy', 'Japan', 'Kenya', 'Laos', 'Libya', 'Macao', 'Mali', 'Malta', 'Nepal', 'Niger', 'Oman', 'Peru', 'Qatar', 'Spain', 'Sudan', 'Syria', 'Togo', 'Yemen'])
    ({'Brazil': 2245, 'Chile': 848, 'China': 2390, 'Egypt': 977, 'India': 3855, 'Italy': 1996, 'Spain': 1172}, [72, 70, 1478, 50, 214, 438, 205], [1161, 377, 30, 338, 1041, 708, 351], [1, 192, 273, 231, 114, 606, 254])
    """
    top_countries = {}
    for x in countries_unique:
        if df[df.geo_country==x].device_brand_name.count() > 500:
            top_countries[x] = df[df.geo_country==x].device_brand_name.count()

    top_3_brands = ['Apple','Samsung','Huawei']

    apple = []
    samsung = []
    huawei = []
    for x in top_countries.keys():
        apple.append(df[df.geo_country==x][df.device_brand_name==top_3_brands[0]].device_brand_name.count())
        samsung.append(df[df.geo_country==x][df.device_brand_name==top_3_brands[1]].device_brand_name.count())
        huawei.append(df[df.geo_country==x][df.device_brand_name==top_3_brands[2]].device_brand_name.count()) 

    return top_countries,apple,samsung,huawei

def get_countries_os_and(df, country_uniq, os):
    countries_os_and = {}

    for x in country_uniq:
        count_os_per_country_and = df[df.geo_country==x][df.device_os==os[0]].device_os.count()
        if count_os_per_country_and > 50:
            countries_os_and[x] = count_os_per_country_and
    return countries_os_and

def get_countries_os_ios(df, countries_os_and, os):
    countries_os_ios = {}

    for x in countries_os_and.keys():
        count_os_per_country_ios = df[df.geo_country==x][df.device_os==os[1]].device_os.count()
        countries_os_ios[x] = count_os_per_country_ios
    return countries_os_ios

def summary(filepath):

    # Using panda to read the csv file and insert it into a dataframe
    df = pd.read_csv(filepath)

    # get a list of unique countries
    countries_uniq_list = getUniqCountries(df)

    os_uniq = getUniqOS(df)
    countries_os_and = get_countries_os_and(df, countries_uniq_list, os_uniq)
    countries_os_ios = get_countries_os_ios(df, countries_os_and, os_uniq)

    india_IOS, indiaAnd, states = indiaStates(df)

    brands = phone_brands(df)

    top_countries,apple,samsung,huawei = topBrandsandCountries(df, countries_uniq_list)
    plotCountriesCount(countries_os_and, countries_os_ios,india_IOS, indiaAnd, states, brands, top_countries,apple,samsung,huawei)

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
            choiceLogic(answers, filepath)
            break


def choiceLogic(answers, filepath):
    for x in answers['function']:
        if x == 'ConvertToJSON':
            convertToJson(filepath)
        elif x == 'DataSummary':
            summary(filepath)
        elif x == 'SQLInsert':
            sqlconvert(filepath)
        else:
            print('Error: Choice feild is incorrect')






def convertToJson(filepath):
    # json array convert from python dictionary place holder
    jsonArray = []
    # open csv file as csvfile and convert it into a python dictory list object
    with open(filepath, encoding='utf-8') as csvfile:
        csvReader = csv.DictReader(csvfile)
        # getting the name of the file
        filename = os.path.basename(filepath).split('.')[0]
        # creates a file under the current directory with the name of the file
        jsonfile =  open("./"+filename+".json", 'w+', encoding='utf-8')
        for row in csvReader:
            jsonArray.append(row)
        jsonfile.write(json.dumps(jsonArray,indent=4))
        jsonfile.close()
    print('==================================')
    print(filename+'.json has been saved under this directory')
    print('===================================')

def sqlconvert(filename):

    data  = pd.read_csv(filename)

    columns_name = []
    # iterating the columns 
    for col in data.columns: 
        columns_name.append(col)
    columns_name_str = str(columns_name).replace('[','').replace(']','')
    filename = os.path.basename(filename).split('.')[0]
    sqlfile =  open("./"+filename+".sql", 'w+', encoding='utf-8')
    for x in range(0,len(data)):
        values = []
        for y in data.iloc[x]:
            values.append(y)
        values_str = str(values).replace('[','').replace(']','')
        stmt = "INSERT INTO employees ("+str(columns_name_str)+") VALUES ("+values_str+");\n\n"
        sqlfile.write(stmt)
    sqlfile.close()

    print('==================================')
    print(filename+'.sql has been saved under this directory')
    print('===================================')

main()
