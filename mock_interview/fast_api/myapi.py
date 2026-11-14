from fastapi import FastAPI, Path, HTTPException, Depends, APIRouter
from pydantic import BaseModel, Field
from typing import Optional

"""FastAPI is a framework used to build endpoints that receive user requests, run your code (like an ML model), and send back the answer.

FastAPI doesn't pass requests to a backend endpoint—FastAPI is what you use to build the backend endpoints.
An endpoint is a specific digital address (a URL) where a client can go to ask for information (or send data).

In tech terms, though, the client is technically the software or device the person is using.

For example, the "client" could be:

A web browser (like Chrome or Safari) on your laptop.

An app on your smartphone.

Another computer program or script asking your endpoint for data.

So, a person uses the client to send the request to your endpoint

 fastapi is a python framework used to build endpoints that listens to incoming client requests and that runs python functions that define the backend.

 

FastAPI > Django or Flask cause
1)  "Out of the box, it automatically generates interactive Swagger documentation at /docs. This makes it effortless to test endpoints and share the API with frontend developers 
or stakeholders without writing extra code"
 
2) It uses Pydantic that checks incoming request data before it hits the model, which prevents crashes

3) supports asynchronous programming (async/await)
When your backend has to wait for a slow operation—like querying a database or fetching data from another website—an async function tells FastAPI: "While you're waiting for this external thing to reply, don't freeze up the whole server; 
go handle other incoming user requests in the meantime."
Your code is the backend.

So it's not waiting for the backend to respond; it's waiting for an external helper—like a database, a file download, or a slow external API (like fetching data from another website or an external AI service).

While your function is paused at that await line waiting for that external helper, FastAPI doesn't just sit there twiddling its thumbs.
It uses that downtime to jump over and process other client requests!


Parameters = Data going in (from client to your endpoint).

Return value = Data going out (from your endpoint back to the client).

Endpoint parameters are used to receive data from the client, not return it.

Think of parameters as the inputs or instructions the user hands you when they make a request.


Depends() allows you to write reusable functions that FastAPI automatically executes whenever an endpoint needs them.
"""
app = FastAPI()


students = {1: {
    "name": "John",
    "age": 22,
    "year": 3,
    "internal_note": "Student is under investigation"
}, 2: {"name": "paige"}}
#  api endpoint = specific location where your code asks for some data and gets an answer back. It's part address, part instruction manua
class StudentPublic(BaseModel):

# the following are called fields (acc to pydantic) or class attributes in standard python
    name:str = Field(min_length = 2, max_length = 50)
    age:int = Field(gt=0, le = 120)
    year:int = Field(ge=1, le=6)

class Student(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=50)
    age: int |None = Field(default=None, gt=0, le=120)
    year: int | None = Field(default= None, gt=0, le=6)
    internal_note: str | None = None


class UpdateStudent(BaseModel):
    name: str | None = Field(default = None, min_length = 2, max_length = 50) # or better name: str|None
    age: int | None = Field(default= None, gt=0, le = 120)
    year: int | None = Field(default=None, ge=1, le=6)



def get_existing_funcion(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code = 404, detail = "Student not found")
    return students[student_id]

@app.get("/")#homepage
def index():
    return {"name": "First Data"} 

@app.get("/get_student/{student_id}")
def get_student(student: dict = Depends(get_existing_funcion)):
    #Path(...) is actually completely optional. You only need to
    #use Path(...) when you want to add extra validation
    #rules or documentation to a path parameter—such as:
    # if student_id not in students:
    #     raise HTTPException(status_code = 404, detail ="not found")





    return student


@app.get("/get-by-name")
def get_student(name:str):
    for id, student in students.items():
        if name == student["name"]:
            return student
    return {"Data": "Not found"}

@app.get("/get-student-extended/{student_id}")

#The URL string in @app.get("/get-student-extended/{student_id}"): 
#Only holds the path parameters (wrapped in {}).
def get_student_extended(student_id: int, q: str | None = None):
    if student_id not in students:
        raise HTTPException(status_code=404, detail= "Not found")

    result = {"student": students[student_id]}
    if q:
        result["query"] = q

    return result


@app.post("/create-student/{student_id}", response_model = StudentPublic)
#response_model filter what goes out through the HTTP response


def create_student(student_id: int, student: Student):

    if student_id in students:
        raise HTTPException("") 
    students[student_id] = student.model_dump() #model_dump() converts a pydantic obj into a dict
     #we instantiate the class pydantic model class Student
    return students[student_id]


@app.put("/update-student/{student_id}")
def updated_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        raise HTTPException("Error man")
    
   """ if student.name != None:
        # when we instantiate a class model (UpdateStudent)
        #the new object has those fields as attributes define 
        # by the class
        students[student_id]["name"] = student.name

    if student.age != None:
        # students[student_id].age = student.age  THIS WOULD NOT WORK CAUSE students is a dict, not 
        # pydantic object 
        students[student_id]["age"] = student.age
"""

"""More efficient alternative"""
    updates = student.model_dump(exclude_unset = True)
    students[student_id].update(updates

    return students[student_id]






@app.delete("/delete-student/{student_id}")
def delete(student_id: str, student: dict = Depends(get_existing_funcion)):

    # del student  WRONG cause it only deletes the local variable
    del students[student_id]
    return {"message": f"Student {student_id} deleted!"}
    return [f"Student {student_id} deleted!"]