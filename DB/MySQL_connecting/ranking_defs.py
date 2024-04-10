def select_ranking_tables(connection):
    cursor = connection.cursor()
    cursor.execute(f"USE ranking_db")
    cursor.execute("SELECT * FROM ranking ORDER BY score DESC")
    print("\nranking_db의 ranking 테이블:")
    for row in cursor.fetchall():
        print(row)
    cursor.close()

def ranking_insert(connection, user_id, score):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO ranking (user_id, score) VALUES (%s, %s)", (user_id, score))
    connection.commit()
    print("ranking insert Finished!")
    cursor.close()

def ranking_delete(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ranking WHERE user_id = %s", (user_id,))
    connection.commit()
    print("ranking delete finished!")
    cursor.close()

def ranking_update(connection, user_id, new_score):
    cursor = connection.cursor()
    cursor.execute("UPDATE ranking SET score = %s WHERE user_id = %s", (new_score, user_id))
    connection.commit()
    print("ranking update finished!")
    cursor.close()

def ranking_reset(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ranking")
    connection.commit()
    print("Ranking table reset")
    cursor.close()
