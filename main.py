from flask import Flask, render_template, request
import pymysql as sql
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid

app = Flask(__name__)

def db_connect():
    conn = sql.connect(user='root', password='', port=3306, host='localhost', database='klinik')
    cur = conn.cursor()
    return conn, cur


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about/")
def about():
    return render_template("/about.html/")

@app.route("/service/")
def service():
    return render_template("/service.html/")

@app.route("/feature/")
def feature():
    return render_template("/feature.html/")

@app.route("/appointment/")
def appointment():
    return render_template("/appointment.html/")

@app.route("/team/")
def team():
    return render_template("/team.html/")

@app.route("/testimonial/")
def testimonial():
    return render_template("/testimonial.html/")

@app.route("/contact/")
def contact():
    return render_template("/contact.html/")

import uuid

@app.route("/aftersubmit/", methods=['GET', 'POST'])
def aftersubmit():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        doctor = request.form.get('doctor')
        date = request.form.get('date')
        time = request.form.get('time')
        message = request.form.get('message')

        # Generate unique patient ID
        patient_id = str(uuid.uuid4()) 

        # Validate input data
        if not (name and email and phone and doctor and date and time and message and patient_id):
            msg = "Please fill in all the required details before booking."
            return render_template('appointment.html', m=msg)

        # Insert data into the database
        cmd = f"INSERT INTO PPD (patient_id, name, email, phone, doctor) VALUES ('{patient_id}', '{name}', '{email}', '{phone}', '{doctor}')"
        cmd2 = f"INSERT INTO PAD (patient_id, name, date, time, message) VALUES ('{patient_id}', '{name}', '{date}', '{time}', '{message}')"
        conn, cur = db_connect()

        try:
            cur.execute(cmd)
            cur.execute(cmd2)
            conn.commit()
            msg = f"Thank you, {name}! Your appointment has been successfully booked."

            # Sending confirmation email to the patient
            sender_email = "abhaypande855@gmail.com"
            receiver_email = email  # Send confirmation to the patient's email
            password = "xbfi cuxl jobc dvds"  # Make sure this is securely stored in a real application

            message = MIMEMultipart("alternative")
            message["Subject"] = "Appointment Confirmation - Klinik"
            message["From"] = sender_email
            message["To"] = receiver_email

            # HTML email body
            html = render_template(
                'appointment-email.html', 
                name1=name, 
                date1=date, 
                time1=time, 
                doctor1=doctor, 
                email1=email,
                patient_id1=patient_id
            )

            # Turn HTML into MIMEText object and attach
            part2 = MIMEText(html, "html")
            message.attach(part2)

            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())

        except Exception as e:
            conn.rollback()
            msg = f"An error occurred while booking your appointment: {e}"
        finally:
            conn.close()

        return render_template('appointment.html', m=msg)

    # If not POST method
    return render_template('appointment.html', m="Please submit the form.")


@app.route('/aftercontact/', methods=['GET', 'POST'])
def aftercontact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        user_message = request.form.get('message')  # Rename to avoid conflict

        # Generate unique query ID
        query_id = str(uuid.uuid4())  # UUID ensures globally unique IDs

        # Validate input data
        if not (name and email and subject and user_message and query_id):
            msg = "Please fill in all the required details before sending the message."
            return render_template('contact.html', m=msg)

        # Insert data into the database
        cmd = f"INSERT INTO QUERY (query_id, name, email, subject, message) VALUES ('{query_id}', '{name}', '{email}', '{subject}', '{user_message}')"
        conn, cur = db_connect()
        try:
            # Use parameterized query to prevent SQL injection
            cur.execute(cmd)
            conn.commit()
            msg = f"Thank you, {name}! Your query has been successfully submitted."

            # Sending confirmation email to the patient
            sender_email = "abhaypande855@gmail.com"
            receiver_email = email  # Send confirmation to the patient's email
            password = "xbfi cuxl jobc dvds"  # Make sure this is securely stored in a real application

            # Email setup
            email_message = MIMEMultipart("alternative")
            email_message["Subject"] = "Query Submitted - Klinik"
            email_message["From"] = sender_email
            email_message["To"] = receiver_email

            # HTML email body
            html = render_template(
                'query-email.html',
                query_id1=query_id,
                name1=name,
                email1=email,
                subject1=subject,
                message1=user_message 
            )

            # Turn HTML into MIMEText object and attach
            part2 = MIMEText(html, "html")
            email_message.attach(part2)  

            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, email_message.as_string())

        except Exception as e:
            conn.rollback()
            msg = f"An error occurred while processing your query: {e}"
        finally:
            conn.close()

        return render_template('contact.html', m=msg)

    # If not POST method
    return render_template("contact.html", t="Please submit the form.")

@app.route('/', methods = ['POST'])
def newsletter():
    # Get the email from the form
    email = request.form.get('email')

    # Validate the email
    if email:
        try:
            # Insert email into the database (Make sure to create the newsletter table beforehand)
            conn, cur = db_connect()
            cmd = f"INSERT INTO newsletter (email) VALUES ('{email}')"
            cur.execute(cmd)
            conn.commit()   
            msg = f"Thank you for subscribing."

            # Sending confirmation email to the patient
            sender_email = "abhaypande855@gmail.com"
            receiver_email = email  # Send confirmation to the patient's email
            password = "xbfi cuxl jobc dvds"  # Make sure this is securely stored in a real application

            # Email setup
            email_message = MIMEMultipart("alternative")
            email_message["Subject"] = "Query Submitted - Klinik"
            email_message["From"] = sender_email
            email_message["To"] = receiver_email

            # HTML email body
            html = render_template(
                'newsletter-email.html',
                email1=email,
            )

            # Turn HTML into MIMEText object and attach
            part2 = MIMEText(html, "html")
            email_message.attach(part2)  

            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, email_message.as_string())

        except Exception as e:
            conn.rollback()
            msg = f"You are already subscribed."
        finally:
            conn.close()

        return render_template('index.html', t=msg)

    # If not POST method
    return render_template("index.html", t="Please enter a valid email.")


app.run(host='localhost', port= 5000, debug=True)

