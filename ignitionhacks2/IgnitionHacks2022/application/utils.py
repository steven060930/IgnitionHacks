import face_recognition
import cv2
import numpy as np
import os
import csv

path = "application/students/"
known_names,known_name_encodings = [], []
images = os.listdir(path)

for img in images:
    image_path = path + img
    image = face_recognition.load_image_file(image_path)

    encoding = np.array(face_recognition.face_encodings(image))[0]

    known_name_encodings.append(encoding)
    known_names.append(os.path.splitext(os.path.basename(image_path))[0].capitalize())


def write(name):
    with open("application/data_storage/class_list.csv", "a") as f:
        writer= csv.writer(f, lineterminator='\n')
        _buf = []
        _buf.append(name)
        writer.writerow(_buf)

def process(test_image_path, date):
    image = cv2.imread(test_image_path, 1)

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    appear_in_image = []

    for (x, y, w, h) , face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_name_encodings, face_encoding, tolerance=0.5)

        name = ""
        face_distances = face_recognition.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if matches[best_match]:
            name = known_names[best_match]
            appear_in_image.append(name)

    cv2.destroyAllWindows()

# ---------------------------------------------------------------------------------------------------------------------------- #
    with open ("application/data_storage/attendance_data.csv", "a") as f:
        writer = csv.writer(f, lineterminator='\n')

        for name in known_names:
            if name in appear_in_image:
                row = [str(date), str(name), "present"]
                writer.writerow(row)
            else:
                row = [str(date), str(name), "absent"]
                writer.writerow(row)



def gen():
    d = {}

    for name in known_names:
        d[name] = []

    line = 0
    with open ("application/data_storage/attendance_data.csv", mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            if line == 0:
                print(f'Headers are {", ".join(row)}')
                line += 1
            else:
                if row[-1] == 'absent':
                    d[row[1]].append(row[0])
    return d


def missing():
    dates = []

    with open("application/data_storage/attendance_data.csv") as f:
        line = 0
        reader = csv.reader(f)
        for row in reader:
            if line == 0:
                line += 1
            else:
                dates.append(row[0])

    dates = set(dates)

    absent_students = []

    with open("application/data_storage/attendance_data.csv") as f:
        cnt = 0
        reader = csv.reader(f)
        for row in reader:
            if cnt == 0:
                cnt += 1
            else:
                if row[-1] == "absent":
                    absent_students.append((row[0], row[1]))

    g = {}

    for date in dates:
        g[date] = []

    for pair in absent_students:
        g[pair[0]].append(pair[1])

    return g

# __________________________________________________________ header ___________________________________________________________ #
