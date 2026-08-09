#Problem Number 1

# print('''Twinkle, twinkle, little star, how I wonder what you are. Up above the world so high,
# like a diamond in the sky. Twinkle, twinkle, little star, how I wonder what you are.
# When the blazing sun is set, and the grass with dew is wet. Then you show your little
# light, twinkle, twinkle all the night. Twinkle, twinkle little star, how I wonder what you
# are.
# Then the traveler in the dark thanks you for your tiny spark. How could he see where to
# go if you did not twinkle so? Twinkle, twinkle little star, how I wonder what you are.
# As your bright and tiny spark lights the traveler in the dark, though I know not what you
# are, twinkle, twinkle, little star. Twinkle, twinkle, little star, how I wonder what you are.''')

# instead of writing each lline in double quotes use three single quotes


#Problem Number 2
#use repl and write table
# print(5*2)

#problem number 3
# import pyttsx3
# engine = pyttsx3.init()

# # For Mac, If you face error related to "pyobjc" when running the `init()` method :
# # Install 9.0.1 version of pyobjc : "pip install pyobjc>=9.0.1"

# engine.say("My name is shreetej")
# engine.runAndWait()

#pyttsx3 is used to listen the line we want to print nut before writing code install pyttsx3 in terminal


# #problem number 5
# import os

# # Specify the directory you want to list
# directory_path = '/Program Files'

# # List all files and directories in the specified path
# contents = os.listdir(directory_path)

# # Print each file and directory name
# for item in contents:
#     print(item) 


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load Dataset
data = pd.read_csv("student_performance.csv")

# Display Dataset
print(data)

# Correlation
correlation = data["Study_Hours"].corr(data["Exam_Score"])
print("\nCorrelation between Study Hours and Exam Score:")
print(correlation)

# Features and Target
X = data[["Study_Hours"]]
y = data["Exam_Score"]

# Regression Model
model = LinearRegression()
model.fit(X, y)

# Prediction
predicted = model.predict(X)

print("\nSlope:", model.coef_[0])
print("Intercept:", model.intercept_)

# Predict score for 7.5 study hours
score = model.predict([[7.5]])
print("Predicted Score for 7.5 Study Hours:", score[0])

# Plot
plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X, predicted, color='red', linewidth=2, label='Regression Line')
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.title("Study Hours vs Exam Score")
plt.legend()
plt.show()