Skin Disease Detector
This project uses an ESP32-CAM to capture skin images, upload them to Firebase Storage, and process them with a Flask server running a machine learning model to detect skin diseases. The result is returned to the ESP32-CAM, which can display the prediction on an LCD.

Features
ESP32-CAM Integration: Captures and uploads skin images to Firebase Storage.
Machine Learning Model: Processes images to predict skin diseases (e.g., Acne, Psoriasis, Vitiligo, Healthy).
Flask Server: Handles image retrieval from Firebase and performs predictions using a pre-trained TensorFlow model.
LCD Display Support: Displays the prediction result on a 16x2 LCD connected to the ESP32-CAM.
Architecture Overview
ESP32-CAM:

Captures skin images.
Uploads images to Firebase Storage.
Sends the file location to the Flask server.
Displays the prediction result.
Firebase Storage:

Stores captured images for analysis.
Flask Server:

Downloads images from Firebase.
Processes images using the TensorFlow model.
Returns the predicted result to the ESP32-CAM.
Machine Learning Model:

Trained to classify skin conditions into predefined categories.
Installation and Setup
ESP32-CAM
Dependencies:

Arduino IDE.
Install the ESP32 board package.
Install the LiquidCrystal_I2C library for the LCD display.
Setup:

Flash the ESP32-CAM Arduino sketch (esp32_cam_skin_disease.ino) to the board.
Update the following values in the sketch:
Wi-Fi credentials (ssid and password).
Firebase Storage URL.
Flask server IP and port.
Connections:

Connect a 16x2 LCD to the ESP32-CAM using an I2C interface.
Flask Server
Dependencies:

Python 3.x.
Install required libraries: firebase-admin, Flask, tensorflow, Pillow, numpy.
bash
Copy code
pip install firebase-admin Flask tensorflow Pillow numpy
Setup:

Place your Firebase Admin SDK JSON file in the same directory as the server script.
Update the Flask server script (skin_disease_server.py) with:
Path to the Firebase Admin SDK JSON file.
Firebase bucket name.
Path to the trained TensorFlow model (skin_disease_model.h5).
Run the Server:

bash
Copy code
python skin_disease_server.py
The server will run on http://0.0.0.0:5000/predict.
Machine Learning Model
Training:

Train a TensorFlow model to classify skin diseases. Ensure the input size matches the Flask script (e.g., 128x128).
Save the model as skin_disease_model.h5.
Categories:

Ensure the model's output categories match those defined in the Flask script (Acne, Psoriasis, Vitiligo, Healthy).
