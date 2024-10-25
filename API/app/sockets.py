from flask_socketio import emit
from .services import stt_service, ner_service, pathfinding_service

def register_socket_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        emit('response', {'message': 'Connected to WebSocket!'})

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
        
    @socketio.on('start_process')
    def handle_start_process_event(data):
        """
        Handle 'start_process' event.
        Expects binary audio data, processes it, and emits the result.
        """
        try:
            audio_bytes = data 
            transcript = stt_service.process_audio_file(audio_bytes)
            entities = ner_service.extract_entities(transcript)
            path = pathfinding_service.find_path(entities)
            emit('pathfinding_response', {'path': path})
        except Exception as e:
            emit('error', {'message': str(e)})


    @socketio.on('stt')
    def handle_stt_event(data):
        """
        Handle Speech-to-Text events.
        Expects audio data and returns transcribed text.
        """
        audio_data = data.get('audio')
        transcript = stt_service.process_audio(audio_data)
        emit('stt_response', {'transcript': transcript})

    @socketio.on('ner')
    def handle_ner_event(data):
        """
        Handle Named Entity Recognition events.
        Expects text data and returns extracted entities.
        """
        text = data.get('text')
        entities = ner_service.extract_entities(text)
        emit('ner_response', {'entities': entities})

    @socketio.on('pathfinding')
    def handle_pathfinding_event(data):
        """
        Handle pathfinding events.
        Expects start and end points and returns the optimal path.
        """
        start = data.get('start')
        end = data.get('end')
        path = pathfinding_service.find_path(start, end)
        emit('pathfinding_response', {'path': path})
