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

* Running Unit Tests

Unit test configuration is found under configurations/testing.cfg. Currently,
expects a seperate mysql database to run unit tests. It is recommended to use
the same dbms for running tests.

Currently, I've got the unit tests running by using the following command:

  ```
  python -m unittest discover gradebook "*_test.py"
  ```

  Note that this line expects any new unit test files to be appended with
  `_test.py`.

  I'll look into writing a command such that unit tests can be run by writing
  `flask test` or similar.
