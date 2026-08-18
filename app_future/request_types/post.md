POST /api/v1/users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "admin"
}


for library to add a new book

POST /book/{name} HTTP/1.1
irrelevant |Host: api.example.com
Content-Type: application/json
irrelevant | Authorization: Bearer <token>

{
  "name": "Wiedźmin miecz przeznaczenia",
  "author": "Andrzej Sapkowski,
  release_year: 2000,
  quantity: 2
}

this sends a request 
curl -X POST http://127.0.0.1:8000/book   -H "Content-Type: application/json"   -d '{"name": "Wiedźmin miecz przeznaczenia", "author": "Andrzej Sapkowski", "release_year": 2000, "quantity": 2}'


curl -X POST http://127.0.0.1:8000/book \
  -H "Content-Type: application/json" \
  -d '{"name": "Faust", "author": "Johann Wolfgang von Goethe", "release_year": 1808, "quantity": 5}'

curl -X POST http://127.0.0.1:8000/book \
  -H "Content-Type: application/json" \
  -d '{"name": "Percy Jackson: Złodziej Pioruna", "author": "Rick Riordan", "release_year": 2005, "quantity": 8}'