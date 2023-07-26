#!/usr/bin/env python
# coding: utf-8

# ### 🍎🫐🥝🥗🥘 CLEVER MEAL  B2C & B2G🍎🫐🥝🥗🥘

# Emojis able: ✅⚠️⁉️➡️▶️⏸️🟡🔴🥳👀🙌🏻🚀🤯

# In[2]:


# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st


from sklearn import datasets # sklearn comes with some toy datasets to practice
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
# from matplotlib import pyplot
from sklearn.metrics import silhouette_score
from PIL import Image
from IPython.display import display
from fuzzywuzzy import fuzz, process

#####################################################################################################

### Connecting with Open AI

import os

api_key = os.getenv("OPENAI_API_KEY")
api_key = "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"

#Ira kEY
#api_key = "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"

#Aleks Key
# api_key = "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"

# Gen Key
# api_key = "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"



import openai

# load and set our key
openai.api_key = api_key

#######################################################################################################


### 1. Weight🏗️  & 2. Hight 🌁  & 3. Edge👵🏼👴🏻

def get_non_empty_float(prompt):
    while True:
        try:
            value = float(st.text_input(prompt))
            if value <= 0:
                st.warning("Please enter a positive non-zero value.")
            else:
                return value
        except ValueError:
            st.warning("Invalid input. Please enter a valid number.")

### 4. Gender 🚺🚹

def get_gender():
    while True:
        gender = st.text_input("Gender (male/female): ").lower()
        if gender in ['male', 'female']:
            return gender
        else:
            st.warning("Invalid gender. Please enter 'male' or 'female'.")


#get_gender()


### 5. Nilvel of phisical Activity ⛹🏽⛹🏻‍♀️

def get_activity_level():
    # Define a list of correct spellings or keywords:
    # correct_spellings = ["sedentary", "lightly active", "moderately active", "very active"]

    activity_levels = ['sedentary', 'lightly active', 'moderately active', 'very active', 'extra active']

    # Use st.selectbox to provide valid options as suggestions
    nivel_activity = st.selectbox("Activity Level", activity_levels)

    # Optionally, you can add a warning message if the entered value is not in the list
    if nivel_activity not in activity_levels:
        st.warning("Invalid activity level. Please choose from the provided options.")
    
    return nivel_activity

#get_activity_level()

### 6. Goal 🏆

def get_user_goal():
    # Define a list of correct spellings or keywords:
    user_goal = ['loss weight', 'maintain weight', 'gain weight']
    
    # Use st.selectbox to provide valid options as suggestions
    user_goals_input = st.selectbox("What is your Goal:", user_goal)

    # Optionally, you can add a warning message if the entered value is not in the list
    if user_goals_input not in user_goal:
        st.warning("Invalid user goal. Please choose from the provided options.")
    
    return user_goals_input

#get_user_goal()

### ➡️ Calculating the User Calories (BMR)

#### BMR:Basal Metabolic Rate

def calculate_bmr(weight, height, age, gender):
    # BMR calculation using the Harris-Benedict equation
    if gender == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

### ➡️ Get user inputs

def get_user_inputs():
 
    print("Please enter the following information:")

    # 1. Weight🏗️  & 2. Hight 🌁  & 3. Edge👵🏼👴🏻 ✅✅✅
    
    weight = get_non_empty_float("Weight (kg): ")
    height = get_non_empty_float("Height (cm): ")
    age = get_non_empty_float("Age (years): ")

    
    # 4. Gender 🚺🚹 ✅
    gender = get_gender()
    
    # 5. Nilvel of phisical Activity ⛹🏽⛹🏻‍♀️ ✅
    nivel_activity = get_activity_level()
    
    # 6. Goal 🏆✅
    user_goals = get_user_goal()

    # ➡️ Calculating the User Calories Basal Metabolic Rate (BMR)
        
    #👀
    
    bmr = round(calculate_bmr(weight, height, age, gender),1)
    
 

    activity_factors = {
        "sedentary": 1.2,
        "lightly active": 1.375,
        "moderately active": 1.55,
        "very active": 1.725,
        "extra active": 1.9
    }
    
    TDEE_goals = {
        "loss weight": 0.85,
        "maintain weight": 1,
        "gain weight": 1.1
    }

    ##### CALCULATING THE TDEE

    # Set a default value for TDEE
    TDEE = None

    if nivel_activity in activity_factors:
        TDEE = (bmr * activity_factors[nivel_activity])

        if user_goals in TDEE_goals:
            TDEE *= round(TDEE_goals[user_goals])   ## 7. ✅
            print(f"Total Calories based on your Goal is: {TDEE:.2f}")
        else:
            print("Invalid goal. Please choose from the provided options.")


    # Macronutrient Ratios
    protein_ratio = 0.3
    fat_ratio = 0.3
    carbohydrate_ratio = 0.4

    # Caloric content per gram of each macronutrient
    protein_calories_per_gram = 4
    fat_calories_per_gram = 9
    carbohydrate_calories_per_gram = 4

    # Calculate the grams of each macronutrient
    
    ## 8. ✅
    protein_grams = round(((protein_ratio * TDEE) / protein_calories_per_gram),1)
    
    ## 9. ✅
    fat_grams = round(((fat_ratio * TDEE) / fat_calories_per_gram),1)
    
    ## 10. ✅
    carbohydrate_grams = round(((carbohydrate_ratio * TDEE) / carbohydrate_calories_per_gram),1)
    
    print(f"The macronutrients distributions  based on your Goal are: Protein {protein_grams}gr, Fat:{fat_grams}gr, Carbohydrate:{carbohydrate_grams}gr.")

 ########################################################################################  
    
      # Create the user question based on the collected inputs
       
    user_question = (
     f"I weigh {weight} kg, my hight is {height} cm, I am {age} years old, my gender is {gender} my activity level is {nivel_activity}, and I aim for {user_goals}."
     f"Please suggest a personalized diet plan (with breakfast, lunch, snack, and dinner) with a total of {TDEE} calories per day, "
     f"The suggested diet must consider the macronutrient distribution of {protein_grams}gr of protein, {fat_grams} gr of Fat, and {carbohydrate_grams}gr of Carbohydrates.The suggested diet also should show the macronutrient contribution that each food has in grams of protein, fat, and carbohydrates and their Caloric intake.")
    
    
    
    #user_question = (
     #f"I weigh {weight} kg, my hight is {height} cm, I am {age} years old, my gender is {gender} my activity level is {nivel_activity}, and I aim for {user_goals}."
     #f"Please suggest a personalized diet plan (with breakfast, lunch, snack, and dinner)  with a total of {TDEE} calories per day, "
     #f"The suggested diet must consider the macronutrient distribution of {protein_grams}gr of protein, {fat_grams} gr of Fat, and {carbohydrate_grams}gr of Carbohydrates.The suggested diet also should show the macronutrient contribution that each food has in grams of protein, fat, and carbohydrates and their Caloric intake.")
    
    return user_question

#get_user_inputs()

def get_personalized_diet_plan(user_inputs):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a famous Nutritionist. Share your best nutritional plan diet. In your nutrition plans, you provide breakfast, lunch, snack, and dinner based on the calories per day, macronutrients, and the goal of the user. In your nutrition plans, you show the macronutrients distributions and calories for the breakfast, lunch, snack, and dinner you suggested" },
            {"role": "user", "content": user_inputs},
        ]
    )
    system_response = response['choices'][0]["message"]["content"]
    return system_response


def main():

    st.title(" ➡️ CLEVER MEAL 🍎🧠")  # Largest size

    st.header("Get your Personalized Diet Plan in seconds!!")  # Slightly smaller than title

    st.subheader("Based on your Nutrition Goals!🎯🚀")
    
    
    st.title("Personalized Diet Plan App")

    user_inputs = get_user_inputs()

    if st.button("Get Personalized Diet Plan"):
        personalized_diet_plan = get_personalized_diet_plan(user_inputs)
        st.markdown("\nPersonalized Diet Plan:")
        st.markdown(personalized_diet_plan)


if __name__ == "__main__":
    main()


        

