from flask import Flask, render_template
from bs4 import BeautifulSoup
from nbformat import write
import requests
import json
import pandas as pd 
#import aspose
#from aspose import jpype


app = Flask(__name__)
@app.route("/")

def index():
    return render_template('index.html')

@app.route("/get_content")
def get_content():
    url = "https://coinmarketcap.com/"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find_all("tr")[1:]
    Crypto = []

    for row in table:
        row = list(filter(lambda x: x != "\n", row))
        crypto_name = row[2].text
        crypto_price = row[3].text
        Crypto.append({"Name":crypto_name,"Price":crypto_price})
    # return states
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(Crypto, f , ensure_ascii=False, indent=4)
        
    return render_template("prices.html", Crypto = Crypto)

@app.route("/excel")
def excel():
    url = "http://127.0.0.1:5001/get_content"
    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    table1 = soup.find_all("table")[1:]
    Data_Crypto= soup.findAll('div', {'class':'main'})
    result1 = [(para.text).strip().split(',') for para in table1] 
    df = pd.DataFrame(result1)
    print(df)
    df.to_excel('ouput.xlsx', index=False)
#     return render_template("prices.html")
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)