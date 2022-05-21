from flask import request
'''Functions for getting data from the inputs for CREATE and READ functionalities'''
def check_empty(userdata):
    # set empty text to null
    index = 0
    for data in userdata:
        if data == '':
            userdata[index] = None
        index += 1
    return userdata

def insert_customers():
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    email = request.form['email']
    reward_id = request.form['reward_id']
    userdata = [fname, lname, phone, email, reward_id]

    userdata = check_empty(userdata)

    if not "checknull" in request.form:
        reward_id = request.form['reward_id']
    else:
        reward_id = None
    return userdata

def update_customers():
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phone']
    email = request.form['email']
    if not "checknull" in request.form:
        reward_id = request.form['reward_id']
    else:
        reward_id = None
    updatedata = (fname, lname, phone, email, reward_id, fname, lname)
    return updatedata

def insert_cashier():
    fname = request.form['fname']
    lname = request.form['lname']
    lane = int(request.form['lane'])
    daytotal = int(request.form['daytotal'])
    dayworked = request.form['dayworked']
    userdata = [fname, lname, daytotal, dayworked, lane]
    userdata = check_empty(userdata)
    print(userdata)
    return userdata
    


def execute_query(db_conn, query=None, parameters = ()):
    cursor = db_conn.cursor() 
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    db_conn.commit()
    return results

