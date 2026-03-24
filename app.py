from flask import Flask, render_template, request
from pymysql import connections
from pymysql.err import MySQLError
from botocore.exceptions import ClientError, NoCredentialsError
import boto3
import os
import random
import argparse
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Database environment variables
DBHOST = os.environ.get("DBHOST") or os.environ.get("MYSQL_HOST") or "localhost"
DBUSER = os.environ.get("DBUSER") or os.environ.get("MYSQL_USER") or "root"
DBPWD = os.environ.get("DBPWD") or os.environ.get("MYSQL_PASSWORD") or "password"
DATABASE = os.environ.get("DATABASE") or os.environ.get("MYSQL_DB") or "employees"
DBPORT = int(os.environ.get("DBPORT") or "3306")

# App environment variables
COLOR_FROM_ENV = os.environ.get("APP_COLOR") or "lime"
APP_HEADER_NAME = os.environ.get("APP_HEADER_NAME") or "Maharshi Mehta"

# S3 background image environment variables
BG_IMAGE_BUCKET = os.environ.get("BG_IMAGE_BUCKET", "")
BG_IMAGE_KEY = os.environ.get("BG_IMAGE_KEY", "")
LOCAL_BG_DIR = "static/backgrounds"
LOCAL_BG_FILE = os.path.join(LOCAL_BG_DIR, "background.jpg")

color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}

SUPPORTED_COLORS = ",".join(color_codes.keys())
COLOR = random.choice(list(color_codes.keys()))

def get_db_connection():
    return connections.Connection(
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        password=DBPWD,
        db=DATABASE
    )

def download_background():
    # Allow local testing even if S3 bucket is not created yet
    if not BG_IMAGE_BUCKET or not BG_IMAGE_KEY:
        app.logger.warning("Background bucket/key not set. Using no background image for now.")
        return None

    app.logger.info(f"Background image location: s3://{BG_IMAGE_BUCKET}/{BG_IMAGE_KEY}")
    os.makedirs(LOCAL_BG_DIR, exist_ok=True)

    try:
        s3 = boto3.client("s3")
        s3.download_file(BG_IMAGE_BUCKET, BG_IMAGE_KEY, LOCAL_BG_FILE)
        return "/" + LOCAL_BG_FILE
    except (ClientError, NoCredentialsError) as e:
        app.logger.error(f"Could not download background image: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    bg_path = download_background()
    return render_template(
        "addemp.html",
        color=color_codes[COLOR],
        app_header_name=APP_HEADER_NAME,
        bg_path=bg_path
    )

@app.route("/about", methods=["GET", "POST"])
def about():
    bg_path = download_background()
    return render_template(
        "about.html",
        color=color_codes[COLOR],
        app_header_name=APP_HEADER_NAME,
        bg_path=bg_path
    )

@app.route("/addemp", methods=["POST"])
def AddEmp():
    emp_id = request.form["emp_id"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    primary_skill = request.form["primary_skill"]
    location = request.form["location"]

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"

    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = first_name + " " + last_name
    except MySQLError as e:
        app.logger.error(f"MySQL insert error: {e}")
        return f"Database insert failed: {e}", 500
    finally:
        try:
            cursor.close()
            db_conn.close()
        except Exception:
            pass

    return render_template(
        "addempoutput.html",
        name=emp_name,
        color=color_codes[COLOR],
        app_header_name=APP_HEADER_NAME
    )

@app.route("/getemp", methods=["GET", "POST"])
def GetEmp():
    bg_path = download_background()
    return render_template(
        "getemp.html",
        color=color_codes[COLOR],
        app_header_name=APP_HEADER_NAME,
        bg_path=bg_path
    )

@app.route("/fetchdata", methods=["GET", "POST"])
def FetchData():
    emp_id = request.form["emp_id"]
    output = {}

    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"

    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()

        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
        else:
            return f"No employee found with ID {emp_id}", 404
    except MySQLError as e:
        app.logger.error(f"MySQL fetch error: {e}")
        return f"Database fetch failed: {e}", 500
    finally:
        try:
            cursor.close()
            db_conn.close()
        except Exception:
            pass

    return render_template(
        "getempoutput.html",
        id=output["emp_id"],
        fname=output["first_name"],
        lname=output["last_name"],
        interest=output["primary_skills"],
        location=output["location"],
        color=color_codes[COLOR],
        app_header_name=APP_HEADER_NAME
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--color", required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =" + args.color)
        COLOR = args.color
        if COLOR_FROM_ENV:
            print("A color was set through environment variable -" + COLOR_FROM_ENV + ". However, color from command line argument takes precedence.")
    elif COLOR_FROM_ENV:
        print("No command line argument. Color from environment variable =" + COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("No command line argument or environment variable. Picking a random color =" + COLOR)

    if COLOR not in color_codes:
        print("Color not supported. Received '" + COLOR + "' expected one of " + SUPPORTED_COLORS)
        exit(1)

    app.run(host="0.0.0.0", port=81, debug=False)
