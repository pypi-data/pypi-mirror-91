#%%writefile anomaly.py

import statistics

class Anomaly():
    '''
    Anomaly detector under statistical method
    
    Attributes:
       _index (obj): list of year_month
       _values (float): agregated values to detect
       _type (obj): list identifying values as: 'historical' or 'target'
       
       
    '''
    def __init__(self, _index, _values, _type, _limits = [1, 2, 3]):
        
        self.values = _values
        self.index = _index
        self.type = _type
        
        self.mean = 0
        self.stdev = 0
        
        self.target = 0
        
        self.limits = _limits

        self.CI = []        

        self.result = []
        
    def calculate_mean(self):
        
        self.mean = statistics.mean(self.values[self.type == 'historical'])
        
        return self.mean
    
    
    def calculate_stdev(self):
        
        self.stdev = statistics.stdev(self.values[self.type == 'historical'])
        
        return self.stdev
    
    
    def calculate_confidence_interval(self):
        ''' 
        Calculate confidence interval iterating over the limits list.
        
        eg. limit = 1 :> superior limit = mean + 1 times standard deviation
        '''
        for limit in self.limits:
            
            lim_inf = self.mean - self.stdev*limit
            lim_sup = self.mean + self.stdev*limit
                
            if lim_inf < 0: # Zeroing negative lower confidence interval
                lim_inf = 0
        
            self.CI.append([lim_inf, lim_sup])

        return self.CI
    
    def obtain_target(self):
        
        self.target = self.values[self.type == 'target'].values[0]
        self.target_date = self.index[self.type == 'target'].values[0]
    
    
    def identify_anomaly(self):
        'Anomaly based on superior limit only in v0.01'
        self.result = []
                
        for i in range(0, len(self.limits)): #Iterates over limits number
        
            if self.target > self.CI[i][1]:            
                self.result.append('Anomaly')
            else:            
                self.result.append('Not_anomaly')

        return self.result
    
    
    def print_data(self):
        import pandas as pd
        print('-------------------')
        data = pd.DataFrame({'vl_agg' : self.values,
                             'index' : self.index,
                             'type': self.type})
        print(data)
        
        return data
