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
    # get all juicy juice products from nutririonix api and decode the json data
    juicy_products = json.loads(get_all_products_by_brand_id("51db37d0176fe9790a899db2").data.decode("utf-8"))
    print(type(juicy_products))

    # variable that stores answer to challenge #1
    juicy_total_products = juicy_products["total_hits"]

    juicy_calories_list = get_calories_per_ounce(juicy_products)
    print(juicy_calories_list)

    # initialize values for average calorie logic
    juicy_calories_average_total = 0
    total_products_with_average_calories = len(juicy_calories_list)

    # loop through calories list and add the calories
    for drink in juicy_calories_list:
        juicy_calories_average_total = juicy_calories_average_total + drink["cals_per_oz"]

    # variable that stores answer to challenge #2
    juicy_average_calories_per_ounce = get_average(total_products_with_average_calories, juicy_calories_average_total)

    return render_template("index.html", juicy_total_products = juicy_total_products, average_calories_per_ounce = juicy_average_calories_per_ounce["average"])

def get_all_products_by_brand_id(brand_id):
    '''
    Send a request to the nutritionix api for all products that match the brand id.

    Arguments:
        brand_id(str), an id assigned to a particular brand in the nutritionix api.

    Returns:
        Json object, the combined results of the nutritionix request for ALL products by the searched brand.
    '''
    # format for api request
    request_body = "{}/?brand_id={}&fields={}&results={}:{}&appId={}&appKey={}"
    # base url for nutritionix
    url = "https://api.nutritionix.com/v1_1/search"
    # fields required to complete tasks
    fields = "item_name,nf_ingredient_statement,nf_calories,nf_serving_size_qty,nf_serving_size_unit"
    # results by index, results_start:results_end
    results_start = 0
    results_end = 50
    # list to store all products of a brand
    all_products = []

    # function to add each product object to all_products list
    def add_hits_to_all_products(request):
        '''
        '''
        for hit in request["hits"]:
            all_products.append(hit)

    # funtion that calls api and converts the response to a json object
    def get_request_and_make_json(api_url, request_body, brand_id, fields, results_start, results_end, juicy_id, juicy_key):
        '''
        '''
        api_request = requests.get(request_body.format(api_url, brand_id, fields, results_start, results_end, juicy_id, juicy_key)).content.decode("utf-8")
        api_request = json.loads(api_request)
        return api_request

    # first call to api
    products_request = get_request_and_make_json(url, request_body, brand_id, fields, results_start, results_end, juicy_id, juicy_key)
    # add the hits from request to all_products list
    add_hits_to_all_products(products_request)
    # get the total amount of hits for the product
    products_total = products_request["total_hits"]
    # make additional requests until all products have been added
    while results_end < products_total:
        results_start = results_start + 50
        results_end = results_end + 50
        new_products_request = get_request_and_make_json(url, request_body, brand_id, fields, results_start, results_end, juicy_id, juicy_key)
        add_hits_to_all_products(new_products_request)
        print(results_end, products_total)
    print("Number of products:", len(all_products))
    return jsonify(total_hits=products_total, products=all_products)


def get_calories_per_ounce(juicy_json):
    '''
    Get the calories per ounce for all Juicy Juice products that have a serving size unit marked in fluid ounces.

    Arguments:
        juicy_json(obj), all Juicy Juice products in the Nutritionix api.

    Returns:
        juicy_calories_per_ounce_list(list), a list of dictionarys for all products and their calories per ounce.
    '''
    # list to store products and their average calories
    juicy_calories_per_ounce_list = []

    # loop through products
    for product in juicy_json["products"]:
        product_fields = product["fields"]
        # get the product if it serving size unit is fluid ounces
        if product_fields["nf_serving_size_unit"] == "fl oz":
            juicy_product = product_fields["item_name"]
            juicy_calories = product_fields["nf_calories"]/product_fields["nf_serving_size_qty"]
            # add dictonary of each product and calories to list
            juicy_calories_per_ounce_list.append({
                "product_name": juicy_product,
                "cals_per_oz": juicy_calories
            })
    return juicy_calories_per_ounce_list

def get_average(divisor, dividend):
    '''
    Divide the sum of the given values in a set by their number.

    Arguments:
        divisor(int): the number of values in a set.
        dividend(float): the sum of the values in a set.

    Returns:
        A dictionary with the average value in it.
    '''
    average = dividend / divisor
    return {"average": average}

# def get_total_hits(request):
#     '''
#     Sets the total hits for an api query.

#     Arguments:
#         request, the request to the nutritionix api.

#     Returns:
#         A json object with the total amount of products for the request.
#     '''
#     request_json = json.loads(request.data.decode("utf-8"))
#     total_hits = request_json["total_hits"]
#     print(total_hits)
#     return jsonify(total_products=total_hits)

# # funtion that calls api and converts the response to a json object
# def get_request_and_make_json(api_url, params):
#     '''
#     '''
#     api_request = requests.get(request_body.format(api_url, brand_id, fields, results_start, results_end, juicy_id, juicy_key)).content.decode("utf-8")
#     api_request = json.loads(api_request)
#     return api_request

if __name__ == "__main__":
    app.run(debug=True)