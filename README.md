# Maintenance-Track2  [![Coverage Status](https://coveralls.io/repos/github/mmosoroohh/Maintenance-Track2/badge.svg?branch=master)](https://coveralls.io/github/mmosoroohh/Maintenance-Track2?branch=master) [![Build Status](https://travis-ci.org/mmosoroohh/Maintenance-Track2.svg?branch=ft-endpints-for-API)](https://travis-ci.org/mmosoroohh/Maintenance-Track2)
Maintenance Tracker App is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

# Usage
- Home page]
- Create an account 
- Login into your account
- Make a request
- A request is approved or disapproved
- View your own requests]
- Admin can view all requests

# Prerequisities
- Python 3.6 or a later version

# Installation
Downlaod / clone the project to your local computer by:
- Download the zip file of this repository.
- Unzip it and navigate into the UI directory.
<pre><code>
$ /Maintenance-Track2
</code></pre>


# Alternatively
Run the following command:
<pre><code> $ git clone https://github.com/mmosoroohh/Maintenance-Track2.git </code></pre>
Locate Maintenance_Tracker folder in your local computer.
<pre><code>$ cd Maintenance-Track2/ </code></pre>

# Virtual environment
Create a virtual environment
<pre><code> $ virtualenv venv </code></pre>
Activate the environment
<pre><code> $. venv/bin/activate </code></pre>

# Dependencies
Install package requirements to your environment
<pre><code> $ pip install -r requirements.txt </code></pre>

# Env
Create a.env file in your Maintenance-Track2 root directory and add:
<pre><code>
$ . venv/bin/activate
$ export FLASK_APP="app.py"
$ export SECRET="any-character-or-STRING-YOU-PREFER"
$ export APP_SETTINGS="development"
$ export DATABASE_URL="postgresql://username:password@localhost/test_mt_db"
</code></pre>

# Database migration
Create two Database in PostgreSQL:
- mt_db (development DB)
- test_mt_db (testing DB)
Run the following commands for each database:
<pre><code>
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
</code></pre>

# Testing
To set up testing environment
<pre><code>
$ pip install nose
$ pip install coverage
</code></pre>
To run test perform the following:
<pre><code>
$ nosetests --with-coverage
</code></pre>
# Testing API endpoints
<pre>
<table>
<tr><th>Test</th>
<th>API-endpoint</th>
<th>HTTP-Verbs</th>
</tr>
<tr>
<td>User can create new request</td>
<td>/api/v1/requests/</td>
<td>POST</td>
</tr>
<tr>
<td>User can view all request</td>
<td>/api/v1/requests/</td>
<td>GET</td>
</tr>
<tr>
<td>user can view single request</td>
<td>/api/v1/requests/request_id</td>
<td>GET</td>
</tr>
<tr>
<td>user can modify request</td>
<td>/api/v1/requests/request_id</td>
<td>PUT</td>
</tr>
<tr>
<td>user can delete a request</td>
<td>/api/v1/requests/request_id</td>
<td>DELETE</td>
</tr>
</tr>
</table>
</pre>

# Authors
- Arnold M. Osoro - [mmosoroohh](https://github.com/mmosoroohh)

# Acknowledgement
Andela Bootcamp - cohort 28
