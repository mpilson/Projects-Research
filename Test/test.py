import numpy as np
import pandas as pd
a = np.array([1,2,3])
b = np.array([1,2,3])
#print(a@b)
#print(np.dot(a,b))


df = pd.read_csv('boston.csv')
print(df.head)

print(b[:len(b)])


