from turtle import done
from flask import Flask, render_template, request, url_for, redirect, Response, session, jsonify
from pymongo import MongoClient
from passlib.hash import sha256_crypt
import uuid
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import face_recognition
import os


app = Flask(__name__)
app.secret_key = "test"

client = MongoClient('localhost', 27017)
db = client.info
info = db.info


@app.route("/")
def home():
    return render_template("home.html")


class User:

    def start_session(self, user):
        print("insert 2")
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        print("Inside func signup")
        print(request.form)

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"]
        }
        global username
        username = user["name"]
        global useremail
        useremail = user["email"]
        # Encrypt the password
        user['password'] = sha256_crypt.hash(user['password'])

        # Check for existing email address
        if db.info.find_one({"email": user['email']}):
            print("email")
            return jsonify({"error": "Email address already in use"}), 400

        if db.info.insert_one(user):
            print("Insert")
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        print(request.form)
        user = db.info.find_one({"email": request.form['email']})
        global username
        username = user["name"]
        global useremail
        useremail = user["email"]

        if user and sha256_crypt.verify(request.form['password'], user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401


@app.route('/signup', methods=['GET'])
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup1():
    return User().signup()


@app.route('/login', methods=["POST"])
def login1():
    return User().login()


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route('/signout')
def signout():
    return User().signout()


@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html", username=username)


@app.route("/data", methods=["POST"])
def dashboard1():
    print("data posted")
    return "done"


@app.route("/bill", methods=["GET"])
def bill():
    return render_template("bill.html", username=username)


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html", username=username, email=useremail)


@app.route("/failedpayment", methods=["GET"])
def failedpayment():
    name = username
    return render_template("failedpayment.html", name=name)


@app.route("/wallet", methods=["GET"])
def wallet():
    return render_template("wallet.html", username=username)


@app.route('/image', methods=['GET'])
def image():
    print("username")
    return render_template("image.html", username=username)


@app.route('/image', methods=['POST'])
def image1():
    print("Image capture stated")
    print(useremail)
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("test")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
        data = "press q to exit and space bar to capture"
        cv2.putText(frame, data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 2)
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k == ord("q"):
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:
            # SPACE pressed
            path = "images"
            img_name = "{}.png".format(useremail)
            print(img_name)
            cv2.imwrite(os.path.join(path, img_name), frame)
            print("{} written!".format(img_name))
            break
    cam.release()
    cv2.destroyAllWindows()
    return "done"


@app.route("/details", methods=["GET"])
def details():
    name = username
    return render_template("details.html", name=name)


@app.route('/capture', methods=['POST'])
def capture():
    cap = cv2. VideoCapture(0)
    while True:
        success, img = cap.read()
        data = "press q to exit"
        cv2.putText(img, data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 2)
        for barcode in decode(img):
            mydata = "verified"
            pts = np.array([barcode.polygon], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (255, 0, 255), 5)
            pts2 = barcode.rect
            cv2.putText(
                img, mydata, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
        cv2.imshow("result", img)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    return "done"


@app.route("/compare", methods=["POST"])
def compare():
    camera = cv2.VideoCapture(0)
    print(username)
    # Load a sample picture and learn how to recognize it.
    known_image = face_recognition.load_image_file(
        "images/{}.png".format(useremail))
    print("ok")
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    recognised_face_encodings = [
        known_face_encoding
    ]
    known_face_names = [
        "{}_user".format(username)
    ]
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break

        else:
            data = "press q to exit"
            cv2.putText(frame, data, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (255, 0, 255), 2)
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    recognised_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(
                    recognised_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35),
                              (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            font, 1.0, (255, 255, 255), 1)
            cv2.imshow("result", frame)
            if cv2.waitKey(1) == ord("q"):
                break
    camera.release()
    cv2.destroyAllWindows()
    if name != "Unknown":
        return "done"
    else:
        return 404


@app.route("/payment", methods=["GET"])
def payment():
    print("payment successful")
    return render_template("payment.html", username=username)


@app.route("/transaction", methods=["GET"])
def transaction():
    return render_template("transaction.html", username=username)


if __name__ == "__main__":
    app.run(debug=True)
