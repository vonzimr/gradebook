# API Documentation


## Create
`Post /classroom/create`

## Delete
`Post /classroom/:id/delete`

** Note: Should only archive classroom.


## Graduate Classroom

`Post /classroom/:id/graduate

Parameters (JSON):
* `grade: <int>` Where, grade can be `1-6`.
    If `6` is specificed, the classroom is archived and removed from the class
    list.

## Get Classroom Info
`Get /classroom/:id`

Returns (JSON Object):
{'specialist': [<Specialist Object>],
 'teacher': [<Teacher Object>],
 'student': [<Student Object>],
 'grade': <int>}

## List Student(s)
`Get /classroom/:id/students

## List Teacher(s)
`Get /classroom/:id/instructors

## List Specialist(s)
`Get /classroom/:id/specialists


** Note For description on teacher/specialist/etc. objects, see root README
