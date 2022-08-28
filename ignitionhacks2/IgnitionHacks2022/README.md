# SmartTendance

Submission to IgnitionHacks 2022 by Tommy Shan, Steven Qiao, Doris Wang and John Lu.

## Inspiration

From a lot of online and on-site lectures and classes, we have found that there is a significant amount of teachers who used too much time on attendance, and once the class has too many students, it might take a while to finish attendance and might affect the lectures.

Therefore, we get the idea of making a smart attendance helper for the teachers to complete the class's attendance forms within seconds to solve this problem.


## What it does

SmartTendance is a full-stack developed web application, based on the website working as a portal. This allows the teacher to just submit a screenshot of the class, either in-person class or online meetings, and the written backend program will effectively help the teacher to turn the attendance into a CSV file, and visualize it in a dynamic table on the website.

Teachers can access the chart directly and will be able to know who is present and who is absent in class. Also, teachers have the access to the statistics of the frequency, distribution and much other information of the whole class or one individual student. This can also be helpful to teachers so that they are able to reach the student and help them very intuitively and efficiently.

## How we built it

### Python

We use the flask-python framework and many methods to build this project.

### HTML, CSS and JavaScript

We use HTML, CSS, and JavaScript to design the website page as the portal for the user and for many features.

### SQL

We worked with Flask-SQLAlchemy database for:

- storing the user data

- managing authentication

for the front-end website.

### OpenCV

We use OpenCV-python to implement the attendance helper tool. We applied a machine learning algorithm to encode face feature points and realize student detection by using a face-recognition algorithm within OpenCV.

## Challenges we ran into

The first challenge we meet is poor CPU / GPU and lack of time for applying TensorFlow machine learning to it and we overcome this challenge by trying many different methods and finding the most suitable one to use. After we solved the poor CPU / GPU issue, the second challenge we met is a lack of experience in operating with databases. We solved this problem by doing a lot of research and learning.

## Accomplishments we are proud of

- We successfully created a database for the web after our efforts.

- We did many amazing optimizations on our website.

- We built all the features successfully with our knowledge.

## What did we learn?

- We learned some machine learning knowledge and how to create a database for a web app. 

- We gained more experience to face and deal with difficulties and handle issues.

- We improved our HTML, CSS and JavaScript skills.

- We know more about many libraries and functions (e.g. OpenCV).

- Besides programming related, we learned how to allocate the work, handle the work, work as a team, and use our time efficiently.

## What's next for SmartTendance?

Due to the time limit of the hackathon, we can't do further it in the way we had planned with many more features. It can create classes for the teachers and separate teachers (admin) accounts and student (user) accounts. Our team will definitely add those features soon, try to publish it on the web, and let everyone be able to use it and take advantage in the close future.

We also plan to make it a real app and continue to test it, updated it to new versions, and benefit others with smartTendance.

Back in the term of the application itself, we are going to connect it to a hardware project and put it into classrooms, and let the mini-camera capture the class pictures and load it itself!



## To run this file

1. Clone this Github repo.

      On your local device, please delete ```application/static/files/1.txt``` and ```application/students/1.txt``` (Github can not upload empty folders).

2. Install Cmake and dilib:

      Add Cmake to Visual Studio, or if u know how to install dlib locally, install it directly.

3. download the dependicies:

      ```$ pip install -r requirements.txt```
