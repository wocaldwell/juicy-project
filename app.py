import os, requests, json, re, collections, operator
from flask import Flask, render_template, jsonify, Markup


# set the nutritionix api secrets from local environment variables
juicy_id = os.environ['JUICYID']
juicy_key = os.environ['JUICYKEY']

app = Flask(__name__)

@app.route("/", methods=["GET"])
def render_juicy_facts():
    '''
    Compile all of the logic and render the website when visiting url.
    '''
    # get all juicy juice products from nutririonix api and decode the json data
    juicy_products = json.loads(get_all_products_by_brand_id("51db37d0176fe9790a899db2").data.decode("utf-8"))

    # variable that stores answer to challenge #1
    juicy_total_products = juicy_products["total_hits"]

    # list of Juicy Juice products and their calories per ounce
    juicy_calories_list = get_calories_per_ounce(juicy_products)

    # initialize values for average calorie logic
    juicy_calories_average_total = 0
    total_products_with_average_calories = len(juicy_calories_list)

    # loop through calories list and add the calories
    for drink in juicy_calories_list:
        juicy_calories_average_total = juicy_calories_average_total + drink["cals_per_oz"]

    # variable that stores answer to challenge #2
    juicy_average_calories_per_ounce = get_average(total_products_with_average_calories, juicy_calories_average_total)

    # variable that stores answer to challenge #3
    juicy_ingredients = get_ingredients_and_thier_products(juicy_products)

    # variable for ingredients and their percentages
    ingredient_frequency = get_ingredient_frequency(juicy_ingredients)

    # sort ingredient frequency by max percentage
    sorted_ingredient_frequency = sort_ingredients_by_product_percentage(ingredient_frequency)

    # variable for top ten ingredients by percentage
    top_ten_ingredients = sorted_ingredient_frequency[:9]

    # visualization variables
    chart_labels = []
    chart_values = []

    # loop through top five ingredients and assign labels and values
    for ingredient in top_ten_ingredients:
        chart_labels.append(ingredient[0])
        chart_values.append(ingredient[1])

    return render_template("index.html", juicy_total_products = juicy_total_products, average_calories_per_ounce = round(juicy_average_calories_per_ounce["average"], 2), juicy_ingredients = juicy_ingredients, values=chart_values, labels=chart_labels, ingredient_frequency=ingredient_frequency)

def get_all_products_by_brand_id(brand_id):
    '''
    Send a request to the nutritionix api for all products that match the brand id.

    Arguments:
        brand_id(str), an id assigned to a particular brand in the nutritionix api.

    Returns:
        Json object, the combined results of the nutritionix requests for ALL products made by the searched brand.
    '''
    # format for api request
    request_body = "{}/search?brand_id={}&fields={}&results={}:{}&appId={}&appKey={}"
    # base url for nutritionix api
    url = "https://api.nutritionix.com/v1_1/"
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
        Loop throught the api response and add each product object to the all_products list.

        Arguments:
            request(json), a "get" request to the nutritionix api.
        '''
        for hit in request["hits"]:
            all_products.append(hit)

    # funtion that calls api and converts the response to a json object
    def get_request_and_make_json(api_url, request_body, brand_id, fields, results_start, results_end, juicy_id, juicy_key):
        '''
        Send a "get" request to the nutritionix api and convert the results into a json object.

        Arguments:
            api_url(str), the base url.
            request_body(str), the protion of the url that contains the request params.
            brand_id(str), a request param for a specific brand.
            fields(str), the fields to be included in the requested api response.
            results_start(int), the starting number for the range of results from the "hits" array.
            results_end(int), the ending number for the range of results from the "hits" array. Maximum is results_start + 50.
            juicy_id(str), the app ID given to the website application by registering with nutritionix.
            juicy_key(str), the app key given to the website application by registering with nutritionix.

        Returns:
            api_request(json), the results of the "get" request from the nutritionix api.
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

    return jsonify(total_hits=products_total, products=all_products)


def get_calories_per_ounce(juicy_drinks):
    '''
    Get the calories per ounce for all Juicy Juice products that have a serving size unit marked in fluid ounces.

    Arguments:
        juicy_drinks(dict), all Juicy Juice products in the Nutritionix api.

    Returns:
        juicy_calories_per_ounce_list(list), a list of dictionarys for products and their calories per ounce.
    '''
    # list to store products and their average calories per ounce
    juicy_calories_per_ounce_list = []

    # loop through products
    for product in juicy_drinks["products"]:
        product_fields = product["fields"]
        # get the product if it serving size unit is fluid ounces
        if product_fields["nf_serving_size_unit"] == "fl oz":
            juicy_product = product_fields["item_name"]
            juicy_calories_per_ounce = product_fields["nf_calories"]/product_fields["nf_serving_size_qty"]
            # add dictonary of each product and calories to list
            juicy_calories_per_ounce_list.append({
                "product_name": juicy_product,
                "cals_per_oz": juicy_calories_per_ounce
            })

    return juicy_calories_per_ounce_list

def get_average(divisor, dividend):
    '''
    Divide the sum of values in a set by their number.

    Arguments:
        divisor(int): the number of values in a set.
        dividend(float): the sum of the values in a set.

    Returns:
        A dictionary with the average value in it.
    '''
    average = dividend / divisor

    return {"average": average}

def get_ingredients_and_thier_products(juicy_products):
    '''
    Get all unique ingredients from the Juicy Juice products and store them along with the product that includes that ingredient.

    Arguments:
        juicy_products(dict), all Juicy Juice products in the Nutritionix api.

    Returns:
        final_ingredients_dict(dict), dictionary of common ingredient names(keys) and the list of products that include that ingredient(values).
    '''
    # variable to store ingredients
    all_ingredients_dict = collections.defaultdict(list)

    # loop through all products
    for product in juicy_products["products"]:
        product_fields = product["fields"]
        ingredients = product_fields["nf_ingredient_statement"]
        # if ingredients is not None
        if ingredients:
            # make all ingredient strings lower case
            ingredients = ingredients.lower()
            # bind ingredient list to product name (doesn't duplicate if already in dict:) )
            all_ingredients_dict[ingredients] = product_fields["item_name"]

    # the dictionary that will store common ingedient names and their related products
    final_ingredients_dict = collections.defaultdict(list)

    # list of common ingredient names to be used with "dirty" data
    common_ingredients = ["apple juice", "pear juice", "grape juice", "rasberry juice", "natural flavor", "ascorbic acid", "citric acid", "orange juice", "tangerine juice", "mango puree", "malic acid", "water", "carbonation", "fish oil", "gellan gum", "strawberry juice", "banana puree", "pineapple juice", "watermelon juice", "kiwi juice", "cherry juice", "tangerine juice", "carrot juice", "sweet potato puree", "gum acacia", "beta carotene", "passion fruit juice", "lemon juice", "cranberry juice", "peach juice", "peach puree", "vegetable juice", "pectin"]

    # loop through all ingredient/product pairs
    for ingredient, product in all_ingredients_dict.items():
        # loop through the common ingredients
        for common_name in common_ingredients:
            if common_name in ingredient:
                final_ingredients_dict[common_name].append(product)

    return final_ingredients_dict

def get_ingredient_frequency(ingredients_dict):
    '''
    Get the percentage of products that include each of the common Juicy Juice ingredients.

    Arguments:
        ingredients_dict(dict), all common Juicy Juice ingredients and their associated products. Each association as ingredient : [product list].

    Returns:
        percent_ingredient_in_products_dict(dict), the ingredients and the amount(in percentage as int) that they occur in all tracked products.
    '''
    # number of products
    total_number_of_tracked_products = 75

    # dictionary to store ingredient and product frequency
    percent_ingredient_in_products_dict = {}

    # loop through the ingredients dict and set the percentage of each ingredient
    for ingredient, products in ingredients_dict.items():
        percent_ingredient_in_products_dict[ingredient] = int((round(len(products)/total_number_of_tracked_products, 2)) * 100)

    return percent_ingredient_in_products_dict

def sort_ingredients_by_product_percentage(percentage_dict):
    '''
    Sort the ingredients by the highest product percentage.

    Arguments:
        percentage_dict(dict), the ingredients and their associated product inclusion.
    '''
    # sort by value, reverse makes it descending
    sorted_ingredients_by_percentage = sorted(percentage_dict.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_ingredients_by_percentage

if __name__ == "__main__":
    app.run()