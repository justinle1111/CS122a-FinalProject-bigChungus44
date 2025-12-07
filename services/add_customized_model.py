from db.connections import get_connection

def addCustomizedModel(mid, bmid):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        mid = int(mid)
        bmid = int(bmid)

        sql = """
            INSERT INTO CustomizedModel(bmid, mid)
            VALUES (%s, %s)
        """

        cursor.execute(sql, (bmid, mid))
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
