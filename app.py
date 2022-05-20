from calendar import c
from crypt import methods
import datetime
from re import L
import MySQLdb
import flask
from flask import render_template, request, redirect, flash
import configparser
from db_connector import connect_to_database, execute_query

# def read_mysql_config(mysql_config_file_name: str):
#     with open(mysql_config_file_name, "r") as mysql_conf:
#         config_info = dict()
#         for line in mysql_conf.readlines():
#             if line.startswith('['): continue
#             config_info.update(dict([(substr.strip() for substr in line.split('='))]))
#     return config_info

# use this function instead..
def read_mysql_config(mysql_config_file_name):
     config = configparser.ConfigParser()
     config.read(mysql_config_file_name)
     return dict(config['client'])


# This will be different for each user.
config_info = read_mysql_config("/nfs/stak/users/swinforb/.my.cnf")

db_conn = MySQLdb.connect(config_info['host'],
                           config_info['user'],
                           config_info['password'],
                           config_info['database'])

webapp = flask.Flask(__name__, static_url_path='/static')

# Example of how to get data from the data base
# @webapp.route('/')
# def get_tables():
#     res_html = "<html>\n<body>\n<table border=\"1\">\n"
#     cursor = db_conn.cursor()
#     cursor.execute('show tables;', ())
#     for [table_name] in cursor.fetchall():
#         res_html += f"<tr><td>{table_name}</td></tr>\n"
#     res_html += "</table>\n"
#     res_html += "<img src=\"/static/logo.png\" />\n</body>\n</html>\n"
#     # res_html += "<p>hello world!</p>"
#     return res_html
# ##get_tables = webapp.route('/')(get_tables)

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
#    print("fetching and rendering product page")
    db_connection = connect_to_database()
#    query = "SELECT * from Products;"
#    result = execute_query(db_connection, query).fetchall();
#    print(result)
#    return render_template('products.html', rows=result)
#def products():
    return render_template('products.html')

@webapp.route('/cashiers/')
def cashiers():
    return "Hello World!"
    return render_template('cashiers.html')

@webapp.route('/rewards/')
def rewards():
    return render_template('rewards.html')

@webapp.route('/purchases_products/')
def purchases_products():
    return render_template('purchases_products.html')


# Once a form is submitted, the corresponding function will get called and will return a new html page to the user interface. Each passes in the form input.
# the cashier form is submitted, then this function will get called which renders the cashier_results.html template, and passes in the inputs


@webapp.route('/cashier_results/', methods=['GET', 'POST'])
def cashier_results():
    return render_template('cashiers.html')

# the cashier form is submitted, then this function will get called which renders the  template, and passes in the arguments
@webapp.route('/customer_results', methods=['GET', 'POST'])
def customer_results():
    return  render_template('customers.html',  form=request.form)

@webapp.route('/purchases_results', methods=['GET', 'POST'])
def purchases_results():
    cursor = db_conn.cursor()
    cid1 = request.form['customerid1']
    cid2 = request.form['customerid2']
    pid = request.form['purchaseid']
    cashierid = request.form['cashierid']
    if request.form.get('purchasecomplete'):
        complete = 1
    else:
        complete = 0
    price = request.form['totalprice']
    try:
        request.form['displaybutton']
        cursor.execute('SELECT * FROM Purchases WHERE customer_id = %s;', (cid2,))
    #    cursor.execute('select * from Purchases;', ())
        result = cursor.fetchall()
        cursor.close()
        return render_template('/purchases.html/', rows=result)
    except:
        request.form['submitbutton']
        cursor.execute('INSERT INTO Purchases (customer_id, purchase_id, cashier_id, total_price, purchase_complete) VALUES (%s, %s, %s, %s, %s);', (cid1, pid, cashierid, price, complete))
        result = cursor.fetchall()
        db_conn.commit()
        cursor.close()
        return render_template('/purchases.html/', rows=result)

@webapp.route('/products_results', methods=['GET', 'POST'])
def products_results():
        cursor = db_conn.cursor()
        name = request.form['productname']
        price = request.form['productprice']
        stock = request.form['stock']
        type = request.form['type']
        try:
            request.form['button1']
            cursor.execute('SELECT * FROM Products WHERE product_name = %s OR product_price = %s OR stock = %s OR type = %s;', (name, price, stock, type))
            result = cursor.fetchall()
            cursor.close()
            return render_template('/products.html/', rows=result)
        except:
            request.form['button2'] == ''
            cursor.execute('INSERT INTO Products (product_name, product_price, stock,  type) VALUES (%s, %s, %s, %s);', (name, price, stock, type))
            result = cursor.fetchall()
            db_conn.commit()
            cursor.close()
            return render_template('/products.html/', rows=result)

@webapp.route('/purchases_products_results', methods=['GET', 'POST'])
def purchase_products_results():
    return render_template('/index.html')






if __name__ == "__main__":
    webapp.run(debug=True,)
