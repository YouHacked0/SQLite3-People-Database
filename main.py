import sqlite3

DEBUG = True


def fill_db(script_name, cursor):
    log("Executing script...")
    try:
        with open(script_name, 'r') as file:
            script = file.read()
        cursor.executescript(script)

    except sqlite3.Error as err:
        log(f"SQL Script Error: {err}", prefix=False)
    finally:
        log("Script executed!")


def main():
    global items, prices
    log("Connecting to SQLite3")
    try:
        db = sqlite3.connect("test.db")
    except sqlite3.Error as err:
        log(f"SQL Connection Error: {err}", prefix=False)
    finally:
        log("Connected!")
    cursor = db.cursor()
    fill_db("scripts.sql", cursor)
    print("Commands:\n view | inp_people | change_item | change_price | stats | help | exit")
    while True:
        cmd = input("> ")
        if cmd == "view":
            sqlite_select_query = """SELECT * FROM users"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("*" * 30)
            for i in records:
                print(f"""    ID: {i[0]}
    FIO: {i[1]}
    ITEMS: {i[2].replace(";", ", ")}
    PRICES: {i[3].replace(";", ", ")}""")
                print("*" * 30)
            if len(records) == 0:
                print("<пусто>")
        elif cmd == "inp_people":
            print("Usage: \"<name>, <1item>;<2item>, <1price>;<2price>\"")
            data = input(" >").split(", ")
            sqlite_select_query = "SELECT * FROM users"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            items = []
            for i in records:
                i = i[2].split(";")
                items.append(i)
            id = len(records) + 1
            itemss = data[1].split(";")
            items = [item for lst in items for item in lst]
            err = False
            for i in itemss:
                if i in items:
                    print("Error: item already in database")
                    err = True
            if not err:
                if cursor.fetchone() is None:
                    cursor.execute("""INSERT INTO users VALUES (?, ?, ?, ?)""", (id, data[0], data[1], data[2]))
                    db.commit()
                else:
                    raise Exception("Row already used!")
                print(f"User added! ID: {id}")
        elif cmd == "change_item":
            print("Usage: \"<name>, <item>, <new_item>\"")
            data = input(" >").split(", ")
            sqlite_select_query = "SELECT * FROM users"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for i in records:
                if str(i[1]) == data[0]:
                    items = i[2]
            items = items.split(";")
            items[items.index(data[1])] = data[2]

            cursor.execute("UPDATE users SET items = ? WHERE name = ?", (';'.join(items), data[0]))
            db.commit()
            print("Updated!")
        elif cmd == "change_price":
            print("Usage: \"<name>, <item>, <new_price>\"")
            data = input(" >").split(", ")
            sqlite_select_query = "SELECT * FROM users"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for i in records:
                if str(i[1]) == data[0]:
                    prices = i[3]
            for i in records:
                if str(i[1]) == data[0]:
                    items = i[2]
            items = items.split(";")
            prices = prices.split(";")
            prices[items.index(data[1])] = data[2]

            cursor.execute("UPDATE users SET prices = ? WHERE name = ?", (';'.join(prices), data[0]))
            print("Updated!")
        elif cmd == "stats":
            prices = []
            sqlite_select_query = "SELECT * FROM users"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            for i in records:
                i = i[3].split(";")
                prices.append(i)
            prices = list(map(int, [item for lst in prices for item in lst]))
            middle = float(sum(prices)) / max(len(prices), 1)
            # for i in prices:
            #
            print(f"All prices: {prices}")
            print(f"Max: {max(prices)}\nMiddle: {middle}\nMin: {min(prices)}")
        elif cmd == "exit" or cmd == "quit" or cmd == "q":
            break
        elif cmd == "help" or cmd == "menu":
            print("Availible commands: view | inp_people | change_item | change_price | stats | help | quit")
        else:
            print("Unknown command. Availible commands: view | inp_people | change_item | change_price | stats | help | quit")


def log(msg, prefix=True):
    if DEBUG:
        if not prefix:
            print(msg)
        else:
            print(f"LOG: {msg}")


if __name__ == '__main__':
    main()
