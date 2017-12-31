#  Grade Report Application
## Setup

### Python Requirements

* Install the requirements with:
    ```
    pip install -r requirements.txt
    ```

### Database Configuration

We'll be using MariaDB 10.2+ in order to store JSON objects.

* Create a database to use, for example `gradebook`

* Edit the `configurations/dev.cfg` file to point to your working database.
    ```
    SQLALCHEMY_DATABASE_URI
    = 'mysql+mysqldb://<user>:<password>@192.168.43.131/<database>'
    ```
* Apply the database migrations:

    ``
    flask db upgrade
    ``

### Running the Application

* Run the application with:

    ``
    FLASK_APP=main.py flask run
    ``

* Currently, the available routes are  `/accounts/*`. Check out the associated
blueprints for how they work.

# Running Unit Tests

The testing configuration is found under `configurations/testing.cfg`. In order to
run these tests, you should create a new database. **all data within the
database will be dropped between tests**

Use the command: 
  ```
 flask test 
  ```
  to run the test cases.


  You can also directly invoke the unittest module,

  ```
  python -m unittest discover gradebook "*_test.py"
  ```

  Note that in order for tests to be discovered, they must be appended with `_test.py`.
