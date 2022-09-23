from flask import Flask, render_template
from bs4 import BeautifulSoup
from nbformat import write
import requests
import json


app = Flask(__name__)

@app.route("/")
# @app.route("/home")

# def home():
#     return render_template('index.html')

@app.route("/get_content")
def get_content():
    url = "https://coinmarketcap.com/"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all("tr")[1:]
    states = []

    for row in table:
        row = list(filter(lambda x: x != "\n", row))
        state_name = row[2].text
        state_price = row[3].text
        states.append({"State":state_name,"Price":state_price})

    # return states
    return render_template("prices.html", states = states)

if __name__ == '__main__':
    app.run(debug=True, port=5001)