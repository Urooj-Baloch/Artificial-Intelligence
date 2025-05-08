import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

np.random.seed(42)

data = {
    'square_footage': np.random.randint(800, 4000, 500),
    'bedrooms': np.random.randint(1, 6, 500),
    'bathrooms': np.round(np.random.uniform(1, 4, 500), 1),
    'age': np.random.randint(0, 50, 500),
    'neighborhood': np.random.choice(['Downtown', 'Suburb', 'Rural', 'Urban'], 500),
    'price': np.random.randint(100000, 800000, 500)
}

df = pd.DataFrame(data)

df.loc[np.random.choice(df.index, 20), 'bedrooms'] = np.nan
df.loc[np.random.choice(df.index, 15), 'bathrooms'] = np.nan
df.loc[np.random.choice(df.index, 10), 'age'] = np.nan

df['bedrooms'] = df['bedrooms'].fillna(df['bedrooms'].median())
df['bathrooms'] = df['bathrooms'].fillna(df['bathrooms'].median())
df['age'] = df['age'].fillna(df['age'].median())

plt.figure(figsize=(12, 8))
sns.pairplot(df[['square_footage', 'bedrooms', 'bathrooms', 'age', 'price']])
plt.show()

plt.figure(figsize=(10, 6))
sns.boxplot(x='neighborhood', y='price', data=df)
plt.show()

corr_matrix = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.show()

df['price_per_sqft'] = df['price'] / df['square_footage']
df['bed_bath_ratio'] = df['bedrooms'] / df['bathrooms']
df['age_category'] = pd.cut(df['age'], bins=[-1, 5, 20, 50], labels=['New', 'Medium', 'Old'])

X = df.drop('price', axis=1)
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ['square_footage', 'bedrooms', 'bathrooms', 'age', 'price_per_sqft', 'bed_bath_ratio']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

categorical_features = ['neighborhood', 'age_category']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

rf_model = Pipeline(steps=[('preprocessor', preprocessor),
                         ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))])
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

lr_model = Pipeline(steps=[('preprocessor', preprocessor),
                         ('regressor', LinearRegression())])
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

def evaluate_model(name, y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    print(f"{name} Evaluation:")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.2f}\n")

evaluate_model("Random Forest", y_test, rf_pred)
evaluate_model("Linear Regression", y_test, lr_pred)

preprocessor.fit(X)
feature_names = numeric_features.copy()
ohe_categories = preprocessor.named_transformers_['cat'].named_steps['onehot'].categories_
for i, cat in enumerate(categorical_features):
    for level in ohe_categories[i]:
        feature_names.append(f"{cat}_{level}")

importances = rf_model.named_steps['regressor'].feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(12, 8))
plt.bar(range(len(importances)), importances[indices], align="center")
plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=90)
plt.tight_layout()
plt.show()

new_house = pd.DataFrame({
    'square_footage': [2000],
    'bedrooms': [3],
    'bathrooms': [2.0],
    'age': [10],
    'neighborhood': ['Suburb'],
    'price_per_sqft': [0],
    'bed_bath_ratio': [0],
    'age_category': ['Medium']
})

new_house['price_per_sqft'] = 0
new_house['bed_bath_ratio'] = new_house['bedrooms'] / new_house['bathrooms']

predicted_price = rf_model.predict(new_house)
print(f"Predicted price for new house: ${predicted_price[0]:,.2f}")
