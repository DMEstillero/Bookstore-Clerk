# imports 'sqlite3' module
import sqlite3

# creates or opens a file called 'ebookstore' 
db = sqlite3.connect('ebookstore')
cursor = db.cursor()


# creates books table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT,
               Author TEXT, Qty INTEGER)
''')
db.commit()

# 'book_inv' stores a list of tuples containing the books and their details
book_inv = [(3001, 'A Tale of Two Cities', 'Charles Dickens', 30), 
            (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40), 
            (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25), 
            (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37), 
            (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]

cursor.executemany('INSERT or REPLACE INTO books VALUES(?,?,?,?);', book_inv)

db.commit()

# 'add_book' function inserts a new row into books table from user input
# asks user for input of the book's id, title, author and quantity
# using 'book_id', 'book_title', 'book_author', 'book_qty' variables
def add_book():
    try:
        book_id = int(input("Enter the book's id number: ")) 
        book_title = input("Enter the book's title: ")
        book_author = input("Enter the book's author: ")
        book_qty = int(input("Enter the quantity of the book: "))
        cursor.execute('''INSERT INTO books(id, Title, Author, Qty) 
                VALUES(?,?,?,?)''', (book_id, book_title, book_author, book_qty))
        print_table()
    except Exception as e:
        db.rollback()
        raise e


# asks user for id number of book that is being updated
# asks user for which value of that book they'd like to update
# if 'Title' updates the Title based on 'value_change' user input
# elif 'Author' updates the Author based on 'value_change' user input
# elif 'Qty' updates the Qty based on 'value_change' user input
def update_book():
    try: 
        book_id = int(input("Enter the book's id number: "))
        header_value = input("Which value would you like to update? (Title, Author, Qty) ").capitalize()
        if header_value == 'Title':
            value_change = input("Enter the updated title: ")
            cursor.execute('UPDATE books SET Title = ? WHERE id = ?;', (value_change, book_id,))
            print_table()

            
        elif header_value == 'Author':
            value_change = input("Enter the updated author: ")
            cursor.execute('UPDATE books SET Author = ? WHERE id = ?;', (value_change, book_id))
            print_table()

            
        elif header_value == 'Qty':
            value_change = input("Enter the updated quantity: ")
            cursor.execute('UPDATE books SET Qty = ? WHERE id = ?;', (value_change, book_id))
            print_table()
    except Exception as e:
        db.rollback()
        raise e   


# 'delete_book' function deletes a row according to the user's input of 'book_id'
def delete_book():
    try:
        book_id = int(input("Enter the book's id number: "))
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,)) 
        print_table()
    except Exception as e:
        db.rollback()
        raise e


# 'search_book' function prints out the row according to the user's input of 'book_id'    
def search_book():
    try: 
        book_id = int(input("Enter the book's id number: "))
        cursor.execute('''SELECT * FROM books WHERE id=?''', (book_id,))
        book = cursor.fetchone()
        print(f'id: {book[0]}\nTitle: {book[1]}\nAuthor: {book[2]}\nQty: {book[3]}')
    except Exception as e:
        db.rollback()
        raise e


# 'print_table' function selects all rows and columns from books table then prints it out
def print_table():
    print('\nUpdated Books Table')
    cursor.execute('SELECT * FROM books')
    for row in cursor:
        print(f'id: {row[0]}, Title: {row[1]}, Author: {row[2]}, Qty: {row[3]} ')
    
    
# Main Menu
while True:

    try:
        menu = int(input('''
Please select from the menu below:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
\n'''))

        if menu == 1:
            add_book()

        elif menu == 2:
            update_book()

        elif menu == 3:
            delete_book()

        elif menu == 4:
            search_book()
        
        elif menu == 0:
            db.close()
            quit()

        elif menu > 4:
            print("\nYou have selected an invalid option. Please try again by choosing from the menu below.\n")

    except ValueError:
        print("\nYou have selected an invalid option. Please try again by entering a number.\n")