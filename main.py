import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup
import bs4

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

def get_pig_latin(url):
    response = requests.get(url)
    pigstring = BeautifulSoup(response.content, "html.parser").find("body")
    retstring = "".join([item for item in pigstring.contents if type(item)==bs4.element.NavigableString])
    return retstring

@app.route('/')
def home():
    #get a random fact
    fact = get_fact()
    #format for pig latinizer
    payload = {'input_text': fact}
    #create session and get response
    session = requests.Session()
    response = session.post('https://hidden-journey-62459.herokuapp.com/piglatinize/', 
                            data=payload, allow_redirects=False)
    full_url = response.headers['Location']
    pig_latin = get_pig_latin(full_url)
    postme = f"""  
            <html>
            <body>
                <h1>Andomray Igpay Atinlay Actsfay</h1>
                <a target='_blank' href='{full_url}'>{"Link to Pig Latinizer Site"}</a>
                <p><b>Random Fact</b>: {fact}</p>
                <p><b>Andomray Actfay</b>: {pig_latin}</p>
            </body>
            </html> 
            """
    return postme

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)

