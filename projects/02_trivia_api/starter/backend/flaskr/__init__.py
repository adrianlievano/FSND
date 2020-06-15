import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={'/': {'origins': '*'}})

    def paginate_questions(response, selection):
        page = response.args.get('page', 1, type=int)
        start = (page - 1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, \
                                                        Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST,\
                                                        DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)
        category_list = []
        for cat in categories:
            category_list.append(cat.type)

        return jsonify({'success': True,
                        'status_code': 200,
                        'categories': category_list,
                        'total_categories': len(categories)})

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        total_questions = len(selection)
        current_category = None
        categories = Category.query.all()
        category_list = []

        for category in categories:
            category_list.append(category.type)

        return jsonify({'success': True,
                        'questions': current_questions,
                        'status_code': 200,
                        'total_questions': total_questions,
                        'current_category': current_category,
                        'categories': category_list})

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id)\
                                                                .one_or_none()
            if question is None:
                abort(404)
            question.delete()
            return jsonify({'success': True,
                            'status_code': 200,
                            'total_questions': len(Question.query.all())})
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        new_question = data.get('question', None)
        new_answer = data.get('answer', None)
        new_category = data.get('category', None)
        new_difficulty = data.get('difficulty', None)
        tag = data.get('searchTerm', None)

        try:
            if tag is not None:
                search_term = '%{}%'.format(tag)
                selection = db.session.query(Question)\
                                .filter(Question.question.ilike(search_term))\
                                .order_by(Question.id).all()
                if selection is None:
                    abort(404)
                paginate_questions = paginate_questions(request, selection)
                result = jsonify({'success': True,
                                  'status_code': 200,
                                  'current_category': None,
                                  'total_questions': len(Question.query.all()),
                                  'questions': paginate_questions})
                return result
            else:
                new_question = Question(question=new_question,
                                        answer=new_answer,
                                        category=new_category,
                                        difficulty=new_difficulty)
                Question.insert(new_question)
                selection = Question.query.order_by(Question.id).all()
                paginated_questions = paginate_questions(request, selection)
                result = jsonify({'success': True,
                                  'created': new_question.id,
                                  'total_questions': len(Question.query.all()),
                                  'current_category': new_category.type,
                                  'questions': paginated_questions})
                return result
        except:
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def find_questions(category_id):
        try:
            questions = Question.query.\
                                    filter(Question.category == category_id).\
                                    all()
            if category_id != 0:
                category = Category.query.get(category_id)
            else:
                category = Category.query.get(category_id + 1)
            if questions is None:
                abort(404)
            formatted_questions = paginate_questions(request, questions)
            return jsonify({'success': True,
                            'status_code': 200,
                            'total_questions': len(Question.query.all()),
                            'current_category': category.type,
                            'questions': formatted_questions})
        except:
            abort(422)

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def play():
        data = request.get_json()
        prev_ques = data['previous_questions']
        category_id = data['quiz_category']['id']
        if prev_quest is None:
            current_q = Question.query.\
                                    filter(Question.category == category_id).\
                                    all()
        else:
            current_q = Question.query\
                .filter(Question.category == category_id, notin_(prev_ques))\
                .all()
        next_ques = random.choice(current_q)
        if next_ques is None:
            abort(404)

        return jsonify({'success': True,
                        'status_code': 200,
                        'question': next_ques})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False,
                        'error': 404,
                        'message': 'Not Found'}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'success': False,
                        'error': 422,
                        'message': 'Request cannot be processed.'}), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False,
                        'error': 400,
                        'message': "Bad request."}), 400
    return app
