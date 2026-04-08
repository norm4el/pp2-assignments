# phonebook.py

from connect import get_connection


def run_sql_file(pathh: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(pathh, "r", encoding="utf-8") as ff:
            sql_code = ff.read()
        cur.execute(sql_code)
        conn.commit()
        print(f"{pathh} executed successfully.")
    except Exception as err:
        conn.rollback()
        print(f"Error in {pathh}: {err}")
    finally:
        cur.close()
        conn.close()


def install_all() -> None:
    run_sql_file("functions.sql")
    run_sql_file("procedures.sql")


def call_upsert(first_name: str, last_name: str, phone: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_contact(%s, %s, %s)", (first_name, last_name, phone))
        conn.commit()
        print("Contact inserted or updated.")
    except Exception as err:
        conn.rollback()
        print("Upsert error:", err)
    finally:
        cur.close()
        conn.close()


def search_by_pattern(pattern: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM search_contacts_by_pattern(%s)", (pattern,))
        rows = cur.fetchall()
        if not rows:
            print("No matches found.")
            return
        for row in rows:
            print(row)
    except Exception as err:
        print("Search error:", err)
    finally:
        cur.close()
        conn.close()


def get_paginated(limit_num: int, offset_num: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit_num, offset_num))
        rows = cur.fetchall()
        if not rows:
            print("No data.")
            return
        for row in rows:
            print(row)
    except Exception as err:
        print("Pagination error:", err)
    finally:
        cur.close()
        conn.close()


def delete_by_value(value: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
        print("Deleted if matching contact existed.")
    except Exception as err:
        conn.rollback()
        print("Delete error:", err)
    finally:
        cur.close()
        conn.close()


def insert_many_users(first_names: list[str], last_names: list[str], phones: list[str]) -> None:
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "CALL insert_many_contacts(%s, %s, %s)",
            (first_names, last_names, phones)
        )

        # temp table exists in same session only
        cur.execute("SELECT * FROM temp_invalid_contacts")
        bad_rows = cur.fetchall()

        conn.commit()
        print("Bulk insert finished.")

        if bad_rows:
            print("\nIncorrect data:")
            for rr in bad_rows:
                print(rr)
        else:
            print("No invalid data.")
    except Exception as err:
        conn.rollback()
        print("Bulk insert error:", err)
    finally:
        cur.close()
        conn.close()


def show_menu() -> None:
    while True:
        print("\n--- PHONEBOOK PRACTICE 8 ---")
        print("1. Install SQL objects")
        print("2. Insert or update one contact")
        print("3. Search contacts by pattern")
        print("4. Show contacts with pagination")
        print("5. Bulk insert contacts")
        print("6. Delete by username or phone")
        print("0. Exit")

        choicee = input("Choose: ").strip()

        if choicee == "1":
            install_all()

        elif choicee == "2":
            f_name = input("First name: ").strip()
            l_name = input("Last name: ").strip()
            phonee = input("Phone: ").strip()
            call_upsert(f_name, l_name, phonee)

        elif choicee == "3":
            patt = input("Enter pattern: ").strip()
            search_by_pattern(patt)

        elif choicee == "4":
            limm = int(input("Limit: ").strip())
            offf = int(input("Offset: ").strip())
            get_paginated(limm, offf)

        elif choicee == "5":
            n = int(input("How many contacts: ").strip())
            arr_first = []
            arr_last = []
            arr_phone = []

            for i in range(n):
                print(f"\nContact {i + 1}")
                arr_first.append(input("First name: ").strip())
                arr_last.append(input("Last name: ").strip())
                arr_phone.append(input("Phone: ").strip())

            insert_many_users(arr_first, arr_last, arr_phone)

        elif choicee == "6":
            val = input("Enter first name or phone to delete: ").strip()
            delete_by_value(val)

        elif choicee == "0":
            print("Bye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    show_menu()