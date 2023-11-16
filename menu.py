# IMPORTS

import sys
import shutil
from time import sleep
from book_dao import BOOK_DAO
from format import Format



# CONSTANTS

WELCOME_STRING = 'BOOK MANAGER'
EXIT_STRING = 'THANK YOU FOR USING BOOK MANAGER'
WIDTH = 100 if (len(sys.argv) > 1 and 'fixed-width' in sys.argv) else shutil.get_terminal_size()[0]
MENU_OPTIONS = {
    1: 'Add a new publisher',
    2: 'Add a new book',
    3: 'Edit an existing book',
    4: 'Delete a book',
    5: 'Search books',
    6: 'Exit',
}
SEARCH_MENU_OPTIONS = {
    1: 'Search all books',
    2: 'Search by title',
    3: 'Search by isbn',
    4: 'Search by publisher',
    5: 'Search by price range',
    6: 'Search by year',
    7: 'Search by title and publisher',
}
DAO = BOOK_DAO()
HIDDEN = {
    69: 'Delete a publisher',
}



# FUNCTIONS

def handle_interrupt() -> None:
    """Function that handles the KeyboardInterrupt exception."""
    # print exit message
    exit_string = 'INTERRUPTED: ' + EXIT_STRING
    print(Format.format(f'\n\n\n{exit_string:-^{WIDTH}}\n{"":*^{WIDTH}}\n\n', ('bold', 'main')))
    # close the database connection
    DAO.exit()
    # exit
    sys.exit(0)

def print_menu(which: str = 'main') -> None:
    """Function that prints either the main menu or the search menu to the console according to the parameter 'which'."""
    # create the menu string
    menu_string = 'Menu Options' if which == 'main' else 'Search Menu Options'
    menu_string_underlined = Format.format(menu_string, ('underline', 'info'))
    header_width = WIDTH - len(menu_string) + len(menu_string_underlined)
    output = f'\n{"":-^{WIDTH}}' if which == 'main' else '\n'
    output += f'{menu_string_underlined: ^{header_width}}\n' if which == 'main' else f'{menu_string_underlined: <{header_width}}\n'
    current_line = ''
    # add the menu options to the menu string
    menu = MENU_OPTIONS if which == 'main' else SEARCH_MENU_OPTIONS
    # create the actual menu string
    for key, value in menu.items():
        option = f'{key}. {value}    '
        if len(current_line) + len(option) > WIDTH:
            output += f'{current_line[:-4]: ^{WIDTH}}\n' if which == 'main' else f'{current_line[:-4]: <{WIDTH}}\n'
            current_line = option
        else:
            current_line += option
    output += f'{current_line[:-4]: ^{WIDTH}}\n' if which == 'main' else f'{current_line[:-4]: <{WIDTH}}'
    # print the menu
    print(output)

def remove_quotes_and_handle_nulls(s: str) -> str:
    """Function that removes quotes from a string."""
    # strip the string of extra leading and trailing whitespaces
    s = s.strip()
    # remove quotes from the string
    while (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        s = s[1:-1]
    # return the string
    if s.lower() in ('null', 'none'):
        s = ''
    return s

def run(debug: bool = False) -> None:
    """Function that runs the book manager program until exit or interrupt."""
    # set option to -1
    option = -1
    # run the program loop until the user exits
    while True:
        # print the menu
        print_menu()
        # try getting the user's option
        try:
            option = int(input(Format.info('Please select a function, type [1 - 6] and press enter: ')))
        except KeyboardInterrupt:
            handle_interrupt()
        except:
            print(Format.format('\nInvalid option. Please enter a number from 1 to 6.', ('bold', 'error')))
            continue
        # carry out the action
        if option not in MENU_OPTIONS.keys() and option not in HIDDEN.keys():
            print(Format.format('\nInvalid option. Please enter a number between 1 and 6.', ('bold', 'error')))
            continue
        elif option == 1:
            option1()
            continue
        elif option == 2:
            option2()
            continue
        elif option == 3:
            option3()
            continue
        elif option == 4:
            option4()
            continue
        elif option == 5:
            option5()
            continue
        elif option == 6:
            break
        elif option == 69:
            option69()
            continue
    # close the database connection
    DAO.exit()

def option1() -> None:
    """Function that handles the 'add a new publisher' option."""
    # print the header
    print(Format.main('\nAdd a new publisher'))
    # set variables to None
    name, phone, city = None, None, None
    # get name loop
    while True:
        try:
            name = remove_quotes_and_handle_nulls(input('Publisher name ("<" to go back): '))
            if name == '<':
                return
        except KeyboardInterrupt:
            handle_interrupt()
        if name == '':
            print(Format.format('Publisher name cannot be empty.', ('bold', 'error')))
            continue
        break
    # get phone loop
    while True:
        try:
            phone = remove_quotes_and_handle_nulls(input('Publisher phone ("<" to go back): '))
            if phone == '<':
                return
            phone = str(int(phone))
        except KeyboardInterrupt:
            handle_interrupt()
        except ValueError:
            print(Format.format('Publisher phone number must be an integer.', ('bold', 'error')))
            continue
        # if len(phone) != 10:
        #     print('Publisher phone number must be 10 digits long.')
        #     continue
        break
    # get city loop
    while True:
        try:
            city = remove_quotes_and_handle_nulls(input('Publisher city ("<" to go back): '))
            if city == '<':
                return
        except KeyboardInterrupt:
            handle_interrupt()
        break
    # add publisher and print result
    print(f'\n{DAO.add_publisher(name, phone, city)}')

def option2() -> None:
    """Function that handles the 'add a new book' option."""
    # print the header
    print(Format.main('\nAdd a new book'))
    # set variables to None
    isbn, title, year, published_by, previous_edition, price = None, None, None, None, None, None
    # get isbn loop
    while True:
        try:
            isbn = remove_quotes_and_handle_nulls(input('Book ISBN ("<" to go back): '))
            if isbn == '<':
                return
            isbn = str(int(isbn))
        except KeyboardInterrupt:
            handle_interrupt()
        except ValueError:
            print(Format.format('Book ISBN must be an integer.', ('bold', 'error')))
            continue
        if isbn == '':
            print(Format.format('Book ISBN cannot be empty.', ('bold', 'error')))
            continue
        # if len(isbn) != 10:
        #     print('Book ISBN must be 10 digits long.')
        #     continue
        break
    # get title loop
    while True:
        try:
            title = remove_quotes_and_handle_nulls(input('Book title ("<" to go back): '))
            if title == '<':
                return
        except KeyboardInterrupt:
            handle_interrupt()
        if title == '':
            print(Format.format('Book title cannot be empty.', ('bold', 'error')))
            continue
        break
    # get year loop
    while True:
        try:
            year = remove_quotes_and_handle_nulls(input('Book year ("<" to go back): '))
            if year == '<':
                return
            year = int(year)
        except KeyboardInterrupt:
            handle_interrupt()
        except ValueError:
            print(Format.format('Book year must be an integer.', ('bold', 'error')))
            continue
        if len(f'{year}') != 4:
            print(Format.format('Book year must be 4 digits long.', ('bold', 'error')))
            continue
        break
    # get published_by loop
    while True:
        try:
            published_by = remove_quotes_and_handle_nulls(input('Book publisher ("<" to go back): '))
            if published_by == '<':
                return
        except KeyboardInterrupt:
            handle_interrupt()
        if published_by == '':
            print(Format.format('Book publisher cannot be empty.', ('bold', 'error')))
            continue
        break
    # get previous_edition loop
    while True:
        try:
            previous_edition = remove_quotes_and_handle_nulls(input('Book previous edition ("<" to go back): '))
            if previous_edition == '<':
                return
            if previous_edition == '':
                previous_edition = None
                break
            previous_edition = str(int(previous_edition))
        except KeyboardInterrupt:
            handle_interrupt()
        except ValueError:
            print(Format.format('Book previous edition must be an integer.', ('bold', 'error')))
            continue
        # if len(previous_edition) != 10:
        #     print('Book previous edition must be 10 digits long.')
        #     continue
        break
    # get price loop
    while True:
        try:
            price = remove_quotes_and_handle_nulls(input('Book price ("<" to go back): '))
            if price == '<':
                return
            if price == '':
                price = None
                break
            price = round(float(price), 2)
        except KeyboardInterrupt:
            handle_interrupt()
        except ValueError:
            print(Format.format('Book price must be a float.', ('bold', 'error')))
            continue
        break
    # add book and print result
    print(f'\n{DAO.add_book(isbn, title, year, published_by, previous_edition, price)}')

def option3() -> None:
    """Function that handles the 'edit an existing book' option."""
    # print the header
    print(Format.main('\nEdit an existing book'))
    # set variables to None
    isbn, title, year, published_by, previous_edition, price = None, None, None, None, None, None
    # get isbn loop
    while True:
        try:
            isbn = remove_quotes_and_handle_nulls(input('Book ISBN ("<" to go back): '))
            if isbn == '<':
                return
            isbn = str(int(isbn))
        except KeyboardInterrupt:
            handle_interrupt()
        except ValueError:
            print(Format.format('Book ISBN must be an integer.', ('bold', 'error')))
            continue
        if isbn == '':
            print(Format.format('Book ISBN cannot be empty.', ('bold', 'error')))
            continue
        # if len(isbn) != 10:
        #     print('Book ISBN must be 10 digits long.')
        #     continue
        break
    # get title loop if change title
    try:
        current = input('Change title? [y/n]: ')
    except KeyboardInterrupt:
        handle_interrupt()
    if current.lower() in ('y', 'yes'):
        while True:
            try:
                title = remove_quotes_and_handle_nulls(input('Book title: '))
            except KeyboardInterrupt:
                handle_interrupt()
            if title == '':
                print(Format.format('Book title cannot be empty.', ('bold', 'error')))
                continue
            break
    # get year loop if change year
    try:
        current = input('Change year? [y/n]: ')
    except KeyboardInterrupt:
        handle_interrupt()
    if current.lower() in ('y', 'yes'):
        while True:
            try:
                year = int(remove_quotes_and_handle_nulls(input('Book year: ')))
            except KeyboardInterrupt:
                handle_interrupt()
            except ValueError:
                print(Format.format('Book year must be an integer.', ('bold', 'error')))
                continue
            if len('{0}'.format(year)) != 4:
                print(Format.format('Book year must be 4 digits long.', ('bold', 'error')))
                continue
            break
    # get published_by loop if change publisher
    try:
        current = input('Change publisher? [y/n]: ')
    except KeyboardInterrupt:
        handle_interrupt()
    if current.lower() in ('y', 'yes'):
        while True:
            try:
                published_by = remove_quotes_and_handle_nulls(input('Book publisher: '))
            except KeyboardInterrupt:
                handle_interrupt()
            if published_by == '':
                print(Format.format('Book publisher cannot be empty.', ('bold', 'error')))
                continue
            break
    # get previous_edition loop if change previous edition
    try:
        current = input('Change previous edition? [y/n]: ')
    except KeyboardInterrupt:
        handle_interrupt()
    if current.lower() in ('y', 'yes'):
        while True:
            try:
                previous_edition = remove_quotes_and_handle_nulls(input('Book previous edition: '))
                if previous_edition == '':
                    previous_edition = None
                    break
                previous_edition = str(int(previous_edition))
            except KeyboardInterrupt:
                handle_interrupt()
            except ValueError:
                print(Format.format('Book previous edition must be an integer.', ('bold', 'error')))
                continue
            if previous_edition == '':
                print(Format.format('Book previous edition cannot be empty.', ('bold', 'error')))
                continue
            # if len(previous_edition) != 10:
            #     print('Book previous edition must be 10 digits long.')
            #     continue
            break
    # get price loop if change price
    try:
        current = input('Change price? [y/n]: ')
    except KeyboardInterrupt:
        handle_interrupt()
    if current.lower() in ('y', 'yes'):
        while True:
            try:
                price = round(float(remove_quotes_and_handle_nulls(input('Book price: '))), 2)
            except KeyboardInterrupt:
                handle_interrupt()
            except ValueError:
                print(Format.format('Book price must be a float.', ('bold', 'error')))
                continue
            break
    # edit book and print result
    print(f'\n{DAO.edit_book(isbn, title, year, published_by, previous_edition, price)}')

def option4() -> None:
    """Function that handles the 'delete a book' option."""
    # print the header
    print(Format.main('\nDelete a book'))
    # set variables to None
    isbn = None
    # get isbn loop
    while True:
        try:
            isbn = remove_quotes_and_handle_nulls(input('Book ISBN ("<" to go back): '))
            if isbn == '<':
                return
            isbn = str(int(isbn))
        except KeyboardInterrupt:
            handle_interrupt()
        except ValueError:
            print(Format.format('Book ISBN must be an integer.', ('bold', 'error')))
            continue
        if isbn == '':
            print(Format.format('Book ISBN cannot be empty.', ('bold', 'error')))
            continue
        # if len(isbn) != 10:
        #     print('Book ISBN must be 10 digits long.')
        #     continue
        break
    # delete book and print result
    print(f'\n{DAO.delete_book(isbn)}')

def option5() -> None:
    """Function that handles the 'search books' option."""
    # print search menu
    print_menu(which = 'search')
    # get user input
    while True:
        try:
            option = input('\nSearch by ("<" to go back): ')
            if option == '<':
                return
            option = int(option)
        except KeyboardInterrupt:
            handle_interrupt()
        except:
            print(Format.format('\nInvalid option. Please enter a number from 1 to 7.', ('bold', 'error')))
            continue
        if option in SEARCH_MENU_OPTIONS.keys():
            break
        else:
            print(Format.format('\nInvalid option. Please enter a number between 1 and 7.', ('bold', 'error')))
            continue
    # carry out the action
    result = None
    if option == 1:
        print('\nSearching all books')
        result = DAO.search_all_books()
    elif option == 2:
        print('\nSearching by title')
        title = None
        while True:
            try:
                title = remove_quotes_and_handle_nulls(input('Book title: '))
            except KeyboardInterrupt:
                handle_interrupt()
            if title == '':
                print(Format.format('\nBook title cannot be empty.', ('bold', 'error')))
                continue
            break
        result = DAO.search_books_by_title(title)
    elif option == 3:
        print('\nSearching by ISBN')
        isbn = None
        while True:
            try:
                isbn = remove_quotes_and_handle_nulls(input('Book ISBN: '))
                isbn = str(int(isbn))
            except KeyboardInterrupt:
                handle_interrupt()
            except ValueError:
                print(Format.format('\nBook ISBN must be an integer.', ('bold', 'error')))
                continue
            if isbn == '':
                print(Format.format('\nBook ISBN cannot be empty.', ('bold', 'error')))
                continue
            # if len(isbn) != 10:
            #     print('Book ISBN must be 10 digits long.')
            #     continue
            break
        result = DAO.search_books_by_ISBN(isbn)
    elif option == 4:
        print('\nSearching by publisher')
        publisher = None
        while True:
            try:
                publisher = remove_quotes_and_handle_nulls(input('Book publisher: '))
            except KeyboardInterrupt:
                handle_interrupt()
            if publisher == '':
                print(Format.format('\nBook publisher cannot be empty.', ('bold', 'error')))
                continue
            break
        result = DAO.search_books_by_publisher(publisher)
    elif option == 5:
        print('\nSearching by price range')
        minimum, maximum = None, None
        while True:
            try:
                minimum = round(float(remove_quotes_and_handle_nulls(input('Minimum price: '))), 2)
            except KeyboardInterrupt:
                handle_interrupt()
            except ValueError:
                print(Format.format('\nMinimum price must be a float.', ('bold', 'error')))
                continue
            break
        while True:
            try:
                maximum = round(float(remove_quotes_and_handle_nulls(input('Maximum price: '))), 2)
            except KeyboardInterrupt:
                handle_interrupt()
            except ValueError:
                print(Format.format('\nMaximum price must be a float.', ('bold', 'error')))
                continue
            break
        result = DAO.search_books_by_price_range(minimum, maximum)
    elif option == 6:
        print('\nSearching by year')
        year = None
        while True:
            try:
                year = int(remove_quotes_and_handle_nulls(input('Book year: ')))
            except KeyboardInterrupt:
                handle_interrupt()
            except ValueError:
                print(Format.format('\nBook year must be an integer.', ('bold', 'error')))
                continue
            if len('{0}'.format(year)) != 4:
                print(Format.format('\nBook year must be 4 digits long.', ('bold', 'error')))
                continue
            break
        result = DAO.search_books_by_year(year)
    elif option == 7:
        print('\nSearching by title and publisher')
        title, publisher = None, None
        while True:
            try:
                title = remove_quotes_and_handle_nulls(input('Book title: '))
            except KeyboardInterrupt:
                handle_interrupt()
            if title == '':
                print(Format.format('\nBook title cannot be empty.', ('bold', 'error')))
                continue
            break
        while True:
            try:
                publisher = remove_quotes_and_handle_nulls(input('Book publisher: '))
            except KeyboardInterrupt:
                handle_interrupt()
            if publisher == '':
                print(Format.format('\nBook publisher cannot be empty.', ('bold', 'error')))
                continue
            break
        result = DAO.search_books_by_title_and_publisher(title, publisher)
    # print the result
    if result == None or result == []:
        print(Format.format('\nNo results found.', ('bold', 'info')))
    elif type(result) == str:
        print(Format.format(f'\n{result}', ('bold', 'error')))
    else:
        # column_widths = [0 for i in range(len(result[0]))]
        column_data = []
        columns = {}
        print(Format.format('\nSearch results:', ('bold', 'info')))
        column_data = DAO.describe_books()
        if type(column_data) == str:
            print(Format.format(f'\n{column_data}', ('bold', 'error')))
            return
        else:
            column_data = [col[0] for col in column_data]
            for i in range(len(column_data)):
                column_data[i] = column_data[i].capitalize()
                width = max([len(str(book[i])) for book in result] + [len(column_data[i])])
                column_data[i] = f'{column_data[i]: ^{width}}'
                columns[column_data[i]] = width
            if len(sys.argv) > 1 and 'adaptive-table' in sys.argv:
                total_width = sum(columns.values()) + len(columns) * 3 - 1
                for key, value in columns.items():
                    columns[key] = round(value / total_width * WIDTH)
            output = ''
            for key, value in columns.items():
                output += f'{key: ^{value}} | '
            print(Format.format(output[:-3], ('bold', 'main')))
        for book in result:
            output = ''
            for i in range(len(book)):
                output += f'{str(book[i]): ^{columns[column_data[i]]}} | '
            print(output[:-3])
    return

def option69() -> None:
    """Function that handles the 'delete a publisher' option."""
    # print the header
    print(Format.main('Hidden: Delete a publisher'))
    # set variables to None
    name = None
    # get name loop
    while True:
        try:
            name = remove_quotes_and_handle_nulls(input('Publisher name ("<" to go back): '))
            if name == '<':
                return
        except KeyboardInterrupt:
            handle_interrupt()
        if name == '':
            print('Publisher name cannot be empty.')
            continue
        break
    # delete publisher and print result
    print(f'\n{DAO.delete_publisher(name)}')

def main() -> None:
    # print welcome message
    print(Format.format(f'\n\n\n{"":*^{WIDTH}}', ('bold', 'main')))
    welcome = f'{WELCOME_STRING:-^{WIDTH}}'
    for i in range(1, WIDTH + 1):
        print(Format.format(welcome[:i], ('bold', 'main')), end='\r', flush=True)
        sleep(1 / WIDTH)
    print()
    # run the program
    run()
    # print exit message
    print(Format.format(f'\n\n{EXIT_STRING:-^{WIDTH}}\n{"":*^{WIDTH}}\n\n', ('bold', 'main')))
    # exit
    sys.exit(0)

if __name__ == '__main__':
    main()
