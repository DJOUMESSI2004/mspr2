
import pandas as pd
from sklearn.model_selection import train_test_split

# Charger le dataset
df = pd.read_csv('cleaned-covid19-data.csv')

# Spit en 80% train et 20% test 
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Sauvegarder
train.to_csv('train.csv', index=False)
test.to_csv('test.csv', index=False)

print('✅ Split terminé : train.csv et test.csv générés dans dataset/')
