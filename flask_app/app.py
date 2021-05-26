import flask
import os
import pickle
import pandas as pd
from skimage import io
from skimage import transform
from io import BytesIO
from PIL import Image
import base64
import cv2
from sklearn.decomposition import PCA

app = flask.Flask(__name__, template_folder='templates')

path_to_vectorizer = 'models/vectorizer.pkl'
path_to_text_classifier = 'models/text-classifier.pkl'
path_to_image_classifier = 'models/image-classifier.pkl'
path_to_SVM_fruitTree_classifer = 'models/SVM_fruitTree_folder_train.pkl'
path_to_RF_fruitTree_classifier = 'models/randomforest_model.sav'
path_to_PCA_model = 'models/pca_model.sav'
path_to_PCA_Scaler = 'models/pca_scaler_model.sav'

with open(path_to_vectorizer, 'rb') as f:
    vectorizer = pickle.load(f)

with open(path_to_text_classifier, 'rb') as f:
    model = pickle.load(f)

with open(path_to_image_classifier, 'rb') as f:
    image_classifier = pickle.load(f)

with open(path_to_SVM_fruitTree_classifer, 'rb') as f:
    SVM_fruitTree_classifier = pickle.load(f)

with open(path_to_RF_fruitTree_classifier, 'rb') as f:
    RF_fruitTree_classifier = pickle.load(f)

with open(path_to_PCA_model, 'rb') as f:
    pca_model = pickle.load(f)

with open(path_to_PCA_Scaler, 'rb') as f:
    pca_scaler = pickle.load(f)

# Uploads can only be up to 15MB, this is checked automatically
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024

# Image types that can be accepted
app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".webp"]

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        # Get the input from the user.
        user_input_text = flask.request.form['user_input_text']
        
        # Turn the text into numbers using our vectorizer
        X = vectorizer.transform([user_input_text])
        
        # Make a prediction 
        predictions = model.predict(X)
        
        # Get the first and only value of the prediction.
        prediction = predictions[0]

        # Get the predicted probabs
        predicted_probas = model.predict_proba(X)

        # Get the value of the first, and only, predicted proba.
        predicted_proba = predicted_probas[0]

        # The first element in the predicted probabs is % democrat
        precent_democrat = predicted_proba[0]

        # The second elemnt in predicted probas is % republican
        precent_republican = predicted_proba[1]

        return flask.render_template('index.html', 
            input_text=user_input_text,
            result=prediction,
            precent_democrat=precent_democrat,
            precent_republican=precent_republican)

@app.route('/input_values/', methods=['GET', 'POST'])
def input_values():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('input_values.html'))

    if flask.request.method == 'POST':
        # Get the input from the user.
        var_one = flask.request.form['input_variable_one']
        var_two = flask.request.form['another-input-variable']
        var_three = flask.request.form['third-input-variable']

        list_of_inputs = [var_one, var_two, var_three]

        return(flask.render_template('input_values.html', 
            returned_var_one=var_one,
            returned_var_two=var_two,
            returned_var_three=var_three,
            returned_list=list_of_inputs))

    return(flask.render_template('input_values.html'))

@app.route('/images/')
def images():
    return flask.render_template('images.html')

@app.route('/bootstrap/')
def bootstrap():
    return flask.render_template('bootstrap.html')

@app.route('/classify_image_SVM/', methods=['GET', 'POST'])
def classify_image_SVM():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('classify_image_SVM.html'))

    if flask.request.method == 'POST':
        # Get file object from user input.
        file = flask.request.files['file']
        img_name = file.filename

        # Checks for the filetype of the file uploaded
        if img_name != "":
            file_ext = os.path.splitext(img_name)[1]

            # Checks for file extensions
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flask.abort(415)  # Unsorported media type
        else:
            return flask.render_template("classify_image_SVM.html")

        item_identifier_names = {0: 'Apple Braeburn',
                                 1: 'Apple Crimson Snow',
                                 2: 'Apple Golden 1',
                                 3: 'Apple Golden 2',
                                 4: 'Apple Golden 3',
                                 5: 'Apple Granny Smith',
                                 6: 'Apple Pink Lady',
                                 7: 'Apple Red 1',
                                 8: 'Apple Red 2',
                                 9: 'Apple Red 3',
                                 10: 'Apple Red Delicious',
                                 11: 'Apple Red Yellow 1',
                                 12: 'Apple Red Yellow 2',
                                 13: 'Apricot',
                                 14: 'Avocado',
                                 15: 'Avocado ripe',
                                 16: 'Banana',
                                 17: 'Banana Lady Finger',
                                 18: 'Banana Red',
                                 19: 'Beetroot',
                                 20: 'Blueberry',
                                 21: 'Cactus fruit',
                                 22: 'Cantaloupe 1',
                                 23: 'Cantaloupe 2',
                                 24: 'Carambula',
                                 25: 'Cauliflower',
                                 26: 'Cherry 1',
                                 27: 'Cherry 2',
                                 28: 'Cherry Rainier',
                                 29: 'Cherry Wax Black',
                                 30: 'Cherry Wax Red',
                                 31: 'Cherry Wax Yellow',
                                 32: 'Chestnut',
                                 33: 'Clementine',
                                 34: 'Cocos',
                                 35: 'Corn',
                                 36: 'Corn Husk',
                                 37: 'Cucumber Ripe',
                                 38: 'Cucumber Ripe 2',
                                 39: 'Dates',
                                 40: 'Eggplant',
                                 41: 'Fig',
                                 42: 'Ginger Root',
                                 43: 'Granadilla',
                                 44: 'Grape Blue',
                                 45: 'Grape Pink',
                                 46: 'Grape White',
                                 47: 'Grape White 2',
                                 48: 'Grape White 3',
                                 49: 'Grape White 4',
                                 50: 'Grapefruit Pink',
                                 51: 'Grapefruit White',
                                 52: 'Guava',
                                 53: 'Hazelnut',
                                 54: 'Huckleberry',
                                 55: 'Kaki',
                                 56: 'Kiwi',
                                 57: 'Kohlrabi',
                                 58: 'Kumquats',
                                 59: 'Lemon',
                                 60: 'Lemon Meyer',
                                 61: 'Limes',
                                 62: 'Lychee',
                                 63: 'Mandarine',
                                 64: 'Mango',
                                 65: 'Mango Red',
                                 66: 'Mangostan',
                                 67: 'Maracuja',
                                 68: 'Melon Piel de Sapo',
                                 69: 'Mulberry',
                                 70: 'Nectarine',
                                 71: 'Nectarine Flat',
                                 72: 'Nut Forest',
                                 73: 'Nut Pecan',
                                 74: 'Onion Red',
                                 75: 'Onion Red Peeled',
                                 76: 'Onion White',
                                 77: 'Orange',
                                 78: 'Papaya',
                                 79: 'Passion Fruit',
                                 80: 'Peach',
                                 81: 'Peach 2',
                                 82: 'Peach Flat',
                                 83: 'Pear',
                                 84: 'Pear 2',
                                 85: 'Pear Abate',
                                 86: 'Pear Forelle',
                                 87: 'Pear Kaiser',
                                 88: 'Pear Monster',
                                 89: 'Pear Red',
                                 90: 'Pear Stone',
                                 91: 'Pear Williams',
                                 92: 'Pepino',
                                 93: 'Pepper Green',
                                 94: 'Pepper Orange',
                                 95: 'Pepper Red',
                                 96: 'Pepper Yellow',
                                 97: 'Physalis',
                                 98: 'Physalis with Husk',
                                 99: 'Pineapple',
                                 100: 'Pineapple Mini',
                                 101: 'Pitahaya Red',
                                 102: 'Plum',
                                 103: 'Plum 2',
                                 104: 'Plum 3',
                                 105: 'Pomegranate',
                                 106: 'Pomelo Sweetie',
                                 107: 'Potato Red',
                                 108: 'Potato Red Washed',
                                 109: 'Potato Sweet',
                                 110: 'Potato White',
                                 111: 'Quince',
                                 112: 'Rambutan',
                                 113: 'Raspberry',
                                 114: 'Redcurrant',
                                 115: 'Salak',
                                 116: 'Strawberry',
                                 117: 'Strawberry Wedge',
                                 118: 'Tamarillo',
                                 119: 'Tangelo',
                                 120: 'Tomato 1',
                                 121: 'Tomato 2',
                                 122: 'Tomato 3',
                                 123: 'Tomato 4',
                                 124: 'Tomato Cherry Red',
                                 125: 'Tomato Heart',
                                 126: 'Tomato Maroon',
                                 127: 'Tomato Yellow',
                                 128: 'Tomato not Ripened',
                                 129: 'Walnut',
                                 130: 'Watermelon'
                                 }
        if file:
            # Read the image using skimage
            img = io.imread(file)

            # Resize the image to match the input the model will accept
            img = transform.resize(img, (45, 45))

            # Flatten the pixels from 28x28 to 784x0
            img = img.flatten()

            # Get prediction of image from classifier
            predictions = SVM_fruitTree_classifier.predict([img])
            # predictions = RF_fruitTree_classifier.predict([img])

            # Get the value of the prediction
            # prediction = item_identifier_names[predictions[0]] + " "+ str(predictions[0])
            prediction = item_identifier_names[predictions[0]]

            # For rendering image
            im = Image.open(file)
            data = BytesIO()
            im.save(data, "PNG")
            # Saves image in-memory, no need to save it into a folder.
            encoded_img_data = base64.b64encode(data.getvalue())

            return flask.render_template('classify_image_SVM.html',
                                         prediction=str(prediction),
                                         img_data = encoded_img_data.decode('utf-8'))

    return(flask.render_template('classify_image_SVM.html'))

@app.route('/classify_image_RF/', methods=['GET', 'POST'])
def classify_image_RF():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('classify_image_RF.html'))

    if flask.request.method == 'POST':
        # Get file object from user input.
        file = flask.request.files['file']
        img_name = file.filename

        # Checks for the filetype of the file uploaded
        if img_name != "":
            file_ext = os.path.splitext(img_name)[1]

            # Checks for file extensions
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flask.abort(415)  # Unsorported media type
        else:
            return flask.render_template("classify_image_RF.html")

        item_identifier_names = {0: 'Apple Braeburn',
                                 1: 'Apple Crimson Snow',
                                 2: 'Apple Golden 1',
                                 3: 'Apple Golden 2',
                                 4: 'Apple Golden 3',
                                 5: 'Apple Granny Smith',
                                 6: 'Apple Pink Lady',
                                 7: 'Apple Red 1',
                                 8: 'Apple Red 2',
                                 9: 'Apple Red 3',
                                 10: 'Apple Red Delicious',
                                 11: 'Apple Red Yellow 1',
                                 12: 'Apple Red Yellow 2',
                                 13: 'Apricot',
                                 14: 'Avocado',
                                 15: 'Avocado ripe',
                                 16: 'Banana',
                                 17: 'Banana Lady Finger',
                                 18: 'Banana Red',
                                 19: 'Beetroot',
                                 20: 'Blueberry',
                                 21: 'Cactus fruit',
                                 22: 'Cantaloupe 1',
                                 23: 'Cantaloupe 2',
                                 24: 'Carambula',
                                 25: 'Cauliflower',
                                 26: 'Cherry 1',
                                 27: 'Cherry 2',
                                 28: 'Cherry Rainier',
                                 29: 'Cherry Wax Black',
                                 30: 'Cherry Wax Red',
                                 31: 'Cherry Wax Yellow',
                                 32: 'Chestnut',
                                 33: 'Clementine',
                                 34: 'Cocos',
                                 35: 'Corn',
                                 36: 'Corn Husk',
                                 37: 'Cucumber Ripe',
                                 38: 'Cucumber Ripe 2',
                                 39: 'Dates',
                                 40: 'Eggplant',
                                 41: 'Fig',
                                 42: 'Ginger Root',
                                 43: 'Granadilla',
                                 44: 'Grape Blue',
                                 45: 'Grape Pink',
                                 46: 'Grape White',
                                 47: 'Grape White 2',
                                 48: 'Grape White 3',
                                 49: 'Grape White 4',
                                 50: 'Grapefruit Pink',
                                 51: 'Grapefruit White',
                                 52: 'Guava',
                                 53: 'Hazelnut',
                                 54: 'Huckleberry',
                                 55: 'Kaki',
                                 56: 'Kiwi',
                                 57: 'Kohlrabi',
                                 58: 'Kumquats',
                                 59: 'Lemon',
                                 60: 'Lemon Meyer',
                                 61: 'Limes',
                                 62: 'Lychee',
                                 63: 'Mandarine',
                                 64: 'Mango',
                                 65: 'Mango Red',
                                 66: 'Mangostan',
                                 67: 'Maracuja',
                                 68: 'Melon Piel de Sapo',
                                 69: 'Mulberry',
                                 70: 'Nectarine',
                                 71: 'Nectarine Flat',
                                 72: 'Nut Forest',
                                 73: 'Nut Pecan',
                                 74: 'Onion Red',
                                 75: 'Onion Red Peeled',
                                 76: 'Onion White',
                                 77: 'Orange',
                                 78: 'Papaya',
                                 79: 'Passion Fruit',
                                 80: 'Peach',
                                 81: 'Peach 2',
                                 82: 'Peach Flat',
                                 83: 'Pear',
                                 84: 'Pear 2',
                                 85: 'Pear Abate',
                                 86: 'Pear Forelle',
                                 87: 'Pear Kaiser',
                                 88: 'Pear Monster',
                                 89: 'Pear Red',
                                 90: 'Pear Stone',
                                 91: 'Pear Williams',
                                 92: 'Pepino',
                                 93: 'Pepper Green',
                                 94: 'Pepper Orange',
                                 95: 'Pepper Red',
                                 96: 'Pepper Yellow',
                                 97: 'Physalis',
                                 98: 'Physalis with Husk',
                                 99: 'Pineapple',
                                 100: 'Pineapple Mini',
                                 101: 'Pitahaya Red',
                                 102: 'Plum',
                                 103: 'Plum 2',
                                 104: 'Plum 3',
                                 105: 'Pomegranate',
                                 106: 'Pomelo Sweetie',
                                 107: 'Potato Red',
                                 108: 'Potato Red Washed',
                                 109: 'Potato Sweet',
                                 110: 'Potato White',
                                 111: 'Quince',
                                 112: 'Rambutan',
                                 113: 'Raspberry',
                                 114: 'Redcurrant',
                                 115: 'Salak',
                                 116: 'Strawberry',
                                 117: 'Strawberry Wedge',
                                 118: 'Tamarillo',
                                 119: 'Tangelo',
                                 120: 'Tomato 1',
                                 121: 'Tomato 2',
                                 122: 'Tomato 3',
                                 123: 'Tomato 4',
                                 124: 'Tomato Cherry Red',
                                 125: 'Tomato Heart',
                                 126: 'Tomato Maroon',
                                 127: 'Tomato Yellow',
                                 128: 'Tomato not Ripened',
                                 129: 'Walnut',
                                 130: 'Watermelon'
                                 }
        if file:
            # Read the image using skimage
            img = io.imread(file)
            #img = transform.resize(img, (45, 45))
            img = cv2.resize(img, dsize=(45, 45))

            img = img.flatten()
            scaled_img = pca_scaler.transform([img])
            prepped_img = pca_model.transform(scaled_img)

            # Get prediction of image from classifier
            predictions = RF_fruitTree_classifier.predict(prepped_img)
            # predictions = RF_fruitTree_classifier.predict([img])

            # Get the value of the prediction
            # prediction = item_identifier_names[predictions[0]] + " "+ str(predictions[0])
            prediction = item_identifier_names[predictions[0]]

            # For rendering image
            im = Image.open(file)
            data = BytesIO()
            im.save(data, "PNG")
            # Saves image in-memory, no need to save it into a folder.
            encoded_img_data = base64.b64encode(data.getvalue())

            return flask.render_template('classify_image_RF.html',
                                         prediction=str(prediction),
                                         img_data = encoded_img_data.decode('utf-8'))

    return(flask.render_template('classify_image_RF.html')) 

@app.route('/classify_image_NFnet', methods=['GET','POST'])
def classify_image_NFnet():
    return

if __name__ == '__main__':
    app.run(debug=True)