#!/usr/bin/python
# -*- coding: utf-8 -*-
# Description: 
# Created: lei.cheng 2021/10/10
# Modified: lei.cheng 2021/10/10
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import speech_recognition
import subprocess
import platform


class VoiceChatBot(ChatBot):

    def speak(self, text):
        if platform.system() == 'Darwin':
            # Use Mac's built-in say command to speak the response
            cmd = ['say', str(text)]

            subprocess.call(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        else:
            subprocess.run(
                'echo "' + str(text) + '" | festival --tts',
                shell=True
            )

    def get_response(self, statement=None, **kwargs):
        response = super().get_response(statement, **kwargs)
        print("Bot:>", response)

        self.speak(response.text)


bot = VoiceChatBot('Example ChatBot')

trainer = ChatterBotCorpusTrainer(bot)

# Train the chat bot with the entire english corpus
# trainer.train('chatterbot.corpus.english')
trainer.train('chatterbot.corpus.chinese')


recognizer = speech_recognition.Recognizer()

while True:
    try:
        with speech_recognition.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            recognizer_function = getattr(recognizer, 'recognize_google')

            result = recognizer_function(audio)

            print("You:>", result)
            bot.get_response(text=result)

    except speech_recognition.UnknownValueError:
        bot.speak('I am sorry, I could not understand that.')
    except speech_recognition.RequestError as e:
        message = 'My speech recognition service has failed. {0}'
        bot.speak(message.format(e))
    except (KeyboardInterrupt, EOFError, SystemExit):
        # Press ctrl-c or ctrl-d on the keyboard to exit
        break
