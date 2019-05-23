from flask import Flask, render_template, request, redirect

import multidict as multidict

import numpy as np

import random
import os
import re
from os import path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}

    # making dict for counting frequencies
    for text in sentence.split(" "):
        if re.match("a|the|an|the|to|in|for|of|or|by|with|is|on|that|be", text):
            continue
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
    for key in tmpDict:
        fullTermsDict.add(key, tmpDict[key])
    return fullTermsDict


def makeImage(text, filename='default.png'):

    wc = WordCloud(background_color="white", max_words=1000)
    # generate word cloud
    wc.generate_from_frequencies(text)

    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(filename, dpi=100)



app = Flask(__name__)

@app.route('/')
def home():
	# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
	d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

	text = open(path.join(d, 'citizen.txt'), encoding='utf-8')
	text = text.read()
	makeImage(getFrequencyDictForText(text), filename="static/citizen.png")

	text = open(path.join(d, 'government.txt'), encoding='utf-8')
	text = text.read()
	makeImage(getFrequencyDictForText(text), filename="static/government.png")

	return render_template("home.html", random1=random.randrange(0,100), random2=random.randrange(0,100))

@app.route("/get_citizen_text")
def get_citizen_text():
	pass

@app.route("/citizen_response")
def citizen_response():
	return render_template("citizen_form.html")

@app.route("/citizen_response_post", methods=["GET", "POST"])
def citizen_response_post():
	if request.method == "POST":
		user_text = request.form["user_input"]
		file = open('citizen.txt', 'a+')
		file.write(user_text+' ')
		print(user_text+' ')
		file.close()

	return redirect("/")

@app.route("/minister_response")
def minister_response():
	return render_template("minister_form.html")

@app.route("/minister_response_post", methods=["GET", "POST"])
def minister_response_post():
	if request.method == "POST":
		user_text = request.form["user_input"]
		file = open('government.txt', 'a+')
		file.write(user_text+' ')
		print(user_text+' ')
		file.close()

	return redirect("/")




if __name__ == '__main__':
	app.run(debug=True)