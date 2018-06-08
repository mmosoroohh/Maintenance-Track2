import psycopg2

GET_USERS = "SELECT * FROM users"

conn = psycopg2.connect("dbname='m_tracker' user='mmosoroohh' host='localhost' password='test123'")

cur = conn.cursor()


def insert_user(user):
    cur.execute("INSERT INTO USERS (name,email,username,password) values(%s,%s,%s,%s)",(
        user['name'],
        user['email'],
        user['username'],
        user['password']))
    conn.commit()

def get_user(username):
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user is None:
        return None
    conn.commit()
    return {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "username": user[3],
        "password": user[4]
    }

def create_request(requests):
    cur.execute("INSERT INTO REQUESTS (name, description, category, department,user_id) values(%s,%s,%s,%s,%s)",(
        requests['name'],
        requests['description'],
        requests['category'],
        requests['department'],
        requests['user_id']))
    conn.commit()

def get_requests(user_id):
    cur.execute("SELECT * FROM REQUESTS WHERE user_id=%s",(user_id,))
    requests = cur.fetchall()
    if requests is None:
        return None
    conn.commit()
    return requests

def get_request(id):
    cur.execute("SELECT * FROM REQUESTS WHERE id = %s", (id,))
    requests = cur.fetchone()
    if requests is None:
        return None
    conn.commit()
    return requests

def modify_request(id):
    cur.execute("UPDATE REQUESTS SET")