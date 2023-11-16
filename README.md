# Book Manager

## Project Overview

This python project has the following features:

1. Add a new publisher (name, phone and city).
2. Add a new book (ISBN, title, year, published_by, previous edition and price).
3. Edit an existing book.
4. Delete a book.
5. Search books based on criteria:
    1. All books.
    2. Based on title. Zero or more books shall be returned.
    3. Based on ISBN. One or zero book shall be returned.
    4. Based on publisher. Zero or more shall be returned.
    5. Based on price range (min and max). Zero or more shall be returned.
    6. Based on year. Zero or more shall be returned.
    7. Based on title and publisher. Zero or more shall be returned.

## Installation Instructions

Github, Docker, MySQL and Python 3 are required to run this project.

### Github setup

1. Open a terminal.
2. Run: `git clone https://github.com/liranmatcu/Database.git`

### Docker and MySQL setup

1. Run: `cd Database/MySQL`
2. Run: `docker-compose up -d mdb`
3. Run: `docker exec -it mysql bash`
4. Run: `mysql -u root -p`
5. Enter the password

### Python setup

1. Install python from [here](https://www.python.org/downloads/)
2. Run: `pip install mysql-connector-python` to install the MySQL connector.

## Usage Guide

### Running the project

1. Open a terminal.
2. Run: `cd <path to project>/project-1`
3. Run: `python main.py` or `python3 main.py` depending on your OS and python installation.
4. Follow the instructions on the screen.
5. Run: `docker stop mysql` to terminate the MySQL server.

### Examples

#### Add a new publisher

```bash
Please select a function, type [1 - 6] and press enter: 1

Add a new publisher
Publisher name ("<" to go back): TEST 
Publisher phone ("<" to go back): 1234
Publisher city ("<" to go back): NO CITY

Publisher TEST added successfully.
```

#### Add a new book

```bash
Please select a function, type [1 - 6] and press enter: 2

Add a new book
Book ISBN ("<" to go back): 123456789
Book title ("<" to go back): TEST BOOK
Book year ("<" to go back): 2020
Book publisher ("<" to go back): TEST
Book previous edition ("<" to go back): 
Book price ("<" to go back): 100
```

### Configuration

Arguments can be passed to the program to configure the UI.

`python3 main.py fixed-width` will set the UI to fixed width mode.

`python3 main.py adaptive-table` will set the UI to adaptive table mode.

Both modes can be used together.

## Project Structure

### Main

This is the file that runs the `main()` method from the `menu.py` file.

### Menu

This file contains the functions that are used to display the menu and get the user input.

### book_dao

This file contains the functions that are used to interact with the database.

### mysql_connector

This file contains the functions that are used to connect to the database.

### schema-creation

This file contains the functions that are used to create the database schema.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
