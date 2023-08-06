# Any changes to the anomaly library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test


import unittest

from anomaly import Anomaly


import pandas as pd
df = pd.DataFrame({'ano_mes' :  ['2020_jan', '2020_fev','2020_mar', '2020_abr','2020_mai','2020_jun','2020_jul',
                         '2020_ago','2020_set','2020_out','2020_nov','2020_dez','2021_jan'],
           'val_agg' :  [10, 12, 8, 15, 17, 15, 17, 20, 23, 18, 20, 20, 25],
           'tipo_dado': ['historical','historical','historical','historical','historical',
                         'historical','historical','historical','historical','historical',
                         'historical', 'historical','target']})


class TestAnomalyClass(unittest.TestCase):
    def setUp(self):
        self.anomaly = Anomaly(_index = df['ano_mes'], _values = df['val_agg'], _type = df['tipo_dado'])

    def test_meancalculation(self):
        self.anomaly.calculate_mean()
        
        mean_pandas = df[df['tipo_dado'] == 'historical']['val_agg'].mean()
        
        self.assertEqual(self.anomaly.mean, mean_pandas, 'incorrect mean')
        
    def test_stdevcalculation(self):
        self.anomaly.calculate_stdev()
        
        stdev_pandas =  df[df['tipo_dado'] == 'historical']['val_agg'].std()
        
        self.assertEqual(self.anomaly.stdev, stdev_pandas, 'incorrect standard deviation')
        
    
    def test_confidenceinterval(self):
        self.anomaly.calculate_mean()
        self.anomaly.calculate_stdev()
        self.anomaly.calculate_confidence_interval()
        
        mean_pandas = df[df['tipo_dado'] == 'historical']['val_agg'].mean()
        stdev_pandas =  df[df['tipo_dado'] == 'historical']['val_agg'].std()
        
        
        lims = [1, 2, 3]
        
        for i in lims:
            
            lower_limit_pandas = mean_pandas - i*stdev_pandas
            higher_limit_pandas = mean_pandas + i*stdev_pandas 

            if lower_limit_pandas < 0:
                lower_limit_pandas = 0

            self.assertEqual(self.anomaly.CI[i-1][0], lower_limit_pandas, 'incorrect confidence interval {}sd lower limit ')
            self.assertEqual(self.anomaly.CI[i-1][1], higher_limit_pandas, 'incorrect confidence interval {}sd higher limit ')

    def test_target(self):        
        target_pandas =  df[df['tipo_dado'] == 'target']['val_agg'].values[0]
        
        self.anomaly.obtain_target()
        self.assertEqual(self.anomaly.target, target_pandas, 'target did not match')
        
    def test_anomalydetection(self):
        self.anomaly.calculate_mean()
        self.anomaly.calculate_stdev()
        self.anomaly.calculate_confidence_interval()  
        self.anomaly.obtain_target()
        self.anomaly.identify_anomaly()
        
        
        lims = [1, 2, 3]
        
        for i in lims:
            print('>>> CI_{}sd {}'.format(i, self.anomaly.CI[i-1]))
            
            results = ['Anomaly', 'Not_anomaly', 'Not_anomaly']
            self.assertEqual(self.anomaly.result[i-1], results[i-1], 'anomaly not detected')


if __name__ == '__main__':
    unittest.main()