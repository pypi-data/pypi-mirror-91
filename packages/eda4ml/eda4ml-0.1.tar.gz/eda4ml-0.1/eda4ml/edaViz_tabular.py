import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from scipy import stats

class edaViz_tab:
    
    def __init__(self, df):

        """ Class providing methods to facilitate the EDA of a dataset.
        Methods:
        - describe
        - numeric_cols
        - categorical_cols
        - discrete_possible_cols
        - categorical_cols_for_dummies
        - cols_with_missing_data
        - cols_for_imputation
        - correlation_plot
        - histograms
        - boxplots
        - scatterplots
        - normality_check

        Attributes:
            df (pandas dataframe) representing the dataset to which we want to apply EDA

        """
        
        self.df = df
        
    def describe(self, full = 'all'):
        """"Provides descriptive data for both numerical and categorical features

        Args:
            full (str): if 'all'' includes the categorical variables

        Returns:
            dataframe: descriptive data of the columns
        """
        return self.df.describe(include = full)
    
    def numeric_cols(self):
        """"Provides the numerical features of the dataset

        Args:
            None

        Returns:
            list: feature column names
        """

        temp = pd.DataFrame(self.df.describe(include = 'all').T)
        return temp[temp['unique'].isnull()].index.tolist()
    
    def categorical_cols(self):
        """Provides the categorical features of the dataset

        Args:
            None

        Returns:
            list: feature column names
        """

        temp = pd.DataFrame(self.df.describe(include = 'all').T)
        return temp[temp['unique'].notnull()].index.tolist()
    
    def discrete_possible_cols(self, k=20):
        """"Provides the numerical features of the dataset that get up to k discrete values. 
        These features could be transformed to dummy variables for better EDA

        Args:
            k (int): the number of the different values the variable can get (default:20)

        Returns:
            list: feature column names
        """
        temp = pd.DataFrame(self.df.describe(include = 'all').T)
        return temp[temp['max'] < k].index.tolist()
    
    def categorical_cols_for_dummies(self, cardinality = 20):
        """"Provides the categirical features which have limited cardinality add could be converted 
            to dummy variables

        Args:
            cardinality (int): the number of possible values the variable can get (defaul:20)

        Returns:
            list: feature column names
        """

        temp = pd.DataFrame(self.df.describe(include = 'all').T)
        return temp[temp['unique'] < cardinality].index.tolist()
    
    def cols_with_missing_data(self, top_N = 20):
        """Provides the top_N features with the highest percentage and actual size of missing data. Columns with percentage
         higher than 15% could be removed from the dataset

        Args:
            top_N (int): the number of features with missing data presented in the result dataframe (defaul:20)

        Returns:
            list: feature column names
        """

        total = self.df.isnull().sum().sort_values(ascending=False)
        percent = (self.df.isnull().sum()/self.df.isnull().count()).sort_values(ascending=False)
        missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
        return missing_data.head(top_N)
        
    def cols_for_imputation(self, min_completeness_pct = 0.85):
        """Provides the features with missing data (less than 15%) that could be imputed. Another option is to remove the entries that
            contain this missing data

        Args:
            min_completeness_pct (float): the minimum percentage of completeness that the columns should have (defaul:0.85)

        Returns:
            list: feature column names
        """

        temp = pd.DataFrame(self.df.describe(include = 'all').T)
        return temp[(temp['count'] >  min_completeness_pct * temp['count'].max()) & (temp['count'] < temp['count'].max())].index.tolist()
    
   
    
    def correlation_plot(self, target = None, top_N = 10, ascending = False):
        """Provides the correlation heatmap between the featues of the dataset
        when it is invoked without target column. 
        Plots the top_N most or less correlated to the target column features
        when the target argument is defined.

        Args:
            target (str): name of the column that it is under prediction
            top_N (int) : number of most of less correlated features
            ascending (boolean): False for most correlated and True for less correlated features

        Returns:
            None
        """
        corrmat = self.df.corr()

        if target is None:
            plt.figure(figsize=(12,9))
            sns.heatmap(corrmat, vmax=.8, square=True)
        else:
            plt.figure(figsize=(10,8))
            sns.heatmap(corrmat[[target]].sort_values(by=[target],ascending = ascending)[:top_N],
            vmin=-1,
            cmap='coolwarm',
            annot=True)
        
    def histograms(self, vars=[]):
        """Plots the histograms of a list of features

        Args:
            vars (list) : list of features
    
        Returns:
            None
        """
        for var in vars:
            plt.figure(figsize=(10,8))
            sns.distplot(self.df[var])
            
    def boxplots(self, target, vars):
        """Plots the boxplots of a list of categorical features with the target variable

        Args:
            target (str): name of the column that it is under prediction
            vars (list) : list of categorical features
    
        Returns:
            None
        """
        for var in vars:
            data = pd.concat([self.df[target], self.df[var]], axis=1)
            plt.figure(figsize=(10,8))
            fig = sns.boxplot(x=var, y=target, data=data)
    
    def scatterplots(self, target, vars):
        """Plots the scatterplots of a list of numerical features with the target variable

        Args:
            target (str): name of the column that it is under prediction
            vars (list) : list of numerical features
    
        Returns:
            None
        """
        for var in vars:
            data = pd.concat([self.df[target], self.df[var]], axis=1)
            plt.figure(figsize=(10,8))
            data.plot.scatter(x=var, y=target)
            
    def normality_check(self, var):
        """Plots checking the normality of a feature

        Args:
            var (str): name of the feature
    
        Returns:
            None
        """
        sns.distplot(self.df[var], fit=norm);
        fig = plt.figure(figsize=(10,8))
        res = stats.probplot(self.df[var], plot=plt)
