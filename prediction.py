import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from joblib import dump


with open('suzuki_colombia_filtered.json', 'r') as json_file:
    data = json.load(json_file)


df = pd.json_normalize(data)
# tratamiento de datos
df['price'] = df['price'].replace(0, None)
df['displacement'] = df['displacement'].str.extract(r'(\d+\.?\d*)').astype(float)
df['compression'] = df['compression'].str.extract(r'(\d+\.?\d*)').astype(float)
df[['bore', 'stroke']] = df['bore_stroke'].str.extract(r'(\d+\.?\d*) x (\d+\.?\d*)').astype(float)
df['power'] = df['power'].str.extract(r'(\d+\.?\d*)').astype(float)
df['torque'] = df['torque'].str.extract(r'(\d+\.?\d*)').astype(float)




X = df[['displacement', 'engine', 'compression', 'bore','stroke', 'fuel_system', 'cooling', 'power', 'torque', 'front_suspension']]
y = df['price']

X = X[~y.isnull()]
y = y[~y.isnull()]

categorical_fts = ['engine', 'fuel_system', 'cooling', 'front_suspension']
numerical_fts = ['displacement', 'compression', 'bore', 'stroke', 'power', 'torque']

# Create transformers
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),  # Impute missing values
    ('scaler', StandardScaler())  # Scale numeric features
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute missing values
    ('onehot', OneHotEncoder(handle_unknown='ignore'))  # Encode categories
])

# Combine into a ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_fts),
        ('cat', categorical_transformer, categorical_fts)
    ]
)

pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor())
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline.fit(X_train, y_train)

predictions = pipeline.predict(X_test)



print("Model score:", pipeline.score(X_test, y_test))
print("Predictions:", predictions)

dump(pipeline, 'precios_suzuki.pkl')  # guardar el modelo