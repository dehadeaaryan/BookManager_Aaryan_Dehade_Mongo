# IMPORTS

from pymongo_connector import collection

def findAll():
    results = collection.find()
    return results


def findByTitle(book_title):
    results = collection.find({'title': book_title})
    return results



# DAO CLASS

class BOOK_DAO:
    """Class that contains all the methods to interact with the database."""
    def __init__(self):
        """Constructor method."""
        # connect to the database
        self.db = BookManagerDB()
        # get a cursor object
        self.cursor = self.db.get_cursor()
        # use the bookmanager database
        self.cursor.execute('use bookmanager')
    
    def add_publisher(self, name: str, phone: str, city: str) -> str:
        """Method that adds a new publisher to the database."""
        # create a query
        query = '''
        insert into bookmanager.Publisher (name, phone, city) 
        values (%s, %s, %s)
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (name, phone, city, ))
            self.db.commit()
            return Format.info(f'Publisher {name} added successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])
    
    def add_book(self, ISBN: str, title: str, year: int, published_by: str, previous_edition: str, price: float) -> str:
        """Method that adds a new book to the database."""
        # round the price to 2 decimal places
        price = round(price, 2) if price else price
        # create a query
        query = '''
        insert into bookmanager.Book (ISBN, title, year, published_by, previous_edition, price) 
        values (%s, %s, %s, %s, %s, %s)
        ''' if previous_edition else '''
        insert into bookmanager.Book (ISBN, title, year, published_by, price)
        values (%s, %s, %s, %s, %s)
        '''
        # try executing the query
        try:
            if previous_edition:
                self.cursor.execute(query, (ISBN, title, year, published_by, previous_edition, price, ))
            else:
                self.cursor.execute(query, (ISBN, title, year, published_by, price, ))
            self.db.commit()
            return Format.info(f'Book {title} added successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])
    
    def edit_book(self, ISBN: str, title: str, year: int, published_by: str, previous_edition: str, price: float) -> str:
        """Method that edits a book in the database."""
        # if no changes were made, return a warning message
        if not all([title, year, published_by, previous_edition, price]):
            return Format.warning('No changes were made.')
        # round the price to 2 decimal places
        price = round(price, 2) if price else price
        # create a query
        query = f'''
        update bookmanager.Book
        set {'title = %s, ' if title else ''}{'year = %s, ' if year else ''}{'published_by = %s, ' if published_by else ''}{'previous_edition = %s, ' if previous_edition else ''}{'price = %s' if price else ''}
        where ISBN = %s
        '''
        # remove the extra comma and space from the query
        query_split = query.split('\n')
        for i in range(len(query_split)):
            if i not in (0, 1, len(query_split) - 1, len(query_split) - 2):
                ele = query_split[i]
                if ele.endswith(', '):
                    ele = ele[:-2]
                query_split[i] = ele
        query = '\n'.join(query_split)
        # try executing the query
        try:
            params = []
            if title:
                params.append(title)
            if year:
                params.append(year)
            if published_by:
                params.append(published_by)
            if previous_edition:
                params.append(previous_edition)
            if price:
                params.append(price)
            params.append(ISBN)
            self.cursor.execute(query, tuple(params))
            self.db.commit()
            return Format.info(f'Book {ISBN} edited successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def delete_book(self, ISBN) -> str:
        """Method that deletes a book from the database."""
        # create a query
        query = f'''
        delete from bookmanager.Book where ISBN = %s
        '''
        # if the book does not exist, return a warning message
        if self.search_books_by_ISBN(ISBN) == []:
            return Format.warning(f'Book {ISBN} does not exist.')
        # try executing the query
        try:
            self.cursor.execute(query, (ISBN, ))
            self.db.commit()
            return Format.info(f'Book {ISBN} deleted successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_all_books(self) -> list or str:
        """Method that searches all books in the database."""
        # create a query
        query = '''
        select * 
        from bookmanager.Book
        '''
        # try executing the query
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_title(self, title: str) -> list or str:
        """Method that searches books by title in the database."""
        # create a query
        query = '''
        select * 
        from bookmanager.Book
        where title like %s
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (f'%{title}%', ))
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_ISBN(self, ISBN: str) -> list or str:
        """Method that searches books by ISBN in the database."""
        # create a query
        query = '''
        select * 
        from bookmanager.Book
        where ISBN = %s
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (ISBN, ))
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_publisher(self, published_by: str) -> list or str:
        """Method that searches books by publisher in the database."""
        # create a query
        query = '''
        select * 
        from bookmanager.Book
        where published_by like %s
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (f'%{published_by}%', ))
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_price_range(self, min: float, max: float) -> list or str:
        """Method that searches books by price range in the database."""
        # create a query
        query = '''
        select * 
        from bookmanager.Book
        where price between %s and %s
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (min, max, ))
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_year(self, year: int) -> list or str:
        """Method that searches books by year in the database."""
        # create a query
        query = '''
        select * 
        from bookmanager.Book
        where year = %s
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (year, ))
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_title_and_publisher(self, title: str, publisher: str) -> list or str:
        """Method that searches books by title and publisher in the database."""
        # create a query
        query = '''
        select * 
        from bookmanager.Book
        where title like %s and published_by like %s
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (f'%{title}%', f'%{publisher}%', ))
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def delete_publisher(self, name: str) -> str:
        """Method that deletes a publisher from the database."""
        # create a query
        query = '''
        delete from bookmanager.Publisher where name = %s
        '''
        # try executing the query
        try:
            self.cursor.execute(query, (name, ))
            self.db.commit()
            return Format.info(f'Publisher {name} deleted successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def describe_books(self) -> list or str:
        """Method that describes the Book table."""
        # create a query
        query = '''
        describe bookmanager.Book
        '''
        # try executing the query
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def exit(self) -> None:
        """Method that exits the program."""
        # close the connection to the database
        self.db.close()
