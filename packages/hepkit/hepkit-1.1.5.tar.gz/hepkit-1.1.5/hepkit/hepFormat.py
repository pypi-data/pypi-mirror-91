import pandas as pd
import matplotlib.pyplot as plt

'''
Really cool color palette
'''
mc = [
    [35/255, 55/255, 59/255],
    [237/255, 138/255, 46/255],
    [131/255, 40/255, 0/255],
    [0/255, 123/255, 68/255],
    [107/255, 60/255, 79/255],
    [118/255, 93/255, 68/255],
    [62/255, 79/255, 51/255],
    [147/255, 161/255, 161/255]
]


def DefaultSetup(mc=999,mr=10):
  '''
  Personal preferences for plt.pyplot
  '''
  plt.rcParams['font.family'] = 'serif'
  plt.rcParams['font.weight'] = 'light'
  plt.rcParams['font.size'] = 16
  plt.rcParams['figure.figsize'] = [12,8]
  pd.options.display.max_columns = mc
  pd.options.display.max_rows = mr
