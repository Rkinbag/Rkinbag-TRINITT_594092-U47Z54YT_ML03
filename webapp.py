import numpy as np
import pickle
import streamlit as st
import pandas as pd
from PIL import Image

loaded_model=pickle.load(open('trained_model3.sav','rb'))

def crop_prediction(input_data):
    

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
    return fin_pred
 
def main():
    
    
    st.title('Crop Prediction Web App')
    with st.sidebar: 
        st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
        st.title("Welcome!!!")
        choice = st.radio("Navigation", ["Check the crop type","Know the Perfect Fertilizer for you","Know about NPK","Dont know Rainfall in your area?","Want to know selling price of your crop?"])
        st.info("This project application helps you to predict crop type suitable for your soil,further it tell you the correct NPK Ratoi for your fertilizer which is very essential and it also tell you Minimum and Maximum Selling Price for Major Crops(Primarlity Grains) for your regions mandi!!")
    
    
    if choice == "Check the crop type":
    
        temperature = st.slider('Temperature of your town', 0.0, 50.0)
        humidity = st.slider('humidity in your town', 0.0, 100.0)
        ph = st.slider('Ph of your soil', 0.0, 11.0)
        rainfall = st.slider('Rainfall in your area, how much it rain in cm', 0.0, 400.0)


        diagnosis = ''
        if st.button('Predict the crop type'):
            with st.spinner("Predicting crop type..."):
                diagnosis = crop_prediction([temperature, humidity, ph, rainfall])
        st.success(diagnosis)
    if choice == "Know the Perfect Fertilizer for you":
        df=pd.read_excel('npk.xlsx')
        st.title("The Correct NPK Ratio for you!!!")
        unique_zones = df["Agroclimatic zone"].unique()
        st.caption(":red[Only for Major crops]")
        st.caption("Select the region if your state does not show in dropdown")

        selected_zone = st.selectbox("Agroclimatic zone", unique_zones)

        mask = (df["Agroclimatic zone"] == selected_zone)
        unique_soils = df[mask]["Soil"].unique()

        selected_soil = st.selectbox("Soil Type", unique_soils)

        mask = (df["Agroclimatic zone"] == selected_zone) & (df["Soil"] == selected_soil)
        unique_crops = df[mask]["crop"].unique()

        selected_crop = st.selectbox("crop", unique_crops)

        mask = (df["Agroclimatic zone"] == selected_zone) & (df["Soil"] == selected_soil) & (df["crop"] == selected_crop)
        npk_ratios = df[mask]["NPK Ratio"].values

        if npk_ratios.size > 0:
            npk_ratio = npk_ratios[0]
            st.write("NPK Ratio:", npk_ratio)

        else:
            st.write("No NPK ratio found for the selected combination of values.")


    if choice == "Know about NPK":
        st.title("Fertilizer Numbers – What Is NPK") 
        st.image("https://www.gardeningknowhow.com/wp-content/uploads/2020/11/npk-made-of-mineral-fertilizers.jpg")   
        st.write("Knowing what the label on a bag of fertiliser says is helpful if you are just starting out with gardening. Before putting a fertiliser in your garden, it's critical to comprehend the three figures on the label, such as 10-20-10..") 
        st.write("## What Do the Numbers on Fertilizer Mean?")
        st.write("The NPK ratio is shown by fertiliser numbers, where N stands for nitrogen, P for phosphorus, and K for potassium. The percentage by weight of each nutrient in the fertiliser is represented by a number. For instance, 15-10-5 fertiliser contains 5% potassium (K), 10% phosphorus (P), and 15% nitrogen (N) by weight.")
        st.write("### The Meaning of Fertilizer Numbers (Explanation of NPK Ratio") 
        st.write("The percentage by weight of the three nutrients nitrogen, phosphorus, and potassium in the fertiliser is indicated by the fertiliser numbers. The package has these three digits printed on it.**Nitrogen, phosphorus, and potassium**is referred to as NPK. To be more exact N represents the nitrogen content of the fertiliser as a proportion of its weight.P is the percentage by weight of phosphate (P2O5) that is present in the fertiliser.K is the percentage by weight of potash (K2O) that is present in the fertiliser.Keep in mind that plants require additional nutrients in addition to nitrogen, phosphorus, and potassium (or NPK) in order to survive and develop. NPK, or the big three, as I like to refer to it, is the nutrient that plants will use the most of out of all the nutrients.")
        st.image('https://cdn-prodapi.iffcobazar.in/pub/media/catalog/product/2/-/2-iffco-npk-front-1kg_1_1_.jpg',width=300)
    if choice == "Dont know Rainfall in your area?":
        st.subheader("Subdivision wise rainfall India 2022")
        st.image('https://sandrp.files.wordpress.com/2022/09/subdivision_rainfall_map-300922.jpeg?w=731') 
        st.caption("### The data in this map is for 2022 and is subdivision wise ,you can search other resources for accurate rainfall in your area" )  
    if choice == "Want to know selling price of your crop?":  
        data=pd.read_excel('crooo.xlsx')
        st.title("Market Price of Commodities")

        States = data["State"].unique()
        state1=st.empty()
        district1=st.empty()
        commodity1=st.empty() 
        State = st.selectbox("Select State", States,key=state1)
        districts = data[data["State"] == State]["District"].unique()

        district = st.selectbox("Select District", districts,key=district1)
        commodities = data[(data["State"] == State) & (data["District"] == district)]["Commodity"].unique()

        commodity = st.selectbox("Select Commodity", commodities,key=commodity1)

        if commodity:
            min_price = data[(data["State"] == State) & (data["District"] == district) & (data["Commodity"] == commodity)]["Min Price"].iloc[0]
            max_price = data[(data["State"] == State) & (data["District"] == district) & (data["Commodity"] == commodity)]["Max Price"].iloc[0]
            st.caption("Prices are Per Quintal")
            st.write("Min Price:", min_price)
            st.write("Max Price:", max_price)

if __name__ == '__main__':
    main()
    
