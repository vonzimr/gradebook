# API Documentation

## Login

`POST /accounts/login`

Log into the gradebook.


Parameters (JSON):
* `username`
* `password`

`GET /accounts/login/`

Returns the `identity` and `claims` of the current user.


## Create

`POST /accounts/create`

Create a user account

Parameters (JSON):
* `username`
* `email`
* `password`
* `role` : Currently either `teacher`, `administrator`, or `specialist`.



## Listing all users with specified role

`GET /accounts/list/:role`

List all Users of a certain role. Requires an account with an `admin` role.
This route will probably change signficantly, given we will need ways of
listing accounts based on classrooms, etc.


Example of an object that is returned:

`GET /acount/list/teacher`
```

[
    {
        "email": "example@example.com",
        "roles": [
            "teacher"
        ],
        "username": "user2",
        "id": 2
    },
    {
        "email": "example@gmail.com",
        "roles": [
            "teacher"
        ],
        "username": "user3",
        "id" : 3
    }
]
```


## Getting a single user's info

`GET /accounts/id/:id`

Returns a single user object of the form:
```
    {
        "email": "example@gmail.com",
        "roles": [
            "teacher"
        ],
        "username": "user3",
        "id" : 1
    }
```
