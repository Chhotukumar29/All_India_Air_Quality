# Project Name: End to End Machine Learning Air Quality Project

# 1. Data Ingestion 
* Import the data with library 
* Laoding the data 
* Read the data

# 2. Data Clearning 
* Convert the data into a DataFrame.
* Extract the data from the DataFrame.
* Merge the data into the DataFrame.
* final_data is the our DataFrame.
 
# 3. EDA
* Check DataFrame summary
* Convert the dtype according to the values in the DataFrame
* Check the missing values(NaN) in the DataFrame
* Fill the missing values(NaN) in the DataFrame
* Check summary statistics of data
* Observation max value of AQI-IN
* Dropping AQI-IN that the greater 1000 from the DataFrame
* Univariate Analysis (distplot)
* Multivariate Analysis (heatmap plot)

# 4. Model Training
* LabelEncoder
* Preparing X and Y variables
* Dropping unnecessary clumns
* Train Test split the data
* Using OneHotEncoder and StandardScaler 
* Transforming the data
* Evaluate Function to give all metrics after model Training
* Implements RandomizedSearchCV to tune & evaluate multiple regression models
* Create table & sorts models by their R2 score (best to worst)
* Checking the accuracy of the models
* Plot "y_pred vs. y_test" visually checks how well predictions match actual values
* Pickle the best model using joblib library

# 5. Deployment with Streamlit 
* use streamlit for deployment (Streamlit run app.py)
* Loading the data model 
* Create function predictions with expanded features
* Create Air quality categorization function
* add title of the app
* Add Geographical and weather inputs
* Add user input to predict Air Quality (AQI) and category
