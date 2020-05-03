from flask import Flask, redirect, url_for, render_template, request, flash, session
from requests import get
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# Jobs
jobs = get("http://api.dataatwork.org/v1/jobs").json()
job_titles = []

for job in jobs:
  try:
    job_titles.append(job["title"])
  except:
    continue

# Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "hello"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


# Database
db = SQLAlchemy(app)

class Assistants(db.Model):
  _id = db.Column("id", db.Integer, primary_key=True)
  first_name = db.Column(db.String(100))
  last_name = db.Column(db.String(100))
  username = db.Column(db.String(100))
  profession = db.Column(db.String(100))
  picture = db.Column(db.String(100))
  
  def __init__(self, username, first_name, last_name, profession, picture):
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.profession = profession
    self.picture = picture

# Routes
@app.route("/")
def home():
  return redirect(url_for("assist_source"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/assistants/create/", methods=["POST", "GET"])
def assist_create():
  if request.method == "POST":
    username = request.form["username"]
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    profession = request.form["professions"]

    if "picture" not in request.files:
            flash('No file part')
            return redirect(request.url)

    f = request.files["picture"]

    if f.filename == "":
            flash("No file selected")
    pic_name = secure_filename(f.filename)
    pic_url = f"static/{pic_name}"

    if f and allowed_file(f.filename):
      f.save(pic_url)
    
    picture = pic_name


    # print(username + first_name + last_name + profession)
    
    found_user = Assistants.query.filter_by(username=username).first()
    if found_user:
      return render_template("assist.html")
    else:
      usr = Assistants(username, first_name, last_name, profession, picture)
      db.session.add(usr)
      db.session.commit()

    return render_template("assist_create.html", jobs=job_titles)
  else:
    return render_template("assist_create.html", jobs=job_titles)

@app.route("/assistants/update/<string:username>", methods=["POST", "GET"])
def assist_update(username):
  found_user = Assistants.query.filter_by(username=username).first()
  if request.method == "POST":
    new_username = request.form["username"]
    new_first_name = request.form["firstName"]
    new_last_name = request.form["lastName"]
    try:
      new_profession = request.form["professions"]
      if new_profession != found_user.profession:
        found_user.profession = new_profession
    except:
      pass
    
    f = request.files["picture"]

    if f.filename == "":
      pass

    pic_name = secure_filename(f.filename)
    pic_url = f"static/{pic_name}"

    if f and allowed_file(f.filename):
      f.save(pic_url)
    
    new_picture = pic_name

    if new_username != found_user.username and len(new_username) >= 1:
      found_user.username = new_username
    if new_first_name != found_user.first_name and len(new_first_name) >= 1:
      found_user.first_name = new_first_name
    if new_last_name != found_user.last_name and len(new_last_name) >= 1:
      found_user.last_name = new_last_name
    if new_picture != found_user.picture and len(new_picture) >= 1:
      os.remove(f"static/{found_user.picture}")
      found_user.picture = new_picture
    
    db.session.commit()

    return render_template("assist_update.html", jobs=job_titles, assist=found_user)

  else:
    return render_template("assist_update.html", jobs=job_titles, assist=found_user)

@app.route("/assistants/")
def assist_source():
  return render_template("assist.html", assistants=Assistants.query.all())

@app.route("/assistants/delete/<string:username>", methods=["POST", "GET", "DELETE"])
def assist_delete(username):
  found_user = Assistants.query.filter_by(username=username).first()
  if request.method == "POST":
    os.remove(f"static/{found_user.picture}")
    db.session.delete(found_user)
    db.session.commit()
    return redirect(url_for("assist_source"))
  else:
    return render_template("assist_delete.html", jobs=job_titles, assist=found_user)


if __name__ == "__main__":
  db.create_all()
  app.run(debug=True)