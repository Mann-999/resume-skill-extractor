import pandas as pd
import glob

files = glob.glob('data/*.csv')
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
df.to_csv('data/career_dataset.csv', index=False)
print(df.shape)
print(df['role'].value_counts())