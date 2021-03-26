import speech_recognition

def recognize_text():
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone(device_index=1) as audio_file:
        audio_content = recognizer.listen(audio_file)

    return recognizer.recognize_google(audio_content, language="ru-RU")

