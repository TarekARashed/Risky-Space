from keras.models import Sequential
from keras.layers import Dense
from pathlib import Path
import pandas as pd
import numpy as np
from csv import reader
from sklearn.model_selection import train_test_split
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# load the dataset
Current_Directory = os.getcwd()
TFIDF_Features_Path=os.path.join(Current_Directory, "TFIDF_Features", "")
TFidf_Data_Feautres=Path(TFIDF_Features_Path, 'tf_idf').with_suffix('.csv')
Tfidf_data = pd.read_csv(TFidf_Data_Feautres, header = None)

Features_Rows=len(Tfidf_data.axes[0]) 
Features_Cols=len(Tfidf_data.axes[1])

Classes_Path=os.path.join(Current_Directory, "TFIDF_Features", "")
Data_class_For_Tfidf_features=Path(Classes_Path, 'Classes').with_suffix('.csv')
Data_Class = pd.read_csv(Data_class_For_Tfidf_features, header = None)
Class_Rows=len(Data_Class.axes[0])
Class_Cols=len(Data_Class.axes[1])


Tfidf_data= np. zeros((Features_Rows-1, Features_Cols-1), float)
tfidf_class = np. zeros((Features_Rows-1, Class_Cols), int)

with open(TFidf_Data_Feautres, 'r') as read_obj:
   
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    i=0
    for row in csv_reader:
        m=0
        for j in range(1, len(row)):
            Tfidf_data[i][m]=row[j]
            m+=1
        i+=1
vocab=[]
for row in header:
    if row !='':
        vocab.append(row)
with open(Data_class_For_Tfidf_features, 'r') as read_obj:
    csv_reader = reader(read_obj)
    header = next(csv_reader)
    i=0
    for row in csv_reader:
        m=0
        for j in range(1, len(row)):
            tfidf_class[i][m]=row[j]
            m+=1
        i+=1
    
X = Tfidf_data
Y = tfidf_class
print(X.shape, Y.shape)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
model = Sequential()
model.add(Dense(100, input_dim=600, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(5, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=150, batch_size=10, verbose=0)
predictions = (model.predict(X) > 0.5).astype(int)
for i in range(5):
	print((predictions[i], Y[i]))


statement = input("Please enter your statement :\n")
#tokens=word_tokenize(statement)
tokens = list(statement.split(" "))


