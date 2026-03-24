import psycopg2
import csv
from config import load_config


def create_table():
    sql = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
            print("Table phonebook created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)


def insert_from_csv(filename):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(filename, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        cur.execute(
                            """
                            INSERT INTO phonebook (username, phone)
                            VALUES (%s, %s)
                            ON CONFLICT (phone) DO NOTHING
                            """,
                            (row["username"], row["phone"])
                        )
            conn.commit()
            print("Data inserted from CSV.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)


def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO phonebook (username, phone)
                    VALUES (%s, %s)
                    """,
                    (username, phone)
                )
            conn.commit()
            print("Contact added successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)


def update_contact():
    choice = input("Update by (1) username or (2) phone? ")

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if choice == "1":
                    old_username = input("Enter current username: ")
                    new_username = input("Enter new username: ")
                    cur.execute(
                        """
                        UPDATE phonebook
                        SET username = %s
                        WHERE username = %s
                        """,
                        (new_username, old_username)
                    )
                elif choice == "2":
                    old_phone = input("Enter current phone: ")
                    new_phone = input("Enter new phone: ")
                    cur.execute(
                        """
                        UPDATE phonebook
                        SET phone = %s
                        WHERE phone = %s
                        """,
                        (new_phone, old_phone)
                    )
                else:
                    print("Invalid choice.")
                    return

            conn.commit()
            print("Contact updated successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)


def query_contacts():
    print("1 - Show all")
    print("2 - Search by username")
    print("3 - Search by phone prefix")

    choice = input("Choose: ")
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if choice == "1":
                    cur.execute("SELECT * FROM phonebook ORDER BY id")

                elif choice == "2":
                    name = input("Enter username: ")
                    cur.execute(
                        """
                        SELECT * FROM phonebook
                        WHERE username ILIKE %s
                        ORDER BY id
                        """,
                        (f"%{name}%",)
                    )

                elif choice == "3":
                    prefix = input("Enter phone prefix: ")
                    cur.execute(
                        """
                        SELECT * FROM phonebook
                        WHERE phone LIKE %s
                        ORDER BY id
                        """,
                        (f"{prefix}%",)
                    )
                else:
                    print("Invalid choice.")
                    return

                rows = cur.fetchall()

                if rows:
                    for row in rows:
                        print(row)
                else:
                    print("No contacts found.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)


def delete_contact():
    print("1 - Delete by username")
    print("2 - Delete by phone")

    choice = input("Choose: ")
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if choice == "1":
                    username = input("Enter username to delete: ")
                    cur.execute(
                        "DELETE FROM phonebook WHERE username = %s",
                        (username,)
                    )
                elif choice == "2":
                    phone = input("Enter phone to delete: ")
                    cur.execute(
                        "DELETE FROM phonebook WHERE phone = %s",
                        (phone,)
                    )
                else:
                    print("Invalid choice.")
                    return

            conn.commit()
            print("Contact deleted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)


def menu():
    while True:
        print("\nPHONEBOOK MENU")
        print("1 - Create table")
        print("2 - Insert from CSV")
        print("3 - Insert from console")
        print("4 - Update contact")
        print("5 - Query contacts")
        print("6 - Delete contact")
        print("0 - Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            query_contacts()
        elif choice == "6":
            delete_contact()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()