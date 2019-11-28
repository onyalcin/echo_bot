import logging
import functools

from .dialogue import text_normalization
from .dialogue.sentence_preparation import SentenceParser
from .empathy_mechanism.empathy_mechanism import Empathy

logger = logging.getLogger().getChild(__name__)


class Controller:
    def __init__(self, agent, microphone, speech_recognizer,
                 video_input, video_emotion_recognizer,
                 gesture_manager):
        self._microphone = microphone
        self._microphone_task = None

        self._speech_recognizer = speech_recognizer

        self._video_input = video_input
        self._video_emotion_recognizer = video_emotion_recognizer

        self._microphone_thread = None
        self._speech_rec_thread = None

        self._agent = agent

        self._gesture_manager = gesture_manager
        self._empathy_mechanisms = Empathy()

        self._sentence_parser = SentenceParser()

    def __enter__(self):
        self._microphone.__enter__()
        self._video_input.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._microphone.__exit__(exc_type, exc_val, exc_tb)
        self._video_input.__exit__(exc_type, exc_val, exc_tb)
        pass

    def process_text_input(self, text):
        self._on_input(text)

    def start_listening(self):
        if self._microphone_task:
            return

        logger.info('Starting to listen')
        self._agent.transition_listening()

        speech_rec_task = self._speech_recognizer.start(
            callback=self._on_speec_rec_result)

        self._microphone_task = self._microphone.enable(
            callback=functools.partial(self._on_microphone_data, speech_rec_task))

        self._video_input.start(
            callback=self._on_frame)

    def stop_listening(self):
        if not self._microphone_task:
            return

        logger.info('Stopping to listen')

        self._microphone_task.disable()
        self._microphone_task = None

        self._video_input.stop()

        self._agent.transition_thinking()

    def start_face_match(self):
        logger.info('Starting to face match')
        self._video_input.start(
            callback=self._on_frame)

    def stop_face_match(self):
        logger.info('Stopping to face match')
        self._video_input.stop()

    def _on_microphone_data(self, sr_task, chunk, final):
        logger.debug('Audio chunk received, final: %s', final)
        sr_task.submit(chunk, final)
        # TODO: add another task submission to the audio emo rec or pause detection queue
        return True

    def _on_speec_rec_result(self, rec_result):
        logger.debug('Speech recognition result received')
        if rec_result.final:
            self._on_input(rec_result.transcript)

    def _on_frame(self, frame):
        emotions = self._video_emotion_recognizer.recognize(frame)
        emotion, value = self._empathy_mechanisms.affect_match(emotions)
        logger.info("EMOTION RECOGNITION RESULTS: %s, %s", emotion, value)
        if emotion is not None:
            bml_list = self._gesture_manager.return_emotion_bml_list(emotion, amount=value)
            self._agent.send_bml(bml_list)

    def _on_input(self, text):
        logger.info('Echoing input: %s', text)
        clean_query = text_normalization.clean(text)

        bml_response = self._get_bml_response(clean_query)
        logger.debug('Bml response: %s', bml_response)

        self._agent.transition_speaking(bml_response)

    def _get_bml_response(self, response, mood=None):
        parsed_response = self._sentence_parser.parse_sent(response, expressiveness=0.3)
        bml_response = self._gesture_manager.get_bml_speech_response(parsed_response, mood)
        return bml_response
