# 📦 E-Commerce Product Recommendation System using H2O AutoML

This project implements an **automatic product recommendation system** using **H2O AutoML** to predict product ratings and generate Top-N recommendations for every user in the dataset.

The script:
- Prompts the user to **upload a CSV file** (via Tkinter GUI)
- Cleans and validates the dataset
- Trains **H2O AutoML** for rating prediction
- Predicts ratings for every `(user_id, product_id)` pair
- Outputs **Top-5 recommendations per user**
- Saves results into `all_user_recommendations.csv`

---

## 🚀 Features

- Automatic dataset upload via GUI  
- AutoML training with leaderboard  
- Built-in validation for required columns  
- Supports very small datasets (prints warning for ≤10 rows)  
- Multi-threaded prediction  
- Generates user-wise recommendations  
- Saves results to CSV  
- Full H2O shutdown and cleanup  

---

## 📂 Dataset Requirements

Your CSV file **must contain** these columns:

