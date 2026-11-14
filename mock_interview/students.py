from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field



"""Why do we need APIRouter?
Currently, all your endpoints are in main.py. Imagine your application eventually has 50 endpoints for students, teachers, courses, and authentication.

Instead of putting everything in one file, we can organize it like this:
my_api/

main.py — Main FastAPI application

students.py — Student endpoints

teachers.py — Teacher endpoints



APIRouter lets you define endpoints in separate files and register them with your main application.

"""


router = APIRouter(prefix = "/students", tags=["students"])
# The prefix="/students" automatically adds /students to every endpoint defined in this router.

students = {1: {"name": "John", "age": 22, "year": 3}}

@router.get("/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Not found")

    return students[student_id]


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

@router.get("/")#homepage
def index():
    return {"name": "First Data"} 

@router.get("/get_student/{student_id}")
def get_student(student: dict = Depends(get_existing_funcion)):
    #Path(...) is actually completely optional. You only need to
    #use Path(...) when you want to add extra validation
    #rules or documentation to a path parameter—such as:
    # if student_id not in students:
    #     raise HTTPException(status_code = 404, detail ="not found")

    return student


@router.get("/get-by-name")
def get_student(name:str):
    for id, student in students.items():
        if name == student["name"]:
            return student
    return {"Data": "Not found"}

@router.get("/get-student-extended/{student_id}")

#The URL string in @app.get("/get-student-extended/{student_id}"): 
#Only holds the path parameters (wrapped in {}).
def get_student_extended(student_id: int, q: str | None = None):
    if student_id not in students:
        raise HTTPException(status_code=404, detail= "Not found")

    result = {"student": students[student_id]}
    if q:
        result["query"] = q

    return result


@router.post("/create-student/{student_id}", response_model = StudentPublic)
#response_model filter what goes out through the HTTP response


def create_student(student_id: int, student: Student):

    if student_id in students:
        raise HTTPException("") 
    students[student_id] = student.model_dump() #model_dump() converts a pydantic obj into a dict
     #we instantiate the class pydantic model class Student
    return students[student_id]


@router.put("/update-student/{student_id}")
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
    students[student_id]["age"] = student.age"""


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