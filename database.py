""" database access
docs:
* http://initd.org/psycopg/docs/
* http://initd.org/psycopg/docs/pool.html
* http://initd.org/psycopg/docs/extras.html#dictionary-like-cursor
"""

from algolia import *
from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor, RealDictCursor

pool = None


def setup():
    global pool
    DATABASE_URL = os.environ["DATABASE_URL"]
    # current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, dsn=DATABASE_URL, sslmode="require")


@contextmanager
def get_db_connection():
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)

@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=DictCursor)
        # cursor = connection.cursor()
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()
            
@contextmanager
def get_db_cursor_realdict(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()
            
            
# ========================
# DB Functions
# ========================

def get_workouts():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM workouts")
        return cursor.fetchall()
    
def search_workouts(search_query=None, sort_by="created_at", order="desc", filter_type=None):
    with get_db_cursor_realdict() as cur:
        query = """
            SELECT * FROM workouts
        """
        
        # add search to query
        if search_query:
            search_pattern = f"%{search_query}%"
            query += " AND (title ILIKE %s OR details ILIKE %s)"
        
        # add grouping
        query += f" GROUP BY id, title"
        
        # filter
        if filter_type == "beginner":
            query += " HAVING difficulty = 'beginner'"
        elif filter_type == "intermediate":
            query += " HAVING difficulty = 'intermediate'"
        elif filter_type == "advanced":
            query += " HAVING difficulty = 'advanced'"
            
        if sort_by:
            query += f" ORDER BY {sort_by} {order}"
        
        if search_query:
            cur.execute(query, (search_pattern, search_pattern))
        else:
            cur.execute(query)
            
        return cur.fetchall()
    
def get_workout(id):
    with get_db_cursor(False) as cur:
        cur.execute("SELECT * FROM workouts WHERE id = %s;", (id,))
        return cur.fetchone() 

def create_workout(title, details, sport, difficulty):
        with get_db_cursor(True) as cur:
            cur.execute("""
                        INSERT INTO workouts ( title,details,sport,difficulty,created_at ) 
                        VALUES (%s , %s , %s , %s , NOW())
                        RETURNING id , created_at;
                        """ , (title,details,sport,difficulty))

            result = cur.fetchone()
            workout_id = result[0]
            created_at = result[1]
            
            # Tech Demo - Algolia
            # algolia_data = {
            # "objectID": workout_id,  
            # "title": title,
            # "details": details,
            # "sport": sport,
            # "difficulty": difficulty,
            # "created_at": created_at.strftime("%m-%d-%Y")
            # }

            # save_resp = client.save_object(index_name=ALGOLIA_WORKOUT_INDEX, body=algolia_data,)
            
            return workout_id
        
def delete_workout(id):
    with get_db_cursor(True) as cur:
        cur.execute("DELETE FROM workouts WHERE id = %s;", (id,))
        
        # Tech Demo - Algolia
        # delete_resp = client.delete_object(index_name=ALGOLIA_WORKOUT_INDEX, object_id=str(id))
        
def update_workout(id, title, details, sport, difficulty):
    with get_db_cursor(True) as cur:
        cur.execute("""
                    UPDATE workouts
                    SET title = %s, details = %s, sport = %s, difficulty = %s
                    WHERE id = %s
                    RETURNING id, created_at;
                    """, (title, details, sport, difficulty, id))
        
        result = cur.fetchone()
        workout_id = result[0]
        created_at = result[1]
        
        # Tech Demo - Algolia
        # algolia_data = {
        #     "objectID": workout_id,
        #     "title": title,
        #     "details": details,
        #     "sport": sport,
        #     "difficulty": difficulty,
        #     "created_at": created_at.strftime("%m-%d-%Y")
        # }
        
        # save_resp = client.save_object(index_name=ALGOLIA_WORKOUT_INDEX, body=algolia_data,)
        
    
    


# regular sql search
def search_workouts(search_query=None):
    with get_db_cursor_realdict() as cur:
        if search_query:
            # SQL query with LIKE to search by title or details
            search_pattern = f"%{search_query}%"
            cur.execute("""
                SELECT * FROM workouts
                WHERE title ILIKE %s OR details ILIKE %s
                ORDER BY created_at DESC;
            """, (search_pattern, search_pattern))
        else:
            # Fetch all workouts if no search query is provided
            cur.execute("""
                SELECT * FROM workouts
                ORDER BY created_at DESC;
            """)
        return cur.fetchall()
