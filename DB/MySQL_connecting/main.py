import mysql.connector
from ranking_defs import *
from user_defs import *

def connect_to_database(database):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="wlstjr1030",
        database=database
    )
    return connection

if __name__ == "__main__":
    ranking_connection = connect_to_database("ranking_db")
    user_connection = connect_to_database("user_db")        

    #reset tables
    ranking_reset(ranking_connection)
    user_reset(user_connection)

    #insert id : user1
    ranking_insert(ranking_connection, "user1", 100)
    user_insert(user_connection, "user1", "John Doe", "password1")

    #insert id : user2
    ranking_insert(ranking_connection, "user2", 90)
    user_insert(user_connection, "user2", "hi Do", "password2")

    #select
    select_ranking_tables(ranking_connection)
    select_user_tables(user_connection)

    #update id : user1
    user_update(user_connection, "user1", "Jane Doe", "newpassword1")
    ranking_update(ranking_connection, "user1", 50)

    #select
    select_ranking_tables(ranking_connection)
    select_user_tables(user_connection)

    #delete id : user2
    user_delete(user_connection, "user1")
    ranking_delete(ranking_connection, "user1")

    #select
    select_ranking_tables(ranking_connection)
    select_user_tables(user_connection)

