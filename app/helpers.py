import psycopg2
import psycopg2.extras

GET_USERS = "SELECT * FROM users"

conn = psycopg2.connect("dbname='m_tracker' user='mmosoroohh' host='localhost' password='test123'")

cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)


def insert_user(user):
    cur.execute("INSERT INTO USERS (name,email,username,password) values(%s,%s,%s,%s)",(
        user.name,
        user.email,
        user.username,
        user.password))
    conn.commit()

def get_user(username):
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user is None:
        return None
    conn.commit()
    return user

def create_request(requests):
    cur.execute("INSERT INTO REQUESTS (name, description, category, department, status, user_id) values(%s,%s,%s,%s,%s, %s)",(
        requests['name'],
        requests['description'],
        requests['category'],
        requests['department'],
        'pending',
        requests['user_id']))
    conn.commit()

def get_requests(user_id):
    cur.execute("SELECT * FROM REQUESTS WHERE user_id =%s",(user_id,))
    requests = cur.fetchall()
    rows = []
    for row in requests:
        rows.append(dict(row))
    if rows is None:
        return None  
    conn.commit()
    return rows

def get_request(id):
    cur.execute("SELECT * FROM REQUESTS WHERE id = %s", (id,))
    requests = cur.fetchone()
    if requests is None:
        return None
    conn.commit()
    return requests

def edit_request(id, req):
    cur.execute("UPDATE requests SET name = %s, description = %s, category = %s, department = %s WHERE id = %s", (
        req['name'],
        req['description'],
        req['category'],
        req['department'],
        id))
    conn.commit()

def delete_request(id):
    cur.execute("DELETE FROM requests WHERE id = %s", (id,))
    conn.commit()


def admin_get_requests():
    cur.execute("SELECT * FROM requests")
    requests = cur.fetchall()
    conn.commit()
    return requests

def admin_modify_request(id, req):
    cur.execute("UPDATE requests SET status = %s WHERE id = %s ", (
        req['status'],
        id))
    conn.commit()