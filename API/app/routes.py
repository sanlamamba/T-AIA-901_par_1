import os
from flask import request, send_from_directory, abort, current_app
from flask_restx import Resource, Namespace, fields
from werkzeug.utils import secure_filename
from .services import (
    stt_service,
    ner_service,
    pathfinding_service
)
from .models import User
from .schemas import UserSchema
from .extensions import db

user_ns = Namespace('users', description='User operations')
stt_ns = Namespace('stt', description='Speech-to-Text Service')
ner_ns = Namespace('ner', description='Named Entity Recognition Service')
path_ns = Namespace('pathfinding', description='Pathfinding Service')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

user_model = user_ns.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
})

ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_routes(api):
    api.add_namespace(user_ns)
    api.add_namespace(stt_ns)
    api.add_namespace(ner_ns)
    api.add_namespace(path_ns)
    

    # User Routes
    @user_ns.route('/')
    class UserList(Resource):
        @user_ns.doc('list_users')
        @user_ns.marshal_list_with(user_model)
        def get(self):
            """List all users"""
            users = User.query.all()
            return users_schema.dump(users)

        @user_ns.doc('create_user')
        @user_ns.expect(user_model)
        @user_ns.marshal_with(user_model, code=201)
        def post(self):
            """Create a new user"""
            data = user_ns.payload
            user = User(name=data['name'], email=data['email'])
            db.session.add(user)
            db.session.commit()
            return user_schema.dump(user), 201

    @user_ns.route('/<int:id>')
    @user_ns.response(404, 'User not found')
    @user_ns.param('id', 'The user identifier')
    class UserResource(Resource):
        @user_ns.doc('get_user')
        @user_ns.marshal_with(user_model)
        def get(self, id):
            """Fetch a user given its identifier"""
            user = User.query.get_or_404(id)
            return user_schema.dump(user)

        @user_ns.doc('delete_user')
        @user_ns.response(204, 'User deleted')
        def delete(self, id):
            """Delete a user given its identifier"""
            user = User.query.get_or_404(id)
            db.session.delete(user)
            db.session.commit()
            return '', 204

        @user_ns.expect(user_model)
        @user_ns.marshal_with(user_model)
        def put(self, id):
            """Update a user given its identifier"""
            user = User.query.get_or_404(id)
            data = user_ns.payload
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            db.session.commit()
            return user_schema.dump(user)

    upload_parser = stt_ns.parser()
    upload_parser.add_argument('file', location='files', type='file', required=True, help='Audio file')

    @stt_ns.route('/')
    class STTResource(Resource):
        @stt_ns.doc('process_audio')
        @stt_ns.expect(upload_parser)
        def post(self):
            files = request.files
            audio_file = files.get('file')     
            if audio_file and allowed_file(audio_file.filename):
                try:
                    audio_bytes = audio_file.read()

                    transcript = stt_service.process_audio_file(audio_bytes)

                    return {'transcript': transcript}, 200
                except Exception as e:
                    abort(400, str(e))

    ner_model = ner_ns.model('TextInput', {
        'text': fields.String(required=True, description='Text input')
    })

    @ner_ns.route('/')
    class NERResource(Resource):
        @ner_ns.doc('extract_entities')
        @ner_ns.expect(ner_model)
        def post(self):
            """Extract named entities from text"""
            data = request.json
            text = data.get('text')

            if not text:
                abort(400, 'No text provided')

            entities = ner_service.extract_entities(text)
            return {'entities': entities}, 200

    path_model = path_ns.model('PathInput', {
        'start': fields.String(required=True, description='Start station code'),
        'end': fields.String(required=True, description='End station code'),
        'algorithm': fields.String(
            required=False,
            description='Algorithm to use',
            enum=['AStar', 'Dijkstra', 'BFS', 'DFS', 'BellmanFord', 'UCS', 'BidirectionalAStar'],
            default='AStar')
    })
    
    
    @path_ns.route('/')
    class PathfindingResource(Resource):
        @path_ns.doc('find_path')
        @path_ns.expect(path_model)
        def post(self):
            """Find the optimal path using the specified algorithm."""
            data = request.json
            start_name = data.get('start')
            end_name = data.get('end')
            algorithm = data.get('algorithm', 'AStar')

            if not start_name or not end_name:
                abort(400, 'Start and end station names are required')

            result = pathfinding_service.find_path(start_name, end_name, algorithm)

            if 'error' in result:
                abort(400, result['error'])

            return result, 200

    @api.route('/static/<path:filename>', doc=False)
    class StaticFileResource(Resource):
        def get(self, filename):
            """Serve static files (e.g., client-side HTML and JS)"""
            static_folder = current_app.static_folder or 'static'
            return send_from_directory(static_folder, filename)
    @api.route('/static/maps/<path:filename>', doc=False)
    class StaticMapResource(Resource):
        def get(self, filename):
            """Serve map files."""
            static_folder = os.path.join(current_app.static_folder or 'static', 'maps')
            return send_from_directory(static_folder, filename)
