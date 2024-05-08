import sqlite3

db = "approot/users.db"

connection = sqlite3.connect(db)
sql = connection.cursor()
sql.execute('''create table if not exists profile
(
"userId" integer,
"FirstName" Text,
"LastName" Text,
"Email" Text,
"Bio" Text,
"ProfileImage" Text,
foreign key(userId) references users(userId)
)''')
connection.close()

def get_profile(userId):
    connection = sqlite3.connect(db)
    sql = connection.cursor()
    result = sql.execute('select * from profile where userId = ?', [userId])
    rows = result.fetchall()
    if len(rows):
        first_row = rows[0]
        return first_row
    connection.close()
    

def update_profile(userId, FirstName, LastName, Email, Bio, image):
    connection = sqlite3.connect(db)
    sql = connection.cursor()
    result = sql.execute('select * from profile where userId = ?', [userId])
    rows = result.fetchall()
    if len(rows):
        sql.execute('''update profile set FirstName = ?, LastName = ?, Email = ?, Bio = ?, ProfileImage = ?
        where userId = ?''', [FirstName, LastName, Email, Bio, image, userId])
    else:
        sql.execute('''insert into profile (userId, FirstName, LastName, Email, Bio, ProfileImage) values
        (?, ?, ?, ?, ?, ?)''', [userId, FirstName, LastName, Email, Bio, image])

    connection.commit()
    connection.close()

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return redirect(url_for('login_page'))

        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm-password']

        if not username or not password:
            msg = "Not so easy, you need to fill the form."
        elif password != confirm:
            msg = "Passwords don't match"
        else:
            msg = create_account(username, password)

    return render_template('login.html', error=msg)