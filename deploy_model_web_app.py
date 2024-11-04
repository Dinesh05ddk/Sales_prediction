import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

st.title("Sales Prediction Model")

# Specify model path
model_path = 'trained_sales_model.pkl'
st.write("Loading model from:", model_path)

# Load the model
try:
    with open(model_path, 'rb') as model_file:
        loaded_model = pickle.load(model_file)
    st.write("Model loaded successfully.")
except FileNotFoundError:
    st.error("Model file not found. Please check the file path.")
    st.stop()

# List of expected columns based on the model's requirements
expected_columns = [
    'Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Establishment_Year', 
    'H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'H11', 
    'H12', 'H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19', 'H20', 'H21', 
    'H22', 'H23', 'H24', 'H25', 'H26', 'H27', 'H28', 'H29', 'H30', 'H31', 
    'H32', 'H33', 'H34', 'H35', 'H36', 'H37', 'H38', 'H39', 'H40', 'H41', 
    'H42', 'H43', 'H44', 'H45', 'H46', 'H47', 'H48', 'H49', 'Item_Fat_Content_Edible', 
    'Item_Fat_Content_Low Fat', 'Item_Fat_Content_Regular', 'Item_Type_Drink', 
    'Item_Type_Food', 'Item_Type_Non_Consumables', 'Outlet_Identifier_OUT010', 
    'Outlet_Identifier_OUT013', 'Outlet_Identifier_OUT017', 'Outlet_Identifier_OUT018', 
    'Outlet_Identifier_OUT019', 'Outlet_Identifier_OUT027', 'Outlet_Identifier_OUT035', 
    'Outlet_Identifier_OUT045', 'Outlet_Identifier_OUT046', 'Outlet_Identifier_OUT049', 
    'Outlet_Size_High', 'Outlet_Size_Medium', 'Outlet_Size_Small', 
    'Outlet_Location_Type_Tier 1', 'Outlet_Location_Type_Tier 2', 'Outlet_Location_Type_Tier 3', 
    'Outlet_Type_Grocery Store', 'Outlet_Type_Supermarket Type1', 
    'Outlet_Type_Supermarket Type2', 'Outlet_Type_Supermarket Type3'
]

# Function to preprocess and align input data with expected columns
def preprocess_input(data):
    # Apply necessary transformations to categorical columns before one-hot encoding
    data['Item_Fat_Content'] = data['Item_Fat_Content'].replace({
        'Low Fat': 'Low Fat', 'Regular': 'Regular', 'LF': 'Low Fat', 'reg': 'Regular', 'low fat': 'Low Fat'
    })
    
    # Apply one-hot encoding to categorical columns
    data = pd.get_dummies(data, columns=[
        'Item_Fat_Content', 'Item_Type', 'Outlet_Identifier', 
        'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type'
    ], drop_first=False)
    
    # Reindex to ensure the DataFrame has all expected columns in the right order
    input_data = data.reindex(columns=expected_columns, fill_value=0)
    
    return input_data

# Sample data for prediction
sample_data = pd.DataFrame({
    "Item_Weight": [10.0],
    "Item_Fat_Content": ["Low Fat"],
    "Item_Visibility": [0.05],
    "Item_MRP": [200.0],
    "Outlet_Establishment_Year": [2004],
    "Item_Type": ["Food"],
    "Outlet_Identifier": ["OUT013"],
    "Outlet_Size": ["Medium"],
    "Outlet_Location_Type": ["Tier 2"],
    "Outlet_Type": ["Supermarket Type1"]
})

# Define options for categorical variables
fat_content_options = ["Low Fat", "Regular"]
item_type_options = ["Food", "Drink", "Non-Consumables"]
outlet_identifier_options = ["OUT010", "OUT013", "OUT017", "OUT018", "OUT019", "OUT027", "OUT035", "OUT045", "OUT046", "OUT049"]
outlet_size_options = ["Small", "Medium", "High"]
outlet_location_type_options = ["Tier 1", "Tier 2", "Tier 3"]
outlet_type_options = ["Grocery Store", "Supermarket Type1", "Supermarket Type2", "Supermarket Type3"]

# Create a form to input data
st.write("### Input Features for Prediction")
input_data = {}

for col, value in sample_data.items():
    if col == "Item_Fat_Content":
        input_data[col] = st.selectbox(f"{col}", options=fat_content_options)
    elif col == "Item_Type":
        input_data[col] = st.selectbox(f"{col}", options=item_type_options)
    elif col == "Outlet_Identifier":
        input_data[col] = st.selectbox(f"{col}", options=outlet_identifier_options)
    elif col == "Outlet_Size":
        input_data[col] = st.selectbox(f"{col}", options=outlet_size_options)
    elif col == "Outlet_Location_Type":
        input_data[col] = st.selectbox(f"{col}", options=outlet_location_type_options)
    elif col == "Outlet_Type":
        input_data[col] = st.selectbox(f"{col}", options=outlet_type_options)
    else:
        # For numeric inputs
        input_data[col] = st.number_input(f"{col}", value=float(value))

# Convert input_data to DataFrame
input_df = pd.DataFrame([input_data])

# Preprocess categorical data by one-hot encoding
input_df = pd.get_dummies(input_df)

# Align input columns with model's expected features
expected_columns = loaded_model.get_booster().feature_names
input_df = input_df.reindex(columns=expected_columns, fill_value=0)

# Make predictions
if st.button("Predict Sales"):
    prediction = loaded_model.predict(input_df)
    st.success(f"Predicted Sales: ${prediction[0]:.2f}")

    # Optional: Visualize prediction
    st.write("### Prediction Visualization")
    fig, ax = plt.subplots()
    ax.bar(["Predicted Sales"], [prediction[0]])
    ax.set_ylabel("Sales Amount")
    st.pyplot(fig)
