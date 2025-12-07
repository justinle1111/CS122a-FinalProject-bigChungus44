import sys
import os
import csv
import mysql.connector


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="cs122a"
    )


# ---------------------------------------------------------
# 1. IMPORT DATA
# ---------------------------------------------------------
def import_data(folder_name: str) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Load schema.sql
        schema_path = os.path.join("ddl", "schema.sql")
        with open(schema_path, "r") as f:
            schema_sql = f.read()

        # Execute schema (drop & recreate tables)
        for _ in cursor.execute(schema_sql, multi=True):
            pass

        folder_path = folder_name

        # Import CSVs alphabetically
        for filename in sorted(os.listdir(folder_path)):
            if not filename.endswith(".csv"):
                continue

            table_name = filename[:-4]
            file_path = os.path.join(folder_path, filename)

            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)

                placeholders = ", ".join(["%s"] * len(header))
                sql = f"INSERT INTO {table_name} VALUES ({placeholders})"

                for row in reader:
                    cursor.execute(sql, row)

        conn.commit()
        return True

    except Exception as e:
        print("ERROR:", e)
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# 2. INSERT AGENT CLIENT
# ---------------------------------------------------------
def insertAgentClient(uid, username, email, card_no, card_holder, expire, cvv, zip_code, interests):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Insert into User
        cursor.execute(
            "INSERT INTO User (uid, email, username) VALUES (%s, %s, %s)",
            (uid, email, username)
        )

        # Insert into AgentClient
        cursor.execute(
            """INSERT INTO AgentClient (uid, interests, cardholder, expire, cardno, cvv, zip)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (uid, interests, card_holder, expire, card_no, cvv, zip_code)
        )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# 3. ADD CUSTOMIZED MODEL
# ---------------------------------------------------------
def addCustomizedModel(mid, bmid):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO CustomizedModel (bmid, mid) VALUES (%s, %s)",
            (bmid, mid)
        )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# 4. DELETE BASE MODEL
# ---------------------------------------------------------
def deleteBaseModel(bmid):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM BaseModel WHERE bmid = %s", (bmid,))

        conn.commit()
        return cursor.rowcount > 0

    except Exception:
        conn.rollback()
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# 5. LIST INTERNET SERVICE
# ---------------------------------------------------------
def listInternetService(bmid):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT I.sid, I.endpoints, I.provider
            FROM InternetService I
            JOIN ModelServices M ON I.sid = M.sid
            WHERE M.bmid = %s
            ORDER BY I.provider ASC
        """

        cursor.execute(sql, (bmid,))
        for row in cursor.fetchall():
            print(",".join(str(x) for x in row))

        return True

    except Exception:
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# 6. COUNT CUSTOMIZED MODEL
# ---------------------------------------------------------
def countCustomizedModel(bmid_list):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for bmid in sorted(bmid_list, key=lambda x: int(x)):
            sql = """
                SELECT B.bmid, B.description, COUNT(C.mid)
                FROM BaseModel B
                LEFT JOIN CustomizedModel C ON B.bmid = C.bmid
                WHERE B.bmid = %s
            """
            cursor.execute(sql, (bmid,))
            row = cursor.fetchone()
            print(",".join(str(x) for x in row))

        return True

    except Exception:
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# 7. TOP N DURATION CONFIG
# ---------------------------------------------------------
def topNDurationConfig(uid, N):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT C.client_uid, MC.cid, C.labels, C.content, MC.duration
            FROM Configuration C
            JOIN ModelConfigurations MC ON C.cid = MC.cid
            WHERE C.client_uid = %s
            ORDER BY MC.duration DESC
            LIMIT %s
        """

        cursor.execute(sql, (uid, N))

        for row in cursor.fetchall():
            print(",".join(str(x) for x in row))

        return True

    except Exception:
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# 8. LIST BASE MODEL KEYWORD
# ---------------------------------------------------------
def listBaseModelKeyword(keyword):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT DISTINCT B.bmid, I.sid, I.provider, L.domain
            FROM BaseModel B
            JOIN ModelServices MS ON B.bmid = MS.bmid
            JOIN InternetService I ON MS.sid = I.sid
            JOIN LLMService L ON I.sid = L.sid
            WHERE L.domain LIKE %s
            ORDER BY B.bmid ASC
            LIMIT 5
        """

        cursor.execute(sql, ("%" + keyword + "%",))

        for row in cursor.fetchall():
            print(",".join(str(x) for x in row))

        return True

    except Exception:
        return False

    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------
# COMMAND ROUTER
# ---------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Fail")
        return

    cmd = sys.argv[1]

    if cmd == "import":
        print("Success" if import_data(sys.argv[2]) else "Fail")

    elif cmd == "insertAgentClient":
        ok = insertAgentClient(*sys.argv[2:11])
        print("Success" if ok else "Fail")

    elif cmd == "addCustomizedModel":
        ok = addCustomizedModel(sys.argv[2], sys.argv[3])
        print("Success" if ok else "Fail")

    elif cmd == "deleteBaseModel":
        ok = deleteBaseModel(sys.argv[2])
        print("Success" if ok else "Fail")

    elif cmd == "listInternetService":
        ok = listInternetService(sys.argv[2])
        print("Success" if ok else "Fail")

    elif cmd == "countCustomizedModel":
        ok = countCustomizedModel(sys.argv[2:])
        print("Success" if ok else "Fail")

    elif cmd == "topNDurationConfig":
        ok = topNDurationConfig(sys.argv[2], sys.argv[3])
        print("Success" if ok else "Fail")

    elif cmd == "listBaseModelKeyWord":
        ok = listBaseModelKeyword(sys.argv[2])
        print("Success" if ok else "Fail")

    else:
        print("Fail")


if __name__ == "__main__":
    main()
