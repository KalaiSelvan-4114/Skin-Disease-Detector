import os
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Initialize Firebase Admin SDK with your service account credentials
cred = credentials.Certificate('path_to_your_firebase_adminsdk.json')  # Update with the path to your Firebase credentials JSON
firebase_admin.initialize_app(cred, {
    'storageBucket': 'your_firebase_storage_bucket_name.appspot.com'  # Replace with your Firebase Storage bucket name
})

# Reference to the Firebase Storage bucket
bucket = storage.bucket()

# Load your trained machine learning model (the one you created above)
model = tf.keras.models.load_model('path_to_your_trained_model.h5')  # Replace with the path to your trained model

# Define function to download an image from Firebase Storage
def download_image_from_storage(file_location, local_save_path):
    """Download image from Firebase Storage to local machine."""
    blob = bucket.blob(file_location)  # Get the image blob from Firebase Storage
    try:
        # Log the file path to ensure it is correct
        print(f"Attempting to download from Firebase Storage at: {file_location}")
        
        # Check if the blob exists
        if blob.exists():
            blob.download_to_filename(local_save_path)
            print(f'Image {file_location} downloaded successfully to {local_save_path}')
        else:
            raise Exception(f"File {file_location} does not exist in Firebase Storage.")
    except Exception as e:
        print(f"Failed to download {file_location}. Error: {e}")
        raise

# Define function to process the image and make a prediction
def process_and_predict(image_path):
    """Process image and predict skin disease."""
    try:
        # Load and preprocess the image
        img = Image.open(image_path).resize((128, 128))  # Resize as per model input size (128x128)
        img = np.array(img) / 255.0  # Normalize the image
        img = np.expand_dims(img, axis=0)  # Add batch dimension

        # Make a prediction using the model
        prediction = model.predict(img)
        predicted_class = np.argmax(prediction, axis=1)[0]  # Get the predicted class index

        # Convert class index to actual label (assuming you have a class label mapping)
        class_labels = {0: 'Acne', 1: 'Psoriasis', 2: 'Vitiligo', 3: 'Healthy'}
        result = class_labels.get(predicted_class, 'Unknown')

        return result
    except Exception as e:
        return f"Error during prediction: {e}"

# Define Flask route to handle the request from ESP32-CAM
@app.route('/predict', methods=['POST'])
def handle_request():
    try:
        # Get the file location sent by ESP32-CAM in the request
        data = request.json
        file_location = data.get('file_location', 'images/captured.jpg')  # Default to 'images/captured.jpg'
        
        # Log the received file location
        print(f"Received file location: {file_location}")
        
        # Ensure file_location does not contain a leading slash
        if file_location.startswith('/'):
            file_location = file_location[1:]

        # Define local save path for the image
        local_save_path = os.path.join(os.getcwd(), 'downloaded_image.jpg')

        # Download the image from Firebase
        download_image_from_storage(file_location, local_save_path)
        
        # Process the image and get the prediction
        prediction_result = process_and_predict(local_save_path)

        # Send the prediction result back to the ESP32-CAM
        return prediction_result

    except Exception as e:
        print(f"Error during request processing: {e}")
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
