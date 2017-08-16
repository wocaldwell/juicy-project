import os
import requests
from flask import Flask, render_template

# set the nutritionix api secrets from local environment variables
juicy_id = os.environ['JUICYID']
juicy_key = os.environ['JUICYKEY']

app = Flask(__name__)

@app.route("/", methods=["GET"])
def render_juicy_facts():
    '''
    '''

    return render_template("index.html")

def get_food_by_brand_id(brandId):
    '''
    '''
    return requests.get("https://api.nutritionix.com/v1_1/search/?brand_id={}&results=0%3A50&fields=*&appId={}&appKey={}".format(brandId, juicy_id, juicy_key)).content

if __name__ == "__main__":
    app.run(debug=True)