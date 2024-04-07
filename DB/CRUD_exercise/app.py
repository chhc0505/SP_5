from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL 연결 설정
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wlstjr1030",
    database="flask_crud_app"
)

# MySQL 커서 생성
cur = db.cursor()

# 사용자 목록 조회
@app.route('/')
def index():
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('index.html', users=users)

# 사용자 추가
@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
        return redirect(url_for('index'))

# 사용자 수정
@app.route('/update/<int:id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cur.execute("UPDATE users SET name = %s, email = %s WHERE id = %s", (name, email, id))
        db.commit()
        return redirect(url_for('index'))

# 사용자 삭제
@app.route('/delete/<int:id>',methods=['POST', 'GET'])
def delete_user(id):
    if request.method == 'POST':
        cur.execute("DELETE FROM users WHERE id = %s", (id,))
        db.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
