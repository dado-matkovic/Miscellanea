from fastapi.testclient import TestClient
from ex2_fast_api import app

client= TestClient(app)
# def test_get_existing_book():
#     response = client.get("/books/3/")
#     response2 = client.post("/books", json={"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"})
#     response3= client.get("/books/hello")
#     assert response3.status_code == 422
#     assert response2.status_code == 201
#     assert response2.json()["title"]=="The Lord of the Rings"


"""| Code | Name | When to use it |
|---|---|---|
| **200** | OK | Request succeeded, such as retrieving or updating a book |
| **201** | Created | A new resource was created |
| **204** | No Content | Request succeeded, with **no response body**, often after deletion |
| **400** | Bad Request | The request is invalid for the operation |
| **401** | Unauthorized | Authentication is missing or invalid |
| **403** | Forbidden | The caller isn’t allowed to perform the operation |
| **404** | Not Found | The requested route or resource doesn’t exist |
| **405** | Method Not Allowed | The path exists, but doesn’t support that HTTP method |
| **409** | Conflict | The request conflicts with current data, such as a duplicate unique value |
| **422** | Unprocessable Content | FastAPI’s default for request validation errors, such as a missing required field |
| **500** | Internal Server Error | An unexpected server-side error |"""



def test_book_lifecycle():
    response = client.post(f"/books", json={"title": "Dune", "author": "Frank Herbert"})
    assert response.status_code == 201

    book_id = response.json()["id"]

    response2 = client.put(f"/books/{book_id}", json={"title": "Dune - Revised", "author": "Frank Herbert"})

    assert response2.status_code == 200
    assert response2.json()["title"] == "Dune - Revised"


    response3 = client.get(f"/books/{book_id}")
    assert response3.status_code == 200
    assert response3.json()["title"]=="Dune - Revised"


    response4 = client.delete(f"/books/{book_id}")
    assert response4.status_code == 200



    
    
    assert response3.status_code == 200
    assert response4.status_code == 200
