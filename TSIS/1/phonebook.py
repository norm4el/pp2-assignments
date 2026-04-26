from connect import get_connection
import json
import csv


def run_sql_file(pathh):
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open(pathh, "r", encoding="utf-8") as ff:
            sql_code = ff.read()
        cur.execute(sql_code)
        conn.commit()
        print(pathh, "executed successfully")
    except Exception as err:
        conn.rollback()
        print("SQL error:", err)
    finally:
        cur.close()
        conn.close()


def install_all():
    run_sql_file("schema.sql")
    run_sql_file("procedures.sql")
    run_sql_file("functions.sql")


def add_contact():
    conn = get_connection()
    cur = conn.cursor()
    try:
        first = input("First name: ").strip()
        last = input("Last name: ").strip()
        email = input("Email: ").strip()
        birthday = input("Birthday YYYY-MM-DD: ").strip()
        group = input("Group: ").strip()

        cur.execute(
            "CALL add_contact(%s, %s, %s, %s, %s)",
            (first, last, email, birthday, group)
        )

        phone = input("Phone: ").strip()
        phone_type = input("Phone type home/work/mobile: ").strip()

        cur.execute(
            "CALL add_phone(%s, %s, %s)",
            (first, phone, phone_type)
        )

        conn.commit()
        print("Contact added")
    except Exception as err:
        conn.rollback()
        print("Add contact error:", err)
    finally:
        cur.close()
        conn.close()


def add_phone_to_contact():
    conn = get_connection()
    cur = conn.cursor()
    try:
        name = input("Contact first name: ").strip()
        phone = input("New phone: ").strip()
        phone_type = input("Type home/work/mobile: ").strip()

        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print("Phone added")
    except Exception as err:
        conn.rollback()
        print("Add phone error:", err)
    finally:
        cur.close()
        conn.close()


def move_contact_to_group():
    conn = get_connection()
    cur = conn.cursor()
    try:
        name = input("Contact first name: ").strip()
        group = input("New group: ").strip()

        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Contact moved")
    except Exception as err:
        conn.rollback()
        print("Move error:", err)
    finally:
        cur.close()
        conn.close()


def search_contacts_console():
    conn = get_connection()
    cur = conn.cursor()
    try:
        query = input("Search: ").strip()
        cur.execute("SELECT * FROM search_contacts(%s)", (query,))
        rows = cur.fetchall()

        if not rows:
            print("No matches")
        else:
            for row in rows:
                print(row)
    except Exception as err:
        print("Search error:", err)
    finally:
        cur.close()
        conn.close()


def filter_by_group():
    conn = get_connection()
    cur = conn.cursor()
    try:
        group = input("Group name: ").strip()

        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            WHERE g.name ILIKE %s
            ORDER BY c.id
        """, (group,))

        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as err:
        print("Filter error:", err)
    finally:
        cur.close()
        conn.close()


def sort_contacts():
    conn = get_connection()
    cur = conn.cursor()
    try:
        print("Sort by: name / birthday / created_at")
        sort_by = input("Choose: ").strip()

        if sort_by == "name":
            order_col = "first_name"
        elif sort_by == "birthday":
            order_col = "birthday"
        elif sort_by == "created_at":
            order_col = "created_at"
        else:
            print("Wrong sort option")
            return

        cur.execute(f"""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, c.created_at
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.{order_col}
        """)

        rows = cur.fetchall()
        for row in rows:
            print(row)
    except Exception as err:
        print("Sort error:", err)
    finally:
        cur.close()
        conn.close()


def pagination_loop():
    limit = int(input("Page size: "))
    offset = 0

    while True:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()

            print("\n--- PAGE ---")
            if not rows:
                print("No data")
            else:
                for row in rows:
                    print(row)

        except Exception as err:
            print("Pagination error:", err)
        finally:
            cur.close()
            conn.close()

        cmd = input("next / prev / quit: ").strip()

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break


def export_json():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
        """)

        contacts = []

        for row in cur.fetchall():
            contact_id, first, last, email, birthday, group_name = row

            cur.execute("""
                SELECT phone, type
                FROM phones
                WHERE contact_id = %s
            """, (contact_id,))

            phones = []
            for phone_row in cur.fetchall():
                phones.append({
                    "phone": phone_row[0],
                    "type": phone_row[1]
                })

            contacts.append({
                "first_name": first,
                "last_name": last,
                "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group_name,
                "phones": phones
            })

        with open("contacts.json", "w", encoding="utf-8") as ff:
            json.dump(contacts, ff, indent=4)

        print("Exported to contacts.json")
    except Exception as err:
        print("Export error:", err)
    finally:
        cur.close()
        conn.close()


def import_json():
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open("contacts.json", "r", encoding="utf-8") as ff:
            contacts = json.load(ff)

        for contact in contacts:
            first = contact["first_name"]

            cur.execute("SELECT id FROM contacts WHERE first_name = %s", (first,))
            old = cur.fetchone()

            if old:
                action = input(f"{first} exists. skip or overwrite? ").strip()

                if action == "skip":
                    continue

                if action == "overwrite":
                    cur.execute("DELETE FROM contacts WHERE first_name = %s", (first,))

            cur.execute(
                "CALL add_contact(%s, %s, %s, %s, %s)",
                (
                    contact["first_name"],
                    contact["last_name"],
                    contact["email"],
                    contact["birthday"],
                    contact["group"]
                )
            )

            for phone in contact["phones"]:
                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (first, phone["phone"], phone["type"])
                )

        conn.commit()
        print("JSON imported")
    except Exception as err:
        conn.rollback()
        print("Import JSON error:", err)
    finally:
        cur.close()
        conn.close()


def import_csv():
    conn = get_connection()
    cur = conn.cursor()
    try:
        with open("contacts.csv", "r", encoding="utf-8") as ff:
            reader = csv.DictReader(ff)

            for row in reader:
                first = row["first_name"]

                cur.execute(
                    "CALL add_contact(%s, %s, %s, %s, %s)",
                    (
                        row["first_name"],
                        row["last_name"],
                        row["email"],
                        row["birthday"],
                        row["group"]
                    )
                )

                cur.execute(
                    "CALL add_phone(%s, %s, %s)",
                    (
                        first,
                        row["phone"],
                        row["type"]
                    )
                )

        conn.commit()
        print("CSV imported")
    except Exception as err:
        conn.rollback()
        print("CSV import error:", err)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    conn = get_connection()
    cur = conn.cursor()
    try:
        value = input("First name or phone: ").strip()
        cur.execute("CALL delete_contact(%s)", (value,))
        conn.commit()
        print("Deleted if existed")
    except Exception as err:
        conn.rollback()
        print("Delete error:", err)
    finally:
        cur.close()
        conn.close()


def show_menu():
    while True:
        print("\n--- TSIS 1 PHONEBOOK ---")
        print("1. Install SQL objects")
        print("2. Add contact")
        print("3. Add phone to contact")
        print("4. Move contact to group")
        print("5. Search contacts")
        print("6. Filter by group")
        print("7. Sort contacts")
        print("8. Pagination")
        print("9. Export to JSON")
        print("10. Import from JSON")
        print("11. Import from CSV")
        print("12. Delete contact")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            install_all()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            add_phone_to_contact()
        elif choice == "4":
            move_contact_to_group()
        elif choice == "5":
            search_contacts_console()
        elif choice == "6":
            filter_by_group()
        elif choice == "7":
            sort_contacts()
        elif choice == "8":
            pagination_loop()
        elif choice == "9":
            export_json()
        elif choice == "10":
            import_json()
        elif choice == "11":
            import_csv()
        elif choice == "12":
            delete_contact()
        elif choice == "0":
            print("Bye")
            break
        else:
            print("Wrong choice")


if __name__ == "__main__":
    show_menu()