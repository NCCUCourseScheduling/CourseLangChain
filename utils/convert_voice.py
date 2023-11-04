import whisper
import struct
import threading
import wave

from pvrecorder import PvRecorder 

recorder = PvRecorder(device_index=-1, frame_length=512)

wavfile = wave.open("test_output.wav", "w")
wavfile.setparams((1, 2, recorder.sample_rate, recorder.frame_length, "NONE", "NONE"))

recording = True

def record_voice():
   global recording
   try:  
      recorder.start()
      print("recording...")
      print("Enter \"stop\" to stop recording and convert to text...")
      
      while recording:  
         frame = recorder.read()
         wavfile.writeframes(struct.pack("h" * len(frame), *frame))

   except KeyboardInterrupt:
      # print("stoping...")
      recorder.stop()
      wavfile.close()

   finally:
      recorder.stop()
      wavfile.close()
      recorder.delete()


def convert_voice():
   global recording
   model = whisper.load_model("base")
   record_thread = threading.Thread(target=record_voice)
   record_thread.daemon = True
   record_thread.start()

   try:
      if input("") == "stop":
         recording = False

   except KeyboardInterrupt:
      pass

   # recording = False
   record_thread.join()
   wavfile.close()
   result = model.transcribe("test_output.wav")
   # print(result["text"])

   return result["text"]