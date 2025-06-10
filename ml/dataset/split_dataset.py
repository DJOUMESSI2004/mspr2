
import pandas as pd
from sklearn.model_selection import train_test_split

# Charger le dataset
df = pd.read_csv('clean_covid19_data_v2.csv')

# Spit en 80% train et 20% test 
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Sauvegarder
train.to_csv('train2.csv', index=False)
test.to_csv('test2.csv', index=False)

print('✅ Split terminé : train.csv et test.csv générés dans dataset/')
