# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 14:09:57 2022

@author: rania

data set info:
    
name: Name of cereal.

manuf: Manufacturer of cereal:

A: American Home Food Products;

G: General Mills;

K: Kelloggs;

N: Nabisco;

P: Post;

Q: Quaker Oats;

R: Ralston Purina;

type: cold or hot.

calories: calories per serving.

protein: grams of protein.

fat: grams of fat.

sodium: milligrams of sodium.

fiber: grams of dietary fiber.

carbo: grams of complex carbohydrates.

sugars: grams of sugars.

potass: milligrams of potassium.

vitamins: vitamins and minerals - 0, 25, or 100, indicating the typical percentage of FDA recommended.

shelf: display shelf (1, 2, or 3, counting from the floor).

weight: weight in ounces of one serving.

cups: number of cups in one serving.

rating: a rating of the cereals (Possibly from Consumer Reports?).

source of above information: https://search.r-project.org/CRAN/refmans/liver/html/cereal.html
    
source of dataset for project: https://perso.telecom-paristech.fr/eagan/class/igr204/datasets

more information about dataset and original source: http://lib.stat.cmu.edu/datasets/1993.expo/

immediate questions: how is the rating of the cereals defined? it could be related to:
    perceived healthiness, fiber content vs. sugar content, or flavor (which could probably be 
                                                                       connected to sugar content)
    however, a lot of these things are subjective, and not having a source for the ratings can be 
    a little problematic. nevertheless, a little data analysis could be interesting! and might
    help put me off eating some of these in the future :)
    
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import seaborn as sns
from pandas.plotting import scatter_matrix
from pandas import set_option
from pandas import read_csv
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import Normalizer
from numpy import set_printoptions

columns = ['name', 'mfr', 'type', 'calories', 'protein', 'fat', 'sodium', 'fiber', 'carbo', 'sugars', 'potass', 'vitamins',
           'shelf', 'weight', 'cups', 'rating']

df = pd.read_csv('https://perso.telecom-paristech.fr/eagan/class/igr204/data/cereal.csv', 
                   names = columns)

data2 = pd.read_csv('https://perso.telecom-paristech.fr/eagan/class/igr204/data/cereal.csv', 
                   sep = ';',  names = columns, engine = 'python', quotechar = '"', encoding = 'utf8')

data = pd.read_csv('https://perso.telecom-paristech.fr/eagan/class/igr204/data/cereal.csv', 
                   sep = ';',  names = columns, engine = 'python', quotechar = '"', encoding = 'utf8')

"""
read_csv from this link caused the entire dataset to be read into one column with many NaNs
the solution was to figure out what separator was being used and use that parameter so that 
the dataset could be appropriately parsed and organized accordingly

the two first rows need to be dropped as they're not relevant (type of data & column titles)

"""

#cleaning the data

#dropping, default axis is 0, which is rows
data.drop(data.index[[0,1]], inplace = True)

#resetting index for df
data.reset_index(drop = True, inplace = True)

#converting categorical data
from sklearn import preprocessing
le = preprocessing.LabelEncoder()

data['mfr'] = le.fit_transform(data['mfr'])
data['type'] = le.fit_transform(data['type'])

data.columns

#dropping string identifying column
data.drop(['name'], axis = 1, inplace = True)

#checking for nulls
data.isnull().sum()

#dropping just in case
data.dropna(inplace = True)

#checking data types
data.dtypes

#converting datatypes
data = data.apply(pd.to_numeric)

#checking to make sure data types are appropriately converted
data.dtypes

#preliminary data analysis
data.head(15)

description = data.describe()

#noticed some negative values for nutritional content, need to drop those
data3 = data[data.ge(0).all(1)]

#describing again
description2 = data3.describe()

"""
I do question how possible it is to have 0g sodium cereals, however a little research
shows that it is possible to buy 0g sodium cereal, so I will consider the data included
though otherwise, it's possible this data was incorrectly entered and would therefore be
considered outliers
"""

#saving features
X1 = data3.drop(['rating'], axis = 1)
Y1 = data3['rating']
X1names = X1.columns

#preliminary histogram of cleaned data
data3.hist(figsize=(15,11))
plt.show()

plt.figure()
corMat = data3.corr(method='pearson')

#correlation analysis

"""
highly positive linear correlations: 
potassium and fiber at r = 0.912
weight and calories at r = 0.696

highly negative linear correlations:
rating and sugars at r = -0.756
rating and calories at r = -0.694

that helps answer some of the questions I initially had
it seems that the rating goes lower the higher sugar is (the two move away from each other)
"""

#plot correlation matrix as a heat map
sns.heatmap(corMat, square=True)
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.title("Correlation Matrix Using Heatmap")
plt.show()

#scatter plot of all data
plt.figure()
scatter_matrix(data3, alpha= 0.3,figsize=(15,15))
plt.show()

"""
next steps: 
-checking a log transform of the output to compare
-applying a standardization transform on input and comparing to normalized transform
-feature selection
"""