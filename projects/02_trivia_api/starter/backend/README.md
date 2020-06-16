# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints

GET '/categories'
GET '/questions
POST '/questions'
DELETE '/questions/<int:question_id>'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category. 
- Request Arguments: None
- Returns: An object key values associated with categories. It contains an object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

### GET '/questions
- Fetches a list of dictionaries for game questions for all categories. 
- Request Arguments: None
- Returns: An list of question objects associated with different categories. 
```
"questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },...
```
### POST '/questions'
- Adds a new question using the client-side form to the Question database for the game.
- Request Arguments: The online form on the client side after a user clicks 'Add' a question.
- Returns: An object of questions that contains the new question created. The object contains data about the number of total questions, the new added question id, and a success indicator. 

Sample output: 
```
{'success': True,
'question_id': new_question.id,
'total_questions': len(Question.query.all()),
'questions': paginated_questions})
```

### DELETE '/questions/<int:question_id>'
- Deletes a question from the Question database. 
- Request Arguments: The id of corresponding question that the user wishes to remove. 
- Returns: An dictionary of values that correspond to a success indicator, the question id removed, and the new total number of questions in the game.

Sample Output: 
```{'success': True,
'question_id': question_id,
'total_questions': len(Question.query.all())}
```
### GET '/categories/<int:category_id>/questions'
- Gets a list of questions associated with a category id. 
- Request Arguments: The id of a category_id that the user wishes to remove. 
- Returns: A success value, list of questions for a give category_id, total number of questions, the category type, and a current category.

Sample Output:
```
{'success': True,
total_questions': len(Question.query.all()),
'current_category': category.type,
'questions': formatted_questions}
```

### POST '/quizzes'
- Starts the game and allows the user to answer a quiz question.
- Request Arguments: None
- Returns: A success value and the next question that will be served to the user that has not appeared in the past. 

```
Sample Output:
{'success': True,
'question': next_ques}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```