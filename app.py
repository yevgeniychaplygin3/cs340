import MySQLdb
import flask
from flask import render_template, request, redirect, flash
import configparser

def read_mysql_config(mysql_config_file_name):
    config = configparser.ConfigParser()
    config.read(mysql_config_file_name)
    return dict(config['client'])


# This will be different for each user.
config_info = read_mysql_config("/nfs/stak/users/chaplygy/Windows.Documents/My_Documents/cs340/.my.cnf")

# db_conn = MySQLdb.connect(config_info['host'],
#                           config_info['user'],
#                           config_info['password'],
#                           config_info['database'])

db_conn = [config_info[k] for k in ['host', 'user', 'password', 'database']]

def db_conn_func():
    return MySQLdb.connect(*db_conn)

# -----------------------------------------------------------------
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
# -----------------------------------------------------------------

# handle submitted forms
@webapp.route('/customer_results', methods=['GET', 'POST'])
def customer_results():
    result = ''
    # if insert button is pressed, insert the provided info
    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Customers (first_name, \
                                                last_name,\
                                                customer_phone,\
                                                customer_email,\
                                                reward_id) \
                                                VALUES (%s,%s,%s,%s, %s);"
        # get the text entered from the website
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        reward_id = request.form['reward_id']
        userdata = [fname, lname, phone, email, reward_id]
        index = 0
        for data in userdata:
            if data == '':
                userdata[index] = None
            index += 1
        # try the query, if something goes wrong, flash a message
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(insertquery, userdata)
            conn.commit()
        except Exception as e:
            result = f"Error: {e.args[1]}" 
            return  render_template('customers.html', customer_info=userdata, customer_results=result)

        result = f'Customer Inserted: {userdata[0]}, {userdata[1]}'
        return  render_template('customers.html',  customer_info=userdata, customer_results=result)

    # if update button is pressed
    elif "updatebutton" in request.form:
        updatequery = "UPDATE Customers SET first_name = %s, \
                                            last_name = %s, \
                                            customer_phone = %s, \
                                            customer_email=%s, \
                                            reward_id = %s \
                                            WHERE first_name = %s and last_name = %s"

        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']
        if not "checknull" in request.form:
            reward_id = request.form['reward_id']
        else:
            reward_id = None                       

        updatedata = (fname, lname, phone, email, reward_id, fname, lname)
        
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(updatequery, updatedata)
            conn.commit()
        except Exception as e:
            error = f"Error: {e.args[1]}"
            return  render_template('customers.html', customer_results=error)
        result = f"Customer Updated: {fname} {lname}"
        return  render_template('customers.html',  customer_results=result)


    # if search button is pressed,
    elif "searchbutton" in request.form:
        searchquery = "SELECT * FROM Customers where first_name = %s and last_name = %s;"
        first_name = request.form['fname']
        last_name = request.form['lname']
        data = (first_name, last_name)
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(searchquery, data)
            conn.commit()
            result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('customers.html', customer_info=userdata, customer_results=result)
        return render_template('customers.html', customer_info=result)
    return  render_template('customers.html')


@webapp.route('/cashier_results/', methods=['GET', 'POST'])
def cashier_results():
    result = ''

    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Cashiers (first_name, \
                                                last_name,\
                                                day_total,\
                                                day_worked,\
                                                lane) \
                                                VALUES (%s,%s,%s,%s, %s);"
        fname = request.form['fname']
        lname = request.form['lname']
        lane = request.form['lane']
        daytotal = (request.form['daytotal'])
        dayworked = request.form['dayworked']
        userdata = [fname, lname, daytotal, dayworked, lane]
        index = 0
        for data in userdata:
            if data == '': userdata[index] = None
            index += 1
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(insertquery, userdata)
            conn.commit()
            # result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('cashiers.html', data=error)
        result = f"Cashier Added: {fname} {lname}"
        return  render_template('cashiers.html',  cashier_insert=result)

    if "searchbutton" in request.form:
        searchquery = "SELECT * FROM Cashiers where (first_name = %s and last_name = %s) or day_worked = %s;"
        first_name = request.form['fname']
        last_name = request.form['lname']
        day_worked = request.form['dayworked']
        data = (first_name, last_name, day_worked)
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(searchquery, data)
            conn.commit()
            result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('cashiers.html',  data=error)
        return  render_template('cashiers.html',  cashier_info=result)
    if "deletebutton" in request.form:
        deletequery = "DELETE FROM Cashiers where cashier_id = %s;"
        cashier_id = request.form['cashierid']
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(deletequery, cashier_id)
            conn.commit()
            result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}"
            return render_template('cashiers.html', Status=error)
        return render_template('cashiers.html', status=result)
    return render_template('cashiers.html')

@webapp.route('/rewards_results', methods=['POST'])
def rewards_results():
    result = ''
    conn = db_conn_func()
    cursor = conn.cursor()
    if 'insertrewards' in request.form:
        insertquery = "INSERT INTO Rewards (reward_points, reward_discount) VALUES (%s,%s);"
        reward_points = int(request.form['rewardpoints'])
        reward_discount = int(request.form['selectdiscount'])
        data = (reward_points, reward_discount)
        
        cursor.execute(insertquery, data)
        conn.commit()
        return render_template('/rewards.html', rewards_info=result)
    elif 'selectall' in request.form:
        selectquery = "SELECT * FROM Rewards;"
        cursor.execute(selectquery, ())
        conn.commit()
        result = cursor.fetchall()
        return render_template('/rewards.html', rewards_info=result)
    elif 'deletebutton' in request.form:
        reward_id = request.form['deletereward']
        reward_id = (reward_id,)
        deletequery = "DELETE FROM Rewards WHERE reward_id=%s;"
        try:
            # conn = db_conn_func()
            # cursor = conn.cursor()
            cursor.execute(deletequery, reward_id)
            conn.commit()
        except Exception as e:
            error = f"Error: {e.args}" 
            return render_template('/rewards.html', delete_status=error )
        result = f"Reward Deleted: {reward_id[0]}"
        return render_template('/rewards.html', delete_status=result )
        

    return render_template('/rewards.html')

@webapp.route('/purchases_results', methods=['GET', 'POST'])
def purchases_results():
    conn = db_conn_func()
    cursor = conn.cursor()
    cid1 = request.form['customerid1']
    cid2 = request.form['customerid2']
    pid = request.form['purchaseid']
    pid2 = request.form['purchaseid2']
    cashierid = request.form['cashierid']
    if request.form.get('purchasecomplete'):
        complete = 1
    else:
        complete = 0
    price = request.form['totalprice']
    if (request.form.get('displaybutton') == ''):
        cursor.execute('SELECT * FROM Purchases WHERE customer_id = %s;', (cid2,))
        result = cursor.fetchall()
        cursor.close()
        return render_template('/purchases.html/', rows=result)
    elif (request.form.get('submitbutton') == ''):
        try:
            cursor.execute('INSERT INTO Purchases (customer_id, purchase_id, cashier_id, total_price, purchase_complete) VALUES (%s, %s, %s, %s, %s);', (cid1, pid, cashierid, price, complete))
        except:
            return render_template('purchases.html')
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('/purchases.html/', rows=result)
    elif (request.form.get('deletebutton') == ''):
        cursor.execute('DELETE FROM Purchases WHERE purchase_id = %s;', (pid2,))
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        return render_template('/purchases.html/', rows=result)




@webapp.route('/products_results', methods=['GET', 'POST'])
def products_results():
    conn = db_conn_func()
    cursor = conn.cursor()
    
    try:
        name2 = request.form['productname2']
        request.form['button1']
        cursor.execute('SELECT * FROM Products WHERE product_name = %s;', (name2,))
        result = cursor.fetchall()
        cursor.close()
        conn.commit()
        return render_template('/products.html/', rows=result)
    except:
        name1 = request.form['productname1']
   
        price = request.form['productprice']
        stock = request.form['stock']
        type = request.form['type']

        request.form['button2'] == ''
        cursor.execute('INSERT INTO Products (product_name, product_price, stock,  type) VALUES (%s, %s, %s, %s);', (name1, price, stock, type))
        result = cursor.fetchall()
        db_conn.commit()
        cursor.close()
        return render_template('/products.html/', rows=result)


if __name__ == "__main__":
    webapp.run(debug=True)
