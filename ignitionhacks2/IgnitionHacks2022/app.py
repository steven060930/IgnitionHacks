from flask import Flask, url_for, redirect, request, session, g, abort, render_template,jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
import csv
from trainer import process
from PIL import Image
import json
from flask_mongoengine import MongoEngine


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

users = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'superscretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config['UPLOAD_FOLDER_STUDENT'] = 'student training'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.condig['MONGODV_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': '27017'
}


class Upload(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.before_request
def before_request():
    g.user = None

    if 'user_name' in session:
        user = [x for x in users if x.username == session['user_name']][0]
        g.user = user


@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ReEnteredPassword = request.form.get('re-entered-password')

        already_been_user = False
        for user in users:
            if user.username == username:
                already_been_user = True
                break
        
        if already_been_user:
            redirect(url_for('login'))
        if password == ReEnteredPassword:
            new_registered_user=User(username, password)
            users.append(new_registered_user)

            return redirect('/')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        registered_user = [x for x in users if x.username==username][0]
        
        if registered_user and registered_user.password == password:
            session['user_username'] = registered_user.username
            return redirect(url_for('admin'))

        else:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/admin/submission', methods=['GET', 'POST'])
def submission():
    form = Upload()

    if request.method == 'POST':
        date = request.form.get('date')

    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        # rename the file to {date}.jpg
        filename = file.filename
        if os.path.splitext(filename)[0] != date.split('-'):
            old_name = r"static/files/" + str(filename)
            date_string = date.split('-')
            res = ('').join(date_string)
            new_name = r"static/files/" + res + ".jpg"

            os.rename(old_name, new_name)
        # return "File has been uploaded"
        return redirect(url_for('admin'))

    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file.filename != "":
            filename = uploaded_file.filename
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
                
        return redirect(url_for('admin'))
    
    return render_template('admin_submit.html', form=form)


@app.route('/admin/spreadsheet', methods=['GET', 'POST'])
def view_spreadsheet():
    path = "static/files/"
    images = os.listdir("static/files")

    for image in images: # the only file, should be correct, remove after processing, prevent duplicating, and save memory
        date = image.split('.')[0]
        path += image
        process(path, date)

        os.remove(path)

    file = open("data_storage/attendance_data.csv")
    csvreader = csv.reader(file)
    
    headings = []
    headings = next(csvreader)

    data = []
    for row in csvreader:
        data.append(row)

    return render_template('view_spreadsheet.html', headings = headings, data = data)


class Student:
    def __init__(self, name, id, profile):
        self.name = name
        self.id = id
        self.profile = profile


@app.route('/admin/viewclass', methods=['GET', 'POST'])
def viewClass():
    students, headings, id = [], ["Name", "id", "profile"], 1
    images = os.listdir('student training/')
    for image in images:
        student_name= os.path.splitext(image)[0]
        path = r"student training/" + image
        image = Image.open(path)
        student = Student(student_name, id, image)
        students.append(student)
        id += 1

    return render_template("view_class.html", headings=headings, data = students, source=image)


@app.route('/admin/viewclass/addstudent', methods=['GET', 'POST'])
def add_student():
    form = Upload()

    if request.method == 'POST':
        name = request.form.get('name')
    
    if form.validate_on_submit():
        file = form.file.data
        new_filename = name + ".jpg"
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER_STUDENT'],secure_filename(new_filename)))

    return render_template("add_student.html", form=form)

@app.route('/admin/viewclass/kickstudent', methods=['GET','POST'])
def kick_student():
    if request.method=='POST':
        name = request.form.get('name')
        images = os.listdir('student training')
        for student_image in images:
            if str(student_image).split('.')[0]== name:
                os.remove('student training/'+student_image)
                return redirect(url_for('viewClass'))

    return render_template("kick_student.html")

if __name__ == '__main__':
    app.run(debug=True, port='5000')