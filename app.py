from flask import Flask, render_template, request
import pandas as pd
from datetime import date
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)


# Home Page
@app.route('/')
def home():
    return render_template("index.html")


# Mark Attendance
@app.route('/mark', methods=['POST'])
def mark():

    name = request.form['name']
    status = request.form['status']

    today = date.today()

    data = {
        "Name": [name],
        "Status": [status],
        "Date": [today]
    }

    df = pd.DataFrame(data)

    if os.path.exists("attendance.csv"):
        df.to_csv("attendance.csv", mode='a', index=False, header=False)
    else:
        df.to_csv("attendance.csv", index=False)

    return render_template("success.html")


# View Attendance
@app.route('/view')
def view():

    if os.path.exists("attendance.csv"):

        df = pd.read_csv("attendance.csv")

        tables = df.to_html(index=False, classes='mytable')

        return render_template("view.html", tables=tables)

    else:
        return "No Data"



# Percentage Page
@app.route('/percentage')
def percentage():

    if os.path.exists("attendance.csv"):


        df = pd.read_csv("attendance.csv")

        total = df.groupby('Name').count()['Date']
        present = df[df['Status']=="Present"].groupby('Name').count()['Date']

        percent = (present/total*100).fillna(0).round(2)

        percent_df = percent.reset_index()

        percent_df.columns=['Name','Attendance %']


        # -------- GRAPH --------

        plt.figure()

        plt.bar(percent_df['Name'], percent_df['Attendance %'])

        plt.xlabel("Students")
        plt.ylabel("Attendance %")
        plt.title("Attendance Percentage")

        plt.savefig("static/graph.png")

        plt.close()

        # -------- TABLE --------

        tables = percent_df.to_html(index=False)

        return render_template("percentage.html",
                               tables=tables,
                               graph="graph.png")

    else:
        return "No Data"

@app.route('/search', methods=['GET','POST'])
def search():

    if request.method == 'POST':

        name = request.form['name']

        if os.path.exists("attendance.csv"):

            df = pd.read_csv("attendance.csv")

            result = df[df['Name']==name]

            tables = result.to_html(index=False)

            return render_template("search.html", tables=tables)

        else:
            return "No Data Found"

    return render_template("search.html")



# GRAPH FEATURE ⭐
@app.route('/graph')
def graph():

    if os.path.exists("attendance.csv"):

        df = pd.read_csv("attendance.csv")

        total = df.groupby('Name').count()['Date']
        present = df[df['Status']=="Present"].groupby('Name').count()['Date']

        percent = (present/total*100).fillna(0)


        plt.figure(figsize=(10,6))

        plt.bar(percent.index, percent.values)

        plt.title("Student Attendance Percentage",fontsize=16)

        plt.xlabel("Students",fontsize=12)

        plt.ylabel("Percentage",fontsize=12)

        plt.xticks(rotation=30)

        plt.tight_layout()

        plt.savefig("static/graph.png")

        plt.close()

        return render_template("graph.html")

    else:
        return "No Data"
