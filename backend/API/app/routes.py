import os
from flask import request, send_from_directory, abort, current_app
from flask_restx import Resource, Namespace, fields
from .services import stt_service, ner_service, pathfinding_service

user_ns = Namespace("users", description="User operations")
stt_ns = Namespace("stt", description="Speech-to-Text Service")
ner_ns = Namespace("ner", description="Named Entity Recognition Service")
path_ns = Namespace("pathfinding", description="Pathfinding Service")
general_processes_ns = Namespace(
    "general", description="General processes combining multiple services"
)


ner_model = ner_ns.model(
    "TextInput", {"text": fields.String(required=True, description="Text input")}
)
path_model = path_ns.model(
    "PathInput",
    {
        "start": fields.String(required=True, description="Start station code"),
        "end": fields.String(required=True, description="End station code"),
        "intermediates": fields.List(
            fields.String,
            required=False,
            description="Intermediate station codes",
            default=[],
        ),
        "algorithm": fields.String(
            required=False,
            description="Algorithm to use",
            enum=[
                "AStar",
                "Dijkstra",
                "BFS",
                "DFS",
                "BellmanFord",
                "UCS",
                "BidirectionalAStar",
            ],
            default="AStar",
        ),
    },
)

general_process_model = general_processes_ns.model(
    "GeneralProcessInput",
    {"text": fields.String(required=True, description="Text input to process")},
)

ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg", "flac"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def register_routes(api):
    api.add_namespace(stt_ns)
    api.add_namespace(ner_ns)
    api.add_namespace(path_ns)
    api.add_namespace(general_processes_ns)

    # --------------------
    # STT Routes
    # --------------------
    upload_parser = stt_ns.parser()
    upload_parser.add_argument(
        "file", location="files", type="file", required=True, help="Audio file"
    )

    @stt_ns.route("/")
    class STTResource(Resource):
        @stt_ns.doc("process_audio")
        @stt_ns.expect(upload_parser)
        def post(self):
            """Process an audio file and return transcript"""
            files = request.files
            audio_file = files.get("file")
            if audio_file and allowed_file(audio_file.filename):
                try:
                    audio_bytes = audio_file.read()
                    transcript = stt_service.process_audio_file(audio_bytes)
                    return {"transcript": transcript}, 200
                except Exception as e:
                    abort(400, str(e))
            else:
                abort(400, "No audio file provided or file type not allowed.")

    # --------------------
    # NER Routes
    # --------------------
    @ner_ns.route("/")
    class NERResource(Resource):
        @ner_ns.doc("extract_entities")
        @ner_ns.expect(ner_model)
        def post(self):
            """Extract named entities from text"""
            data = request.json
            text = data.get("text")
            if not text:
                abort(400, "No text provided")

            try:
                entities = ner_service.extract_entities(text)
                return {"entities": entities}, 200
            except Exception as e:
                abort(400, f"NER Error: {str(e)}")

    # --------------------
    # Pathfinding Routes
    # --------------------
    @path_ns.route("/")
    class PathfindingResource(Resource):
        @path_ns.doc("find_path")
        @path_ns.expect(path_model)
        def post(self):
            """Find the optimal path using the specified algorithm."""
            data = request.json
            start_name = data.get("start")
            intermediates = data.get("intermediates", [])
            end_name = data.get("end")
            algorithm = data.get("algorithm", "AStar")

            if not start_name or not end_name:
                abort(400, "Start and end station names are required")

            try:
                result = pathfinding_service.find_path(
                    start_name, end_name, intermediates, algorithm
                )
                if "error" in result:
                    abort(400, result["error"])
                return result, 200
            except Exception as e:
                abort(400, f"Pathfinding Error: {str(e)}")

    # --------------------
    # General Processes Routes
    # --------------------
    @general_processes_ns.route("/process")
    class TextToPathfindingResource(Resource):
        @general_processes_ns.doc("process_text_to_path")
        @general_processes_ns.expect(general_process_model)
        def post(self):
            """Process text input to find optimal path"""
            data = request.json
            text = data.get("text")
            if not text:
                abort(400, "No text provided")

            try:
                entities = ner_service.extract_entities(text)
            except Exception as e:
                abort(400, f"NER Error: {str(e)}")

            start_name = None
            end_name = None
            intermed_stations = []
            for entity in entities:
                if entity.get("status") == "start":
                    start_name = entity.get("station")
                elif entity.get("status") == "end":
                    end_name = entity.get("station")
                elif entity.get("status") == "intermediate":
                    intermed_stations.append(entity.get("station"))

            if not start_name or not end_name:
                abort(400, "Unable to extract start and end stations from text")
            if not intermed_stations:
                intermed_stations = None
            algorithm = "AStar"

            try:
                result = pathfinding_service.find_path(
                    start_name, end_name, intermed_stations, algorithm
                )
                print("Pathfinding result:", result)
                result["algorithm"] = algorithm
                if "error" in result:
                    abort(400, result["error"])
                return {"entities": entities, "pathfinding_result": result}, 200
            except Exception as e:
                abort(400, f"Pathfinding Error: {str(e)}")

    # --------------------
    # Static File Routes
    # --------------------
    @api.route("/static/<path:filename>", doc=False)
    class StaticFileResource(Resource):
        def get(self, filename):
            """Serve static files (e.g., client-side HTML and JS)"""
            static_folder = current_app.static_folder or "static"
            return send_from_directory(static_folder, filename)

    @api.route("/static/maps/<path:filename>", doc=False)
    class StaticMapResource(Resource):
        def get(self, filename):
            """Serve map files."""
            static_folder = os.path.join(current_app.static_folder or "static", "maps")
            return send_from_directory(static_folder, filename)
