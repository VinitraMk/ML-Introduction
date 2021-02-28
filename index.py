import pandas as pd
import os
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return mae

input_file_path = "./input"
app_data= pd.read_csv(os.path.join(input_file_path,"train.csv"))
y = app_data.SalePrice
features = ['LotArea', 'YearBuilt','1stFlrSF','2ndFlrSF','FullBath','BedroomAbvGr','TotRmsAbvGrd']
X = app_data[features]

train_X, val_X, train_y, val_y =  train_test_split(X,y,random_state=0)

model = DecisionTreeRegressor()
model.fit(train_X,train_y)

val_predictions = model.predict(val_X)
print(mean_absolute_error(val_y,val_predictions))

for max_leaf_nodes in [5, 50, 500, 5000]:
    my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
    print("Max leaf nodes: %d \t\t Mean Absolute Error: %d"%(max_leaf_nodes,my_mae))
