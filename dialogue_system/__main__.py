import os
import logging
from concurrent.futures import ThreadPoolExecutor

from .ui import app_kivy
from .controller import Controller

from .input.microphone_thread import Microphone, DEFAULT_RATE

from .speech_recognition.google_speech_rec import GoogleSpeechRecognizer
from .speech_recognition.async_speech_rec import AsyncSpeechRecognizer

from .input.video_thread import VideoInput
from .emotion_recognition.video_recognition import Emo_VideoRecognizer

from .smart_body.smart_body import SmartBody
from .smart_body.unity_body import UnityBody
from .agent.agent_queue import Agent
from .gesture import gs_utils
from .gesture.gesture_manager import GestureManager

import config as cfg


logger = logging.getLogger().getChild(__package__)


if __name__ == '__main__':
    os.environ["KIVY_NO_CONSOLELOG"] = "1"
    from kivy.logger import Logger
    from kivy.config import Config
    Logger.setLevel(logging.INFO)
    Config.set('kivy', 'log_dir', 'D:\\kivy_logs\\')

    logger.info('\nagent: %s \nuser: %s', cfg.agent, cfg.user)


    with ThreadPoolExecutor() as executor:
        speech_recognizer = GoogleSpeechRecognizer(sample_rate_hertz=DEFAULT_RATE)

        async_speech_recognizer = AsyncSpeechRecognizer(
            executor=executor,
            recognizer=speech_recognizer)

        video_input = VideoInput(executor)
        video_emotion_recognizer = Emo_VideoRecognizer()

        gesture_db, gesture_categories, emotion_categories, au_categories = gs_utils.load_gesture_dbs(cfg.agent['body'])
        gesture_manager = GestureManager(gesture_db, gesture_categories, emotion_categories, au_categories)
		 

        with \
                Microphone(executor) as microphone, \
                SmartBody() if cfg.agent['body'] == 'smartbody' else UnityBody() as character, \
                Agent(character, gesture_manager) as agent, \
                Controller(
                    agent=agent,
                    microphone=microphone,
                    speech_recognizer=async_speech_recognizer,
                    video_input=video_input,
                    video_emotion_recognizer=video_emotion_recognizer,
                    gesture_manager=gesture_manager
                ) as controller:
            app_kivy.run(controller)
