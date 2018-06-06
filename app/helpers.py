import psycopg2

GET_USERS = "SELECT * FROM users"

conn = psycopg2.connect("dbname='m_tracker' user='mmosoroohh' host='localhost' password='test123'")

cur = conn.cursor()

def get_users():
    cur.execute(GET_USERS)
    items = cur.fetchall()
    conn.commit()
    return items


def insert_user(user):
    cur.execute("INSERT INTO USERS (name,email,username,password) values(%s,%s,%s,%s)",(
        user['name'],
        user['email'],
        user['username'],
        user['password']))
    conn.commit()

def get_user(username):
    cur.execute("SELECT * FROM users WHERE username = %s", (username))
    user = cur.fetchone()
    conn.commit()
    return user

def create_request(requests):
    cur.execute("INSERT INTO REQUESTS (name, description, category, department) values(%s,%s,%s,%s)",(
        requests['name'],
        requests['description'],
        requests['category'],
        requests['department']))
    conn.commit()

def get_requests():
    cur.execute("INSERT FROM REQUESTS")
    requests = cur.fetchall()
    conn.commit()
    return requests




   