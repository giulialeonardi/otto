###############################################################################
#Otto is an emotional robot that answers accordingly to what you say to her
###############################################################################
from lib import record, speech_to_text, tone_analyzer, eyes, output
import threading, Queue
import sys

#calculate ambient silence threshold
silence_threshold=record.get_trs()

#display default eyes
eyes_emotion=Queue.Queue()
eyes_emotion.put("neutral")
eyes_on=Queue.Queue()
eyes_on.put(True)
eyes_thr=threading.Thread(target=eyes.displayEyes, args=(eyes_on, eyes_emotion))
eyes_thr.start()

while (1):
    try:
        #record what user has to say and save to ./records/user-record.wav
        record.detectVoice(silence_threshold)

        #send the audio to the ibm speech-to-text api and get their json response
        transcript=speech_to_text.stt()
        #if noise was recorded, record again
        if (transcript == False): 
            continue

        #use otto-lexicon and ibm tone-analyzer to get the emotion
        emotion=tone_analyzer.getPredominantEmotion(transcript)
	eyes_emotion.put(emotion)
	print("RESTARTANDO THREAD")
	eyes_emotion.put_nowait(emotion)
	print("TAMO VORTANDO AQUI")

        #otto's sound reaction
        output.sound(emotion)

    #terminate threads when keyboard interrupts occur
    except(KeyboardInterrupt, SystemExit):
        print("Wrapping threads up...")
        eyes_on.put(False)
        eyes_thr.join()
        sys.exit()
