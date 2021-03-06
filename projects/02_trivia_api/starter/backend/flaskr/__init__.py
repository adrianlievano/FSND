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

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, \
                                                        Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    def paginate_questions(response, selection):
        page = response.args.get('page', 1, type=int)
        start = (page - 1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        if len(categories) == 0:
            abort(404)
        category_list = []
        for cat in categories:
            category_list.append(cat.type)
        return jsonify({'success': True,
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
                            'question_id': question_id,
                            'total_questions': len(Question.query.all())})
        except BaseException:
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
            if tag:
                search_term = '%{}%'.format(tag)
                selection = Question.query\
                    .filter(Question.question.ilike(search_term))\
                    .order_by(Question.id).all()
                if len(selection) == 0:
                    abort(404)
                paginated_questions = paginate_questions(request, selection)
                result = jsonify({'success': True,
                                  'current_category': None,
                                  'total_questions': len(Question.query.all()),
                                  'questions': paginated_questions})
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
                                  'question_id': new_question.id,
                                  'total_questions': len(Question.query.all()),
                                  'questions': paginated_questions})
                return result
        except BaseException:
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
                            'total_questions': len(Question.query.all()),
                            'current_category': category.type,
                            'questions': formatted_questions})
        except BaseException:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play():
        data = request.get_json()
        if not data:
            abort(400)
        prev_ques = data['previous_questions']
        category_id = data['quiz_category']['id']
        if category_id != 0:
            if len(prev_ques) == 0:
                current_q = Question.query.\
                    filter(Question.category == category_id).\
                    all()
            else:
                current_q = Question.query\
                    .filter(Question.id == category_id, Question.id.notin_(prev_ques))\
                    .all()
        else:
            if len(prev_ques) == 0:
                current_q = Question.query.all()
            else:
                current_q = Question.query.filter(Question.id.notin_(prev_ques)).all()
        if len(current_q) == 0:
            abort(404)
        next_ques = random.choice(current_q).format()

        return jsonify({'success': True,
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

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'success': False,
                        'error': 500,
                        'message': 'Request cannot be processed.'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False,
                        'error': 400,
                        'message': "Bad request."}), 400
    return app
