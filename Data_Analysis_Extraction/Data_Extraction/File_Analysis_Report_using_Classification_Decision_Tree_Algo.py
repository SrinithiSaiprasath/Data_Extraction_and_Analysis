# Import necessary libraries
import pandas as pd
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt
from joblib import load 
from sklearn.tree import plot_tree

csv_file_path = 'GPP_12.5_86.0.csv'  # Replace with the actual path to your CSV file
model_data = pd.read_csv('GPP_12.5_86.0.csv')

threshold = 0.8# Set an appropriate threshold for classification
model_data['Cyclone'] = np.where(model_data['GPP'] > threshold, 1, 0)

X_classification = model_data[['E_850', 'M_(RH)', 'I_sub', 'S_Val', 'TCHP']]
y_classification = model_data['Cyclone']

X_train_classification, X_test_classification, y_train_classification, y_test_classification = train_test_split(
    X_classification, y_classification, test_size=0.2, random_state=42
)
classification_model_decision_tree = DecisionTreeClassifier(random_state=42)
classification_model_decision_tree.fit(X_train_classification, y_train_classification)

classification_predictions_decision_tree = classification_model_decision_tree.predict(X_test_classification)

accuracy_classification_decision_tree = accuracy_score(y_test_classification, classification_predictions_decision_tree)
classification_report_result_decision_tree = classification_report(y_test_classification, classification_predictions_decision_tree)

print(f'Accuracy for Cyclone Classification (Decision Tree): {accuracy_classification_decision_tree}')
print('Classification Report (Decision Tree):')
print(classification_report_result_decision_tree)

joblib.dump(classification_model_decision_tree, 'cyclone_classification_model_decision_tree.joblib')

loaded_model = load('cyclone_classification_model_random_forest.joblib')

probabilities = loaded_model.predict_proba(X_test_classification)[:, 0]

threshold = 0.9

high_probability_cyclones = X_test_classification[probabilities > threshold]

dates_of_high_probability_cyclones = model_data.loc[high_probability_cyclones.index, 'Date']

print("Dates with High Probability of Cyclones:")
print(dates_of_high_probability_cyclones)
'''
'''

print("Number of trees (estimators):", loaded_model.n_estimators)
print("Feature importances:", loaded_model.feature_importances_)


print("Max depth:", loaded_model.max_depth)

# Access the first tree in the Random Forest
first_tree = loaded_model.estimators_[0]

# Option 1: Using get_params() method
tree_params = first_tree.get_params()
print("Tree Parameters:")   #full error 
print(tree_params) #full error venam indha line 


# Access basic information about the model
print("Classes:", loaded_model.classes_)
#print("Number of Features:", loaded_model.n_features_)
print("Number of Classes:", loaded_model.n_classes_)

# Access model parameters (including max_depth, max_features, criterion)
model_params = loaded_model.get_params()
print("Model Parameters:", model_params)

# Access the first tree in the Random Forest
first_tree = loaded_model.estimators_[0]

# Option 1: Using get_params() method
tree_params = first_tree.get_params()
print("Tree Parameters:")
print(tree_params)

# Option 2: Accessing attributes directly
tree_max_depth = first_tree.tree_.max_depth
tree_feature_importances = first_tree.feature_importances_
tree_n_features = first_tree.tree_.n_features

print(f"Max Depth of the Tree: {tree_max_depth}")
print(f"Feature Importances of the Tree: {tree_feature_importances}")
print(f"Number of Features in the Tree: {tree_n_features}")

# Accessing attributes of the Random Forest model
rf_n_features = loaded_model.n_features_in_
print(f"Number of Features in the Random Forest: {rf_n_features}")
