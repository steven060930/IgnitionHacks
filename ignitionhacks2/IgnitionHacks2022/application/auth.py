from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
import csv
from .utils import process, gen, write, missing
from PIL import Image
from .cropper import cropping
import cv2


auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'static/files'
UPLOAD_EXTENSIONS= ['.jpg', '.png']
UPLOAD_FOLDER_STUDENT = 'application\students'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('firstName')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/registration', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("registration.html", user=current_user)


from .models import Upload


@auth.route("/submission", methods=['GET', 'POST'])
def submission():
    form = Upload()

    if request.method == 'POST':
        date = request.form.get('date')

    if form.validate_on_submit():
        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), UPLOAD_FOLDER,secure_filename(file.filename)))
        # rename the file to {date}.jpg
        filename = file.filename
        if os.path.splitext(filename)[0] != date.split('-'):
            old_name = r"application/static/files/" + str(filename)
            date_string = date.split('-')
            res = ('').join(date_string)
            new_name = r"application/static/files/" + res + ".jpg"

            os.rename(old_name, new_name)

        return redirect(url_for('views.home'))

    if request.method == 'POST':
        uploaded_file = request.files['file']

        if uploaded_file.filename != "":
            filename = uploaded_file.filename
            file_ext = os.path.splitext(filename)[1]

            if file_ext not in UPLOAD_EXTENSIONS:
                abort(400)
                
        return redirect(url_for('views.home'))
    
    return render_template('admin_submit.html', form=form)


@auth.route('/spreadsheet', methods=['GET', 'POST'])
def view_spreadsheet():
    path = "application/static/files/"
    images = os.listdir("application/static/files")

    for image in images: # the only file, should be correct, remove after processing, prevent duplicating, and save memory
        if image[-3:] != 'jpg':
            continue
        date = image.split('.')[0]
        path += image
        process(path, date)

        os.remove(path)

    file = open("application/data_storage/attendance_data.csv")
    csvreader = csv.reader(file)
    
    headings, data = [], []
    headings = next(csvreader)

    for row in csvreader:
        data.append(row)

    return render_template('view_spreadsheet.html', headings = headings, data = data)


from .models import Student

@auth.route('/viewclass', methods=['GET', 'POST'])
def classview():
    students, headings, id = [], ["Name", "id", "Profile"], 1

    ar = []
    line = 0
    with open('application/data_storage/class_list.csv', "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if line == 0:
                line += 1
            else:
                if len(row) == 0:
                    return redirect(url_for('auth.adding'))
                ar.append(row[0])

    for stu in ar:
        student = Student(stu, id)
        id += 1
        students.append(student)


    return render_template("view_class.html", headings=headings, data = students)


@auth.route('/admin/viewclass/addstudent', methods=['GET', 'POST'])
def adding():
    form = Upload()

    if request.method == 'POST':
        name = request.form.get('name')
        write(name)
    
    if form.validate_on_submit():
        file = form.file.data
        new_filename = name + ".jpg"
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'students/' ,secure_filename(new_filename)))
        
        images = os.listdir('application/students/')
        for image in images:
            image_path = 'application/students/' + image
            cropped_image= cropping(image_path)
            image_name = 'application/students/' + image
            os.remove(image_path)
            cv2.imwrite(image_name, cropped_image)
        
        return redirect(url_for('auth.classview'))

    return render_template("add_student.html", form=form)

@auth.route('/admin/viewclass/kickstudent', methods=['GET','POST'])
def kicking():
    if request.method=='POST':
        name = request.form.get('name')
        images = os.listdir('application/students')
        for student_image in images:
            if str(student_image).split('.')[0]== name:
                os.remove('application/students/'+student_image)
                return redirect(url_for('auth.classview'))

    return render_template("kick_student.html")


@auth.route('/viewfullattendance', methods=['GET', 'POST'])
def rawData():
    d = gen()

    headings, data = ["name", "absent days"], []
    
    for student in d:
        s= ", ".join(d[student])
        if len(d[student]) == 0:
            s = "The Student didn't miss any class!"
        data.append((student, s))

    return render_template('view_raw_data.html', headings=headings, data=data, user=current_user)
    

@auth.route('/viewmissingstudents')
def missingStudents():
    g = missing()
    headings, data = ("Date", "Students"), []
    for key in g:
        s = ", ".join(g[key])
        data.append((key, s))
    return render_template("missing_students_date.html", headings=headings, data=data)
