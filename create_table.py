import psycopg2


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE users (
            idUser SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            datetime VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE lists (
                idList SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                date VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE tasks (
                idTask SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                date VARCHAR(255) NOT NULL,
                idList VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
        )
        """,
        """
        CREATE TABLE admin (
            idAdmin SERIAL PRIMARY KEY,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
        """)
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(user="dani",
                                  password="0410",
                                  host="localhost",
                                  port="5432",
                                  database="dani")

        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()