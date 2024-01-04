# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import hashlib

# Initialize the app from Flask
# 首先引入了Flask包，并创建一个Web应用的实例”app”
app = Flask(__name__, template_folder="templates", static_folder="templates/static")  # template location

# Configure MySQL
# 数据库对象
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='db_finals',  # db name
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# ---------------------------------------------------------------
# --------------------------------------------------------------
# Define a route to hello function
# 表示地址为“/”路径时就调用下方的函数
@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')


@app.route('/public_info', methods=['GET', 'POST'])
def public_info():
    depart_airport = request.form["depart_airport"]
    arrival_airport = request.form["arrival_airport"]
    departure = request.form["dept_date"]
    # date just be current sql date time

    cursor2 = conn.cursor()

    if len(departure) == 0:
        if len(depart_airport) == 0:
            if len(arrival_airport) == 0:
                query2 = 'SELECT * FROM flight WHERE status = "Upcoming"'
                cursor2.execute(query2)
            else:
                query2 = 'SELECT * FROM flight WHERE departure_airport = departure_airport and arrival_airport = %s and status = "Upcoming"'
                cursor2.execute(query2, (arrival_airport))
        else:
            if len(arrival_airport) == 0:
                query2 = 'SELECT * FROM flight where departure_airport = %s and status = "Upcoming"'
                cursor2.execute(query2, (depart_airport))
            else:
                query2 = 'SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and status = "Upcoming"'
                cursor2.execute(query2, (depart_airport, arrival_airport))
    else:
        if len(depart_airport) == 0:
            if len(arrival_airport) == 0:
                query2 = 'SELECT * FROM flight WHERE status = "Upcoming" and departure_time >= %s'
                cursor2.execute(query2, (departure))
            else:
                query2 = 'SELECT * FROM flight WHERE departure_airport = departure_airport and arrival_airport = %s and status = "Upcoming" and departure_time >= %s'
                cursor2.execute(query2, (arrival_airport, departure))
        else:
            if len(arrival_airport) == 0:
                query2 = 'SELECT * FROM flight where departure_airport = %s and status = "Upcoming" and departure_time >= %s'
                cursor2.execute(query2, (depart_airport, departure))
            else:
                query2 = 'SELECT * FROM flight WHERE departure_airport = %s and arrival_airport = %s and status = "Upcoming" and departure_time >= %s'
                cursor2.execute(query2, (depart_airport, arrival_airport, departure))

    data2 = cursor2.fetchall()

    cursor2.close()
    return render_template('upcoming_flight_public.html', posts=data2)


@app.route('/public_info_status', methods=['GET', 'POST'])
def public_info_status():
    # status
    flight = request.form["flight_number"]  # 对应html 文件的form class
    departure = request.form['departure_date']
    arrival = request.form['arrival_date']

    cursor1 = conn.cursor()

    if len(flight) == 0:
        if len(departure) == 0:
            if len(arrival) == 0:
                query1 = 'SELECT flight_num, status FROM flight'
                cursor1.execute(query1)
            else:
                query1 = 'SELECT flight_num, status FROM flight WHERE arrival_time >= %s'
                cursor1.execute(query1, (arrival))
        else:
            if len(arrival) == 0:
                query1 = 'SELECT flight_num, status FROM flight WHERE departure_time >= %s'
                cursor1.execute(query1, (departure))
            else:
                query1 = 'SELECT flight_num, status FROM flight WHERE departure_time >= %s and arrival_time >= %s'
                cursor1.execute(query1, (departure, arrival))
    else:
        if len(departure) == 0:
            if len(arrival) == 0:
                query1 = 'SELECT flight_num, status FROM flight WHERE flight_num = %s'
                cursor1.execute(query1, (flight))
            else:
                query1 = 'SELECT flight_num, status FROM flight WHERE flight_num = %s abd arrival_time >= %s'
                cursor1.execute(query1, (flight, arrival))
        else:
            if len(arrival) == 0:
                query1 = 'SELECT flight_num, status FROM flight WHERE flight_num = %s and departure_time >= %s'
                cursor1.execute(query1, (flight, departure))
            else:
                query1 = 'SELECT flight_num, status FROM flight WHERE flight_num = %s and departure_time > %s and arrival_time > %s'
                cursor1.execute(query1, (flight, departure, arrival))

    data1 = cursor1.fetchall()
    cursor1.close()
    return render_template('flight_status_public.html', posts=data1)


# -----------------------------------------------------------
# --------------------------------------------------------------

@app.route('/register_customer')
def register_customer():
    return render_template('register/register_customer.html')


# Authenticates the register
@app.route('/registerAuth_customer', methods=['GET', 'POST'])
def registerAuth_customer():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    building = request.form['building']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    passport = request.form['passport']
    passport_exp = request.form['passport_exp']
    passport_country = request.form['passport_country']
    birth = request.form['birth']

    # cursor used to send queries
    cursor = conn.cursor()

    # executes query
    query = 'SELECT email FROM customer WHERE email = %s'  # check for no same email
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register/register_customer.html', error=error)

    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (
            username, name, password, building, street, city, state, phone, passport, passport_exp, passport_country,
            birth))
        conn.commit()
        cursor.close()
        return render_template('index.html')


# ----------------------------------------------------------------------

@app.route('/register_agent')
def register_agent():
    return render_template('register/register_agent.html')


# Authenticates the register
@app.route('/registerAuth_agent', methods=['GET', 'POST'])
def registerAuth_agent():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    airline = request.form["airline"]

    # cursor used to send queries
    cursor = conn.cursor()

    # executes query
    query = 'SELECT email FROM booking_agent WHERE email = %s'  # check for no same email
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register/register_agent.html', error=error)

    else:
        # check if this airline exists in the db, foreign constraints
        check_airline = 'SELECT name FROM airline where %s in (select name FROM airline)'
        cursor.execute(check_airline, (airline))
        check_data = cursor.fetchall()

        if len(check_data) == 0:
            ins = 'INSERT INTO airline VALUES(%s)'
            cursor.execute(ins, (airline))

        query = 'SELECT max(booking_agent_id) as id FROM booking_agent'  # check for no same email
        cursor.execute(query)
        # stores the results in a variable
        data2 = cursor.fetchone()

        ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (username, password, str(int(data2['id'])+ 1),airline))


        conn.commit()
        cursor.close()
        return render_template('index.html')


# --------------------------------------------------------------------------

@app.route('/register_staff')
def register_staff():
    return render_template('register/register_staff.html')


# Authenticates the register
@app.route('/registerAuth_staff', methods=['GET', 'POST'])
def registerAuth_staff():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    birth = request.form['birth']
    airline = request.form['airline']

    # cursor used to send queries
    cursor = conn.cursor()

    # executes query
    query = 'SELECT username FROM airline_staff WHERE username = %s'  # check for no same email
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row

    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register/register_staff.html', error=error)

    else:
        # check if this airline exists in the db, foreign constraints
        check_airline = 'SELECT name FROM airline where %s in (select name FROM airline)'
        cursor.execute(check_airline, (airline))
        check_data = cursor.fetchall()

        if len(check_data) == 0:
            ins = 'INSERT INTO airline VALUES(%s)'
            cursor.execute(ins, (airline))

        ins = 'INSERT INTO `airline_staff` (`username`, `airline_name`, `password`, `first_name`, `last_name`, `date_of_birth`) VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, airline, password, first_name, last_name, birth))
        conn.commit()
        cursor.close()
        return render_template('index.html')


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

# Define route for login
@app.route('/log_in')
def login():
    return render_template("log_in/log_in.html")  # relative route to templates folder defined above


# Define route for register
@app.route('/register')
def register():
    return render_template('register/register.html')


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

@app.route('/log_in_customer')
def log_in_customer():
    return render_template('log_in/log_in_customer.html')


# Authenticates the login
# 既可以向外展示，也可以获取数据
@app.route('/customer_auth', methods=['GET', 'POST'])
def loginAuth_customer():
    # grabs information from the forms
    # get
    username = request.form["username"]  # 对应html 文件的form class
    password = request.form['password']

    # cursor used to send queries
    # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
    cursor = conn.cursor()

    # executes query
    query = 'SELECT * FROM customer WHERE email = %s and password = %s'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if data is not None:
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        session['username'] = username
        return redirect('/customer_home')  # a url in app.route
    else:
        # returns an error message to the html page
        error = 'Invalid username or password'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("log_in/log_in_customer.html", error=error)


@app.route('/customer_home')
def customer_home():
    return render_template('customer_page/customer_home.html', username=session['username'])


@app.route("/customer_flight_search", methods=['GET', 'POST'])
def customer_flight_search():
    return render_template('customer_page/customer_flight_search.html')


@app.route('/customer_search', methods=['GET', 'POST'])
def customer_search():
    dept_city = request.form["dept_city"]  # now required to fill in
    dept_airport = request.form["dept_airport"]
    arrival_city = request.form["arrival_city"]  # now required to fill in    type str
    arrival_airport = request.form["arrival_airport"]
    date = request.form["date"]  # now required to fill in

    # cursor used to send queries
    # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
    cursor = conn.cursor()

    # executes query

    if len(dept_airport) == 0:
        if len(arrival_airport) == 0:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = f.arrival_airport and f.departure_time > %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (date, dept_city, arrival_city))
        else:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = %s and f.departure_time > %s  and a1.airport_city = ' \
                    '%s and a2.airport_city = %s '
            cursor.execute(query, (arrival_airport, date, dept_city, arrival_city))
    else:
        query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                '%s and f.arrival_airport = %s and f.departure_time > %s  and ' \
                'a1.airport_city = %s and a2.airport_city = %s '
        cursor.execute(query, (dept_airport, arrival_airport, date, dept_city, arrival_city))

    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchall()  # list(dict())
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if len(data) > 0:
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        return render_template("customer_page/customer_search_result.html", posts=data)  # a url in app.route
    if len(data) == 0:
        # returns an error message to the html page
        error = 'no such flight'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("customer_page/customer_flight_search.html", error=error)


@app.route('/customer_display_purchased', methods=['GET', 'POST'])
def customer_display_purchased():
    username = session['username']
    cursor = conn.cursor()
    query = "SELECT t.flight_num, t.airline_name FROM ticket as t WHERE " \
            "t.customer_email = %s "
    cursor.execute(query, (username))
    data = cursor.fetchall()  # list(dict())
    cursor.close()
    if len(data) == 0:
        error = "You don't have a purchase record"
        return render_template("customer_page/customer_display_purchased.html", error=error)
    else:
        return render_template("customer_page/customer_display_purchased.html", posts=data)  # a url in app.route


@app.route('/customer_ticket_view', methods=['GET', 'POST'])
def customer_ticket_view():
    cursor = conn.cursor()

    query = 'SELECT * FROM flight WHERE status = "Upcoming"'
    cursor.execute(query)
    data = cursor.fetchall()  # list(dict())

    cursor.close()

    return render_template("customer_page/customer_purchase_ticket.html", posts=data)  # a url in app.route


@app.route("/customer_purchase_ticket", methods=['GET', 'POST'])
def customer_purchase_ticket():
    username = request.form["username"]
    flight_num = request.form["flight_num"]

    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE status = "Upcoming"'
    cursor.execute(query)
    data = cursor.fetchall()  # list(dict())


    query_check = "select email from customer"
    cursor.execute(query_check)
    check = cursor.fetchall()
    # print(check)
    # print(type(check[0]))

    check2 = []
    for item in check:
        check2.append(item["email"])
    if username not in check2:
        error = "Sorry, you are booking ticket for someone not registered !"
        return render_template("customer_page/customer_purchase_ticket.html", posts=data, error=error)

    query_check2 = "select flight_num from flight"
    cursor.execute(query_check2)
    check_f = cursor.fetchall()
    check3 = []
    for item in check_f:
        check3.append(item["flight_num"])
    if flight_num not in check3:
        error = "Sorry, you input a wrong flight number !"
        return render_template("customer_page/customer_purchase_ticket.html", posts=data, error=error)


    # check seat availability
    query1 = "select count(ticket_id) as c from ticket where flight_num = %s"
    cursor.execute(query1, (flight_num))
    current_occupied = cursor.fetchall()  # list(dict())

    query2 = "select seats from flight as f, airplane as a where a.airplane_id = f.airplane_id and flight_num = %s"
    cursor.execute(query2, (flight_num))
    available = cursor.fetchall()  # list(dict())

    if current_occupied[0]["c"] < available[0]["seats"]:
        query3 = "select max(ticket_id) as next_id from ticket"
        cursor.execute(query3)
        ticket_id = cursor.fetchall()
        ticket_id = ticket_id[0]["next_id"]

        query_n = "select distinct airline_name from flight where flight_num = %s"
        cursor.execute(query_n, (flight_num))
        airline = cursor.fetchall()

        ins2 = 'INSERT INTO ticket VALUES(%s, %s , %s,NULL, %s)'
        cursor.execute(ins2, (ticket_id + 1, airline[0]["airline_name"], flight_num,  username))

        
        conn.commit()
        cursor.close()
        return render_template('customer_page/customer_purchase_successful.html')
    else:
        error = "Sorry, there is no vacant seat on this flight !"
        return render_template('customer_page/customer_purchase_ticket.html', posts=data, error=error)


@app.route('/customer_track', methods=['GET', 'POST'])
def customer_track():
    data3 = None
    return render_template("customer_page/customer_track_my_spending.html", data3=data3)


@app.route("/customer_track_my_spending", methods=['GET', 'POST'])
def customer_track_spending():
    username = session["username"]
    start = request.form["start_date"]
    end = request.form['end_date']

    cursor = conn.cursor()

    query1 = "SELECT SUM(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE() AND customer_email = %s "
    cursor.execute(query1, (username))
    sum_past_year = cursor.fetchone()

    query2 = "SELECT SUM(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN %s " \
             "AND %s AND customer_email = %s "
    cursor = conn.cursor()
    cursor.execute(query2, (start, end, username))
    sum_period = cursor.fetchone()

    query3 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() AND customer_email = %s "
    query4 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 2 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND customer_email = %s "
    query5 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 2 MONTH) AND customer_email = %s "
    query6 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 4 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 3 MONTH) AND customer_email = %s "
    query7 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 5 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 4 MONTH) AND customer_email = %s "
    query8 = "SELECT sum(price) as total FROM flight NATURAL JOIN ticket WHERE departure_time BETWEEN " \
             "DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND DATE_SUB(CURDATE(), INTERVAL 5 MONTH) AND customer_email = %s "

    cursor = conn.cursor()
    cursor.execute(query3, (username))
    sum_1_month = cursor.fetchone()
    cursor.execute(query4, (username))
    sum_2_month = cursor.fetchone()
    cursor.execute(query5, (username))
    sum_3_month = cursor.fetchone()
    cursor.execute(query6, (username))
    sum_4_month = cursor.fetchone()
    cursor.execute(query7, (username))
    sum_5_month = cursor.fetchone()
    cursor.execute(query8, (username))
    sum_6_month = cursor.fetchone()

    data_temp = [sum_1_month["total"], sum_2_month["total"], sum_3_month["total"], sum_4_month["total"],
             sum_5_month["total"], sum_6_month["total"]]
    data3 = []
    for item in data_temp:
        if item is None:
            item = 0
            data3.append(item)
        else:
            data3.append(int(item))

    return render_template("customer_page/customer_track_my_spending.html", data1=sum_past_year, data2=sum_period,
                           data3=data3)


# -----------------------------------------------------------
# ------------------------------------------------------------


@app.route('/log_in_agent')
def log_in_agent():
    return render_template('log_in/log_in_agent.html')


# Authenticates the login
# 既可以向外展示，也可以获取数据
@app.route('/agent_auth', methods=['GET', 'POST'])
def loginAuth_agent():
    # grabs information from the forms
    # get
    username = request.form["username"]  # 对应html 文件的form class
    password = request.form['password']

    # cursor used to send queries
    # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
    cursor = conn.cursor()

    # executes query
    # query = 'SELECT * FROM booking_agent_work_for as a, booking_agent as b WHERE a.email = b.email ' \
    #         'and b.email = %s and b.password = MD5(%s) '
    query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s '
    # and a.airline_name = "Jet Blue"
    cursor.execute(query, (username, password))
    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    # if data is not none
    if (data):
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        session['username'] = username
        return redirect('/agent_home')  # a url in app.route
    else:
        # returns an error message to the html page
        error = 'Invalid username or password'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("log_in/log_in_agent.html", error=error)


@app.route('/agent_home')
def agent_home():
    return render_template('agent_page/agent_home.html', username=session['username'])


@app.route("/agent_flight_search", methods=['GET', 'POST'])
def agent_flight_search():
    return render_template('agent_page/agent_flight_search.html')


@app.route('/agent_search', methods=['GET', 'POST'])
def agent_search():
    dept_city = request.form["dept_city"]  # now required to fill in
    dept_airport = request.form["dept_airport"]
    arrival_city = request.form["arrival_city"]  # now required to fill in    type str
    arrival_airport = request.form["arrival_airport"]
    date = request.form["date"]  # now required to fill in

    cursor = conn.cursor()

    # executes query


    if len(dept_airport) == 0:
        if len(arrival_airport) == 0:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = f.arrival_airport and f.departure_time >= %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (date, dept_city, arrival_city))
        else:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    'f.departure_airport and f.arrival_airport = %s and f.departure_time >= %s  and a1.airport_city = ' \
                    '%s and a2.airport_city = %s '
            cursor.execute(query, (arrival_airport, date, dept_city, arrival_city))
    else:
        if len(arrival_airport) == 0:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    '%s and f.arrival_airport = f.arrival_airport and f.departure_time > %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (dept_airport, date, dept_city, arrival_city))
        else:
            query = 'SELECT * FROM flight as f, airport as a1, airport as a2 WHERE a1.airport_name = ' \
                    'f.departure_airport and a2.airport_name = f.arrival_airport and f.departure_airport = ' \
                    '%s and f.arrival_airport = %s and f.departure_time > %s  and ' \
                    'a1.airport_city = %s and a2.airport_city = %s '
            cursor.execute(query, (dept_airport, arrival_airport, date, dept_city, arrival_city))

    data = cursor.fetchall()  # list(dict())
    cursor.close()
    error = None
    if len(data) > 0:
        return render_template("agent_page/agent_search_result.html", posts=data)  # a url in app.route
    if len(data) == 0:
        error = 'no such flight'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("agent_page/agent_flight_search.html", error=error)


@app.route('/agent_display_purchased', methods=['GET', 'POST'])
def agent_display_purchased():
    agent_email = session['username']
    cursor = conn.cursor()

    query5 = "select booking_agent_id as id from booking_agent where email = %s"
    cursor.execute(query5, (agent_email))
    agent_id = cursor.fetchall()
    agent_id = agent_id[0]["id"]

    query = """
    SELECT t.ticket_id, f.Airline_name, f.flight_num, f.departure_airport, f.departure_time, 
    f.arrival_airport, f.arrival_time, f.price, f.status, f.Airplane_id 
FROM ticket AS t
JOIN flight AS f ON t.flight_num = f.flight_num
WHERE t.agent_email = %s
ORDER BY f.departure_time ASC
"""
    cursor.execute(query, (agent_email))
    data = cursor.fetchall()  # list(dict())
    cursor.close()

    if len(data) == 0:
        error = "You don't have a purchase record"
        return render_template("agent_page/agent_display_purchased.html", error=error)
    else:
        return render_template("agent_page/agent_display_purchased.html", posts=data)  # a url in app.route


@app.route('/agent_ticket_view', methods=['GET', 'POST'])
def agent_ticket_view():
    cursor = conn.cursor()
    username = session["username"]

    query0 = 'SELECT airline_name from booking_agent where email = %s'
    cursor.execute(query0, (username))
    airline = cursor.fetchall()  # list(dict())

    query = 'SELECT * FROM flight WHERE airline_name = %s and status = "Upcoming"'
    cursor.execute(query, (airline[0]["airline_name"]))
    data = cursor.fetchall()  # list(dict())

    cursor.close()

    if len(data) == 0:
        error2 = "Sorry, the airline you work for has no flight for you to purchase !"
        return render_template("agent_page/agent_purchase_ticket.html", posts=data, error2=error2, error=error2)  # a url in app.route
    else:
        return render_template("agent_page/agent_purchase_ticket.html", posts=data)

@app.route("/agent_purchase_ticket", methods=['GET', 'POST'])
def agent_purchase_ticket():
    agent_email = session["username"]
    username = request.form["username"]
    flight_num = request.form["flight_num"]

    cursor = conn.cursor()

    # check his airline
    query0 = 'SELECT airline_name from booking_agent where email = %s'
    cursor.execute(query0, (agent_email))
    airline = cursor.fetchall()  # list(dict())
    if (airline):


        query = 'SELECT * FROM flight WHERE airline_name = %s and status = "Upcoming"'
        cursor.execute(query, (airline[0]["airline_name"]))
        data = cursor.fetchall()  # list(dict())


        query_check = "select email from customer"
        cursor.execute(query_check)
        check = cursor.fetchall()
        check2 = []
        for item in check:
            check2.append(item["email"])
        if username not in check2:
            error = "Sorry, you are booking ticket for someone not registered !"
            return render_template("agent_page/agent_purchase_ticket.html", posts=data, error=error)

        query_check2 = "select flight_num from flight"
        cursor.execute(query_check2)
        check_f = cursor.fetchall()
        check3 = []
        for item in check_f:
            check3.append(item["flight_num"])
        if flight_num not in check3:
            error = "Sorry, you input a wrong flight number !"
            return render_template("agent_page/agent_purchase_ticket.html", posts=data, error=error)

        # check seat availability
        query1 = "select count(ticket_id) as c from ticket where flight_num = %s"
        cursor.execute(query1, (flight_num))
        current_occupied = cursor.fetchall()  # list(dict())

        query2 = "select seats from flight as f, airplane as a where a.airplane_id = f.airplane_id and flight_num = %s"
        cursor.execute(query2, (flight_num))
        available = cursor.fetchall()  # list(dict())

        if current_occupied[0]["c"] < available[0]["seats"]:
            query3 = "select max(ticket_id) as next_id from ticket"
            cursor.execute(query3)
            ticket_id = cursor.fetchall()
            ticket_id = ticket_id[0]["next_id"]

            query_n = "select distinct airline_name from flight where flight_num = %s"
            cursor.execute(query_n, (flight_num))
            airline = cursor.fetchall()
            query5 = "select booking_agent_id as id from booking_agent where email = %s"
            agent_email = session["username"]
            cursor.execute(query5, (agent_email))
            agent_id = cursor.fetchall()
            agent_id = agent_id[0]["id"]

            ins2 = 'INSERT INTO  ticket VALUES(%s, %s , %s, %s, %s)'
            cursor.execute(ins2, (ticket_id + 1, airline[0]["airline_name"], flight_num, agent_email, username))

            
            conn.commit()
            cursor.close()
            return render_template('agent_page/agent_purchase_successful.html')
        else:
            error = "Sorry, there is no vacant seat on this flight !"
            return render_template('agent_page/agent_purchase_ticket.html', posts=data, error=error)

    else:
        error2 = "Sorry, the airline you work for has no flight for you to purchase !"
        return render_template('agent_page/agent_error.html', error2=error2, error=error2)


@app.route('/agent_commission', methods=['GET', 'POST'])
def agent_commission():
    agent_email = session["username"]
    cursor = conn.cursor()

    query5 = "select booking_agent_id as id from booking_agent where email = %s"
    cursor.execute(query5, (agent_email))
    agent_id = cursor.fetchall()
    agent_id = agent_id[0]["id"]

    query_money = '''
SELECT price 
FROM flight 
NATURAL JOIN ticket 
NATURAL JOIN booking_agent 
WHERE booking_agent.email = %s 
AND flight.departure_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
'''
    cursor.execute(query_money, (agent_email))
    commission = cursor.fetchall()
    total_commission = 0
    for item in commission:
        total_commission += int(item["price"])
    avg_commission = str(int(total_commission / 30))
    total_commission = str(int(total_commission))

    query_count = '''
SELECT count(ticket_id) as c 
FROM flight 
NATURAL JOIN ticket 
NATURAL JOIN booking_agent 
WHERE booking_agent.email = %s 
AND flight.departure_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
'''
    cursor.execute(query_count, (agent_email))
    ticket = cursor.fetchall()  # list(dict())
    ticket_num = ticket[0]["c"]

    cursor.close()

    return render_template("agent_page/agent_view_commission.html", commission=total_commission, num_ticket=ticket_num,
                           average_commission=avg_commission)


@app.route('/agent_customize_commission', methods=['GET', 'POST'])
def agent_customize_commission():
    agent_email = session["username"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]

    cursor = conn.cursor()

    query5 = "select booking_agent_id as id from booking_agent where email = %s"
    cursor.execute(query5, (agent_email))
    agent_id = cursor.fetchall()
    agent_id = agent_id[0]["id"]

    

    query_count = 'SELECT count(ticket_id) as c FROM flight NATURAL JOIN ticket NATURAL JOIN booking_agent WHERE ' \
                  'booking_agent_id = %s AND flight.departure_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() '
    cursor.execute(query_count, (agent_id))
    ticket = cursor.fetchall()  # list(dict())
    ticket_num = ticket[0]["c"]
    
    
    
    query_money = 'SELECT price FROM flight NATURAL JOIN ticket NATURAL JOIN booking_agent WHERE ' \
                  'booking_agent_id = %s AND flight.departure_time BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE() '
    cursor.execute(query_money, (agent_id))
    commission = cursor.fetchall()
    total_commission = 0
    for item in commission:
        total_commission += int(item["price"]) * (15/100)
    # Calculate average commission
    if ticket_num > 0:
        avg_commission = str(int(total_commission / ticket_num))
    else:
        avg_commission = '0'  # or any default value you prefer
    total_commission = str(int(total_commission))



    query_count_2 = 'SELECT count(ticket_id) as c FROM flight NATURAL JOIN ticket NATURAL JOIN booking_agent WHERE ' \
                    'booking_agent_id = %s AND flight.departure_time BETWEEN %s AND %s '
    cursor.execute(query_count_2, (agent_id, start_date, end_date))
    ticket_c = cursor.fetchall()  # list(dict())
    ticket_num_c = ticket_c[0]["c"]
    
    
    
    query_money_2 = 'SELECT price FROM flight NATURAL JOIN ticket NATURAL JOIN booking_agent WHERE ' \
                    'booking_agent_id = %s AND flight.departure_time BETWEEN %s AND %s '
    cursor.execute(query_money_2, (agent_id, start_date, end_date))
    commission_c = cursor.fetchall()
    total_commission_c = 0
    for item in commission_c:
        total_commission_c += int(item["price"]) * (15/100)
    # Calculate average commission for custom date range
    if ticket_num_c > 0:
        avg_commission_c = str(int(total_commission_c / ticket_num_c))
    else:
        avg_commission_c = '0'  # or any default value you prefer
    total_commission_c = str(int(total_commission_c))

    cursor.close()
    return render_template("agent_page/agent_view_commission.html", commission=total_commission, num_ticket=ticket_num,
                           average_commission=avg_commission, commission_c=total_commission_c,
                           num_ticket_c=ticket_num_c,
                           average_commission_c=avg_commission_c)


@app.route('/agent_top_customer', methods=['GET', 'POST'])
def agent_top_customer():
    agent_email = session["username"]
    cursor = conn.cursor()

    query5 = "select booking_agent_id as id from booking_agent where email = %s"
    cursor.execute(query5, (agent_email))
    agent_id = cursor.fetchall()
    agent_id = agent_id[0]["id"]

    query_money = 'SELECT sum(price) as cp, customer_email FROM flight NATURAL JOIN ticket NATURAL JOIN ' \
                  'booking_agent WHERE ' \
                  'booking_agent_id = %s and flight.departure_time between DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND ' \
                  'CURDATE() group by customer_email '
    cursor.execute(query_money, (agent_id))
    data = cursor.fetchall()

    commission = []
    customer1 = []

    for item in data:
        commission.append(int(item["cp"]))
        customer1.append(item["customer_email"])


    if len(commission) > 5:
        max_index = []
        commission2 = commission.copy()
        for i in range(5):
            maxi = max(commission2)
            index = commission2.index(maxi)
            max_index.append(index)
            commission2.pop(index)
        commission2 = []
        customer2 = []
        max_index = max_index[::-1]
        for i in range(5):
            commission2.append(commission[max_index[i]])
            customer2.append(customer1[max_index[i]])
        commission = commission2
        customer1 = customer2


    data_price = []
    for i in range(len(customer1)):
        temp = []
        temp.append(customer1[i])
        temp.append(commission[i])
        data_price.append(temp)
    while len(data_price)<5:
        data_price.append(["None", 0])


    query_count = 'SELECT count(ticket_id) as ct, customer_email as c FROM flight NATURAL JOIN ticket NATURAL JOIN booking_agent WHERE ' \
                  'booking_agent_id = %s group by customer_email'
    cursor.execute(query_count, (agent_id))
    data = cursor.fetchall()  # list(dict())

    ticket = []
    customer2 = []

    for item in data:
        ticket.append(int(item["ct"]))
        customer2.append(item["c"])

    if len(ticket) > 5:
        max_index = []
        commission3 = ticket.copy()
        for i in range(5):
            maxi = max(commission3)
            index = commission3.index(maxi)
            max_index.append(index)
            commission3.pop(index)
        ticket5 = []
        customer5 = []
        max_index = max_index[::-1]
        for i in range(5):
            ticket5.append(ticket[max_index[i]])
            customer5.append(customer2[max_index[i]])
        ticket = ticket5
        customer2 = customer5

    data_num = []
    for i in range(len(customer2)):
        temp = []
        temp.append(str(customer2[i]))
        temp.append(int(ticket[i]))
        data_num.append(temp)
    while len(data_num)<5:
        data_num.append(["None", 0])

    cursor.close()


    return render_template("agent_page/agent_top_customer.html", data1=data_price, data2=data_num)


# --------------------------------------------------------------------
# ---------------------------------------------------------------------


@app.route('/log_in_staff')
def log_in_staff():
    return render_template('log_in/log_in_staff.html')



# Authenticates the login
# 既可以向外展示，也可以获取数据
@app.route('/staff_auth', methods=['GET', 'POST'])
def loginAuth_staff():
    # grabs information from the forms
    # get
    username = request.form["username"]  # 对应html 文件的form class
    password = request.form['password']
    ack = request.form['ack']

    # cursor used to send queries
    # 游标（Cursor）是处理数据的一种方法，为了查看或者处理结果集中的数据，游标提供了在结果集中一次一行或者多行前进或向后浏览数据的能力。可以把游标当作一个指针，它可以指定结果中的任何位置，然后允许用户对指定位置的数据进行处理
    cursor = conn.cursor()

    # executes query
    query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    # stores the results in a variable
    # fetchone 即每次只读一行
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()

    error = None
    # if data is not none
    if data is not None and ack == "airline_staff":
        # creates a session for the the user
        # 创造一个会话
        # session is a built in
        session['username'] = username

        cursor = conn.cursor()
        query = 'SELECT permission_type FROM permission WHERE username = %s'
        cursor.execute(query, (username))
        permission_type = cursor.fetchall()
        cursor.close()
        print(permission_type)
        if len(permission_type) == 2:
            session['permission_type'] = tuple(['Admin', 'Operator'])
        elif permission_type == tuple():
            session['permission_type'] = tuple(['Common'])
        elif permission_type[0]['permission_type'] == 'Admin':
            session['permission_type'] = tuple(['Admin'])
        elif permission_type[0]['permission_type'] == 'Operator':
            session['permission_type'] = tuple(['Opreator'])

        cursor = conn.cursor()
        query = "select DISTINCT airline_name from airline_staff where username = %s"
        cursor.execute(query, (username))
        airline = cursor.fetchone()
        cursor.close()
        session['airline'] = airline

        return redirect('/staff_home')  # a url in app.route

    else:
        # returns an error message to the html page
        error = 'Invalid username or password or identity!'
        # 用于返回静态页面，同时可以实现参数传递，render_template函数会自动在templates文件夹中找到对应的html，因此我们不用写完整的html文件路径
        return render_template("log_in/log_in_staff.html", error=error)



@app.route('/staff_home')
def staff_home():
    return render_template('staff_page/staff_home.html')



@app.route('/staff_add_airport')
def staff_add_airport():

    permission_type = session['permission_type']

    if "Admin" not in permission_type:
        flash("Sorry! You don't have admin permission!")
        return render_template('staff_page/staff_home.html')    
    
    return render_template('staff_page/staff_add_airport.html')



@app.route('/staff_add_airport_form', methods=['GET', 'POST'])
def staff_add_airport_form():
  

    airport_name = request.form['airport_name']
    airport_city = request.form['airport_city']
    
    try:
        cursor = conn.cursor()
        query = "insert into airport VALUES(%s, %s)"
        cursor.execute(query, (airport_name, airport_city))
        conn.commit()
        cursor.close()

        flash('You have successfully add an airport!')
        return render_template('staff_page/staff_add_airport.html')

    except:
        flash('Failed! The airport already exists!')
        return render_template('staff_page/staff_add_airport.html')



@app.route('/staff_add_airplane')
def staff_add_airplane():
    
    permission_type = session['permission_type']
    airline = session['airline']

    if "Admin" not in permission_type:
        flash("Sorry! You don't have admin permission!")
        return render_template('staff_page/staff_home.html')

    return render_template('staff_page/staff_add_airplane.html', airline = airline)




@app.route('/staff_add_airplane_form', methods=['GET', 'POST'])
def staff_add_airplane_form():
    cursor = conn.cursor()
    # Fetch the list of airlines
    cursor.execute("SELECT name FROM airline")  # Replace 'airline_table' with your actual table name
    airlines = cursor.fetchall()
    print(airlines) 
    cursor.close()
    
    if request.method == 'POST':
        try:
            airline = request.form['airline']
            airplane_id = request.form['airplane_id']
            seats = request.form['seats']

            # Insert airplane data
            cursor = conn.cursor()
            query = "insert into airplane VALUES(%s, %s, %s)"
            cursor.execute(query, (airplane_id, airline, seats))
            conn.commit()

            # Fetch airplanes for the selected airline
            query = "select airplane_id from airplane where airline_name = %s"
            cursor.execute(query, (airline,))
            airplanes = cursor.fetchall()
            cursor.close()

            flash('You have successfully added an airplane!')
            return render_template('staff_page/staff_add_airplane.html', airlines=airlines, airline=session['airline'], airplanes = airplanes)
        except Exception as e:
            flash('Failed! Invalid input or the airplane already exists!')
            print(e)  # For debugging
            return render_template('staff_page/staff_add_airplane.html', airlines=airlines, airline=session['airline'], airplanes = airplanes)


      

@app.route('/staff_create_flight')
def staff_create_flight():
    username = session['username']
    permission_type = session['permission_type']
    airline = session['airline']

    cursor = conn.cursor()

    query = "select airline_name from airline_staff where username = %s"
    cursor.execute(query, (username))
    airline = cursor.fetchone()
    
    query = "select DISTINCT airport_name from airport"
    cursor.execute(query)
    arrival_airport = cursor.fetchall()

    departure_airport = arrival_airport

    cursor.close()

    if "Admin" not in permission_type:
        flash("Sorry! You don't have admin permission!")
        return render_template('staff_page/staff_home.html')

    return render_template('staff_page/staff_create_flight.html',  airline = airline,
                                                                   arrival_airport = arrival_airport,
                                                                   departure_airport = departure_airport)
     



@app.route('/staff_create_flight_form', methods=['GET', 'POST'])
def staff_create_flight_form():

    cursor = conn.cursor()
    query = "select DISTINCT airport_name from airport"
    cursor.execute(query)
    arrival_airport_1 = cursor.fetchall()
    departure_airport_1 = arrival_airport_1
    airline_1 = session['airline']
    
    try:
        airline = request.form['airline']
        flight_num = request.form['flight_num']
        departure_airport = request.form['departure_airport']
        departure_time = request.form['departure_time']
        arrival_airport = request.form['arrival_airport']
        arrival_time = request.form['arrival_time']
        price = request.form['price']
        status = request.form['status']
        airplane_id = request.form['airplane_id']
        
        cursor = conn.cursor()
        inserting = "insert into flight (`Airline_name`, `flight_num`, `departure_time`, `arrival_time`, `price`, `status`, `departure_airport`, `arrival_airport`, `Airplane_id`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(inserting, (airline, flight_num, departure_time, arrival_time, price, status, departure_airport, arrival_airport, airplane_id))
        conn.commit()
        cursor.close()
        flash('You have successfully create a flight!')
        return render_template('staff_page/staff_create_flight.html', airline = airline_1,
                                                                      arrival_airport = arrival_airport_1,
                                                                      departure_airport = departure_airport_1)
    except:
        flash('Failed! Invalid input or the flight already exists!')
        return render_template('staff_page/staff_create_flight.html', airline = airline_1,
                                                                      arrival_airport = arrival_airport_1,
                                                                      departure_airport = departure_airport_1)
   




@app.route('/staff_change_status', methods=['GET', 'POST'])
def staff_change_status():
    username = session['username']
    permission_type = session['permission_type']
    airline = session['airline']
    
    cursor = conn.cursor()
    query = "select DISTINCT airline_name from airline_staff where username = %s"
    cursor.execute(query, (username))
    airline = cursor.fetchone()

    query = "select DISTINCT flight_num from flight where airline_name = %s"
    cursor.execute(query, (airline['airline_name']))
    flight_num = cursor.fetchall()
    cursor.close()

    if "Operator" not in permission_type:
        flash("Sorry! You don't have operator permission!")
        return render_template('staff_page/staff_home.html')

    return render_template('staff_page/staff_change_status.html',  airline = airline,
                                                                   flight_num = flight_num)
     
   


@app.route('/staff_change_status_form', methods=['GET', 'POST'])
def staff_change_status_form():

    airline_1 = session['airline']

    cursor = conn.cursor()
    query = "select DISTINCT flight_num from flight where airline_name = %s"
    cursor.execute(query, (airline_1['airline_name']))
    flight_num_1 = cursor.fetchall()
    cursor.close()

    flight_num = request.form['flight_num']
    airline = request.form['airline']
    status = request.form['status']

    cursor = conn.cursor()
    query = "update flight set status = %s where flight.airline_name = %s and flight.flight_num = %s"
    cursor.execute(query, (status, airline, flight_num))
    conn.commit()
    cursor.close()

    flash('You have successfully changed status!')
    return render_template('staff_page/staff_change_status.html',  airline = airline_1,
                                                                   flight_num=flight_num_1)



@app.route('/staff_add_agent', methods=['GET', 'POST'])
def staff_add_agent():
    
    permission_type = session['permission_type']
    airline = session['airline']

    if "Admin" not in permission_type:
        flash("Sorry! You don't have admin permission!")
        return render_template('staff_page/staff_home.html')

    return render_template('staff_page/staff_add_agent.html',  airline = airline)
                                                                 
                                                            


@app.route('/staff_add_agent_form', methods=['GET', 'POST'])
def staff_add_agent_form():
    
    airline_1 = session['airline']

    try:
        agent_id = request.form['agent_id']
        agent_email_address = request.form['agent_email_address']
        agent_password = request.form['agent_password']
        airline = request.form['airline']

        cursor = conn.cursor()
        query = "insert into booking_agent (`email`, `password`, `booking_agent_id`, `airline_name`) values (%s, %s, %s, %s)"
        cursor.execute(query, (agent_email_address, agent_password, agent_id, airline))
        conn.commit()
    
        cursor.close()
        flash('You have successfully add an agent!')
        return render_template('staff_page/staff_add_agent.html',  airline = airline_1)
    except Exception as e:
        flash(f'Failed! {str(e)}')
        return render_template('staff_page/staff_add_agent.html', airline = airline_1)





@app.route('/staff_grant_new_permission', methods=['GET', 'POST'])
def staff_grant_new_permission():
    username = session['username']
    permission_type = session['permission_type']
    airline = session['airline']

    cursor = conn.cursor()
    query = "select DISTINCT airline_name from airline_staff where username = %s"
    cursor.execute(query, (username))
    airline = cursor.fetchone()    
    cursor.close()

    if "Admin" not in permission_type:
        flash("Sorry! You don't have admin permission!")
        return render_template('staff_page/staff_home.html')
    
    return render_template('staff_page/staff_grant_new_permission.html', airline = airline)



@app.route('/staff_grant_new_permission_form', methods=['GET', 'POST'])
def staff_grant_new_permission_form():

    permission_type = session['permission_type']
    airline_1 = session['airline']
    
    try:
        permission_type = request.form['permission_type']
        staff_username = request.form['staff_username']

        cursor = conn.cursor()
        query = "insert into permission values (%s, %s)"
        cursor.execute(query, (staff_username, permission_type))
        conn.commit()
        cursor.close()
        flash('You have successfully grant a new permission!')
        return render_template('staff_page/staff_grant_new_permission.html', airline = airline_1)
    except:
        flash('Failed! Invalid input or the permission already exists on this person!')
        return render_template('staff_page/staff_grant_new_permission.html', airline = airline_1)




@app.route('/staff_view_top_agent')
def staff_view_top_agent():

    query = "select b.email, b.booking_agent_id, count(DISTINCT t.ticket_id) " \
        "from ticket as t, booking_agent as b, flight as f " \
        "where b.email = t.agent_email AND f.flight_num = t.flight_num " \
        "and f.departure_time >= adddate(date(now()), interval -1 month) " \
        "group by b.email, b.booking_agent_id " \
        "order by count(t.ticket_id) desc"
    cursor = conn.cursor()
    cursor.execute(query)
    agent_ticket_month = []
    agent_ticket_month_temp = cursor.fetchall()
    if len(agent_ticket_month_temp) >= 5:
        for i in range(0, 5):
            agent_ticket_month.append(agent_ticket_month_temp[i])
    else:
        for i in range(0, len(agent_ticket_month_temp)):
            agent_ticket_month.append(agent_ticket_month_temp[i])
    cursor.close()

    query = "SELECT b.email, b.booking_agent_id, COUNT(DISTINCT t.ticket_id) " \
        "FROM ticket t " \
        "JOIN booking_agent b ON b.email = t.agent_email " \
        "JOIN flight f ON f.flight_num = t.flight_num " \
        "WHERE f.departure_time >= ADDDATE(CURDATE(), INTERVAL -1 YEAR) " \
        "GROUP BY b.email, b.booking_agent_id " \
        "ORDER BY COUNT(t.ticket_id) DESC"
    cursor = conn.cursor()
    cursor.execute(query)
    agent_ticket_year = []
    agent_ticket_year_temp = cursor.fetchall()
    if len(agent_ticket_year_temp) >= 5:
        for i in range(0, 5):
            agent_ticket_year.append(agent_ticket_year_temp[i])
    else:
        for i in range(0, len(agent_ticket_year_temp)):
            agent_ticket_year.append(agent_ticket_year_temp[i])
    cursor.close()
    
    query = "SELECT b.email, b.booking_agent_id, SUM(f.price) * 0.1 AS commission " \
        "FROM flight f " \
        "JOIN ticket t ON f.flight_num = t.flight_num " \
        "JOIN booking_agent b ON t.agent_email = b.email " \
        "WHERE f.departure_time >= ADDDATE(CURDATE(), INTERVAL -1 YEAR) " \
        "GROUP BY b.email, b.booking_agent_id " \
        "ORDER BY commission DESC"
    cursor = conn.cursor()
    cursor.execute(query)
    agent_commission = []
    agent_commission_temp = cursor.fetchall()
    if len(agent_commission_temp) >= 5:
        for i in range(0, 5):
            agent_commission.append(agent_commission_temp[i])
    else:
        for i in range(0, len(agent_commission_temp)):
            agent_commission.append(agent_commission_temp[i])
    cursor.close()

    return render_template('/staff_page/staff_view_top_agent.html', agent_ticket_month = agent_ticket_month,
                                                                    agent_ticket_year = agent_ticket_year,
                                                                    agent_commission = agent_commission)




@app.route('/staff_view_most_freq_customer')
def staff_view_freq_customer():
    try:
        username = session['username']
        cursor = conn.cursor()

        # Fetch the airline name associated with the staff
        query = "SELECT airline_name FROM airline_staff WHERE username = %s"
        cursor.execute(query, (username,))
        airline = cursor.fetchone()

        # Fetch the most frequent customer for that airline
        query = ("""
        SELECT ticket.customer_email, customer.name 
    FROM ticket JOIN flight ON flight.flight_num = ticket.flight_num 
    JOIN customer ON customer.email = ticket.customer_email 
    WHERE flight.airline_name = %s
    GROUP BY ticket.customer_email
    ORDER by COUNT(ticket.ticket_id) DESC
    LIMIT 5"""
    )

        cursor.execute(query, (airline["airline_name"],))
        most_freq_customer = cursor.fetchall()

        cursor.close()
        return render_template('/staff_page/staff_view_most_freq_customer.html', most_freq_customer=most_freq_customer)
    except Exception as e:
        # Handle your error/exception here; you might want to log it or send it to an error page
        print("An error occurred:", e)
        return render_template('error_page.html')  # Assuming you have an error_page template





@app.route('/staff_view_all_flights_of_customer_init', methods=['GET', 'POST'])
def staff_view_all_flights_of_customer_init():
    
    return render_template('/staff_page/staff_view_all_flights_of_customer_init.html')


@app.route('/staff_view_all_flights_of_customer_form', methods=['GET', 'POST'])
def staff_view_all_flights_of_customer_form():
    
    email = request.form['email']
    session['email_view_flights'] = email
    return redirect(url_for('staff_view_all_flights_of_customer'))
                                                            

@app.route('/staff_view_all_flights_of_customer', methods=['GET', 'POST'])
def staff_view_all_flights_of_customer():

        
        username = session['username']

        cursor = conn.cursor()
        query = "select airline_name from airline_staff where username = %s"
        cursor.execute(query, (username))
        airline = cursor.fetchone()
        cursor.close()

        email = session['email_view_flights']
        cursor = conn.cursor()
    
        query = "select * " \
                "from flight as f, ticket as t " \
                "where t.customer_email = %s " \
                "and f.airline_name = %s " \
                "and t.flight_num = f.flight_num " 
               
        cursor.execute(query, (email, airline['airline_name']))
        flight = cursor.fetchall()
        cursor.close()

        if flight != tuple():
            return render_template('/staff_page/staff_view_all_flights_of_customer.html', airline = airline,
                                                                                            flight = flight)
        else:
            flash('This customer did not buy any of flights in your airline or this customer do not exist')
            return render_template('/staff_page/staff_view_all_flights_of_customer.html', airline = airline,
                                                                                        flight = flight)



@app.route('/staff_view_Top_destinations', methods=['GET', 'POST'])
def staff_view_Top_destinations():

        username = session['username']
        
        cursor = conn.cursor()
        query = "select airline_name from airline_staff where username = %s"
        cursor.execute(query, (username))
        airline = cursor.fetchone()
        cursor.close()

        query = "SELECT f.arrival_airport " \
        "FROM flight f " \
        "JOIN ticket t ON t.flight_num = f.flight_num " \
        "JOIN airport a ON a.airport_name = f.arrival_airport " \
        "WHERE t.airline_name = f.airline_name " \
        "AND f.airline_name = %s " \
        "AND f.arrival_time BETWEEN ADDDATE(NOW(), INTERVAL -3 MONTH) AND NOW() " \
        "GROUP BY f.arrival_airport " \
        "ORDER BY COUNT(t.customer_email) DESC"
        
        cursor = conn.cursor()
        cursor.execute(query, (airline['airline_name']))
        top_dest_month = []
        top_dest_month_temp = cursor.fetchall()
        if len(top_dest_month_temp) >= 3:
            for i in range(0, 3):
                top_dest_month.append(top_dest_month_temp[i])
        else:
            for i in range(0, len(top_dest_month_temp)):
                top_dest_month.append(top_dest_month_temp[i])
        cursor.close()

        
        query = "SELECT f.arrival_airport " \
        "FROM flight f " \
        "JOIN ticket t ON t.flight_num = f.flight_num " \
        "JOIN airport a ON a.airport_name = f.arrival_airport " \
        "WHERE t.airline_name = f.airline_name " \
        "AND f.airline_name = %s " \
        "AND f.arrival_time BETWEEN ADDDATE(NOW(), INTERVAL -12 MONTH) AND NOW() " \
        "GROUP BY f.arrival_airport " \
        "ORDER BY COUNT(t.customer_email) DESC"

        cursor = conn.cursor()
        cursor.execute(query, (airline['airline_name']))
        top_dest_year = []
        top_dest_year_temp = cursor.fetchall()
        if len(top_dest_year_temp) >= 3:
            for i in range(0, 3):
                top_dest_year.append(top_dest_year_temp[i])
        else:
            for i in range(0, len( top_dest_year_temp)):
                top_dest_year.append(top_dest_year_temp[i])
        cursor.close()
        
        return render_template('/staff_page/staff_view_Top_destinations.html', destination_month= top_dest_month,  destination_year= top_dest_year)
                                                                             
        


@app.route('/staff_view_customer_of_flight_init', methods=['GET', 'POST'])
def staff_view_customer_of_flight_init():
    return render_template('/staff_page/staff_view_customer_of_flight_init.html')                                                                        
                                                                                   
@app.route('/staff_view_customer_of_flight', methods=['GET','POST'])
def staff_view_customer_of_flight():
        
        flight_number = request.form['flight_num']

        username = session['username']
        cursor = conn.cursor()
        query = "select airline_name from airline_staff where username = %s"
        cursor.execute(query, (username))
        airline = cursor.fetchone()

        query = "select c.email, c.name " \
                "from customer as c, ticket as t " \
                "where c.email = t.customer_email " \
                "and t.airline_name = %s "\
                "and t.flight_num = %s"
        
        cursor.execute(query, (airline['airline_name'], flight_number))
        customer = cursor.fetchall()
        cursor.close()
        
        error = None
        if (customer):
            return render_template('/staff_page/staff_view_customer_of_flight.html',  customer = customer)
        else:
            error = "No customer on this flight"
            return render_template('/staff_page/staff_view_customer_of_flight.html', error = error)


@app.route('/staff_view_my_flights')
def staff_view_my_flights():
    cursor = conn.cursor()
    airline = session['airline']

    query = "SELECT * FROM flight WHERE Airline_name = %s AND departure_time BETWEEN NOW() AND ADDTIME(NOW(), '30 0:0:0') AND status = 'upcoming'"
    cursor.execute(query, (airline['airline_name'],))
    flights = cursor.fetchall()
    cursor.close()

    return render_template('/staff_page/staff_view_my_flights.html', flights=flights, airline=airline)
                       
                                                   


@app.route('/staff_search', methods=['GET','POST'])
def staff_search():
    check1 = request.form.get('Use_airport_to_search')
    if check1 == 'Use_airport_to_search':
        airline = request.form['airline']
        departure_airport = request.form['departure_airport']
        arrival_airport = request.form['arrival_airport']
        starting_date = request.form['earliest_date']
        ending_date = request.form['Latest_date']

        cursor = conn.cursor()
        query = 'select *  ' \
                'from flight as f, airport as a1, airport as a2 ' \
                'where a1.airport_name = f.departure_airport ' \
                'and a2.airport_name = f.arrival_airport ' \
                'and a1.airport_name = %s and a2.airport_name = %s ' \
                'and f.arrival_time >= %s and f.arrival_time <= %s ' \
                'and f.airline_name = %s ' 

        cursor.execute(query, (starting_date, ending_date, departure_airport, arrival_airport, airline))
        cursor.close()
        flights_result = cursor.fetchall()
        if len(flights_result) == 0:
            flash('There is no any flight being selected out!')
        return render_template('/staff_page/staff_search_result.html', flights_result = flights_result)
    
    else:
        airline = request.form['airline']
        departure_city = request.form['departure_city']
        arrival_city = request.form['arrival_city']
        starting_date = request.form['earliest_date_city']
        ending_date = request.form['Latest_date_city']
        cursor = conn.cursor()
        query = 'select * ' \
                'from flight as f, airport as a1, airport as a2 ' \
                'where a1.airport_name = f.departure_airport ' \
                'and a2.airport_name = f.arrival_airport ' \
                'and a1.airport_city = %s and a2.airport_city = %s ' \
                'and f.arrival_time >= %s  and f.arrival_time <= %s ' \
                'and f.airline_name = %s ' 
                
        cursor.execute(query, (starting_date, ending_date, departure_city, arrival_city, airline))      
        flights_result = cursor.fetchall()
        cursor.close()
        if len(flights_result) == 0:
              flash('There is no any flight being selected out!')
        return render_template('/staff_page/staff_search_result.html', flights_result = flights_result)




@app.route('/staff_comparison_of_revenue_earned', methods=['GET','POST'])
def staff_comparision_of_reveneue_earned():
    airline = session['airline']
    cursor = conn.cursor()

    query = "select sum(f.price) " \
            "from flight as f, ticket as t " \
            "where (f.departure_time >= adddate(date(now()), interval -1 month)) " \
            "and t.flight_num = f.flight_num " \
            "and t.agent_email is null " \
            "and f.airline_name = %s " 
    cursor.execute(query, (airline['airline_name']))
    one_month_revenue_direct = cursor.fetchone()

    query = "select sum(f.price) " \
            "from flight as f, ticket as t " \
            "where (f.departure_time >= adddate(date(now()), interval -12 month)) " \
            "and t.flight_num = f.flight_num " \
            "and t.agent_email is null " \
            "and f.airline_name = %s " 
    cursor.execute(query, (airline['airline_name']))
    one_year_revenue_direct = cursor.fetchone()

    query = "select sum(f.price) " \
            "from  flight as f,ticket as t " \
            "where (f.departure_time >= adddate(date(now()), interval -1 month)) " \
            "and t.flight_num = f.flight_num " \
            "and t.agent_email is not null " \
            "and f.airline_name = %s " 
    cursor.execute(query, (airline['airline_name']))
    one_month_revenue_undirect = cursor.fetchone()

    query = "select sum(f.price) " \
            "from flight as f, ticket as t " \
            "where (f.departure_time >= adddate(date(now()), interval -12 month)) " \
            "and t.flight_num = f.flight_num " \
            "and t.agent_email is not null " \
            "and f.airline_name = %s " 
    cursor.execute(query, (airline['airline_name']))
    one_year_revenue_undirect = cursor.fetchone()
    cursor.close()

    return render_template('staff_page/staff_comparison_of_revenue_earned.html', one_month_revenue_direct = one_month_revenue_direct,
                                                                         one_year_revenue_direct = one_year_revenue_direct,
                                                                         one_month_revenue_undirect = one_month_revenue_undirect,
                                                                         one_year_revenue_undirect = one_year_revenue_undirect)




    
@app.route('/staff_view_report', methods=['GET','POST'])
def staff_view_report():
    return render_template('staff_page/staff_view_report.html')


@app.route('/staff_view_report_form', methods=['GET','POST'])
def staff_view_report_form():
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    airline = session['airline']
    cursor = conn.cursor()

    query = "select date_format(`date`, '%%Y-%%m') yearAndMonth  "  \
"from (select adddate('1970-01-01', interval   "  \
   "       t2.i * 100 + t1.i * 10 + t0.i month) `date`  "  \
   "   from (select 0 i union select 1 union  "  \
    "  select 2 union select 3 union  "  \
     " select 4 union select 5 union  "  \
    "  select 6 union select 7 union  "  \
    "  select 8 union select 9) t0,  "  \
   "  (select 0 i union select 1 union "  \
    "   select 2 union select 3 union "  \
   "   select 4 union select 5 union "  \
    "   select 6 union select 7 union "  \
   "   select 8 union select 9) t1, "   \
   "  (select 0 i union select 1 union "  \
   "   select 2 union select 3 union "  \
   "   select 4 union select 5 union "  \
   "   select 6 union select 7 union "  \
   "   select 8 union select 9) t2) a  "  \
"where `date` between %s and %s "

    cursor.execute(query, (start_date, end_date))
    months = cursor.fetchall()
    cursor.close()
    all_month = []
    for i in months:
        all_month.append(i['yearAndMonth'])
    
    tickets_sold = []
    for i in range(len(all_month)-1):
        a = all_month[i]
        b = all_month[i + 1]
        cursor = conn.cursor()
        query = "select COUNT(*) " \
                "from flight NATURAL JOIN ticket " \
                "where airline_name=%s and flight.departure_time >= %s and flight.departure_time < %s "
        cursor.execute(query, (airline['airline_name'] , str(a)+"-1" , str(b)+"-1"))
        amount = cursor.fetchall()
        cursor.close()
        tickets_sold.append(amount)
    
    data = []
    for i in range(len(all_month)-1):
        data.append([str(all_month[i]), tickets_sold[i][0]['COUNT(*)']])

    return render_template('staff_page/staff_view_report.html', months = months, data1 = data)



@app.route('/staff_logout')
def staff_logout():
    session.pop('username')
    session.pop('airline')
    session.pop('permission_type')
    return render_template('/index.html')




# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


@app.route('/logout')
def logout():
    session.pop('username')
    return render_template('index.html')


app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
