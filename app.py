from calendar import c
from crypt import methods
import datetime
from re import L
import MySQLdb
import flask
from flask import render_template, request, redirect, flash
import configparser
from execute import execute_query, insert_customers, update_customers, insert_cashier

def read_mysql_config(mysql_config_file_name):
    config = configparser.ConfigParser()
    config.read(mysql_config_file_name)
    return dict(config['client'])


# This will be different for each user.
config_info = read_mysql_config("/nfs/stak/users/chaplygy/Windows.Documents/My_Documents/cs340/.my.cnf")

db_conn = MySQLdb.connect(config_info['host'],
                          config_info['user'],
                          config_info['password'],
                          config_info['database'])

webapp = flask.Flask(__name__, static_url_path='/static')

# Home 
@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/customers/')
def customers():
    return render_template('customers.html')

@webapp.route('/purchases/')
def Purchases():
    return render_template('purchases.html')

@webapp.route('/products/')
def products():
    return render_template('products.html')

@webapp.route('/cashiers/')
def cashiers():
    return render_template('cashiers.html')

@webapp.route('/rewards/')
def rewards():
    return render_template('rewards.html')

@webapp.route('/purchases_products/')
def purchases_products():
    return render_template('purchases_products.html')


# handle submitted forms
@webapp.route('/customer_results', methods=['GET', 'POST'])
def customer_results():
    cursor = db_conn.cursor()
    result = ''

    # if insert button is pressed, insert the provided info
    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Customers (first_name, \
                                                last_name,\
                                                customer_phone,\
                                                customer_email,\
                                                reward_id) \
                                                VALUES (%s,%s,%s,%s, %s);"
        # call the insert_customers function in the execute.py file to get the text entered from the website                                         
        userdata = insert_customers()

        # try the query, if something goes wrong, flash a message
        try:
            result = execute_query(db_conn, insertquery, userdata)
        except:
            print("something went wrong")
            flash('invalid insert info', 'warning')
            return  render_template('customers.html')
            
        flash('Customer Inserted')
        return  render_template('customers.html',  customer_info=result)

    # if update button is pressed
    elif "updatebutton" in request.form:
        updatequery = "UPDATE Customers SET first_name = %s, \
                                            last_name = %s, \
                                            customer_phone = %s, \
                                            customer_email=%s, \
                                            reward_id = %s \
                                            WHERE first_name = %s and last_name = %s"
        updatedata = update_customers()
        try:
            result = execute_query(db_conn, updatequery, updatedata)
        except:
            print("something went wrong")
            flash('Could not update', 'warning')
            return  render_template('customers.html')

        flash('Customer updated')
        return  render_template('customers.html',  customer_info=result)

    # if search button is pressed,
    elif "searchbutton" in request.form:
        searchquery = "SELECT * FROM Customers where first_name = %s and last_name = %s;"
        first_name = request.form['fname'] 
        last_name = request.form['lname'] 
        data = (first_name, last_name)
        result = execute_query(db_conn, searchquery, data)
        return render_template('customers.html', customer_info=result)

    return  render_template('customers.html')
           

@webapp.route('/cashier_results/', methods=['GET', 'POST'])
def cashier_results():
    cursor = db_conn.cursor()
    result = '' 
    
    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Cashiers (first_name, \
                                                last_name,\
                                                day_total,\
                                                day_worked,\
                                                lane) \
                                                VALUES (%s,%s,%s,%s, %s);"
        cashiersdata = insert_cashier()
        try: 
            result = execute_query(db_conn, insertquery, cashiersdata)
        except:
            print("something went wrong")
            flash('invalid insert info', 'warning')
            return  render_template('cashiers.html')

        flash('Cashier Inserted')
        return  render_template('cashiers.html',  cashier_info=result)

    if "searchbutton" in request.form:
        searchquery = "SELECT * FROM Cashiers where (first_name = %s and last_name = %s) or day_worked = %s;"
        first_name = request.form['fname'] 
        last_name = request.form['lname'] 
        day_worked = request.form['dayworked']
        data = (first_name, last_name, day_worked)
        result = execute_query(db_conn, searchquery, data)
        return  render_template('cashiers.html',  cashier_info=result)

        
    return render_template('cashiers.html')

@webapp.route('/rewards_results', methods=['POST'])
def rewards_results():
    cursor = db_conn.cursor()
    result = ''

    if 'insertrewards' in request.form:
        insertquery = "INSERT INTO Rewards (reward_points, reward_discount) VALUES (%s,%s);"
        reward_points = int(request.form['rewardpoints'])
        reward_discount = int(request.form['selectdiscount'])
        data = (reward_points, reward_discount)
        result = execute_query(db_conn, insertquery, data)
        return render_template('/rewards.html', rewards_info=result)
    elif 'selectall' in request.form:
        selectquery = "SELECT * FROM Rewards;"
        result = execute_query(db_conn, selectquery, ())
        return render_template('/rewards.html', rewards_info=result)

    return render_template('/rewards.html')





#-------------------------------------------------------------
@webapp.route('/purchases_results', methods=['GET', 'POST'])
def purchases_results():
    return render_template('/purchases.html')

# @webapp.route('/products_results', methods=['GET', 'POST'])
# def products_results():
#     # cursor object that handles the requests
#     cursor = db_conn.cursor()
#     name = request.form['productname']
#     try:
#         request.form['button1']
#         cursor.execute('SELECT * FROM Products where product_name = %s;',(name,) ) 
#         # create results object with all the results from the query above
#         result = cursor.fetchall()
#         cursor.close()
#         return render_template('/products.html/', rows=result )
#     except:
#         request.form['button2'] == ''
#         cursor.execute('INSERT INTO Products (product_name, product_price, stock, type) VALUES ("new name", 20.99, 5, "type")') 
#         # create results object with all the results from the query above
#         result = cursor.fetchall()
#         db_conn.commit()
#         cursor.close()
#         return render_template('/products.html/', rows=result )
        

# @webapp.route('/purchases_products_results', methods=['GET', 'POST'])
# def purchase_products_results():
#     return render_template('/index.html')


if __name__ == "__main__":
    webapp.secret_key = "mysecretkey123"
    webapp.run(debug=True)
    
