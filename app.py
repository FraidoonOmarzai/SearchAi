from crypt import methods
from click import password_option
from flask import Flask, url_for, render_template, redirect, request
import flask
from flask_pymongo import PyMongo
import joblib
import numpy as np

app = Flask(__name__, template_folder='templates')

# mongodb connection codes
app.config["MONGO_URI"] = "mongodb://localhost:27017/User"
mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/math')
def math():
    return render_template('math.html')


@app.route('/main')
def main():
    return render_template('main.html')


# form section
@app.route('/register', methods=['POST', 'GET'])
def register():
    users = db.users

    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            users.insert_one({'name': request.form['name'],
                              'email': request.form['email'],
                              'password': request.form['password']})
            return redirect(url_for('main'))

        return "That email already exists! Please enter a different email"

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    users = db.users

    if request.method == 'POST':

        login_user = users.find_one({'email': request.form['email']})

        if login_user:
            if request.form['password'] == login_user['password']:
                return redirect(url_for('main'))
        return "wrong email/ password!" + f"{login_user['password']}"
    return render_template('login.html')


@app.route('/admin-login', methods=['POST', 'GET'])
def admin_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        if email == "omarzai@search.ai" and password == "112233":
            return redirect(url_for('admin'))

        return "wrong password/email!"

    return render_template('admin-login.html')


@app.route('/admin')
def admin():
    users = db.users.find()
    return render_template('admin.html', users=users)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    users = db.users.find()

    if request.method == 'POST':
        db.users.delete_one({"email": request.form['email_id']})

    return render_template('delete.html', users=users)


@app.route('/edit', methods=['POST', 'GET'])
def edit():

    if request.method == 'POST':
        db.users.delete_one({"email": request.form['email_id']})
        return render_template('updateUser.html')

    users = db.users.find()
    return render_template('edit.html', users=users)


@app.route('/updateUser', methods=['POST', 'GET'])
def updateUSer():
    users = db.users

    if request.method == 'POST':
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            users.insert_one({'name': request.form['name'],
                              'email': request.form['email'],
                              'password': request.form['password']})
            return redirect(url_for('edit'))

        return "That email already exists! Please enter a different email"

    return render_template('updateUser.html')


# medicine section
# 1- Breast Cancer
@app.route("/cancer")
def cancer():
    return render_template("cancer.html")


def CancerPredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if(size == 5):
        loaded_model = joblib.load(
            'Trained Model/breast_cancer/cancer_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictCancer', methods=["POST"])
def predictCancer():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))

        if(len(to_predict_list) == 5):
            result = CancerPredictor(to_predict_list, 5)

    if(int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return(render_template("result.html", prediction_text=prediction))

# 2- Diabetes


@app.route("/diabetes")
def diabetes():
    return render_template("diabetes.html")


def DiabetPredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if(size == 6):
        loaded_model = joblib.load('Trained Model/diabetes/diabetes_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictDiabet', methods=["POST"])
def predictDiabet():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))

        if(len(to_predict_list) == 6):
            result = DiabetPredictor(to_predict_list, 6)

    if(int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return(render_template("result.html", prediction_text=prediction))

# 3- Heart Disease


@app.route("/heart")
def heart():
    return render_template("heart.html")


def HeartPredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if(size == 9):
        loaded_model = joblib.load("Trained Model/heart/heart_model.pkl")
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictHeartD', methods=["POST"])
def predictHeartD():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        # print(to_predict_list)
        to_predict_list = list(to_predict_list.values())
        # print(to_predict_list)
        to_predict_list = list(map(float, to_predict_list))
        # print(to_predict_list)
        if(len(to_predict_list) == 9):
            result = HeartPredictor(to_predict_list, 9)

    if(int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return(render_template("result.html", prediction_text=prediction))

# 4- kidney


@app.route("/kidney")
def kidney():
    return render_template("kidney.html")


def KidneyPredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if(size == 7):
        loaded_model = joblib.load('Trained Model/kidney/kidney_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictKidneyD', methods=["POST"])
def predictKidneyD():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
        # print(to_predict_list)
        if(len(to_predict_list) == 7):
            result = KidneyPredictor(to_predict_list, 7)

    if(int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return(render_template("result.html", prediction_text=prediction))

# 5- Liver


@app.route("/liver")
def liver():
    return render_template("liver.html")


def LPredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1, size)
    if(size == 7):
        loaded_model = joblib.load('Trained Model/liver/liver_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]


@app.route('/predictLiverD', methods=["POST"])
def predictLiverD():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))

        if(len(to_predict_list) == 7):
            result = LPredictor(to_predict_list, 7)

    if(int(result) == 1):
        prediction = "Sorry you chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease"
    return(render_template("result.html", prediction_text=prediction))


if __name__ == '__main__':
    app.config['Debug'] = True
    app.run()
