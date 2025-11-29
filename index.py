import h2o
from h2o.automl import H2OAutoML
import pandas as pd
from sklearn.model_selection import train_test_split
from tkinter import Tk, filedialog
# Step 1: Initialize H2O
h2o.init()
# Step 2: Upload Dataset
def upload_dataset():
root = Tk()
root.withdraw() # Hide the main Tkinter window
file_path = None
while not file_path: # Keep prompting until a file is selected
file_path = filedialog.askopenfilename(
title="Select Dataset",
filetypes=[("CSV Files", ".csv"), ("All Files", ".*")]
)
if not file_path:
print("No file selected. Please try again.")
root.destroy() # Close the Tkinter root window
return pd.read_csv(file_path)
df = upload_dataset()
# Check if dataset has required columns
required_columns = ['productid', 'userid', 'score']
if not all(column in df.columns for column in required_columns):
raise ValueError(f"Dataset must contain the following columns: {required_columns}")
# Rename columns for consistency
column_mapping = {
'productid': 'product_id',
'userid': 'user_id',
'score': 'rating'
}
df.rename(columns=column_mapping, inplace=True)
# Step 3: Handle Small Datasets (e.g., 10 rows)
if len(df) <= 10:
print("Warning: Dataset is very small. Results may not be meaningful.")
# Step 4: Clean and Validate Data
df.dropna(inplace=True) # Remove rows with missing values
print("Data after cleaning:")
print(df.head())
# Convert to H2O Frame
h2o_df = h2o.H2OFrame(df)
# Step 5: Specify Features and Target
x = ['user_id', 'product_id'] # Minimal features for small datasets
y = 'rating'
# Step 6: Train AutoML Model with Increased Runtime
aml = H2OAutoML(max_runtime_secs=300, seed=42) # Longer runtime for better
accuracy
aml.train(x=x, y=y, training_frame=h2o_df)
# Step 7: Evaluate the Best Model
leader = aml.leader
print("Best Model:", leader)
# Evaluate Model Performance
perf = leader.model_performance(test_data=h2o_df)
print("Model Performance:")
print(perf)
# Step 8: Generate Recommendations for All Users
all_users = df['user_id'].unique() # Get all unique users
all_products = df['product_id'].unique() # Get all unique products
# Create a DataFrame to store recommendations
recommendations = pd.DataFrame()
for user_id in all_users:
# Create User-Product Pairs
user_data = pd.DataFrame({
'user_id': [user_id] * len(all_products),
'product_id': all_products
})
# Convert to H2O Frame
user_h2o = h2o.H2OFrame(user_data)
# Predict for User
user_predictions = leader.predict(user_h2o).as_data_frame(use_multi_thread=True) #
Enable multi-threading
# Add Predictions to the User Data
user_data['predicted_rating'] = user_predictions['predict']
# Get Top-N Recommendations for the User
top_recommendations = user_data.sort_values(by='predicted_rating',
ascending=False).head(5) # Top 5
recommendations = pd.concat([recommendations, top_recommendations])
# Save All Recommendations
recommendations.to_csv("all_user_recommendations.csv", index=False)
print("Recommendations saved to all_user_recommendations.csv")
# Debug Outputs
print("Sample Recommendations:")
print(recommendations.head())
# Step 9: Shutdown H2O
h2o.shutdown(prompt=False)
# Additional Debugging and Metrics
print("Leaderboard of Models:")
print(aml.leaderboard)