#  Grade Report Application
## To get up and running, do the following:

* Install the requirements with:
    ```
    pip install -r requirements.txt
    ```
* Edit the `configurations/dev.cfg` file to point to a working mysql database.
Alternatively, plug in your favorite db connector. Note that we'll most likely
end up using Mariadb 10.2+ in order to store JSON objects.

* Apply the database migrations:

    ``
    flask db upgrade
    ``


* Run the application with:

    ``
    FLASK_APP=main.py flask run
    ``

* Currently, the available routes are  `/accounts/*`. Check out the associated
blueprints for how they work.

# Running Unit Tests

Unit test configuration is found under configurations/testing.cfg. In order to
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
