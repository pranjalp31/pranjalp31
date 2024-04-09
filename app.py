import os
from flask import Flask, session, render_template, request, redirect,url_for,jsonify,flash
from flask_session import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import secrets
from models import *
from werkzeug.utils import secure_filename
from datetime import datetime
import qrcode
from flask import Flask, render_template, send_file
from io import BytesIO
import qrcode
import pandas as pd

import plotly.graph_objs as go


app = Flask(__name__)

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/qrconnect"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def login():
    if session.get("username") == None:
        return render_template("login.html")
    else:
        if session.get("user_type") == "mentee":
            return redirect(url_for('menteeHome'))
        else:
            return redirect(url_for('mentorHome'))

@app.route("/validateUser", methods=["POST"])
def validateUser():
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        user_data = Mentee.query.filter_by(username=username).one()
    except:
        #username not in the mentee table try the mentor table
        try:
            user_data = Mentor.query.filter_by(username=username).one()
        except:
            #not in the mentor or mentee table
            flash("Username does not exist")
            return redirect(url_for('login'))
        else:
            user_data_fetched = True
            user_type = "mentor"
    else:
        user_data_fetched = True
        user_type = "mentee"

    if user_data_fetched:
        if password == user_data.password:
            file_path = "img/" + str(user_data.profile_pic)
            session.update({"username":username, "fname":user_data.fname, "lname":user_data.lname,"user_type":user_type,"email":user_data.email, "pic":file_path, "cv_help":user_data.cv_help, "bio":user_data.bio ,"mockInterview":user_data.mockInterview })
            if user_type == "mentee":
                session.update({"meetAlumni": user_data.meetAlumni, "prn_num":user_data.prn_num, "branch": user_data.branch, "batch": user_data.batch, "linkedin_pro": user_data.linkedin_pro})
                return redirect(url_for('menteeHome'))
            else:
                session.update({"job":user_data.job, "meetStudents":user_data.meetStudents,  "workExp":user_data.workExp})
                return redirect(url_for('mentorHome'))
        else:
            flash("Incorrect password or username, please try again!")
            return redirect(url_for('login'))

@app.route('/log_out')
def log_out():
    session.pop("username")
    return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerUser", methods=["POST"])
def registerUser():
    menteeForm = request.form.get("menteeFormbutton")
    mentorForm = request.form.get("mentorFormButton")

    print(" ---------------- in the register user function ---------------- ----------------")

    if mentorForm != None:
        fname = request.form.get("fname2")
        lname = request.form.get("lname2")
        username = request.form.get("username2")
        password = request.form.get("password2")
        email = request.form.get("email2")
        job = request.form.get("job")

        cv_help = True if request.form.get("cvhelp2") == "on" else False
        meet_students = True if request.form.get("meet_students") == "on" else False
        mockInterview = True if request.form.get("mockInterview2")  == "on" else False
        workExp = True if request.form.get("workExp") == "on" else False

        new_mentor = Mentor(fname=fname, lname=lname, username=username, profile_pic= "mentor_pic.png" ,password=password, email=email, job=job, cv_help=cv_help, meetStudents= meet_students, mockInterview=mockInterview, workExp=workExp)
        db.session.add(new_mentor)
        db.session.commit()
        session.update({"username":username, "fname":fname, "lname":lname, "bio":"-", "pic":"img/mentor_pic.png" , "user_type":"mentor", "email":email, "job":job, "cv_help":cv_help,"meetStudents":meet_students, "mockInterview":mockInterview, "workExp":workExp })

    else:
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        prn_num = request.form.get("")
        dob = request.form.get("")
        year = request.form.get("")
        mobile_no = request.form.get("")
        address = request.form.get("")
        blood_grp = request.form.get("")
        branch = request.form.get("")
        batch = request.form.get("")
        linkedin_pro = request.form.get("")
        father_name = request.form.get("")
        father_occupation = request.form.get("")
        father_mobile_no = request.form.get("")
        father_email = request.form.get("")
        mother_name = request.form.get("")
        mother_occupation = request.form.get("")
        mother_mobile_no = request.form.get("")
        mother_email = request.form.get("")
        hobbies = request.form.get("")
        strengths = request.form.get("")
        weakness = request.form.get("")
        goals = request.form.get("")
        ssc = request.form.get("")
        hsc = request.form.get("")
        cet_jee = request.form.get("")

        cv_help = True if request.form.get("cvhelp") == "on" else False
        meetAlumni = True if request.form.get("meetAlumni") == "on" else False
        mockInterview = True if request.form.get("mockInterview") == "on" else False

        new_mentee = Mentee(fname=fname, lname=lname, prn_num = "", year = '', branch = "", batch = "",username=username, profile_pic= "mentee_pic.png" , password=password, linkedin_pro = "", dob = "", mobile_no = "", address = '', blood_grp = '', father_name = '', father_occupation = '', father_mobile_no = '', father_email = '', mother_name = '', mother_occupation = '', mother_mobile_no = '', mother_email = '', ssc = '', hsc = '', cet_jee = '', hobbies = '', strengths = '', weakness = '', goals = '', email=email, cv_help=cv_help, meetAlumni= meetAlumni, mockInterview=mockInterview)
        db.session.add(new_mentee)
        db.session.commit()
        session.update({"username":username, "fname":fname, "lname":lname, 'prn_num': prn_num, 'dob': dob, 'mobile_no': mobile_no, 'address': address, 'blood_grp': blood_grp, 'father_name': father_name, 'father_occupation': father_occupation, 'father_mobile_no': father_mobile_no, 'father_email': father_email, 'mother_name': mother_name, 'mother_occupation': mother_occupation, 'mother_mobile_no': mother_mobile_no, 'mother_email': mother_email, 'hobbies': hobbies, 'strengths': strengths, 'weakness': weakness, 'goals': goals, 'ssc': ssc, 'hsc': hsc, 'cet_jee': cet_jee,"bio":"-", "pic":"img/mentee_profile.png", "user_type":"mentee", 'year': year, "email":email, "branch": branch, "batch": batch, "linkedin_pro": linkedin_pro,"cv_help":cv_help,"meetAlumni": meetAlumni, "mockInterview":mockInterview})

    return redirect(url_for('mentorHome')) if mentorForm != None else redirect(url_for('menteeHome'))

@app.route("/menteeHome", methods=["GET"])
def menteeHome():
    return render_template("menteeHome.html")

@app.route("/resources", methods=["GET"])
def resources():
    username = session.get('username')
    resources_data = Resource.query.filter_by(username=username).all()
    NUMBER_OF_RESOURCES = len(resources_data)
    return render_template("resources.html", resources_data = resources_data)

@app.route("/deleteResource/<int:id>", methods=["POST"])
def deleteResource(id):
    # Fetch the resource by its ID and delete it
    resource = Resource.query.get(id)
    if resource:
        db.session.delete(resource)
        db.session.commit()
    return redirect(url_for('resources'))

@app.route("/network", methods=["GET", "POST"])
def network():
    mentee_data = session["mentee_data"] = True
    mentor_data = session["mentor_data"] = True
    if request.method == 'POST':
        mentee_data = session["mentee_data"] = True if request.form.get("viewMentees") == "on" else False
        mentor_data = session["mentor_data"] = True if request.form.get("viewMentors") == "on" else False
    if mentee_data:
        mentee_data = Mentee.query.filter_by().all()
    if mentor_data:
        mentor_data = Mentor.query.filter_by().all()
    if (not mentee_data) and (not mentor_data):
        flash("I hope you enjoy looking at a blank screen...")
    return render_template("network.html",  mentee_data = mentee_data, mentor_data = mentor_data)

@app.route('/changePassword', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        username = session.get('username')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        # Query the Mentee table for the specific user
        mentee = Mentee.query.filter_by(username=username).first()

        if mentee:
            if mentee.password == old_password:
                # The old password is correct, update the password for the user
                mentee.password = new_password
                db.session.commit()
                flash('Password successfully changed')
                return redirect(url_for('editProfile'))
            else:
                flash('Error: Old password is incorrect')
        
    # Render the "Change Password" page for GET requests
    return render_template('change_password.html')

@app.route('/deleteMentee/<username>', methods=['GET', 'POST'])
def delete_mentee(username):
    # Handle the deletion of the mentee with the given username
    mentee = Assigned_Mentee.query.filter_by(mentee=username).first()

    if mentee:
        # Delete the mentee from your database
        db.session.delete(mentee)
        db.session.commit()
        flash(f'Mentee {username} has been deleted', 'success')
    else:
        flash(f'Mentee {username} not found', 'error')

    return redirect(url_for('mentee'))

@app.route("/mentorHome", methods=["GET"])
def mentorHome():
    #add a check to make sure that the user is indeed a mentor
    return render_template("mentorHome.html")

'''@app.route("/editProfile", methods=["GET"])
def editProfile():
    return render_template("editProfile.html")
'''

@app.route("/editProfile", methods=["GET"])
def editProfile():
    # Fetch academic details for the logged-in mentee
    if session.get("user_type") == "mentee":
        username = session.get('username')
        academic_details = Mentee_Grades.query.filter_by(username=username).all()

        # Initialize lists to store semester-wise CGPA and corresponding semester numbers
        semesters = []
        cgpa_values = []

        # Iterate through academic details to calculate CGPA
        current_semester = 0
        total_marks = 0
        total_credit_hours = 0

        for detail in academic_details:
            # Assuming each subject has a fixed credit hour
            credit_hours = 4  # Example: 4 credit hours per subject

            if detail.sem != current_semester:
                if current_semester != 0:
                    # Calculate CGPA for the previous semester and append to lists
                    cgpa = total_marks / total_credit_hours
                    semesters.append(current_semester)
                    cgpa_values.append(cgpa)

                # Reset variables for the new semester
                current_semester = detail.sem
                total_marks = 0
                total_credit_hours = 0

            # Accumulate total marks and credit hours for the current semester
            total_marks += detail.marks_sem
            total_credit_hours += credit_hours

        # Calculate CGPA for the last semester
        cgpa = total_marks / total_credit_hours
        semesters.append(current_semester)
        cgpa_values.append(cgpa)

        # Create line chart data
        line_chart = go.Figure()
        line_chart.add_trace(go.Scatter(x=semesters, y=cgpa_values, mode='lines+markers', name='CGPA'))

        # Update chart layout
        line_chart.update_layout(title='Semester-wise CGPA',
                                 xaxis_title='Semester',
                                 yaxis_title='CGPA')

        # Convert Plotly chart to HTML
        line_chart_html = line_chart.to_html(full_html=False)

        return render_template("editProfile.html", line_chart_html=line_chart_html)
    else:
        # Handle mentor profile editing
        return render_template("editProfile.html")
    

    

@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/profileChanges", methods=["POST"])
def profileChanges():
    if session.get("user_type") == "mentee":
        user_data = Mentee.query.filter_by(username=session.get("username")).one()
        user_data.meetAlumni = session["meetAlumni"] = True if request.form.get("meetAlumni") == "on" else False
        user_data.mockInterview = session["mockInterview"] = True if request.form.get("mockInterview") == "on" else False
        
        user_data.fname = session["fname"] = request.form.get("fname")
        user_data.lname = session["lname"] = request.form.get("lname")
        user_data.prn_num = session["prn_num"] = request.form.get("prn_num")
        user_data.dob = session["dob"] = request.form.get("dob")
        user_data.year = session["year"] = request.form.get("year")
        user_data.mobile_no = session["mobile_no"] = request.form.get("mobile_no")
        user_data.address = session["address"] = request.form.get("address")
        user_data.blood_grp = session["blood_grp"] = request.form.get("blood_grp")
        user_data.branch = session["branch"] = request.form.get("branch")
        user_data.batch = session["batch"] = request.form.get("batch")
        user_data.father_name = session["father_name"] = request.form.get("father_name")
        user_data.father_occupation = session["father_occupation"] = request.form.get("father_occupation")
        user_data.father_mobile_no = session["father_mobile_no"] = request.form.get("father_mobile_no")
        user_data.father_email = session["father_email"] = request.form.get("father_email")
        user_data.mother_name = session["mother_name"] = request.form.get("mother_name")
        user_data.mother_occupation = session["mother_occupation"] = request.form.get("mother_occupation")
        user_data.mother_mobile_no = session["mother_mobile_no"] = request.form.get("mother_mobile_no")
        user_data.mother_email = session["mother_email"] = request.form.get("mother_email")
        user_data.hobbies = session["hobbies"] = request.form.get("hobbies")
        user_data.strengths = session["strengths"] = request.form.get("strengths")
        user_data.weakness = session["weakness"] = request.form.get("weakness")
        user_data.goals = session["goals"] = request.form.get("goals")
        user_data.ssc = session["ssc"] = request.form.get("ssc")
        user_data.hsc = session["hsc"] = request.form.get("hsc")
        user_data.cet_jee = session["cet_jee"] = request.form.get("cet_jee")
        user_data.linkedin_pro = session["linkedin_pro"] = request.form.get("linkedin_pro")        
    else:
        user_data = Mentor.query.filter_by(username=session.get("username")).one()
        user_data.meetStudents = session["meetStudents"] = True if request.form.get("meet_students") == "on" else False
        user_data.mockInterview = session["mockInterview"] = True if request.form.get("mockInterview2") == "on" else False
        user_data.workExp = session["workExp"] = True if request.form.get("workExp") == "on" else False
    
        user_data.job = session["job"] = request.form.get("job")
        user_data.bio = session["bio"] = request.form.get("bio")
        user_data.cv_help = session["cv_help"] = True if request.form.get("cvhelp2") == "on" else False
        
    file = request.files['file'] #this gets the file
    if not file.filename == '':
        filename = secure_filename(file.filename)
        picture_path = os.path.join(app.root_path, 'static/img', filename)
        print(picture_path)
        file.save(picture_path)
        user_data.profile_pic = filename
        session["pic"] = "img/" + str(filename)
        flash("Profile picture has been uploaded")
    
    username = session.get('username')
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=15, border=5)
    filename = f"static/img/qrcode_{session['username']}.png"
    profile_data = f'http://127.0.0.1:5000//verify_mentor_credentials/{username}'
    qr.add_data(profile_data)
    qr.make(fit=True)

    # Create an image of the QR code
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(filename)
    
    timestamp = int(datetime.now().timestamp())
    db.session.commit()
    
    if session["bio"] == "":
        flash("Adding a bio will make your profile look good! (Changes of any other fields have been saved)")
        return redirect(url_for('editProfile'))
    flash("Changes have been saved to the database")
    return render_template("editProfile.html", timestamp=timestamp)


@app.route('/view_profile/<username>', methods=['GET', 'POST'])
def view_profile(username):
    mentee = Mentee.query.filter_by(username=username).first()
    return render_template('viewProfile.html', mentee=mentee)


@app.route('/verify_mentor_credentials/<username>', methods=['GET', 'POST'])
def verify_mentor_credentials(username):
    mentee_username = username
    if request.method == 'POST':
        mentor_username = request.form.get('mentor_username')
        mentor_password = request.form.get('mentor_password')
        
        # Check if mentor exists in the database with the provided credentials
        mentor = Mentor.query.filter_by(username=mentor_username, password=mentor_password).first()
        
        if mentor:
            # Get the mentee and mentor usernames and update the assigned_mentees table
            mentor_username = mentor.username

            try:# Update the assigned_mentees table
                assignment = Assigned_Mentee(mentee=mentee_username, mentor=mentor_username)
                db.session.add(assignment)
                db.session.commit()
                return redirect(url_for('view_profile', username=mentee_username))
            except Exception as e:
                flash("Error: Mentor already assigned to mentee")
        else:
            flash("Error: Invalid mentor credentials.")
    
    return render_template('mentor_credentials_prompt.html')


@app.route("/academicChanges", methods=["POST"])
def academicChanges():
    if session.get("user_type") == "mentee":
        username = session.get('username')
        
        # Retrieve the total number of rows from the form
        total_rows = int(request.form.get('row-count'))
        all_rows_filled = True
        user_data_list = []

        try:
            # Iterate through the rows and retrieve data
            for i in range(total_rows):
                # Do not assign a value to 'id', it's an auto-incremented primary key
                sem = request.form.get('sem')
                subject = request.form.get(f'subject_{i}')
                marks_ia = request.form.get(f'marks_ia_{i}')
                marks_sem = request.form.get(f'marks_sem_{i}')
                attempt2 = request.form.get(f'attempt2_{i}')
                attempt3 = request.form.get(f'attempt3_{i}')
                attempt4 = request.form.get(f'attempt4_{i}')
                
                # Check if any of the fields in the row are empty
                if not subject or not marks_ia or not marks_sem:
                    all_rows_filled = False
                    flash("Error: Please fill in all fields for each row.")
                    break  # Exit the loop if any row is incomplete

                # Create a new Mentee_Grades instance
                user_data1 = Mentee_Grades(
                    username=username,
                    sem=sem,
                    subject=subject,
                    marks_ia=marks_ia,
                    marks_sem=marks_sem,
                    attempt2=attempt2,
                    attempt3=attempt3,
                    attempt4=attempt4)
                user_data_list.append(user_data1)
            # Check if all rows are filled before committing
            if all_rows_filled:
               for user_data1 in user_data_list:
                  db.session.add(user_data1)
               db.session.commit()
               flash("Grades have been added!")
        except Exception as e:
            flash("Error: An error occurred while saving data: " + str(e))
            db.session.rollback()
    else:
        flash("Error: User is not a mentee")

    return redirect(url_for('editProfile'))


@app.route('/mentee', methods=['GET'])
def mentee():
    mentor_username = session.get('username')  # Get the mentor's username from the session

    # Fetch the usernames of mentees assigned to the mentor
    mentee_usernames = [record.mentee for record in Assigned_Mentee.query.with_entities(Assigned_Mentee.mentee)]
    
    # Fetch all records from the assigned_mentees table for the specific mentor
    assigned_mentees = Assigned_Mentee.query.filter_by(mentor=mentor_username).all()
    
    mentee_names = [mentee.mentee for mentee in assigned_mentees]
    
    academic_details = Mentee_Grades.query.filter(Mentee_Grades.username.in_(mentee_usernames)).all()
    # Fetch resources corresponding to the mentees in the mentee_usernames list
    resources_data = Resource.query.filter(Resource.username.in_(mentee_usernames)).all()

    return render_template('mentee.html', mentees=mentee_names, resources_data=resources_data, academic_details=academic_details)

@app.route("/addResource", methods=["POST"])
def addResource():
    username = session.get('username')
    title = request.form.get("resource_title")
    description = request.form.get("resource_description")
    file = request.files['file']  # this gets the file
    date_uploaded = datetime.utcnow()  # Get the current date and time

    # Define the target directory for saving files
    target_dir = os.path.join(app.root_path, 'static', 'resources')

    # Ensure the target directory exists, and create it if it doesn't
    os.makedirs(target_dir, exist_ok=True)

    # Check if a file was selected
    if not file.filename == '':
        filename = secure_filename(file.filename)
        resource_path = os.path.join(target_dir, filename)
        file.save(resource_path)
    else:
        # If they haven't added a resource, flash them a message
        flash("Please select a file to add as a resource")
        return redirect(url_for('resources'))

    NUMBER_OF_RESOURCES = len(Resource.query.filter_by().all())
    new_resource = Resource(id=NUMBER_OF_RESOURCES + 1, username=username, title=title, description=description, file=filename, date_uploaded=date_uploaded)
    db.session.add(new_resource)
    db.session.commit()
    flash("Resource has been added!")
    return redirect(url_for('resources'))


if __name__ == "__main__":
    app.run(debug=True)
