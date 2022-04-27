import MySQLdb
import flask
from flask import render_template

def read_mysql_config(mysql_config_file_name: str):
    with open(mysql_config_file_name, "r") as mysql_conf:
        config_info = dict()
        for line in mysql_conf.readlines():
            if line.startswith('['): continue
            config_info.update(dict([(substr.strip() for substr in line.split('='))]))
    return config_info

# This will be different for each user.
config_info = read_mysql_config("/nfs/stak/users/chaplygy/Windows.Documents/My Documents/cs340/.my.cnf")

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
    return render_template('products.html')

@webapp.route('/cashiers/')
def cashiers():
    return render_template('cashiers.html')

if __name__ == "__main__":
    webapp.run(debug=True)