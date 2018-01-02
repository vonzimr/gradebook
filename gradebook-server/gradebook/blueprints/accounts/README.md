# API Documentation

## Login
Log into the gradebook.
`POST /accounts/login`

Parameters (JSON):
* `username`
* `password`

`GET /accounts/login/`
Returns the `identity` and `claims` of the current user.


## Create a New User
Create a user account
`POST /accounts/create`

Parameters (JSON):
* `username`
* `email`
* `password`
* `role` : Currently either `teacher`, `administrator`, or `specialist`.



## List
List all Users of a certain role.
This route will probably change signficantly, given we will need ways of
listing user's based on classrooms, etc.

`GET /accounts/list/:role`

Return Object Example:

`GET /acount/list/teacher`
```
[
    {
        "email": "example@example.com",
        "roles": [
            "teacher"
        ],
        "username": "user2"
    },
    {
        "email": "example@gmail.com",
        "roles": [
            "teacher"
        ],
        "username": "user3"
    }
]
```
