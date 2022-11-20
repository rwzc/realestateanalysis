# ## Package requirements
# - check the requirements.txt file
# - Citations and Credits to 
#     - https://github.com/aloysiuschan/99co
#     - https://towardsdatascience.com/get-your-own-data-building-a-scalable-web-scraper-with-aws-654feb9fdad7


# 1st way get requirements.txt
jupyter nbconvert webscrape.ipynb --to=python
# install pipreqs
pip install pipreqs
# This will create a requirements.txt file for your project. if you are in the project folder
pipreqs ./ --force


# 2nd way to get requirements.txt ( but gets all of the requirements in your PIP)
pip3 freeze > requirements.txt



## To install the requirements use
pip3 install -r requirements.txt


