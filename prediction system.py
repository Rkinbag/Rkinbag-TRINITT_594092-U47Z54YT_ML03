import numpy as np
import pickle 
import sklearn
print(sklearn.__version__)
loaded_model=pickle.load(open('D:/ml model/trained_model1.sav','rb'))
input_data=(50.05,	100.23,	82.01,	80.36	,5.98,	104.63,	27.38)
input_data_as_numpy_array = np.asarray(input_data)
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
prediction = loaded_model.predict(input_data_reshaped)
labels_mapping = {0:'rice',1:'maize', 2:'chickpea', 3:'kidneybeans', 4:'pigeonpeas',
       5:'mothbeans', 6:'mungbean', 7:'blackgram', 8:'lentil', 9:'pomegranate',
       10:'banana', 11:'mango', 12:'grapes', 13:'watermelon', 14:'muskmelon', 15:'apple',
       16:'orange', 17:'papaya', 18:'coconut', 19:'cotton', 20:'jute',21: 'coffee'}

def decode_labels(encoded_value):
    return labels_mapping[encoded_value]

fin_pred = decode_labels(prediction[0])
print(fin_pred)

