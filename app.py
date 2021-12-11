from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
import numpy as np
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads/'
model = load_model('model_kesatu.h5')


def predict_label(img_path):
    x = load_img(img_path, target_size=(250,250))
    x = img_to_array(x)
    x = np.expand_dims(x, axis=0)
    array = model.predict(x)
    result = array[0]
    answer = np.argmax(result)
    if answer == 0:
        print("Label: daisy")
    elif answer == 1:
	    print("Label: dandelion")
    elif answer == 2:
	    print("Label: rose")
    elif answer == 3:
	    print("Label: sunflower")
    elif answer == 4:
	    print("Label: tulip")
    
    return answer

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.files:
            image = request.files['image']
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(img_path)
            result = predict_label(img_path)
            if result == 0:
                prediction = 'daisy'
            elif result == 1:
                prediction = 'dandelion'			
            elif result == 2:
                prediction = 'rose'
            elif result == 3:
                prediction = 'sunflower'
            elif result == 4:
                prediction = 'tulip'
            return render_template('index.html', uploaded_image=image.filename, prediction=prediction)

    return render_template('index.html')

@app.route('/display/<filename>')
def send_uploaded_image(filename=''):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run()