import psycopg2

conn = psycopg2.connect("dbname='m_tracker' user='mmosoroohh' host='localhost' password='test123'")

cur = conn.cursor()

# create a table

cur.execute("CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, name varchar, email varchar, username varchar, password varchar);")

cur.execute("CREATE TABLE IF NOT EXISTS requests(id serial PRIMARY KEY, name varchar, description varchar, category varchar, department varchar);")

cur.execute("SELECT * FROM users WHERE username = 'admin'")

admin = cur.fetchone()

if admin is None:
    cur.execute("INSERT INTO users(username, password) VALUES ('admin', 'test254')")

cur.execute('SELECT * FROM users')

items = cur.fetchone()
print("Migrations are a success!", items)
conn.commit()