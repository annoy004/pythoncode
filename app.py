from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import base64

# Import overlay functions from the verify.py and verify2.py modules
from verify import overlay_cloth_on_model
from verify2 import overlay_lower_body_garment

app = Flask(__name__)

# Directory setup
UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = os.path.join('static', 'results')  # Output images saved here
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        model_image = request.files.get('model_image')
        clothes_image = request.files.get('clothes_image')
        garment_type = request.form.get('garment_type')

        if model_image and clothes_image:
            model_filename = secure_filename(model_image.filename)
            clothes_filename = secure_filename(clothes_image.filename)

            model_image_path = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)
            clothes_image_path = os.path.join(app.config['UPLOAD_FOLDER'], clothes_filename)
            output_filename = 'output_' + model_filename
            output_image_path = os.path.join(app.config['STATIC_FOLDER'], output_filename)

            model_image.save(model_image_path)
            clothes_image.save(clothes_image_path)

            if garment_type == 'lower_body':
                output_path, message = overlay_lower_body_garment(model_image_path, clothes_image_path, output_image_path)
            elif garment_type == 'upper_body':
                output_path, message = overlay_cloth_on_model(model_image_path, clothes_image_path, output_image_path)
            else:
                return jsonify({'error': 'Invalid garment type specified'})

            if output_path:
                # Encode the output image to base64
                with open(output_path, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
                return render_template('result.html', img_data=img_data)

            else:
                return jsonify({'error': message})
        else:
            return jsonify({'error': 'Files not provided or invalid file names'})

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
