from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Response
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, PasswordField, validators
from camera import VideoCamera
import jsonify

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Change this to a strong secret key

# Initialize the database
db = SQLAlchemy(app)

# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Create the database tables
with app.app_context():
    db.create_all()
    
    
def get_user(username):
    users = {
        "john": {"password": sha256_crypt.hash("password123")},
        "jane": {"password": sha256_crypt.hash("password321")}
    }
    return users.get(username)


@app.route('/')
def index():
    """
    Render the home page.

    Returns:
        str: Rendered HTML content for the home page.
    """
    return render_template('home.html')

def gen(camera):
    """
    Video streaming generator function.

    Continuously captures frames from the given VideoCamera instance and yields them
    as a byte stream.

    Args:
        camera (VideoCamera): Instance of the VideoCamera class to capture frames from.

    Yields:
        bytes: Byte stream of the captured video frames.
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    Validates user credentials by comparing the entered password with the stored hashed password.
    
    Returns:
        str: Rendered HTML content for the login page or redirects to another page upon successful login.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        user = User.query.filter_by(username=username).first()

        if user:

            print(f"User found: {user.username}, Password hash: {user.password}")

            if sha256_crypt.verify(password, user.password):

                session['logged_in'] = True
                session['username'] = username

                print("Login successful!")
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                print("Password did not match.")
                flash('Invalid login', 'danger')
                return redirect(url_for('login'))
        else:
            print("Username not found.")
            flash('Username not found', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    """
    Handle user logout

    Clears the previous session and redirects to the login page.
    
    Returns:
        str: Rendered HTML content for the login page or redirects to another page upon successful login.
    """
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))


@app.route('/video_feed')
def video_feed():
    """
    Video streaming route. Used in the src attribute of the img tag.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():
    """
    Generates video frames with emotion detection results.
    """
    cam = VideoCamera()  
    
    while True:
        frame, emotion = cam.get_frame()  # Gets the processed frame and emotion
        if frame is None:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        


@app.route('/about')
def about():
    """
    Render the about page.

    Returns:
        str: Rendered HTML content for the about page.
    """
    return render_template('about.html')

class RegisterForm(Form):
    """
    Registration form class.

    Defines form fields and validation for user registration.

    Attributes:
        name (StringField): The name of the user.
        username (StringField): The username of the user.
        email (StringField): The email of the user.
        password (PasswordField): The password for the user.
        confirm (PasswordField): Field to confirm the password.
    """
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    Displays and processes the registration form. If the form is valid and the request
    method is POST, hashes the password and saves the user data to the database.
    
    Returns:
        str: Rendered HTML content for the registration page.
    """
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = sha256_crypt.hash(form.password.data)
        
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page after login.

    Returns:
        str: Rendered HTML content for the dashboard page.
    """
    if 'logged_in' in session:
        return render_template('dashboard.html')
    else:
        flash('Unauthorized, Please login', 'danger')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)