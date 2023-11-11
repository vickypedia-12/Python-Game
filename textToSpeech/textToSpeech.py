from gtts import gTTS

text = "Hello guys, How are you? I am fine, thankyou!"

language = 'en'

obj = gTTS(text = text, lang  = language , slow = False)

obj.save("textToSpeech.mp3")