# Emotion Recognition Web App

## Overview

The Emotion Recognition Web App is a Flask-based application that captures video feed from the user's webcam and detects the user's emotions in real-time using a pre-trained machine learning model. The app provides a dashboard where users can view their current emotional state, displayed along with the webcam feed.

## Features

- **User Authentication:** Users can register, log in, and log out securely.
- **Dashboard:** The main interface where the user's webcam feed is displayed alongside the detected emotion.
- **Real-Time Emotion Detection:** The app utilizes a machine learning model to recognize and display emotions such as happiness, sadness, anger, and more.
- **Responsive Design:** The application is designed to be mobile-friendly and works across various screen sizes.

## Tech Stack

- **Backend:** Flask, Python
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Machine Learning:** TensorFlow/Keras
- **Database:** MySQL (or any other database supported by Flask)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/emotion-recognition-web-app.git
cd emotion-recognition-web-app
```

2. Create a Virtual Environment


```bash
python3 -m venv venv
source venv/bin/activate 
# On Windows use `venv\Scripts\activate`
```
3. Install Dependencies

```bash
pip install -r requirements.txt
```
4. Configure the Database

Set up your database (e.g., MySQL) and update the database URI in the Flask app configuration.

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'

5. Apply Migrations

If you're using Flask-Migrate or a similar tool, apply the migrations to create the necessary database tables.

flask db init
flask db migrate -m "Initial migration."
flask db upgrade

6. Run the Application

```bash
python app.py
```
The application will start on http://127.0.0.1:5000/.
Usage
Register and Log In

    Navigate to the /register page to create an account.
    Log in using your credentials on the /login page.

Access the Dashboard

Once logged in, you can access the dashboard via the /dashboard route. The dashboard will display your webcam feed and the detected emotion.


Logout

You can log out using the /logout route, which will redirect you back to the login page.
File Structure

The application uses the following file structure:
```plaintext
.
├── app.py # Main application file
├── models.py # Database models
├── camera.py # Handles webcam and video processing
├── templates/ # HTML templates
│ ├── layout.html # Base layout template
│ ├── login.html # Login page template
│ ├── register.html # Registration page template
│ ├── dashboard.html # Dashboard page template
├── static/ # Static files (CSS, JS)
│ ├── styles.css # Custom styles
├── models/ # Pre-trained machine learning models
│ ├── \_mini_XCEPTION.102-0.66.hdf5 # Model for emotion detection
├── haarcascade_files/ # Haarcascade files for face detection
│ ├── haarcascade_frontalface_default.xml
├── README.md # This README file
├── requirements.txt # Python dependencies
└── ...
```

Future Enhancements

    Improved Emotion Detection: Incorporate additional models and techniques to enhance the accuracy of emotion detection.
    Emotion History: Add a feature to track and display emotion history over time.
    3D Rendering: Implement 3D models or avatars that change expressions based on the detected emotion.
    Mobile Support: Optimize the app for mobile devices, including the ability to capture video from mobile cameras.

Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any bugs or feature requests.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    The Emotion Recognition Web App is inspired by various open-source projects in the field of emotion detection and real-time video processing.
    Special thanks to the contributors who have worked on this project.

