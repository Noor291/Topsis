from flask import Flask,render_template,request
# from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import csv
import pandas as pd
from Topsis import topsis
from email.message import EmailMessage
# from werkzeug import security
import ssl
import smtplib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/files'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def hello_world():
    data = request.form
    w = request.form['weights']
    i = request.form['impacts']
    m = request.form['mail']
    f = request.files['filename']
    f.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

    file = "static/files/"+f.filename
    weight=w.split(',')
    im=i.split(',')

    try:
        ans=topsis(file,weight,im)
    except:
        return render_template('error.html')

    result=ans.to_csv("static/files/result.csv",index=False)

    email_sender = 'noordeepk2002@gmail.com'
    email_password = 'yhofghzgsaktuuqg'

    em = EmailMessage()
    em['From'] = email_sender
    em['Subject'] = 'Your Output is here!'
    em['Body'] = 'Output.csv file for your provided input is attached.'
    with open("static/files/result.csv","rb") as fp:
        file_data=fp.read()
    em.add_attachment(file_data,maintype='text',subtype='csv',filename='output.csv')

    context = ssl.create_default_context()

    email_receiver = m
    em['To'] = email_receiver
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

    return render_template('success.html')
    

if __name__ == '__main__':
    app.run(debug=True,port=8000)