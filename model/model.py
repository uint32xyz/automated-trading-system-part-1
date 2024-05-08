import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Column names, 
vars = ['VWRSI', 'RSI','cmc_rank','num_market_pairs','sma_5', 'sma_10', 'sma_20', 'pvt', 'volume','volume_change_24h' , 'percent_change_7d','MACD', 'MACD_signal','EMA_9','EMA_21','bollinger_hband','bollinger_lband','OBV','VPT']

# Get data
data = pd.read_csv('processed_data.csv')
# Ensure correct data type for the timestamp column (if it's not already in datetime format)
data['timestamp'] = pd.to_datetime(data['timestamp'])
# Sort the data by the timestamp column in ascending order
data = data.sort_values(by='timestamp')
# Drop null values
data = data.dropna()
# Define the split proportion between training and testing data
test_size = 0.2 
# Calculate the index at which to split
split_idx = int(len(data) * (1 - test_size))
# Split the features and target variable into train and test sets
X_train, X_test = data[vars].iloc[:split_idx], data[vars].iloc[split_idx:]
y_train, y_test = data['y'].iloc[:split_idx], data['y'].iloc[split_idx:]
# Apply SMOTE for addressing class imbalance in training data only
smote = SMOTE()
X_resampled_smote, y_resampled_smote = smote.fit_resample(X_train, y_train)
# Scaling the features
scaler_X = StandardScaler()
X_scaled_train = scaler_X.fit_transform(X_resampled_smote)
X_scaled_test = scaler_X.transform(X_test)
#convert back to dataframe
X_scaled_train = pd.DataFrame(X_scaled_train, columns=vars)
X_scaled_test = pd.DataFrame(X_scaled_test, columns=vars)
# Model Training
model = RandomForestClassifier(n_jobs=1, n_estimators=60, class_weight={0: 1, 1: 1}, random_state=5, max_depth=100, min_samples_split=5)
model.fit(X_scaled_train, y_resampled_smote)
probabilities = model.predict_proba(X_scaled_test)
# Apply threshold to the probabilities for the positive class (e.g., class 1)
threshold = 0.60
y_pred = (probabilities[:, 1] >= threshold).astype(int)

