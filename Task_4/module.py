import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

#global constants
SALES_DATA_PATH = "/Users/rajaallmdar/Desktop/Cognizant AI Virual Job Experience/Data/sales.csv"
STOCK_DATA_PATH = "/Users/rajaallmdar/Desktop/Cognizant AI Virual Job Experience/Data/sensor_stock_levels.csv"
TEMP_DATA_PATH = "/Users/rajaallmdar/Desktop/Cognizant AI Virual Job Experience/Data/sensor_storage_temperature.csv"
TARGET_VARIABLE = "estimated_stock_pct"
CROSS_VALIDATION_FOLDS = 10
TRAIN_SIZE = 0.75

#load data function
def load_data(path: str):
    df = pd.read_csv(path)
    df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
    return df

#create target and predictors function
def create_target_and_predictors(data, target):
    if target not in data.columns:
        raise Exception(f"Target: {target} is not present in the data")
    X = data.drop(columns=[target])
    y = data[target]
    return X, y

#train algorithm with cross validation function
def train_algorithm_with_cross_validation(X, y):
    accuracy = []
    for fold in range(CROSS_VALIDATION_FOLDS):
        model = RandomForestRegressor()
        scaler = StandardScaler()
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=TRAIN_SIZE, random_state=42)
        scaler.fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)
        trained_model = model.fit(X_train, y_train)
        y_pred = trained_model.predict(X_test)
        mae = mean_absolute_error(y_true=y_test, y_pred=y_pred)
        accuracy.append(mae)
        print(f"Fold {fold + 1}: MAE = {mae:.3f}")
    print(f"Average MAE: {(sum(accuracy) / len(accuracy)):.2f}")
    return trained_model

#feature importance function
def plot_feature_importance(model, X):
    features = [i.split("__")[0] for i in X.columns]
    importances = model.feature_importances_
    indices = np.argsort(importances)

    fig, ax = plt.subplots(figsize=(10, 20))
    plt.title('Feature Importances')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.show()

#main function
def main():
    sales_df = load_data(SALES_DATA_PATH)
    stock_df = load_data(STOCK_DATA_PATH)
    temp_df = load_data(TEMP_DATA_PATH)
    X, y = create_target_and_predictors(sales_df, TARGET_VARIABLE)
    trained_model = train_algorithm_with_cross_validation(X, y)
    plot_feature_importance(trained_model, X)

if __name__ == "__main__":
    main()
