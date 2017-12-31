#  Grade Report Application
## Setup

### Python Requirements
Everything should be done in a virtual environment. If you do not have virtualenv, install it with:
```
$ sudo pip install virtualenv
``` 
(or use your distro's package manager). 
I prefer to store my virtual environment in the root of the project. I've also conveniently added a line to the project's `.gitignore` to keep this directory from being committed.
```
$ virtualenv gb
$ . gb/bin/activate
```

Once inside the virtual environment Install the requirements with:

```
pip install -r requirements.txt
```
    
Finally, we need to add an environment variable so flask can find the project
```
$ export FLASK_APP=/path/to/project/gradebook-server/main.py
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
    $ flask db upgrade
    ``


* Run the application with:

    ``
    flask run
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
