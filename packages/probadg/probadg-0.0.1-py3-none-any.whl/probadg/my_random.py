import numpy as np 
import pandas as pd

#------------ Random Object Class----------
class RandomObject(object):
    '''Class of object that simulates a wide variety of random objects'''

    def __init__(self,probs=None,results=None):
        '''Initiates the RandomObject instance
        Arguments:
            probs: list of probabilities associated to the results
            results: list of the names of the results of the random object
        '''
        assert len(probs)==len(results), 'There is a missmatch between the probs and results'
        assert np.array(probs).sum()==1, "The probabilities don't add up to 1"
        self.probabilities = np.array(probs)
        self.results = np.array(results)
    
    def get_probablities(self):
        '''Get the probabilities of the RandomObject'''
        return self.probabilities

    def set_probabilities(self,new_probabilities):
        ''' Sets the probabilities of the object'''
        assert len(new_probabilities)==self.get_results() and np.array(new_probabilities).sum()==1,'The new probabilities are not valid'
        self.probabilities = np.array(new_probabilities)
    
    def get_results(self):
        '''Get the results of the RandomObject instance'''
        return self.results
    
    def set_results(self,new_results):
        '''Set new list of results to the RandomObject'''
        assert len(new_results)==len(self.get_results()),'Results introduced are not valid'
        self.results = new_results

    def get_generator(self,throws=2):
        '''Generates a RandomObject generator
        Arguments:
            throws: the number of throws or iterations of the random object
        
        Output: generator object that yields all possible combinations for the 
                RandomObject, giving a tuple with dictionary with the number of 
                appearances of each result given the number of throws, and the 
                probability of that event
        '''
        results = self.get_results() #store the results of the RandomObject
        num_results = len(results)
        for i in range(num_results**throws):
           
            #Create a dictionary with a count of the results
            generated = {result:0 for result in results}
            for j in range(throws):
                for k in range(num_results):
                    if i//(num_results**j)%num_results == k:
                        generated[results[k]] += 1
           
           #Calculate the probability of that specific throw
            probability_throw = (self.get_probablities()**np.array(list(generated.values()))).prod()
           
            yield (generated,probability_throw)

    def see_table(self,throws=2):
        '''Produces a table with all the possible results given the number of
        throws

        Arguments:
            throws: number of throws simulated
        '''

        # Create a data frame to store the results of each throw
        column_names = self.get_results().tolist()
        index_names = ['Combination '+str(throw+1) for throw in range(throws)]+['Total']
        df = pd.DataFrame(columns=column_names,index=index_names)
        
        # Create a generator of the RandomObject
        random_object_generator = self.get_generator(throws)

        # Fill the table with the results of all possible outcomes
        throw = 0 
        
        while True: 
            #Exhaust all possible options
            try:
                throw += 1
                (generated,probability) = next(random_object_generator)
                df.loc['Combination '+str(throw),'Probability'] = probability
                for result in generated.keys():
                    df.loc['Combination '+str(throw),result] = generated[result]
            #Get totals
            except:
                df.loc['Total','Probability'] = df['Probability'].sum()
                for result in generated.keys():
                    df.loc['Total',result] = df[result].sum()
                return df.sort_index()
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
def calculate_bayes(prob_a,sensitivity,specificity,b=True):
    '''Calculates the Bayes algorithm for an event A and a test B
    prob_a: float between 0 and 1 that represents the probability of event A
    sensitivity: probability of B given that A occurred
    specificity: probability of not B given that not A occured
    '''
    
    # Calculating the complements of the information we know
    prob_nota = 1-prob_a
    prob_notb_a = 1-sensitivity # probability of not B given A
    prob_b_nota = 1-specificity # probability of B given not A
    
    # If the test is B:
    if b:
        prob_a_join_b = prob_a*sensitivity
        prob_nota_join_b = prob_nota*prob_b_nota
        prob_b = prob_a_join_b+prob_nota_join_b
        prob_a_b = prob_a_join_b/prob_b       #probability of A given B
        prob_nota_b = prob_nota_join_b/prob_b #probability of not A given B
        return (prob_a_b,prob_nota_b)
    
    # If the test is not B:
    else:
        prob_a_join_notb = prob_a*prob_notb_a
        prob_nota_join_notb = prob_nota*specificity
        prob_notb = prob_a_join_notb+prob_nota_join_notb
        prob_a_notb = prob_a_join_notb/prob_notb       # probability of A given not B
        prob_nota_notb = prob_nota_join_notb/prob_notb #probability of not A given not B
        return (prob_a_notb,prob_nota_notb)




