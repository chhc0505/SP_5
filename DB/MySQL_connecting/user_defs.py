def select_user_tables(connection):
    cursor = connection.cursor()
    cursor.execute(f"USE user_db")
    cursor.execute("SELECT * FROM user")
    print("\nuser_db의 user 테이블:")
    for row in cursor.fetchall():
        print(row)
    cursor.close()

def user_insert(connection, user_id, user_name, user_password):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO user (user_id, user_name, user_password) VALUES (%s, %s, %s)", (user_id, user_name, user_password))
    connection.commit()
    print("user insert finished!")
    cursor.close()

def user_delete(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
    connection.commit()
    print("user delete finished!")
    cursor.close()

def user_update(connection, user_id, new_user_name, new_user_password):
    cursor = connection.cursor()
    cursor.execute("UPDATE user SET user_name = %s, user_password = %s WHERE user_id = %s", (new_user_name, new_user_password, user_id))
    connection.commit()
    print("user update finished!")
    cursor.close()

def user_reset(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM user")
    connection.commit()
    print("user table reset")
    cursor.close()
