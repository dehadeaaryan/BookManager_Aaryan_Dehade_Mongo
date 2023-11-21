# IMPORTS

from pymongo_connector import DBConnection
from bson.regex import Regex
from format import Format



# DAO CLASS

class BookDAO:
    """Class that contains all the methods to interact with the database."""
    def __init__(self):
        """Constructor method."""
        # connect to the database
        self.connection = DBConnection()
        # get the client object
        self.client = self.connection.getClient()
        # get the database object
        self.db = self.connection.getDB()
        # get the collection objects
        self.publisherCollection = self.connection.getPublisherCollection()
        self.bookCollection = self.connection.getBookCollection()
        # create the indexes
        self.create_indexes()
    
    def create_indexes(self) -> None:
        """Method that creates indexes for the database."""
        # create the indexes
        self.bookCollection.create_index('ISBN')
        self.bookCollection.create_index('title')
        self.bookCollection.create_index('published_by')
        self.bookCollection.create_index('price')
        self.bookCollection.create_index('year')
    
    def delete_indexes(self) -> None:
        """Method that deletes indexes for the database."""
        # delete the indexes
        self.bookCollection.drop_index('ISBN_1')
        self.bookCollection.drop_index('title_1')
        self.bookCollection.drop_index('published_by_1')
        self.bookCollection.drop_index('price_1')
        self.bookCollection.drop_index('year_1')
    
    def add_publisher(self, name: str, phone: str, city: str) -> str:
        """Method that adds a new publisher to the database."""
        # create the document
        publisher = {
            'name': name,
            'phone': phone,
            'city': city,
        }
        # try inserting the publisher
        try:
            self.publisherCollection.insert_one(publisher)
            return Format.info(f'Publisher {name} added successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])
    
    def add_book(self, ISBN: str, title: str, year: int, published_by: str, previous_edition: str, price: float) -> str:
        """Method that adds a new book to the database."""
        # round the price to 2 decimal places
        price = round(price, 2) if price else price
        # create the document
        book = {
            'ISBN': ISBN,
            'title': title,
            'year': year,
            'published_by': published_by,
            'price': price,
        }
        # if the book has a previous edition, add it to the document
        if previous_edition:
            book['previous_edition'] = previous_edition
        # try inserting the book
        try:
            self.bookCollection.insert_one(book)
            return Format.info(f'Book {title} added successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])
    
    def edit_book(self, ISBN: str, title: str, year: int, published_by: str, previous_edition: str, price: float) -> str:
        """Method that edits a book in the database."""
        # if no changes were made, return a warning message
        if not any([title, year, published_by, previous_edition, price]):
            return Format.warning('No changes were made.')
        # round the price to 2 decimal places
        price = round(price, 2) if price else price
        # create the filter
        fltr = {'ISBN': ISBN}
        # create the document
        book = {}
        # if the book has a title, add it to the document
        if title:
            book['title'] = title
        # if the book has a year, add it to the document
        if year:
            book['year'] = year
        # if the book has a publisher, add it to the document
        if published_by:
            book['published_by'] = published_by
        # if the book has a previous edition, add it to the document
        if previous_edition:
            book['previous_edition'] = previous_edition
        # if the book has a price, add it to the document
        if price:
            book['price'] = price
        # create the action
        action = {'$set': book}
        # try updating the book
        try:
            self.bookCollection.update_one(fltr, action)
            return Format.info(f'Book {ISBN} edited successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def delete_book(self, ISBN) -> str:
        """Method that deletes a book from the database."""
        # create the filter
        fltr = {'ISBN': ISBN}
        # try deleting the book
        try:
            self.bookCollection.delete_one(fltr)
            return Format.info(f'Book {ISBN} deleted successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_all_books(self) -> list or str:
        """Method that searches all books in the database."""
        # create the filter
        fltr = {}
        # create the projection
        prj = {'_id': 0}
        # try executing the query
        try:
            return list(self.bookCollection.find(fltr, prj))
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_title(self, title: str) -> list or str:
        """Method that searches books by title in the database."""
        # create the regex
        regex = Regex(f'.*{title}.*', 'i')
        # create the filter
        fltr = {'title': regex}
        # create the projection
        prj = {'_id': 0}
        # try executing the query
        try:
            # explain the query
            print(self.bookCollection.find(fltr, prj).explain()['queryPlanner']['winningPlan'])
            return list(self.bookCollection.find(fltr, prj))
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_ISBN(self, ISBN: str) -> list or str:
        """Method that searches books by ISBN in the database."""
        # create the regex
        regex = Regex(f'^{ISBN}$', 'i')
        # create the filter
        fltr = {'ISBN': regex}
        # create the projection
        prj = {'_id': 0}
        # try executing the query
        try:
            return [self.bookCollection.find_one(fltr, prj)]
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_publisher(self, published_by: str) -> list or str:
        """Method that searches books by publisher in the database."""
        # create the regex
        regex = Regex(f'.*{published_by}.*', 'i')
        # create the filter
        fltr = {'published_by': regex}
        # create the projection
        prj = {'_id': 0}
        # try executing the query
        try:
            return list(self.bookCollection.find(fltr, prj))
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_price_range(self, min: float, max: float) -> list or str:
        """Method that searches books by price range in the database."""
        # create the filter
        fltr = {'price': {'$gte': min, '$lte': max}}
        # create the projection
        prj = {'_id': 0}
        # try executing the query
        try:
            return list(self.bookCollection.find(fltr, prj))
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_year(self, year: int) -> list or str:
        """Method that searches books by year in the database."""
        # create the filter
        fltr = {'year': year}
        # create the projection
        prj = {'_id': 0}
        # try executing the query
        try:
            return list(self.bookCollection.find(fltr, prj))
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def search_books_by_title_and_publisher(self, title: str, publisher: str) -> list or str:
        """Method that searches books by title and publisher in the database."""
        # create the regex
        regex_title = Regex(f'.*{title}.*', 'i')
        regex_publisher = Regex(f'.*{publisher}.*', 'i')
        # create the filter
        fltr = {'title': regex_title, 'published_by': regex_publisher}
        # create the projection
        prj = {'_id': 0}
        # try executing the query
        try:
            return list(self.bookCollection.find(fltr, prj))
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def delete_publisher(self, name: str) -> str:
        """Method that deletes a publisher from the database."""
        # create the filter
        fltr = {'name': name}
        # try deleting the publisher
        try:
            self.publisherCollection.delete_one(fltr)
            return Format.info(f'Publisher {name} deleted successfully.')
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def get_fields(self) -> list or str:
        """Method that describes the books collection."""
        # create a filter
        fltr = {}
        # create a projection
        prj = {'_id': 0}
        # try executing the query
        try:
            return list(self.bookCollection.find_one(fltr, prj).keys())
        except Exception as e:
            return Format.warning(str(e).split(' ', 2)[2])

    def close(self) -> None:
        """Method that exits the program."""
        # delete indexes
        self.delete_indexes()
        # close the connection to the database
        self.connection.close()
