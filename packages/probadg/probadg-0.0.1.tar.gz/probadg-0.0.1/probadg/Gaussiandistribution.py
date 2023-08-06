#-------------------------------- Gaussian Class -------------------------------
import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution
import numpy as np

class Gaussian(Distribution):
    """ Gaussian distribution class for calculating and 
    visualizing a Gaussian distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file
            
    """
    def __init__(self, mu = 0, sigma = 1):
        
        Distribution.__init__(self,mu,sigma)


    
    def calculate_mean(self):
    
        """Method to calculate the mean of the data set.
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        mean = float(sum(self.data)/len(self.data))
        self.mean = mean
        return self.mean


    def calculate_stdev(self, sample=True):

        """Method to calculate the standard deviation of the data set.
        
        Args: 
            sample (bool): whether the data represents a sample or population
        
        Returns: 
            float: standard deviation of the data set
    
        """
        numerator = np.power((np.array(self.data)-self.mean),2).sum()
        if sample:
            std = np.sqrt(numerator/(len(self.data)-1))
        else:
            std = np.sqrt(numerator/len(self.data))
        self.stdev = std
        return self.stdev
        


    def plot_histogram(self):
        """Method to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        plt.figure(figsize=(10,5))
        plt.hist(self.data,bins=30,color='teal')
        plt.xlabel('Data')
        plt.ylabel('Frequency')
        plt.title('Distribution of the Data')
        plt.show()
        # TODO: Plot a histogram of the data_list using the matplotlib package.
        #       Be sure to label the x and y axes and also give the chart a title
        
                
        
    def pdf(self, x):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            x (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        return (1/(self.stdev*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-self.mean)\
                                                             /self.stdev)**2)
        # TODO: Calculate the probability density function of the Gaussian distribution
        #       at the value x. You'll need to use self.stdev and self.mean to do the calculation       

    def plot_histogram_pdf(self, n_spaces = 50):

        """Method to plot the normalized histogram of the data and a plot of the 
        probability density function along the same range
        
        Args:
            n_spaces (int): number of data points 
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        #TODO: Nothing to do for this method. Try it out and see how it works.

        min_range = min(self.data)
        max_range = max(self.data)
        
         # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=.5)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normed Histogram of Data')
        axes[0].set_ylabel('Density')

        axes[1].plot(x, y)
        axes[1].set_title('Normal Distribution for \n Sample Mean and Sample Standard Deviation')
        axes[0].set_ylabel('Density')
        plt.show()

        return x, y
    
    def __add__(self,other):
        '''Function to add together two Gaussian distributions
        
        Arguments:
            other (Gaussian): a Gaussian instance
        
        Output:
            Gaussian: Gaussian distribution
        '''
        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = np.sqrt(self.stdev**2 + other.stdev**2)
        
        return result
    
    def __repr__(self):
        '''Function to output the characteristics of the Gaussian instance
        
        Arguments:
            None
        Output:
            string: characteristic of the Gaussian
        '''
        return 'Mean {}, Standard Deviation {}'.format(self.mean,self.stdev)

