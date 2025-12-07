from db.connections import get_connection

def insertAgentClient(uid, username, email, card_number, card_holder, expiration_date, cvv, zip_code, interests):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Convert numeric fields
        uid = int(uid)
        card_number = int(card_number)
        cvv = int(cvv)
        zip_code = int(zip_code)

        # 1. Insert into User
        sql_user = """
            INSERT INTO User(uid, email, username)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_user, (uid, email, username))

        # 2. Insert into AgentClient
        sql_client = """
            INSERT INTO AgentClient(uid, interests, cardholder, expire, cardno, cvv, zip)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_client, (uid, interests, card_holder, expiration_date, card_number, cvv, zip_code))

        conn.commit()
        return True

    except Exception as e:
        print("ERROR:", e)
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
