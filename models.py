from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
db = SQLAlchemy()

class Mentor(db.Model):
  __tablename__ = "mentors"
  fname = db.Column(db.String(255), nullable=False)
  lname = db.Column(db.String(255), nullable=False)
  username = db.Column(db.String(255), primary_key=True)
  password = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  profile_pic = db.Column(db.String(255), nullable=False, default="mentor_pic.png")
  bio = db.Column(db.Text, nullable=False, default="Bio has not been edited by the user")
  job = db.Column(db.String(255), nullable=False)
  cv_help = db.Column(db.Boolean, nullable=False)
  meetStudents = db.Column(db.Boolean, nullable=False)
  mockInterview = db.Column(db.Boolean, nullable=False)
  workExp = db.Column(db.Boolean, nullable=False)


class Mentee(db.Model):
  __tablename__ = "mentees"
  fname = db.Column(db.String(255), nullable=False)
  lname = db.Column(db.String(255), nullable=False)
  prn_num = db.Column(db.String(255), nullable=False)
  dob = db.Column(db.String(255), nullable=False)
  username = db.Column(db.String(255), primary_key=True)
  year = db.Column(db.String(255), nullable=False)
  password = db.Column(db.String(255), nullable=False)
  branch = db.Column(db.String(255), nullable=False)
  batch = db.Column(db.String(255), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  mobile_no = db.Column(db.Integer(), nullable=False)
  address = db.Column(db.String(255), nullable=False)
  blood_grp = db.Column(db.String(255), nullable=False)
  linkedin_pro = db.Column(db.String(255), nullable=False)
  profile_pic = db.Column(db.String(255), nullable=False, default="mentee_pic.png")
  father_name = db.Column(db.String(255), nullable=False)
  father_occupation = db.Column(db.String(255), nullable=False)
  father_mobile_no = db.Column(db.Integer(), nullable=False)
  father_email = db.Column(db.String(255), nullable=False)
  mother_name = db.Column(db.String(255), nullable=False)
  mother_occupation = db.Column(db.String(255), nullable=False)
  mother_mobile_no = db.Column(db.Integer(), nullable=False)
  mother_email = db.Column(db.String(255), nullable=False)
  hobbies = db.Column(db.String(255), nullable=False)
  strengths = db.Column(db.String(255), nullable=False)
  weakness = db.Column(db.String(255), nullable=False)
  goals = db.Column(db.String(255), nullable=False)
  ssc = db.Column(db.Float(), nullable=False)
  hsc = db.Column(db.Float(), nullable=False)
  cet_jee = db.Column(db.Float(), nullable=False)
  bio = db.Column(db.Text, nullable=False, default="Bio has not been edited by the user")
  cv_help = db.Column(db.Boolean, nullable=False)
  meetAlumni = db.Column(db.Boolean, nullable=False)
  mockInterview = db.Column(db.Boolean, nullable=False)


class Resource(db.Model):
    _tablename_ = "resources"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    file = db.Column(db.String(255), nullable=False, default="c.pdf")
    date_uploaded = db.Column(db.DateTime, default=datetime.utcnow)


class Mentee_Grades(db.Model):
  __tablename__ = "mentee_grades"
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  username = db.Column(db.String(255), nullable=False)
  sem = db.Column(db.Integer(), nullable=False)
  subject = db.Column(db.String(255), nullable=False)
  marks_ia = db.Column(db.Float(), nullable=False)
  marks_sem = db.Column(db.Float(), nullable=False)
  attempt2 = db.Column(db.Float(), nullable=False)
  attempt3 = db.Column(db.Float(), nullable=False)
  attempt4 = db.Column(db.Float(), nullable=False)
  
  
class Assigned_Mentee(db.Model):
   __tablename__ = "assigned_mentees"
   mentee = db.Column(db.String(255), primary_key = True)
   mentor = db.Column(db.String(255), nullable=False)