import os
import requests
import json
from flask import Flask, render_template, jsonify

# set the nutritionix api secrets from local environment variables
juicy_id = os.environ['JUICYID']
juicy_key = os.environ['JUICYKEY']

app = Flask(__name__)

@app.route("/", methods=["GET"])
def render_juicy_facts():
    '''
    '''
    juicy_foods = get_all_food_by_brand_id("51db37d0176fe9790a899db2")
    print("----------------------")
    print(juicy_foods)
    juicy_total_object = json.loads(get_total_hits(juicy_foods).data.decode("utf-8"))
    print(juicy_total_object)
    juicy_total_products = juicy_total_object["total_products"]
    return render_template("index.html", juicy_total_products = juicy_total_products)

def get_all_food_by_brand_id(brandId):
    '''
    '''
    # initial request to get total number of food hits
    url = "https://api.nutritionix.com/v1_1/search"
    offset = 0
    food_request = requests.get("{}/?brand_id={}&limit=5offset={}&fields=*&appId={}&appKey={}".format(url, brandId, offset, juicy_id, juicy_key)).content.decode("utf-8")
    food_request = json.loads(food_request)
    return food_request

# def get_all_food_by_brand_id(brandId):
#     '''
#     '''
#     url = "https://api.nutritionix.com/v1_1/search"
#     headers = {"Content-Type": "application/json"}
#     # data = {
#     #     "appId": juicy_id,
#     #     "appKey": juicy_key,
#     #     "fields": [
#     #         "item_name",
#     #         "nf_ingredient_statement",
#     #         "nf_calories",
#     #         "nf_serving_size_qty",
#     #         "nf_serving_size_unit"
#     #     ],
#     #     "offset": 0,
#     #     "limit": 50,
#     #     "sort": {
#     #         "field": "item_name.sortable_na",
#     #         "order": "desc"
#     #     },
#     #     "filters": {
#     #         "brand_id": brandId
#     #     }
#     # }
#     data = {
#         "appId": juicy_id,
#         "appKey": juicy_key,
#         "query": '"brand_id" : "51db37d0176fe9790a899db2"'
#     }

#     food_request = requests.get(url, data=json.dumps(data), headers=headers)

#     return food_request

def get_total_hits(request):
    '''
    Sets the total hits for an api query.

    Arguments:
        request, the request to the nutritionix api.

    Returns:
        total_hits(int), The number of hits for the api query.
    '''
    total_hits = request["total_hits"]
    print(total_hits)
    return jsonify(total_products=total_hits)

if __name__ == "__main__":
    app.run(debug=True)