
# Introduction
Hello!  
Probably after the name of the project you wonder what you can find in this repository  
So, let's take a look :D.

From the beginning of my programming path, I always wanted to create something useful that I could use or share for the community. That's why I decided to finally get on with something and do it. The project is an AI model, which using data collected from otomoto (Polish website selling cars) is able to value your car. The model works best on cars, the market price of which varies from 10 - 50 thousand dollars.

## Jupyter Notebook
In the jupyter notebook you will find all my code connected to modelling, data exploration (plots included) and all information connected to model feature importance.  
Here I included also data dictionary, that explains features of data collected on my own.

## Python script (main.py)
It is the main and the only one script, that I used for data collection, it's pretty simple and contain only 3 libraries, which allow me scrap data from web browser.
I decided on bs4 (totally ignoring Selenium) in order to save computer memory resources.

## Model evaluation
As you can see in jupyter notebook, model accuracy is pretty good ~ 84 %.
Like I mentioned at the beginning, the model is best suited to "middle class" cars.
At ,,low class" and "high class" cars you can expect error in range 1000 (low class cars),
10 000 (high class cars).  

All metrics like:
 1. R^2
 2. MAE
 3. MSE
 4. RMSE  
You will find inside the notebook.
