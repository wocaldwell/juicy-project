## A Juicy Project
The Nutritionix API contains nutritional information for a wide variety of food products. Use the Python Flask package to satisfy the following requirements:

1. Return the total number of Juicy Juice products in JSON format.
2. Return average calories per fluid ounce for all Juicy Juice products in JSON format.
3. Create an index from all unique Juicy Juice ingredients to the products that contain them (e.g., the ingredient "mango puree" is in Tropical Mango Juice, Mango Blast, Banana Mango Punch). The data here is dirty; the final results don’t have to be perfect.
4. Build a simple web page to display the results of questions 1-3 and host it on Heroku (https://www.heroku.com/).  Include an exported jpg/png visualization of the Nutritionix data that shows something interesting about the data using a  visualization tool of your choice (an Excel chart is acceptable).  Make sure to include a brief explanation of the visualization.

#### To see the deployed project click [here](https://afternoon-spire-21273.herokuapp.com/)!

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
Install [pip](https://packaging.python.org/installing/)

Install [Python 3.6](https://www.python.org/downloads/)

### Installing
Clone repo:

```
git clone https://github.com/wocaldwell/juicy-project.git
```
Install the project dependencies:

```
pip install -r requirements.txt
```

Create environment variables for Nutritionix API:

Visit the [Nutritionix](https://developer.nutritionix.com/) website and [signup](https://developer.nutritionix.com/signup) for an API key. Then, in your cli type
```
nano ~/.zshrc
```
(or `/.bashrc`, or `/.bash_profile`)and add the following lines ot the bottom of the file.
```
export JUICYID="YOUR NUTRITIONIX ID"
export JUICYKEY="YOUR NUTRITIONIX KEY"
```
Then press `control + x` to exit, `y` to confirm the changes and then `return` to write to the file.


### Running Project Locally
Run project in browser:

```
python app.py
```
Navigate to `http://localhost:5000/`.

In your browser you should see somthing like this:

![screenshot](assets/juicy_screenshot.png?raw=true)

To stop the project press `control + c` in your cli.

### Built With

* [Python](http://www.dropwizard.io/1.0.2/docs/) - Main Language
* [Flask](http://flask.pocoo.org/) - Python Microframework
* [pip](https://maven.apache.org/) - Dependency Management
* [Bootstrap](http://getbootstrap.com/) - Javascript Library


### Authors

* **William Caldwell** - [wocaldwell](https://github.com/wocaldwell)

### Acknowledgments
"Thank you all and GOOD NIGHT!" - Every Musician Ever
