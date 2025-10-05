from datetime import datetime, timedelta

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

#####################################################################
app = Flask(__name__)
app.secret_key = "Galaxy123"  # Needed for session management
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
app.app_context().push()
#####################################################################


#####################################################################
# Global Variables
#####################################################################
class t_user(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    user_type = db.Column(db.Integer, nullable=False)
    # 1 - Admin
    # 2 - Doctor
    # 3 - Patient

    def __init__(self, username, password, user_type):
        self.username = username
        self.password = password
        self.user_type = user_type

    # def __repr__(self):
    #     return f"<User {self.username}>"


class t_doctor(db.Model):
    doctor_id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __init__(
        self, doctor_id, name, designation, department, qualification, contact, email
    ):
        self.doctor_id = doctor_id
        self.name = name
        self.designation = designation
        self.department = department
        self.qualification = qualification
        self.contact = contact
        self.email = email


class t_patient(db.Model):
    patient_id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

    def __init__(self, patient_id, name, dob, gender, address, contact, email):
        self.patient_id = patient_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.contact = contact
        self.email = email


class t_department(db.Model):
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    contact = db.Column(db.String(80), nullable=False)

    def __init__(self, name, description, contact):
        self.name = name
        self.description = description
        self.contact = contact


class t_appointment(db.Model):
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    doctor_id = db.Column(db.String(80), nullable=False)
    appointment_date = db.Column(db.String(80), nullable=False)
    appointment_time = db.Column(db.String(80), nullable=False)
    appointment_status = db.Column(db.String(80), nullable=False)
    patient_id = db.Column(db.String(80), nullable=True)
    diagnosis = db.Column(db.String(80), nullable=True)
    prescription = db.Column(db.String(80), nullable=True)
    notes = db.Column(db.String(80), nullable=True)

    def __init__(
        self,
        # appointment_id,
        doctor_id,
        appointment_date,
        appointment_time,
        appointment_status,  # Available, Booked, Cancelled, Completed
        patient_id,
        diagnosis,
        prescription,
        notes,
    ):
        # self.appointment_id = appointment_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.appointment_status = appointment_status
        self.patient_id = patient_id
        self.diagnosis = diagnosis
        self.prescription = prescription
        self.notes = notes


#####################################################################
# Home
#####################################################################
@app.route("/")
def home():
    with app.app_context():
        db.create_all()
        # ------------------------------------------------------------
        found_user = t_user.query.filter_by(username="admin").first()
        if not found_user:
            flash("User created successfully!!")
            # ------------------------------------------------------------
            table_user = t_user("admin", "admin312!", "1")
            db.session.add(table_user)
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
    return render_template("home.html")
    # return jsonify(message="Hello, World!!")
    # return "Hello, World!! <h1> This is a heading... </h1>"
    # return render_template("home.html", content=["Flask", "Django", "FastAPI"])
    # return render_template("index.html", content="Flask")


#####################################################################
# Doctor - Root
#####################################################################
@app.route("/doctor", methods=["GET", "POST"])
def doctor_root():
    if request.method == "POST":
        button_name = request.form.get("action")
        if button_name == "home":  # if Logout button is clicked
            flash("You have been logged out!", "info")
            return render_template("home.html")
        elif button_name == "manageDoctor":  # Login button is clicked
            # return render_template("patient_manage.html")
            return redirect(url_for("doctor_manage"))
            # return render_template("patient_manage.html")
        elif button_name == "bookAppointment":  # Login button is clicked
            return render_template("view.html")
        elif button_name == "cancelAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            flash("Doctor selected!", "info")
            return render_template(
                "doctor_appointment_cancel.html",
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter(
                        t_appointment.doctor_id == session["username"],
                        t_appointment.appointment_status.in_(["Booked", "Available"]),
                    )
                ],
            )
        elif button_name == "completeAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            flash("Doctor selected!", "info")
            return render_template(
                "doctor_appointment_complete.html",
                appointmentHidden=False,
                notesHidden=True,
                values=None,
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter(
                        t_appointment.doctor_id == session["username"],
                        t_appointment.appointment_status.in_(["Booked"]),
                    )
                ],
            )
    else:  # if Login page is accessed using GET method, i.e., clicking on Login link
        flash("Choose options to proceed!", "info")
        return render_template("doctor_root.html")


#####################################################################
# Doctor - Manage
#####################################################################
@app.route("/doctor_manage", methods=["GET", "POST"])
def doctor_manage():
    if request.method == "POST":
        # ------------------------------------------------------------
        button_name = request.form.get("action")
        if button_name == "select":  # if Logout button is clicked
            flash("Getting data from DB!", "info")
            found_user = t_doctor.query.filter_by(
                doctor_id=request.form.get("select")
            ).first()
            if found_user:
                flash("User data retrieved from DB")
                return render_template(
                    "doctor_update.html",
                    values=found_user,
                    dataDepartment=t_department.query.all(),
                )
        # ------------------------------------------------------------
        elif button_name == "save":  # if Logout button is clicked
            found_user = t_doctor.query.filter_by(
                doctor_id=request.form.get("doctor_id")
            ).first()
            if found_user:
                # ------------------------------------------------------------
                found_user.name = request.form.get("name")
                found_user.designation = request.form.get("designation")
                found_user.department = request.form.get("department")
                found_user.qualification = request.form.get("qualification")
                found_user.contact = request.form.get("contact")
                found_user.email = request.form.get("email")
                # ------------------------------------------------------------
                db.session.commit()
                flash("User data saved successfully!!")
                return render_template(
                    "doctor_update.html",
                    values=found_user,
                    dataDepartment=t_department.query.all(),
                )
            else:  # Not logged in
                flash("Data NOT Found in DB! Contact Admin!", "info")
                return render_template("doctor_update.html")
    else:  # if Patient Manage Login page is accessed using GET method, i.e., clicking on Manage Patient link
        found_user = t_doctor.query.filter_by(doctor_id=session["username"]).first()
        if found_user:
            flash("User data retrieved from DB")
            return render_template(
                "doctor_update.html",
                values=found_user,
                dataDepartment=t_department.query.all(),
            )
        else:  # Not logged in
            flash("Data NOT Found in DB! Contact Admin!", "info")
            return render_template("doctor_update.html")


#####################################################################
# Doctor - Book Appointment
#####################################################################
@app.route("/doctor_appointment", methods=["GET", "POST"])
def doctor_appointment():
    if request.method == "POST":
        # ------------------------------------------------------------
        button_name = request.form.get("action")
        if button_name == "selectAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("selectAppointment")
            ).first()
            # ------------------------------------------------------------
            # ------------------------------------------------------------
            flash("Appointment retrieved!", "info")
            return render_template(
                "doctor_appointment_complete.html",
                appointmentHidden=True,
                notesHidden=False,
                values=found_user,
            )
        if button_name == "completeAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("appointment_id")
            ).first()
            # ------------------------------------------------------------
            found_user.diagnosis = request.form.get("diagnosis")
            found_user.prescription = request.form.get("prescription")
            found_user.notes = request.form.get("notes")
            found_user.appointment_status = "Completed"
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment completed!", "info")
            return render_template(
                "doctor_appointment_complete.html",
                appointmentHidden=True,
                notesHidden=False,
                values=found_user,
            )
            # ------------------------------------------------------------
        elif button_name == "cancelAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("selectAppointment")
            ).first()
            # ------------------------------------------------------------
            found_user.appointment_status = "Cancelled"
            # found_user.patient_id = None
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment booked!", "info")
            return render_template(
                "patient_appointment_cancel.html",
                appointmentHidden=True,
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter_by(
                        appointment_id=request.form.get("selectAppointment"),
                    )
                ],
            )
            # ------------------------------------------------------------
        elif button_name == "reset":  # Login button is clicked
            # ------------------------------------------------------------
            flash("Appointment datetime selected!", "info")
            flash("Booking an appointment!", "info")
            return render_template(
                "patient_appointment_book.html",
                selectedDepartment=None,
                selectedDoctor=None,
                departmentHidden=False,
                doctorHidden=True,
                appointmentHidden=True,
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
    else:  # if Patient Manage Login page is accessed using GET method, i.e., clicking on Manage Patient link
        found_user = t_patient.query.filter_by(patient_id=session["username"]).first()
        if found_user:
            flash("User data retrieved from DB")
            return render_template("patient_update.html", values=found_user)
        else:  # Not logged in
            flash("Data NOT Found in DB! Contact Admin!", "info")
            return render_template("patient_update.html")


#####################################################################
# Patient - Root
#####################################################################
@app.route("/patient", methods=["GET", "POST"])
def patient_root():
    if request.method == "POST":
        button_name = request.form.get("action")
        if button_name == "home":  # if Logout button is clicked
            flash("You have been logged out!", "info")
            return render_template("home.html")
        elif button_name == "managePatient":  # Login button is clicked
            # return render_template("patient_manage.html")
            return redirect(url_for("patient_manage"))
            # return render_template("patient_manage.html")
        elif button_name == "bookAppointment":  # Login button is clicked
            flash("Booking an appointment!", "info")
            return render_template(
                "patient_appointment_book.html",
                selectedDepartment=None,
                selectedDoctor=None,
                departmentHidden=False,
                doctorHidden=True,
                appointmentHidden=True,
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        elif button_name == "cancelAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            flash("Doctor selected!", "info")
            return render_template(
                "patient_appointment_cancel.html",
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter_by(
                        patient_id=session["username"],
                        appointment_status="Booked",
                    )
                ],
            )
    else:  # if Login page is accessed using GET method, i.e., clicking on Login link
        flash("Choose options to proceed!", "info")
        return render_template("patient_root.html")


#####################################################################
# Patient - Manage
#####################################################################
@app.route("/patient_manage", methods=["GET", "POST"])
def patient_manage():
    if request.method == "POST":
        # ------------------------------------------------------------
        button_name = request.form.get("action")
        if button_name == "select":  # if Logout button is clicked
            flash("Getting data from DB!", "info")
            found_user = t_patient.query.filter_by(
                patient_id=request.form.get("select")
            ).first()
            if found_user:
                flash("User data retrieved from DB")
                return render_template("patient_update.html", values=found_user)
        # ------------------------------------------------------------
        elif button_name == "save":  # if Logout button is clicked
            found_user = t_patient.query.filter_by(
                patient_id=request.form.get("patient_id")
            ).first()
            if found_user:
                # ------------------------------------------------------------
                found_user.name = request.form.get("name")
                found_user.dob = request.form.get("dob")
                found_user.gender = request.form.get("gender")
                found_user.address = request.form.get("address")
                found_user.contact = request.form.get("contact")
                found_user.email = request.form.get("email")
                # ------------------------------------------------------------
                db.session.commit()
                flash("User data saved successfully!!")
                return render_template("patient_update.html", values=found_user)
            else:  # Not logged in
                flash("Data NOT Found in DB! Contact Admin!", "info")
                return render_template("patient_update.html")
    else:  # if Patient Manage Login page is accessed using GET method, i.e., clicking on Manage Patient link
        found_user = t_patient.query.filter_by(patient_id=session["username"]).first()
        if found_user:
            flash("User data retrieved from DB")
            return render_template("patient_update.html", values=found_user)
        else:  # Not logged in
            flash("Data NOT Found in DB! Contact Admin!", "info")
            return render_template("patient_update.html")


#####################################################################
# Patient - Book Appointment
#####################################################################
@app.route("/patient_appointment", methods=["GET", "POST"])
def patient_appointment():
    if request.method == "POST":
        # ------------------------------------------------------------
        button_name = request.form.get("action")
        if button_name == "selectDepartment":  # if Logout button is clicked
            # ------------------------------------------------------------
            flash("Department selected!", "info")
            return render_template(
                "patient_appointment_book.html",
                selectedDepartment=request.form.get("selectDepartment"),
                selectedDoctor=None,
                departmentHidden=True,
                doctorHidden=False,
                appointmentHidden=True,
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.filter_by(
                        department=request.form.get("selectDepartment")
                    ).all()
                ],
            )
        elif button_name == "selectDoctor":  # if Logout button is clicked
            # ------------------------------------------------------------
            flash("Doctor selected!", "info")
            return render_template(
                "patient_appointment_book.html",
                selectedDepartment=request.form.get("selectDepartment"),
                selectedDoctor=request.form.get("selectDoctor"),
                departmentHidden=True,
                doctorHidden=True,
                appointmentHidden=False,
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.filter_by(
                        department=request.form.get("selectDepartment")
                    ).all()
                ],
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    # for obj in t_appointment.query.all()
                    for obj in t_appointment.query.filter_by(
                        doctor_id=request.form.get("selectDoctor"),
                        appointment_status="Available",
                    )
                    # .query.filter_by(doctor_id=request.form.get("select"))
                    # .first()
                ],
            )
        elif button_name == "selectAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("selectAppointment")
            ).first()
            # ------------------------------------------------------------
            found_user.appointment_status = "Booked"
            found_user.patient_id = session["username"]
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment booked!", "info")
            return render_template(
                "patient_appointment_book.html",
                departmentHidden=True,
                doctorHidden=True,
                appointmentHidden=True,
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    # for obj in t_appointment.query.all()
                    for obj in t_appointment.query.filter_by(
                        appointment_id=request.form.get("selectAppointment")
                    )
                ],
            )
            # ------------------------------------------------------------
        elif button_name == "cancelAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("selectAppointment")
            ).first()
            # ------------------------------------------------------------
            found_user.appointment_status = "Available"
            found_user.patient_id = None
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment booked!", "info")
            return render_template(
                "patient_appointment_cancel.html",
                appointmentHidden=True,
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter_by(
                        patient_id=session["username"],
                    )
                ],
            )
            # ------------------------------------------------------------
        elif button_name == "reset":  # Login button is clicked
            # ------------------------------------------------------------
            flash("Appointment datetime selected!", "info")
            flash("Booking an appointment!", "info")
            return render_template(
                "patient_appointment_book.html",
                selectedDepartment=None,
                selectedDoctor=None,
                departmentHidden=False,
                doctorHidden=True,
                appointmentHidden=True,
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
    else:  # if Patient Manage Login page is accessed using GET method, i.e., clicking on Manage Patient link
        found_user = t_patient.query.filter_by(patient_id=session["username"]).first()
        if found_user:
            flash("User data retrieved from DB")
            return render_template("patient_update.html", values=found_user)
        else:  # Not logged in
            flash("Data NOT Found in DB! Contact Admin!", "info")
            return render_template("patient_update.html")


#####################################################################
# Admin - Appointment
#####################################################################
@app.route("/admin_appointment_manage", methods=["GET", "POST"])
def admin_appointment_manage():
    if request.method == "POST":
        # ------------------------------------------------------------
        button_name = request.form.get("action")
        if button_name == "create":  # if Logout button is clicked
            # ------------------------------------------------------------
            doctor = request.form.get("select")
            appDate = datetime.strptime(
                request.form.get("appDate"), "%Y-%m-%dT%H:%M"
            ).date()
            appTime = datetime.strptime(request.form.get("appDate"), "%Y-%m-%dT%H:%M")
            # ------------------------------------------------------------
            for i in range(int(request.form.get("appNum"))):
                table_appointment = t_appointment(
                    doctor_id=doctor,
                    appointment_date=appDate,  # start_dt.strftime("%Y-%m-%d"),
                    appointment_time=appTime,  # start_dt.strftime("%H:%M"),
                    appointment_status="Available",
                    patient_id=None,
                    diagnosis=None,
                    prescription=None,
                    notes=None,
                )
                db.session.add(table_appointment)
                db.session.commit()
                appTime = appTime + timedelta(minutes=int(request.form.get("appDur")))
            # ------------------------------------------------------------
            flash("Getting data from DB!", "info")
            return render_template(
                "appointment_create.html",
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date/Time",
                    "Appointment Status",
                    "Patient ID",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                    ]
                    for obj in t_appointment.query.filter_by(
                        doctor_id=request.form.get("select"), appointment_date=appDate
                    )
                    # .query.filter_by(doctor_id=request.form.get("select"))
                    # .first()
                ],
            )
            # return render_template("appointment_create.html", values=found_user)
        # ------------------------------------------------------------
        elif button_name == "save":  # if Logout button is clicked
            found_user = t_doctor.query.filter_by(
                doctor_id=request.form.get("doctor_id")
            ).first()
            if found_user:
                # ------------------------------------------------------------
                found_user.name = request.form.get("name")
                found_user.designation = request.form.get("designation")
                found_user.department = request.form.get("department")
                found_user.qualification = request.form.get("qualification")
                found_user.contact = request.form.get("contact")
                found_user.email = request.form.get("email")
                # ------------------------------------------------------------
                db.session.commit()
                flash("User data saved successfully!!")
                return render_template("doctor_update.html", values=found_user)
            else:  # Not logged in
                flash("Data NOT Found in DB! Contact Admin!", "info")
                return render_template("doctor_update.html")
        # ------------------------------------------------------------
        if button_name == "selectDepartment":  # if Logout button is clicked
            # ------------------------------------------------------------
            flash("Department selected!", "info")
            return render_template(
                "admin_appointment_manage.html",
                selectedDepartment=request.form.get("selectDepartment"),
                selectedDoctor=None,
                departmentHidden=True,
                doctorHidden=False,
                appointmentHidden=True,
                patientHidden=True,
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.filter_by(
                        department=request.form.get("selectDepartment")
                    ).all()
                ],
            )
        elif button_name == "selectDoctor":  # if Logout button is clicked
            # ------------------------------------------------------------
            flash("Doctor selected!", "info")
            return render_template(
                "admin_appointment_manage.html",
                selectedDepartment=request.form.get("selectDepartment"),
                selectedDoctor=request.form.get("selectDoctor"),
                departmentHidden=True,
                doctorHidden=True,
                appointmentHidden=False,
                patientHidden=True,
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.filter_by(
                        department=request.form.get("selectDepartment")
                    ).all()
                ],
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    # for obj in t_appointment.query.all()
                    for obj in t_appointment.query.filter(
                        t_appointment.doctor_id == request.form.get("selectDoctor"),
                        t_appointment.appointment_status.in_(["Booked", "Available"]),
                    )
                    # .query.filter_by(doctor_id=request.form.get("select"))
                    # .first()
                    #                     for obj in t_appointment.query.filter(
                    #     t_appointment.doctor_id == session["username"],
                    #     t_appointment.appointment_status.in_(["Booked", "Available"]),
                    # )
                ],
            )
        elif button_name == "selectAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            # found_user = t_appointment.query.filter_by(
            #     appointment_id=request.form.get("selectAppointment")
            # ).first()
            # ------------------------------------------------------------
            # found_user.appointment_status = "Booked"
            # found_user.patient_id = session["username"]
            # ------------------------------------------------------------
            # db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment booked!", "info")
            return render_template(
                "admin_appointment_manage.html",
                departmentHidden=True,
                doctorHidden=True,
                appointmentHidden=True,
                patientHidden=False,
                appointment_id=request.form.get("selectAppointment"),
                # heading=(
                #     "Appointment ID",
                #     "Doctor ID",
                #     "Appointment Date",
                #     "Appointment Time",
                #     "Appointment Status",
                #     "Patient ID",
                #     "Diagnosis",
                #     "Prescription",
                #     "Notes",
                # ),
                # dataAppointment=[
                #     [
                #         obj.appointment_id,
                #         obj.doctor_id,
                #         obj.appointment_date,
                #         obj.appointment_time,
                #         obj.appointment_status,
                #         obj.patient_id,
                #         obj.diagnosis,
                #         obj.prescription,
                #         obj.notes,
                #     ]
                #     # for obj in t_appointment.query.all()
                #     for obj in t_appointment.query.filter_by(
                #         appointment_id=request.form.get("selectAppointment")
                #     )
                # ],
                dataPatient=[
                    [
                        obj.patient_id,
                        obj.name,
                        obj.dob,
                        obj.gender,
                        obj.address,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_patient.query.all()
                ],
            )
            # ------------------------------------------------------------
        elif button_name == "removeAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("selectAppointment")
            ).first()
            # ------------------------------------------------------------
            found_user.appointment_status = "Available"
            found_user.patient_id = None
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment booked!", "info")
            return render_template(
                "admin_appointment_manage.html",
                departmentHidden=True,
                doctorHidden=True,
                appointmentHidden=True,
                patientHidden=True,
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter_by(
                        appointment_id=request.form.get("selectAppointment"),
                    )
                ],
            )
            # ------------------------------------------------------------
        elif button_name == "cancelAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("selectAppointment")
            ).first()
            # ------------------------------------------------------------
            found_user.appointment_status = "Cancelled"
            found_user.patient_id = None
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment booked!", "info")
            return render_template(
                "admin_appointment_manage.html",
                departmentHidden=True,
                doctorHidden=True,
                appointmentHidden=True,
                patientHidden=True,
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter_by(
                        appointment_id=request.form.get("selectAppointment"),
                    )
                ],
            )
            # ------------------------------------------------------------
        elif button_name == "bookAppointment":  # if Logout button is clicked
            # ------------------------------------------------------------
            found_user = t_appointment.query.filter_by(
                appointment_id=request.form.get("appointment_id")
            ).first()
            # ------------------------------------------------------------
            found_user.appointment_status = "Booked"
            found_user.patient_id = request.form.get("selectPatient")
            # ------------------------------------------------------------
            db.session.commit()
            # ------------------------------------------------------------
            flash("Appointment booked!", "info")
            return render_template(
                "admin_appointment_manage.html",
                departmentHidden=True,
                doctorHidden=True,
                appointmentHidden=True,
                patientHidden=True,
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataAppointment=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter_by(
                        appointment_id=request.form.get("appointment_id"),
                    )
                ],
            )
            # ------------------------------------------------------------
        elif button_name == "reset":  # Login button is clicked
            # ------------------------------------------------------------
            flash("Appointment datetime selected!", "info")
            flash("Booking an appointment!", "info")
            return render_template(
                "admin_appointment_manage.html",
                selectedDepartment=None,
                selectedDoctor=None,
                departmentHidden=False,
                doctorHidden=True,
                appointmentHidden=True,
                patientHidden=True,
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        # ------------------------------------------------------------
    else:  # if Patient Manage Login page is accessed using GET method, i.e., clicking on Manage Patient link
        found_user = t_doctor.query.filter_by(doctor_id=session["username"]).first()
        if found_user:
            flash("User data retrieved from DB")
            return render_template("doctor_update.html", values=found_user)
        else:  # Not logged in
            flash("Data NOT Found in DB! Contact Admin!", "info")
            return render_template("doctor_update.html")


#####################################################################
# Login
#####################################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        button_name = request.form.get("action")
        if button_name == "login":  # Login button is clicked
            # ------------------------------------------------------------
            if not request.form.get("username") or not request.form.get("password"):
                flash("Please enter both username and password!")
                return render_template("login.html")
            # ------------------------------------------------------------
            found_user = t_user.query.filter_by(
                username=request.form.get("username")
            ).first()
            if found_user:
                # ------------------------------------------------------------
                if found_user.password == request.form.get("password"):
                    # ------------------------------------------------------------
                    session["username"] = request.form.get("username")
                    # session["password"] = request.form.get("password")
                    session["user_type"] = request.form.get("user_type")
                    # ------------------------------------------------------------
                    flash("Successfully Logged in!!")
                    return render_template(
                        "login.html",
                        username=session["username"],
                    )
                else:
                    flash("Password did not match!!")
                    return render_template("login.html")
                # ------------------------------------------------------------
            else:
                flash("User not found!!")
                return render_template("login.html")
                # ------------------------------------------------------------
        elif button_name == "logout":  # if Logout button is clicked
            session.pop("username", None)
            # session.pop("password", None)
            session.pop("user_type", None)
            flash("You have been logged out!", "info")
            return render_template("login.html")
        elif button_name == "go_register":  # register button is clicked
            flash("Register for new user!", "info")
            return render_template(
                "register.html", user_type=3, user_desc="Patient"
            )  # Patient
            # return redirect(url_for("/register"))
            # ------------------------------------------------------------
        elif button_name == "register":  # register button is clicked
            # ------------------------------------------------------------
            if "username" not in session:
                user_type = 3
                user_desc = "Patient"
            elif session["username"] == "admin":
                user_type = 2
                user_desc = "Doctor"
            else:
                flash("You are already logged in!", "info")
                return render_template(
                    "login.html",
                    username=session["username"],
                )
            # ------------------------------------------------------------
            if (
                not request.form.get("username")
                or not request.form.get("password")
                or not request.form.get("password2")
            ):
                flash("Please enter both username and password!")
                return render_template("register.html")
            # ------------------------------------------------------------
            found_user = t_user.query.filter_by(
                username=request.form.get("username")
            ).first()
            # ------------------------------------------------------------
            if found_user:
                flash(
                    'User "'
                    + request.form.get("username")
                    + '" already exists! Try another username.'
                )
                return render_template(
                    "register.html", user_type=user_type, user_desc=user_desc
                )
            else:
                # ------------------------------------------------------------
                # if session["username"] == "admin":
                #     flash(
                #         "User "
                #         + request.form.get("username")
                #         + " registered successfully!",
                #         "info",
                #     )
                #     return render_template(
                #         "register.html", user_type=user_type, user_desc=user_desc
                #     )  # Doctor
                # ------------------------------------------------------------
                if request.form.get("password") != request.form.get("password2"):
                    flash("Password not matching with validation!")
                    return render_template(
                        "register.html", user_type=user_type, user_desc=user_desc
                    )
                # ------------------------------------------------------------
                if "username" not in session:
                    session["username"] = request.form.get("username")
                    session["user_type"] = request.form.get("password")
                # ------------------------------------------------------------
                table_user = t_user(
                    request.form.get("username"),
                    request.form.get("username"),
                    request.form.get("user_type"),
                )
                db.session.add(table_user)
                # ------------------------------------------------------------
                if request.form.get("user_type") == "2":  # 3 - Doctor
                    table_patient = t_doctor(
                        request.form.get("username"),
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                    )
                    db.session.add(table_patient)
                elif request.form.get("user_type") == "3":  # 3 - Patient
                    table_patient = t_patient(
                        request.form.get("username"),
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                        "To_Fill",
                    )
                    db.session.add(table_patient)
                # ------------------------------------------------------------
                db.session.commit()
                flash("User created successfully!!")
                # ------------------------------------------------------------
                if session["username"] == "admin":
                    flash(
                        "User "
                        + request.form.get("username")
                        + " registered successfully!",
                        "info",
                    )
                    return render_template(
                        "register.html",
                        user_type=user_type,
                        user_desc=user_desc,
                        username="",
                        password="",
                    )  # Doctor
                # ------------------------------------------------------------
            pass
            # ------------------------------------------------------------
            return render_template(
                "login.html",
                username=session["username"],
            )
            # ------------------------------------------------------------
    else:  # if Login page is accessed using GET method, i.e., clicking on Login link
        if "username" in session:  # If already logged in
            username = session["username"]
            # flash("Message 1!", "info")
            return render_template("login.html", username=username)
            pass
        else:  # Not logged in
            flash("Enter username & password!", "info")
            return render_template("login.html")


#####################################################################
# Admin
#####################################################################
@app.route("/admin", methods=["GET", "POST"])
def admin_root():
    if request.method == "POST":
        # ------------------------------------------------------------
        button_name = request.form.get("action")
        # ------------------------------------------------------------
        if button_name == "home":  # if Logout button is clicked
            flash("You have been logged out!", "info")
            return render_template("home.html")
        # ------------------------------------------------------------
        elif button_name == "manageDoctor":  # Login button is clicked
            return render_template(
                "doctor_select.html",
                heading=(
                    "Doctor ID",
                    "Name",
                    "Designation",
                    "Department",
                    "Qualification",
                    "Contact",
                    "EMail",
                ),
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "managePatient":  # Login button is clicked
            return render_template(
                "patient_select.html",
                heading=(
                    "Patient ID",
                    "Name",
                    "DOB",
                    "Gender",
                    "Address",
                    "Contact",
                    "EMail",
                ),
                dataPatient=[
                    [
                        obj.patient_id,
                        obj.name,
                        obj.dob,
                        obj.gender,
                        obj.address,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_patient.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "manageDepartment":  # Login button is clicked
            return render_template(
                "department_select.html",
                heading=(
                    "Department ID",
                    "Department Name",
                    "Description",
                    "Contact",
                ),
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
            )
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        elif button_name == "createAppointment":  # Login button is clicked
            flash("Create Appointment for Doctors!", "info")
            return render_template(
                "appointment_create.html",
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "manageAppointment":  # Login button is clicked
            flash("Booking an appointment!", "info")
            return render_template(
                "admin_appointment_manage.html",
                selectedDepartment=None,
                selectedDoctor=None,
                departmentHidden=False,
                doctorHidden=True,
                appointmentHidden=True,
                patientHidden=True,
                dataDepartment=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
                dataDoctor=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "registerDoc":  # Login button is clicked
            flash("Register for new user!", "info")
            return render_template(
                "register.html", user_type=2, user_desc="Doctor"
            )  # Doctor
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        elif button_name == "viewDoctor":  # Login button is clicked
            return render_template(
                "view.html",
                heading=(
                    "Doctor ID",
                    "Name",
                    "Designation",
                    "Department",
                    "qualification",
                    "Contact",
                    "EMail",
                ),
                dataView=[
                    [
                        obj.doctor_id,
                        obj.name,
                        obj.designation,
                        obj.department,
                        obj.qualification,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_doctor.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "viewPatient":  # Login button is clicked
            return render_template(
                "view.html",
                heading=(
                    "Patient ID",
                    "Name",
                    "DOB",
                    "Gender",
                    "Address",
                    "Contact",
                    "EMail",
                ),
                dataView=[
                    [
                        obj.patient_id,
                        obj.name,
                        obj.dob,
                        obj.gender,
                        obj.address,
                        obj.contact,
                        obj.email,
                    ]
                    for obj in t_patient.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "viewUser":  # Login button is clicked
            return render_template(
                "view.html",
                heading=(
                    "User Name",
                    "Password",
                    "User Type",
                ),
                dataView=[
                    [
                        obj.username,
                        obj.password,
                        obj.user_type,
                    ]
                    for obj in t_user.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "viewDepartment":  # Login button is clicked
            return render_template(
                "view.html",
                heading=(
                    "Department ID",
                    "Name",
                    "Description",
                    "Contact",
                ),
                dataView=[
                    [
                        obj.department_id,
                        obj.name,
                        obj.description,
                        obj.contact,
                    ]
                    for obj in t_department.query.all()
                ],
            )
        # ------------------------------------------------------------
        elif button_name == "viewAppointment":  # Login button is clicked
            return render_template(
                "view.html",
                heading=(
                    "Appointment ID",
                    "Doctor ID",
                    "Appointment Date",
                    "Appointment Time",
                    "Appointment Status",
                    "Patient ID",
                    "Diagnosis",
                    "Prescription",
                    "Notes",
                ),
                dataView=[
                    [
                        obj.appointment_id,
                        obj.doctor_id,
                        obj.appointment_date,
                        obj.appointment_time,
                        obj.appointment_status,
                        obj.patient_id,
                        obj.diagnosis,
                        obj.prescription,
                        obj.notes,
                    ]
                    for obj in t_appointment.query.filter_by(doctor_id="d1")
                    # for obj in t_appointment.query.all()
                ],
            )
        # ------------------------------------------------------------
    else:  # if Login page is accessed using GET method, i.e., clicking on Login link
        flash("Choose options to proceed!", "info")
        return render_template("admin_root.html")


#####################################################################
# Department
#####################################################################
@app.route("/department_manage", methods=["GET", "POST"])
def department_manage():
    if request.method == "POST":
        # ------------------------------------------------------------
        button_name = request.form.get("action")
        if button_name == "select":  # if Logout button is clicked
            flash("Getting data from DB!", "info")
            found_user = t_department.query.filter_by(
                department_id=request.form.get("select")
            ).first()
            if found_user:
                flash("User data retrieved from DB")
                return render_template("department_update.html", values=found_user)
        # ------------------------------------------------------------
        elif button_name == "new":  # New button is clicked
            # ------------------------------------------------------------
            flash("Create new Department!", "info")
            return render_template(
                "department_update.html",
                values={
                    "department_id": "BLANK",
                    "name": "To_Fill",
                    "description": "To_Fill",
                    "contact": "To_Fill",
                },
            )
        # ------------------------------------------------------------
        elif button_name == "save":  # if Logout button is clicked
            if request.form.get("department_id") == "BLANK":
                table_department = t_department(
                    # request.form.get("department_id"),
                    name=request.form.get("name"),
                    description=request.form.get("description"),
                    contact=request.form.get("contact"),
                )
                db.session.add(table_department)
                # ------------------------------------------------------------
                db.session.commit()
                flash("New Department created successfully!!")
                return render_template(
                    "department_update.html",
                    values={
                        "department_id": "BLANK",
                        "name": request.form.get("name"),
                        "description": request.form.get("description"),
                        "contact": request.form.get("contact"),
                    },
                )

            else:
                found_user = t_department.query.filter_by(
                    department_id=request.form.get("department_id")
                ).first()
                if found_user:
                    # ------------------------------------------------------------
                    found_user.name = request.form.get("name")
                    found_user.description = request.form.get("description")
                    found_user.contact = request.form.get("contact")
                    # ------------------------------------------------------------
                    db.session.commit()
                    flash("Data saved successfully!!")
                    return render_template("department_update.html", values=found_user)
    else:  # if Patient Manage Login page is accessed using GET method, i.e., clicking on Manage Patient link
        found_user = t_patient.query.filter_by(patient_id=session["username"]).first()


#####################################################################

#####################################################################
# @app.route("/logout")
# def logout():
#     session.pop("username", None)
#     session.pop("password", None)
#     return redirect(url_for("login"))
#####################################################################
# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"
#####################################################################
# @app.route("/admin")
# def admin():
#     return redirect(url_for("user", name="Admin"))
#####################################################################
# Bottom of the file
#####################################################################

if __name__ == "__main__":
    app.run(debug=True)

# import sys

# try:
#     app.run(debug=True)
# except SystemExit as e:
#     print(f"SystemExit with code: {e.code}")
#     app.run(debug=True)
#     # sys.exit(e.code)
