
from pydoc import pager
from re import search
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    Set up CORS. Allow '*' for origins.
    """
    CORS(app, resources={r"/api/*" : {'origins' : '*'}})

    """
    After_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    def format_categories(categories):
        cat = {} 
        for category in categories:
            cat.update(category.format())

        return cat

        
    @app.route('/categories', methods=['GET'])
    def categories():
        categories = Category.query.all()
        if not categories:
            abort(404)

        return jsonify({
            'success':True,
            'categories':format_categories(categories)
        })

    def paginate(request, list):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        return list[start:end]

    @app.route('/questions', methods=['GET', 'POST'])
    def questions():
        categories = Category.query.all()
    
        if request.method == 'GET':
            # get all questions
            query = request.args.get('searchTerm')
            if not query:
                questions = Question.query.all()
                if not questions:
                    abort(404)
                total_questions = len(questions)
                questions = [question.format() for question in questions]
                questions = paginate(request, questions)
                return jsonify({
                    'success':True,
                    'questions':questions,
                    'total_questions':total_questions,
                    'categories':format_categories(categories)
                })
            else:
                # Serch a question using url parameter
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(query))).all()
                total_questions = len(questions)
                if questions:
                    questions = [question.format() for question in questions]
                    questions = paginate(request, questions)
                    return jsonify({
                        'success':True,
                        'questions':questions,
                        'total_questions':total_questions,
                        'categories':format_categories(categories)
                    }) 
                else:
                    return abort(404)

        elif request.method == 'POST':
            _json = request.json
            
            if 'searchTerm' not in _json.keys():
                """
                TEST: When you submit a question on the "Add" tab,
                the form will clear and the question will appear at the end of the last page
                of the questions list in the "List" tab.
                """
                try:
                    # add a new question

                    question = _json['question']
                    answer = _json['answer']
                    category = _json['category']
                    difficulty = _json['difficulty']

                    new_question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
                    new_question.insert()
                    db.session.commit()
                    return jsonify({
                        'success':True,
                        'questions': new_question.format()
                    })
                except:
                    db.session.rollback()
                    return abort(500)
                finally:
                    db.session.close() 
            else:
            
                """
                TEST: Search by any phrase. The questions list will update to include
                only question that include that string within their question.
                Try using the word "title" to start.
                """
                # Search a question using form
                questions = Question.query.filter(Question.question.ilike('%{}%'.format(_json['searchTerm']))).all()
                total_questions = len(questions)
                if questions:
                    questions = [question.format() for question in questions]
                    questions = paginate(request, questions)
                    return jsonify({
                        'success':True,
                        'questions':questions,
                        'total_questions':total_questions,
                        'categories':format_categories(categories)
                    }) 
                else:
                    return abort(500)
        
        
        
    @app.route('/questions/<int:del_id>', methods=['DELETE'])    
    def remove_question(del_id):
            """
            TEST: When you click the trash icon next to a question, the question will be removed.
            This removal will persist in the database and when you refresh the page.
            """
            try:
                Question.query.filter_by(id = del_id).delete()
                db.session.commit()
                return jsonify({
                    'success':True
                })
            except:
                db.session.rollback()
                return abort(404)
            finally:
                db.session.close() 

    # Update question
    @app.route('/questions/<int:id>', methods=['PUT'])
    def update_question(id):
        """
        This endpoint updates a question.
        """
        try:
            _json = request.json
            question = Question.query.get(id)
            # Populate question object
            question.question =_json['question']
            question.answer = _json['answer']
            question.category = _json['category']
            question.difficulty = _json['difficulty']

            db.session.add(question)
            db.session.commit()
            return jsonify({
                'success':True
            })
        except:
            db.session.rollback()
            return abort(500)
        finally:
            db.session.close() 
                

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/questions/<int:category>', methods=['GET'])
    def question_categories(category):
        questions = Question.query.filter(Question.category == str(category)).all()
        total_questions = len(questions)
        if questions:
            questions = [q.format() for q in questions]
            return jsonify({
                        'success':True,
                        'questions':questions,
                        'totalQuestions':total_questions
                    })
        else:
            return abort(404)


    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/play', methods=['POST'])
    def play():
        _json = request.json
        category = _json.get('quiz_category')
        prev_question = _json.get('previous_questions')

        if category['id'] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.category == str(category['id'])).all()

        # form a list of questions that excludes previous questions
        questions = [question.format() for question in questions if question.id not in prev_question]
        if questions:
            # get random question from that list
            question = random.choice(questions)
        else:
            return jsonify({
                'success': True,
                'question': None,
                'forceEnd': True
                })    
                
        return jsonify({
        'success': True,
        'question': question,
        'forceEnd': False
        })

    """
    Error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":400,
            "message":"The server will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)."
        }),400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success":False,
            "error":404,
            "message":"The server can not find the requested resource."
        }),404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success":False,
            "error":405,
            "message":"The request method is known by the server but is not supported by the target resource."
        }),405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success":False,
            "error":422,
            "message":"The request was well-formed but was unable to be followed due to semantic errors."
        }),422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success":False,
            "error":500,
            "message":"The server has encountered a situation it does not know how to handle."
        }),500


    return app

