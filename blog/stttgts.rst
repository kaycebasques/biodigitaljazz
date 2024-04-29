.. _STTTGTS:

==================================
Speech To Text To Gemini To Speech
==================================

*2024 Feb 8*

.. raw:: html

   <iframe style="width: 100%; aspect-ratio: 560 / 315;" 
           src="https://www.youtube.com/embed/endL2syBwh0"
           title="jeff" frameborder="0" allow="encrypted-media; web-share"
           allowfullscreen></iframe>

.. code-block:: python


   # setup instructions are at the bottom

   import os
   import random
   import subprocess
   import threading
   import time
   
   import dotenv
   import gpiozero  # gpiozero is good people https://gpiozero.readthedocs.io
   from google.cloud import speech  # will need to go through the rigmarole of creating
                                    # a project, enabling billing, etc.
   import google.generativeai as gemini  # it's actually super easy to tinker on gemini
                                         # now e.g. no google cloud setup stuff required
                                         # https://ai.google.dev/tutorials/python_quickstart
   
   os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '...'  # Absolute path to service acct JSON file
   env = dotenv.dotenv_values('.env')
   gemini.configure(api_key=env['GEMINI_API_KEY'])
   model = gemini.GenerativeModel('gemini-pro')
   
   # https://projects.raspberrypi.org/en/projects/physical-computing/5
   button = gpiozero.Button(2)
   audio_file = 'user.flac'
   led = gpiozero.RGBLED(16, 20, 21)
   
   # https://codelabs.developers.google.com/codelabs/cloud-speech-text-python3#3
   # https://cloud.google.com/speech-to-text/docs/sync-recognize
   def speech_to_text():
       client = speech.SpeechClient()
       with open(audio_file, 'rb') as f:
           content = f.read()
       config = speech.RecognitionConfig(
           language_code='en',
           encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
           sample_rate_hertz=48000,
           audio_channel_count=2
       )
       audio = speech.RecognitionAudio(content=content)
       response = client.recognize(config=config, audio=audio)
       transcript = ''
       # full transcript is weirdly fragmented across this iterable thing...
       for result in response.results:
           transcript += result.alternatives[0].transcript
       return transcript
   
   def record():
       led.on()
       led.color = (1, 0, 0)  # red
       # start the audio recording
       process = subprocess.Popen(['rec', audio_file, 'rate', '48k'])
       # https://unix.stackexchange.com/a/57593
       while not stop_recording.is_set():
           time.sleep(1)
       process.terminate()
       led.off()
   
   def thinky_blinky():
       """blink like an octopus dreaming... https://youtu.be/0vKCLJZbytU"""
       colors = [
           (0, 0, 0),
           (1, 0, 0),
           (1, 1, 0),
           (1, 0, 1),
           (0, 1, 0),
           (0, 1, 1),
           (1, 1, 1)
       ]
       led.on()
       while not stop_blinking.is_set():
           led.color = random.choice(colors)
           time.sleep(0.1)
       led.off()
   
   while True:
       button.wait_for_press()
       stop_recording = threading.Event()
       record_thread = threading.Thread(target=record)
       record_thread.start()
       button.wait_for_release()
       stop_recording.set()
       record_thread.join()
       stop_blinking = threading.Event()
       blink_thread = threading.Thread(target=thinky_blinky)
       blink_thread.start()
       # subprocess.run(['play', '-v', '3.0', audio_file])
       text = speech_to_text()
       print(text)
       response = model.generate_content(text)
       print(response.text)
       stop_blinking.set()
       blink_thread.join()
       led.on()
       led.color = (0, 0.2, 1)  # blueish
       # yes, i'm aware that there are now uncanny valley TTS services,
       # i like my old school friendly robot voice thank you very much
       p = subprocess.Popen(['spd-say', '--wait', '--volume', '+100', f'"{response.text}"'])
       while p.poll() is None:
           time.sleep(1)
       led.off()

   """
   ##### SETUP #####
   ----------------------------------------------------------
   using the rinkydink sparkfun usb microphone dingle dongle and speaker:
   https://www.sparkfun.com/products/18488
   https://www.sparkfun.com/products/18343
   don't think the mic or speaker required any setup...
   just plugged them in and Stuff Just Worked...

   --------------------------------------------
   create .env and put Gemini API key there:
   GEMINI_API_KEY=...

   ----------------------------------------------------
   create requirements.txt and put these deps in there:
   gpiozero==2.0
   RPi.GPIO==0.7.1
   google-cloud-speech==2.24.1
   google-generativeai==0.3.2
   python-dotenv==1.0.1

   ------------------------------------------
   install the above deps into a virtual env:
   python3 -m venv venv
   source venv/bin/activate  # remember to do this before running the app too
   python3 -m pip install -r requirements.txt

   -------------------------------
   install these libs system-wide:
   sudo apt install -y sox  # audio recording command (`rec`)
   sudo apt install -y speech-dispatcher  # text-to-speech command (`spd-say`)
   wget http://abyz.me.uk/lg/lg.zip   # https://abyz.me.uk/lg/download.html
   unzip lg.zip
   cd lg  # low-level GPIO lib used by gpiozero (I think)
   make
   sudo make install
   """
