# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
set FLASK_APP=init.py
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

The configured database is called `trivia`. The setup of the database is found in the file models.py.


## API Documentation
* The base url for all the endpoints listed below is `http://localhost:5000`
<hr>

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

* error: `404`
<hr>

`GET '/questions'`

* Fetches an array of dictionaries called questions and a dictionary of categories in the same format as the one we get from *get categories* endpoint.
* Request argument: **None**
*  Returns: An array, `questions`, that contains an object of key: value pairs

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }],
    "success": true,
    "total_questions": 20
}
```

* error: `404`
<hr>

`POST '/questions'`

* Creates a new question using a json object with keys question, answer, categorie and difficulty
* Request arguement:

```json
{
    "question": "Who are You?",
    "answer":" I dont know",
    "category": 2,
    "difficulty":2
}
```
* Returns: Json object with keys

```json
{
    "questions": {
        "answer": " I dont know",
        "category": "2",
        "difficulty": 2,
        "id": 78,
        "question": "Who are You?"
    },
    "success": true
}
```

* error: `500`
<hr>

`GET '/questions?searchTerm='`

* Fetches all questions with a substring of the search term.
* Request arguement: `searchTerm=`
* Returns: Json object with keys

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": " I dont know",
            "category": "2",
            "difficulty": 2,
            "id": 78,
            "question": "Who are You?"
        }],
    "success": true,
    "total_questions": 1
}
```

* error: `400`
<hr>

`POST '/questions`

* Fetches all questions with a substring of the search term.
* Request arguement: `{
    "searchTerm": "Which is"
}`
* Returns: Json object with keys

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Brazil",
            "category": "6",
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

* error: `404`
<hr>

`DELETE '/questions/id'`

* Deletes the question with the id `id`
* Request arguement: An integer `id`
* Returns: Json object with keys

```json
{'success':True}
```

* error: `404`
<hr>

`PUT '/questions/id'`

* Updates the question with the id `id`
* Request arguement: An integer `id`,

```json
{
    "question": "Who are Youuu?????",
    "answer":" I dont know",
    "category": 2,
    "difficulty":2
}
```

* Returns: Json object with keys

```json
{'success':True}
```
* error: `500`
<hr>

`GET '/questions/category'`

* Fetches all questions in the category with id `category`
* Request arguement: An integer `category`
* Returns: Json object with keys

```json
{
    "questions": [
        {
            "answer": "Escher",
            "category": "2",
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": "2",
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }],
    "success": true,
    "totalQuestions": 7
}
```

* error: `404`
<hr>

`POST '/play'`

* Sets up a list of questions in a given category
* Request arguements: `quiz_category`, `previous_question`
* Returns: Json object with keys

```json
{
        "success": True,
        "question": {
            "answer": "Mona Lisa",
            "category": "2",
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        }],
        "forceEnd": False
        }
```
<hr>

## Error Codes
`400 Bad Request`, `404 Not Found`, `405 Method Not Allowed`, `422 Unprocessable Entity`, `500 Internal Server Error`

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
