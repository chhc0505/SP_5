from flask import Flask, render_template, url_for, flash, redirect, request, session
import pymysql

app = Flask(__name__)
app.secret_key = 'secret_key'

# MySQL 연결 설정
# user_list 데이터베이스 설정
app.config['MYSQL_USER_HOST'] = 'localhost'
app.config['MYSQL_USER_USER'] = 'root'
app.config['MYSQL_USER_PASSWORD'] = 'root'
app.config['MYSQL_USER_DB'] = 'user_db'

# ranking_list 데이터베이스 설정
app.config['MYSQL_RANKING_HOST'] = 'localhost'
app.config['MYSQL_RANKING_USER'] = 'root'
app.config['MYSQL_RANKING_PASSWORD'] = 'root'
app.config['MYSQL_RANKING_DB'] = 'ranking_db'

# MySQL 연결을 위한 함수 정의
def create_mysql_connection(host, user, password, db):
    connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

# 데이터베이스 인스턴스 생성
user_db_connection = create_mysql_connection(app.config['MYSQL_USER_HOST'],
                                             app.config['MYSQL_USER_USER'],
                                             app.config['MYSQL_USER_PASSWORD'],
                                             app.config['MYSQL_USER_DB'])

ranking_db_connection = create_mysql_connection(app.config['MYSQL_RANKING_HOST'],
                                                app.config['MYSQL_RANKING_USER'],
                                                app.config['MYSQL_RANKING_PASSWORD'],
                                                app.config['MYSQL_RANKING_DB'])


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        user_name = userDetails.get('user_name')
        user_password = userDetails.get('user_password')
        user_id = userDetails.get('user_id')

        if not user_name or not user_password or not user_id:
            return render_template('register.html', message="모든 필드를 채워주세요.")

        cur = user_db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM user WHERE user_id = %s", (user_id, ))
        count = cur.fetchone()

        if (count["COUNT(*)"]) > 0:
            cur.close()
            return render_template('register.html', message="이미 존재하는 아이디입니다.")

        cur.execute("INSERT INTO user(user_name, user_password, user_id) VALUES(%s, %s, %s)", (user_name, user_password, user_id))
        user_db_connection.commit()
        cur.close()
        return render_template('success.html')
    
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        userDetails = request.form
        user_id = userDetails.get('user_id')
        user_password = userDetails.get('user_password')
        cur = user_db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM user WHERE user_id=%s && user_password=%s", (user_id, user_password,))
        isUserExist = cur.fetchone()
        if isUserExist["COUNT(*)"] > 0:
            session['user_id'] = user_id  # 사용자 ID 세션에 저장
            cur.execute("SELECT user_name FROM user WHERE user_id=%s AND user_password=%s", (user_id, user_password,))
            result = cur.fetchone()
            session['user_name'] = result['user_name']
            return redirect(url_for('index'))
        else:
            return render_template("login.html", message="아이디 또는 비밀번호가 올바르지 않습니다.")

    return render_template('login.html')


@app.route('/ranking', methods=["GET"])
def ranking():
    cur = ranking_db_connection.cursor()
    cur.execute("SELECT user_id FROM ranking ORDER BY score DESC")
    ranking_user_data = cur.fetchall()
    cur.execute("SELECT score FROM ranking ORDER BY score DESC")
    ranking_score_data = cur.fetchall()
    ranking_data = list(zip(ranking_user_data, ranking_score_data))
    return render_template('ranking.html', ranking = ranking_data)



@app.route('/logout')
def logout():
    session.pop('user_id', None)  # 로그아웃 시 세션에서 사용자 아이디 제거
    session.pop('user_name', None)
    return redirect(url_for('index'))



@app.route('/game', methods=["GET", "POST"])
def game():
    if 'user_id' not in session:
        flash("로그인이 필요합니다.")
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            user_id = session['user_id']
            new_score = int(request.form['score'])  # 폼에서 받은 점수를 정수로 변환

            # 데이터베이스에 접속하여 현재 사용자의 최고 점수를 조회
            cur = ranking_db_connection.cursor()
            cur.execute("SELECT score FROM ranking WHERE user_id = %s ORDER BY score DESC LIMIT 1", (user_id,))
            result = cur.fetchone()
            
            
            # 사용자의 현재 최고 점수가 존재하지 않거나, 새로운 점수가 더 높은 경우에만 데이터 업데이트
            if result is None:
                cur.execute("INSERT INTO ranking(user_id, score) VALUES(%s, %s)", (user_id, new_score))
                ranking_db_connection.commit()
                cur.close()
                return redirect(url_for('game')) 
            elif new_score > result['score']:
                cur.execute("UPDATE ranking SET score = %s WHERE user_id = %s", (new_score, user_id))
                ranking_db_connection.commit()
                cur.close()
                return redirect(url_for('game'))  # 데이터 저장 후 페이지 리디렉션
            else:
                cur.close()
                return render_template('game.html')
        return render_template("game.html")
    


@app.route('/rankingtest', methods=["GET", "POST"])
def rankingtest():
    if request.method == 'POST':
        # 세션에 user_id가 존재하고 폼 데이터에서 score를 받는 경우
        if 'user_id' in session and 'score' in request.form:
            user_id = session['user_id']
            new_score = int(request.form['score'])  # 폼에서 받은 점수를 정수로 변환

            # 데이터베이스에 접속하여 현재 사용자의 최고 점수를 조회
            cur = ranking_db_connection.cursor()
            cur.execute("SELECT score FROM ranking WHERE user_id = %s ORDER BY score DESC LIMIT 1", (user_id,))
            result = cur.fetchone()
            
            
            # 사용자의 현재 최고 점수가 존재하지 않거나, 새로운 점수가 더 높은 경우에만 데이터 업데이트
            if result is None:
                cur.execute("INSERT INTO ranking(user_id, score) VALUES(%s, %s)", (user_id, new_score))
                ranking_db_connection.commit()
                cur.close()
                return redirect(url_for('rankingtest')) 
            elif new_score > result['score']:
                cur.execute("UPDATE ranking SET score = %s WHERE user_id = %s", (new_score, user_id))
                ranking_db_connection.commit()
                cur.close()
                return redirect(url_for('rankingtest'))  # 데이터 저장 후 페이지 리디렉션
            else:
                cur.close()
                return render_template('index.html')

    # GET 요청 또는 다른 조건에서는 폼을 보여주는 페이지를 렌더링
    return render_template("rankingtest.html")



if __name__ == '__main__':
    app.run(debug=True)


