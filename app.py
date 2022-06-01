import MySQLdb
import flask, datetime
from flask import render_template, request
import configparser

# parse login info for database in the .my.cnf file
def read_mysql_config(mysql_config_file_name):
    config = configparser.ConfigParser()
    config.read(mysql_config_file_name)
    return dict(config['client'])


# This will be different for each user.
config_info = read_mysql_config("/nfs/stak/users/chaplygy/Windows.Documents/My_Documents/cs340/.my.cnf")


db_conn = [config_info[k] for k in ['host', 'user', 'password', 'database']]

''' Set up the connection to the MySQLdb. Connection to the database will be initialized by calling this function.'''
def db_conn_func():
    return MySQLdb.connect(*db_conn)


'''
    This function will be used for the purchases page. It query the information (Customers, Cashiers, Products Tables) 
    needed and return it in a list. 
'''
def purchases_helper():
    conn = db_conn_func()
    cursor = conn.cursor()

    # get the list of current customers
    cursor.execute("SELECT first_name, last_name FROM Customers;")
    customers = cursor.fetchall()

    # add customers to a list and format   
    customer_list = []
    for customer in customers:
        customer = str(customer).strip("()").replace("'", "").replace(",", '')
        customer_list.append(customer) 

     # get the list of current cashiers
    cursor.execute("SELECT DISTINCT first_name, last_name FROM Cashiers;")
    cashiers = cursor.fetchall()

    # add customers to a list and format   
    cashiers_list = []
    for cashier in cashiers:
        cashier = str(cashier).strip("()").replace("'", "")
        
        cashiers_list.append(cashier) 

    # get the list of products
    cursor.execute("SELECT product_name FROM Products;")
    products = cursor.fetchall()
    
    # add customers to a list and format   
    products_list = []
    for p in products:
        p = str(p).strip("()").replace("'", "").replace(",", '')
        products_list.append(p)
    cursor.execute("SELECT * FROM Purchases;")
    all_info = cursor.fetchall()
    
    return (all_info, customer_list, cashiers_list, products_list)



webapp = flask.Flask(__name__, static_url_path='/static')


# Render Home page
@webapp.route('/')
def index():
    return render_template('index.html')


'''
    When opening the customer page, it will query all the customers and render that in the customers.html page.
    It will also get a list of all the rewards that a customer can have. This will implement the relationship beween Customers 
    and Rewards as described in the outline. This will implement the READ functionality by reading all the data in the database
    using the SELECT statement. 
'''
@webapp.route('/customers/')
def customers():
    # connect to DB. Create Cursor Object
    conn = db_conn_func()
    cursor = conn.cursor()

    # Run this SELECT query
    cursor.execute("SELECT reward_id FROM Rewards;")
    
    # get the results of the select query
    rewards_results = cursor.fetchall()

    # Rewards results returns a tuple of tuples. Extract the first element from each tuple 
    # which will be the reward_id and store in list
    reward_id_list = []
    for i in rewards_results:
        reward_id_list.append(i[0]) 

    # get all the colomns from the Customers table
    cursor.execute("SELECT * FROM Customers;")
    customers_results = cursor.fetchall()

    return render_template('customers.html', customer_info=customers_results, reward_options=reward_id_list)




'''
    Purchases page will call the purchase helper funciton to query the information needed to be displayed 
    on the web page. Render it into the purchases.html file. 
'''
@webapp.route('/purchases/')
def Purchases():
    # this return a list of all Customers, Cashiers, and Products information
    results = purchases_helper()

    # parse out the list and render it in the HTML page
    all_info = results[0]
    customer_list = results[1]
    cashiers_list = results[2]
    products = results[3]

    return render_template('purchases.html', rows=all_info, customers=customer_list, cashiers=cashiers_list, products=products)

''' 
    When the products page is first opened, it will render a list of all the products in the 
    database using the SELECT query. 
'''
@webapp.route('/products/')
def products():
    # connect to DB
    conn = db_conn_func()
    cursor = conn.cursor()
    
    # Run the query. Fetch the results and render the webpage.
    cursor.execute("SELECT * FROM Products;")
    result = cursor.fetchall()

    return render_template('products.html', rows=result)

''' Similar to the other functions above. Query the database, render the webpage with the results of the query '''
@webapp.route('/cashiers/')
def cashiers():
    # connect to DB
    conn = db_conn_func()
    cursor = conn.cursor()

    # Run the query. Fetch the results and render the webpage.
    cursor.execute("SELECT * FROM Cashiers;")
    result = cursor.fetchall()
    
    return render_template('cashiers.html', cashier_info=result)

''' Similar to the other functions above. Query the database, render the webpage with the results of the query.'''
@webapp.route('/rewards/')
def rewards():
    # connect to DB
    conn = db_conn_func()
    cursor = conn.cursor()

    # Run the query. Fetch the results and render the webpage.
    selectquery = "SELECT * FROM Rewards;"
    cursor.execute(selectquery, ())
    result = cursor.fetchall()

    return render_template('rewards.html', rewards_info=result)


# Handle submitted forms

''' 
    This will be called once a form is submitted in the customers page. The functionaility implemented is CREATE, READ, and UPDATE.
    Customers will have a optional relationship with Rewards, where a customer can have zero or one rewards. 
'''
@webapp.route('/customer_results', methods=['GET', 'POST'])
def customer_results():
    # connect to the database
    conn = db_conn_func()
    cursor = conn.cursor()

    # get all the columns and rows from Customers Table
    cursor.execute("SELECT * FROM Customers;")
    result = cursor.fetchall()

    # get all the reward_id from Rewards Table
    cursor.execute("SELECT reward_id FROM Rewards;")
    result1 = cursor.fetchall()

    # parse out the result. It will be a tuple of tuples, where the reward_id 
    # is the first element in each tuple. Add to list
    reward_id_list = []
    for i in result1:
        reward_id_list.append(i[0]) 
    


    # if insert button is pressed, insert the provided info
    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Customers (first_name, \
                                                last_name,\
                                                customer_phone,\
                                                customer_email,\
                                                reward_id) \
                                                VALUES (%s,%s,%s,%s, %s);"
        # get the text entered from the website. Add to list.
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']

        reward_id = request.form['reward_id']

        userdata = [fname, lname, phone, email, reward_id]

        # check for null/empty data
        index = 0
        for data in userdata:
            if data == '':
                userdata[index] = None
            index += 1

        # try the query, if something goes wrong return an error
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(insertquery, userdata)
            conn.commit()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('customers.html', customer_info=result, reward_options=reward_id_list, customer_results_error=error)

        # print out a message to let the user know a customer was added
        insertedresult = f'Customer Inserted: {userdata[0]}, {userdata[1]}'

        # query again to get the new list of customers. Render it in the page.
        cursor.execute("SELECT * FROM Customers;")
        result = cursor.fetchall()

        return  render_template('customers.html',  customer_info=result,reward_options=reward_id_list, customer_results=insertedresult)

    # if update button is pressed, update the provided info
    elif "updatebutton" in request.form:
        updatequery = "UPDATE Customers SET first_name = %s, \
                                            last_name = %s, \
                                            customer_phone = %s, \
                                            customer_email=%s, \
                                            reward_id = %s \
                                            WHERE first_name = %s and last_name = %s"

        # get the text entered from the website. Add to list.
        fname = request.form['fname']
        lname = request.form['lname']
        phone = request.form['phone']
        email = request.form['email']

        # see if the NULL checkbox is checked.
        if not "checknull" in request.form:
            reward_id = request.form['reward_id']
        else:
            reward_id = None                       

        updatedata = (fname, lname, phone, email, reward_id, fname, lname)
        
        # try the query, if something goes wrong return an error
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(updatequery, updatedata)
            conn.commit()

        except Exception as e:
            error = f"Error: {e.args[1]}"
            return  render_template('customers.html', customer_info=result, reward_options=reward_id_list, customer_results_error=error)

        # print out a message to let the user know a customer was updated
        updateresult = f"Customer Updated: {fname} {lname}"

        # query again to get the updated list of customers. Render it in the page.
        cursor.execute("SELECT * FROM Customers;")
        result = cursor.fetchall()

        return render_template('customers.html', customer_info=result, reward_options=reward_id_list, customer_results=updateresult)


    # if search button is pressed, query the requested information
    elif "searchbutton" in request.form:
        searchquery = "SELECT * FROM Customers where first_name = %s and last_name = %s;"
        
        # get the text entered from the website. Add to data.
        first_name = request.form['fname']
        last_name = request.form['lname']
        data = (first_name, last_name)


        # try the query, if something goes wrong return an error
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(searchquery, data)
            conn.commit()
            result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('customers.html', customer_info=result, reward_options=reward_id_list, customer_results_error=error)

        return render_template('customers.html', customer_info=result, reward_options=reward_id_list)

    return  render_template('customers.html', customer_info=result, reward_options=reward_id_list)



''' 
    Once a form is submitted, this will be called. The functionality implemented is READ and CREATE.
    Cashiers will have an optional relationship, where cashiers can have zero or more purchases.   
'''
@webapp.route('/cashier_results/', methods=['GET', 'POST'])
def cashier_results():
    # connect to the database
    conn = db_conn_func()
    cursor = conn.cursor()

    # get all the columns and rows from Cashiers Table
    cursor.execute("SELECT * FROM Cashiers;")
    result = cursor.fetchall()

    # if insert button is pressed, insert the provided info
    if "insertbutton" in request.form:
        insertquery = "INSERT INTO Cashiers (first_name, \
                                                last_name,\
                                                day_total,\
                                                day_worked,\
                                                lane) \
                                                VALUES (%s,%s,%s,%s, %s);"
        # get the text entered from the website. Add to userdata list.
        fname = request.form['fname']
        lname = request.form['lname']
        lane = request.form['selectlane']
        daytotal = (request.form['daytotal'])
        dayworked = request.form['dayworked']
        userdata = [fname, lname, daytotal, dayworked, lane]

        # check for null/empty data
        index = 0
        for data in userdata:
            if data == '': userdata[index] = None
            index += 1

        # try the query, if something goes wrong return an error
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(insertquery, userdata)
            conn.commit()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('cashiers.html', cashier_info=result, data=error)

        # print out a message to let the user know a cashier was added
        insertresult = f"Cashier Added: {fname} {lname}"

        # query again to get the new list of Cashiers. Render it in the page.
        cursor.execute("SELECT * FROM Cashiers;")
        result = cursor.fetchall()

        return  render_template('cashiers.html', cashier_info=result, cashier_insert=insertresult)

    # if search button is pressed, query the requested information
    if "searchbutton" in request.form:
        searchquery = "SELECT * FROM Cashiers where (first_name = %s and last_name = %s) or day_worked = %s;"

        # get the text entered from the website. Add to data.
        first_name = request.form['fname']
        last_name = request.form['lname']
        day_worked = request.form['dayworked']
        data = (first_name, last_name, day_worked)


        # try the query, if something goes wrong return an error
        try:
            conn = db_conn_func()
            cursor = conn.cursor()
            cursor.execute(searchquery, data)
            conn.commit()
            result = cursor.fetchall()
        except Exception as e:
            error = f"Error: {e.args[1]}" 
            return  render_template('cashiers.html',  data=error)

        # render the page
        return  render_template('cashiers.html',  cashier_info=result)
  
    return render_template('cashiers.html', cashier_info=result)


''' 
    The functionality implemented is CREATE and DELETE. Rewards will be an optional relaionship to Customers
    where a reward can be assigned to no customers, or many customers. 
'''
@webapp.route('/rewards_results', methods=['POST'])
def rewards_results():
    # place holders
    result = ''
    result1 = ''
    # connect to the database
    conn = db_conn_func()
    cursor = conn.cursor()

    # if insert button is pressed, insert the provided info
    if 'insertrewards' in request.form:
        insertquery = "INSERT INTO Rewards (reward_points, reward_discount) VALUES (%s,%s);"

        # get the text entered from the website. Add to 'data'.
        reward_points = int(request.form['rewardpoints'])
        reward_discount = int(request.form['selectdiscount'])
        data = (reward_points, reward_discount)
        
        # run the query
        cursor.execute(insertquery, data)
        conn.commit()

    # if delete button is pressed, delete the provided info from the DB
    if 'deletebutton' in request.form:

        # get the text entered from the website.
        reward_id =request.form.get('deletereward')
        reward_id = (reward_id,)
        deletequery = "DELETE FROM Rewards WHERE reward_id = %s"

        # try the query, if something goes wrong return an error
        try:
    
            cursor.execute(deletequery, reward_id)
            conn.commit()
            
        except Exception as e:
            error = f"Error: {e.args}" 
            return render_template('/rewards.html', delete_status=error )
        result1 = f"Reward Deleted: {reward_id[0]}"

    # retrieve the new results of rewards from the database queries. 
    selectquery = "SELECT * FROM Rewards;"
    cursor.execute(selectquery, ())
    result = cursor.fetchall()
    return render_template('/rewards.html', rewards_info=result, delete_status=result1 )



'''
    The functionality provided for Purchases is CREATE, READ, and DELETE. 
    Purchases will have mandatory relationship with Cashiers, Customers, and Products. 
    Each purchase must have a Customer, Cashier, and Product. On the same note,
    the Purchase to Customer relationship is many to one. One purchase with one customer, 
    and many customers have none or more purchases. Purchases can have many products, and products 
    can have many purchases, this is the many-to-many implementation. Purchases can have one cashier,
    so it will have a many to one relationship. 
'''
@webapp.route('/purchases_results', methods=['GET', 'POST'])
def purchases_results():
    # connect to the database
    conn = db_conn_func()
    cursor = conn.cursor()
    # place holders
    submitresult = ''
    deleteresult = ''

    # this return a list of all Customers, Cashiers, and Products information
    results = purchases_helper()

    # parse out the list 
    all_info = results[0]
    customer_list = results[1]
    cashiers_list = results[2]
    products_list = results[3]

    # if submit purchase button is pressed, insert the provided info
    if "submitbutton" in request.form:
        
        # try to find the customer, print error if not found
        try:
            # perform a query to get customer id
            firstname = request.form['fname']
            lastname = request.form['lname']
            querycustomer = "SELECT customer_id FROM Customers WHERE first_name =%s and last_name=%s;"
            customer = (firstname, lastname)
            cursor.execute(querycustomer, customer)
            cid1 = cursor.fetchall()
            cid1 =cid1[0][0] 
        except:
            error = "Customer Not found"
            return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, purchases_result=error, products=products_list)


        # perform a query to get cashier id
        
        # get the first name of cashier
        cashiername = str(request.form['selectcashier']).replace(",", '')
        querycashier = "SELECT cashier_id FROM Cashiers WHERE first_name =%s;"
        cashiername = (cashiername, )

        cursor.execute(querycashier, cashiername)
        cashierid = cursor.fetchall()
        # cashierid will be 2d tuple. ID is the first element. 
        cashierid = cashierid[0][0]

        # check to see if the checkbox is checked
        if request.form.get('purchasecomplete'):
            complete = 1
        else:
            complete = 0
        # get price from website input 
        price = request.form['totalprice']

        
        products_bought = []
        # get the list of products that were checked
        for i in  request.form.getlist('productsbought'):
            products_bought.append(i) 

        quantity= []
        # get all quantities for the products
        for i in request.form.getlist('quantity'):
            if i != '':
                quantity.append(i)


        productids = []
        # get the id's for each product
        for i in products_bought:
            i = i + "%"
            selectproduct = "SELECT product_id FROM Products WHERE product_name LIKE %s;"
            cursor.execute(selectproduct, [i])

            # this will get just the id's and put them in the results list. 
            productids.append(str(cursor.fetchall()).replace("(", "").replace(")", "").replace(',','')) 

        # set the purchase date
        date = datetime.datetime.now()


        # try the insert query, if something goes wrong return an error
        try:
            cursor.execute('INSERT INTO Purchases (date, customer_id, cashier_id, total_price, purchase_complete) VALUES (%s,%s, %s, %s, %s);', (date, cid1, cashierid, price, complete))
            conn.commit()

            # get the purchase_id that was just inserted
            cursor.execute("SELECT purchase_id FROM Purchases ORDER BY purchase_id DESC LIMIT 1;", )
            purchase_id = cursor.fetchall()
            purchase_id = purchase_id[0][0]

            # insert every product bought into the Purchases_Products table 
            for i in range(len(products_bought)):
                insertquery = "INSERT INTO Purchases_Products (purchase_id, product_id, quantity) VALUES (%s, %s, %s);"
                args = (purchase_id, productids[i], quantity[i])
                cursor.execute(insertquery, args)
                conn.commit()

        except Exception as e:
            error = f"Error: {e.args}" 
            return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, purchases_result=error, products=products_list)

        submitresult = f"Purchase Info Submitted for: {firstname} {lastname}"


    # if search button is pressed, query the requested information
    if 'searchbutton' in request.form:

        # get the text entered from the website. 
        cid2 = request.form['customerid2']
        cursor.execute('SELECT * FROM Purchases WHERE customer_id = %s;', (cid2,))
        searchresult = cursor.fetchall()

        # this return a list of all Customers, Cashiers, and Products information
        results = purchases_helper()

        # parse out the list 
        customer_list = results[1]
        cashiers_list = results[2]
        products_list = results[3]

        # get the purchase id from the customer
        try:
            purchase_id = searchresult[0][0]
            purchase_id = (purchase_id, )
        except Exception as e:
            error = f"Error: {e.args}" 
            return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, search_error=error, products=products_list)


        # perform the query and get the results
        products_query = "SELECT * FROM Purchases_Products WHERE purchase_id = %s;"
        cursor.execute(products_query, purchase_id)
        products_retrieve_result = cursor.fetchall()

        # get the products_id and quantity from a purchase
        productsID_list = []
        quantity = []
        # parse the result, where product_id is the second element, and quantity is the third. Add to lists. 
        for i in products_retrieve_result:
            productsID_list.append(i[1]) 
            quantity.append(i[2])
        
        index = 0
        
        # get the list of products and price that a customer bought from the purchase_id retrieved above.
        # add to the customer_products_list 
        customer_products_list = []
        for i in productsID_list:

            cursor.execute("SELECT product_name, product_price FROM Products WHERE product_id = %s;", (i,))
            # to hold the results (name and price)
            l = []
            
            product_name_price_result = cursor.fetchall()
            
            l.append(quantity[index])
            l.append(product_name_price_result[0][0])
            l.append(product_name_price_result[0][1])
            
            customer_products_list.append(l)

            index += 1
            

        cursor.close()
        return render_template('/purchases.html/', rows=searchresult,  customers=customer_list, cashiers=cashiers_list, purchases_result=submitresult, products=products_list, products_bought=customer_products_list )
        
    
    # if delete button is pressed, delete the provided info from the DB
    elif (request.form.get('deletebutton') == ''):

        # get the id entered from the website.
        pid2 = request.form['purchaseid2']
        # run the delete query 
        
        cursor.execute('DELETE FROM Purchases WHERE purchase_id = %s;', (pid2,))
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        # return a message 
        deleteresult = f"Purchase Deleted: {pid2}"
    
    # return all the information
    results = purchases_helper()
    all_info = results[0]
    customer_list = results[1]
    cashiers_list = results[2]
    products_list = results[3]
    
    return render_template('/purchases.html/', rows=all_info, customers=customer_list, cashiers=cashiers_list, purchases_result=submitresult, products=products_list, delete_result=deleteresult)



''' 
    The functionality implemented is CREATE, READ and DELETE. Products will have a many to many 
    optional relationship with Purchases, where a product can be apart of zero or more purchases. 
'''
@webapp.route('/products_results', methods=['GET', 'POST'])
def products_results():
    # connect to the database
    conn = db_conn_func()
    cursor = conn.cursor()

    # if search button is pressed, query the requested information
    if "searchbutton" in request.form:

        # try the query, if something goes wrong print an error
        try:
            seachproduct = request.form['searchproduct']
            cursor.execute('SELECT * FROM Products WHERE product_name = %s;', (seachproduct,))
            result = cursor.fetchall()
            cursor.close()
            conn.commit()
            return render_template('/products.html/', rows=result)
        except Exception as e:
            error = f"Error: {e.args}" 
            print(error)
            pass


    # if insert button is pressed, insert the provided info
    elif "insertbutton" in request.form:
        # get the text entered from the website. Add to list.
        name1 = request.form['productname1']
        price = request.form['productprice']
        stock = request.form['stock']
        type = request.form['type']

        # run the query 
        cursor.execute('INSERT INTO Products (product_name, product_price, stock,  type) VALUES (%s, %s, %s, %s);', (name1, price, stock, type))
        result = cursor.fetchall()
        conn.commit()
    
    # if delete button is pressed, delete the provided info from the database
    elif "deletebutton" in request.form:

        # get the text entered from the website. 
        productid = request.form['deleteproduct']
        productid = (productid, )
        
        deletequery = "DELETE FROM Products WHERE product_id = %s;"

        cursor.execute(deletequery, productid)
        conn.commit()

    # render the new product added, deleted, or show all
    cursor.execute("SELECT * FROM Products;")
    result = cursor.fetchall()
    cursor.close()
    return render_template('/products.html/', rows=result)


if __name__ == "__main__":
    webapp.run(debug=True)
