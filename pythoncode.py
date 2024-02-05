from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
import pymysql
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

CORS(app)

auth = HTTPBasicAuth()

@auth.verify_password
def checkpassword(username, password):
    if username == "GBCA" and password == "abc!!":
        return True
    else:
        return False

#Database connection
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Gbca-123'
app.config['MYSQL_DATABASE_DB'] = 'classicmodels'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def format_response(data, status_code=200):
    response = jsonify(data)
    response.status_code = status_code
    return response

#1
@app.route("/employees")
def get_employees():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = "select employeeNumber, lastName, firstName, email, jobTitle from employees"
        cursor.execute(sql_commnd)
        employees = cursor.fetchall()
        return format_response(employees)

    except pymysql.Error as e:
        return format_response(e.args[1], 404)

#2
@app.route("/employees/<int:id>")
def get_employee(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = f"select employeeNumber, lastName, firstName, email, jobTitle from employees where employeenumber = {id}"
        cursor.execute(sql_commnd)
        employee = cursor.fetchone()
        return format_response(employee)

    except pymysql.Error as e:
        return format_response(e.args[1], 404)

#3 - add employee
@app.route("/employees", methods = ["POST"])
@auth.login_required
def add_employee():
    try: 
        employee = request.json
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = f"insert into employees(lastName, firstName, email, jobTitle) values('{employee.get('lastName')}', '{employee.get('firstName')}', '{employee.get('email')}', '{employee.get('jobTitle')}')"

        affected_row = cursor.execute(sql_commnd)
        conn.commit()
        if affected_row == 1:
            return format_response("Employee added successfully")

    except pymysql.Error as e:
        return format_response(e.args[1], 404)
    else:
        return format_response("Error with insert.", 404)

#4 - update employee
@app.route("/employees", methods = ["PUT"])
@auth.login_required
def update_employee():
    try: 
        employee = request.json
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = f"Update employees set lastName = '{employee.get('lastName')}', firstName = '{employee.get('firstName')}', email = '{employee.get('email')}', jobTitle = '{employee.get('jobTitle')}' where employeeNumber = {employee.get('employeeNumber')}"

        affected_row = cursor.execute(sql_commnd)
        conn.commit()
        if affected_row == 1:
            return format_response("Employee updated successfully")
        else:
            return format_response("No update.", 404)

    except pymysql.Error as e:
        return format_response(e.args[1], 404)

#5 - delete employee
@app.route("/employees/<int:id>", methods = ["DELETE"])
@auth.login_required
def delete_employee(id):
    try: 
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = f"delete from employees where employeenumber = {id}"
        affected_row = cursor.execute(sql_commnd)
        conn.commit()
        if affected_row == 1:
            return format_response("Employee deleted successfully")
        else:
            return format_response("Error with Delete.", 404)
    except pymysql.Error as e:
        return format_response(e.args[1], 404)

#6
@app.route("/chart1")
def chart1():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = "select country, count(*) as count from customers group by country order by count(*) desc limit 5;"
        cursor.execute(sql_commnd)
        results = cursor.fetchall()

        data = {"xValues": [], "yValues": []}

        for result in results:
            data.get("xValues").append(result.get("country"))
            data.get("yValues").append(result.get("count"))

        return format_response(data)

    except pymysql.Error as e:
        return format_response(e.args[1], 404)

#7  
@app.route("/chart2/<int:year>")
def chart2(year):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = f"select month(orderDate) as month, count(*) as count from orders where year(orderDate) = {year} group by month order by month;"
        cursor.execute(sql_commnd)
        results = cursor.fetchall()

        data = {"year": year, "xValues": [], "yValues": []}

        for result in results:
            data.get("xValues").append(result.get("month"))
            data.get("yValues").append(result.get("count"))

        return format_response(data)
    
    except pymysql.Error as e:
        return format_response(e.args[1], 404)

#8
@app.route("/chart3")
def chart3():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = f"select productline, count(*) as count from products group by productline"
        cursor.execute(sql_commnd)
        results = cursor.fetchall()

        data = {"xValues": [], "yValues": []}

        for result in results:
            data.get("xValues").append(result.get("productline"))
            data.get("yValues").append(result.get("count"))

        return format_response(data)
    
    except pymysql.Error as e:
        return format_response(e.args[1], 404)

#9
@app.route("/chart4")
def chart4():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = f"select year(orderDate) as year, count(*) as count from orders group by year order by year;"
        cursor.execute(sql_commnd)
        results = cursor.fetchall()

        data = {"xValues": [], "yValues": []}

        for result in results:
            data.get("xValues").append(result.get("year"))
            data.get("yValues").append(result.get("count"))

        return format_response(data)
    
    except pymysql.Error as e:
        return format_response(e.args[1], 404)
    
#10
@app.route("/total_employees")
def get_total_employees():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql_commnd = "select count(*) as totalemployees from employees;"
        cursor.execute(sql_commnd)
        results = cursor.fetchone()

        return format_response(results)
    
    except pymysql.Error as e:
        return format_response(e.args[1], 404)

app.run(host='localhost', port=3001)