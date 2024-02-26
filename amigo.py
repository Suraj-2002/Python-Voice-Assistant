import pyttsx3
import speech_recognition as sr
import wikipedia
from wikipedia.exceptions import DisambiguationError
import webbrowser
import os
import warnings
warnings.filterwarnings("ignore")

# init pyttsx
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

engine.setProperty('voice', voices[1].id)  # 1 for female and 0 for male voice


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said:" + query + "\n")
    except Exception as e:
        print(e)
        speak("I didnt understand")
        return "None"
    return query


if __name__ == '__main__':

    speak("Amigo assistance activated ")
    speak("How can i help you")
    while True:
        query = take_command().lower()
        if 'wikipedia' in query:
            speak("Searching Wikipedia ...")
            query = query.replace("wikipedia", '').strip()
            if query:  # Check if the query is not empty
                try:
                    results = wikipedia.summary(query, sentences=2)
                except DisambiguationError as e:
                    # Present the options to the user
                    speak("There are multiple possibilities for '{}'. Options are: {}".format(query, ', '.join(e.options)))
                    # Ask the user to choose one of the options
                    choice = take_command().lower()
                    if choice in e.options:
                        results = wikipedia.summary(choice, sentences=2)
                    else:
                        speak("That's not a valid option. Please try again.")
                        continue
                except wikipedia.exceptions.PageError as e:
                    speak("The page you requested could not be found.")
                    continue  # Continue the loop to accept a new command
                else:
                    results = wikipedia.summary(query, sentences=2)
                speak("According to wikipedia")
                speak(results)
            else:
                speak("Please provide a valid search term.")
        elif 'are you' in query:
            speak("I am amigo developed by Jaspreet Singh")
        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")
        elif 'open github' in query:
            speak("opening github")
            webbrowser.open("github.com")
        elif 'open stack overflow' in query:
            speak("opening stack overflow")
            webbrowser.open("stackoverflow.com")
        elif 'open spotify' in query:
            speak("opening spotify")
            webbrowser.open("spotify.com")
        elif 'open whatsapp' in query:
            speak("opening whatsapp")
            loc =  r'C:\\Users\\jaspr\\AppData\\Local\\WhatsApp\\WhatsApp.exe'
            os.startfile(loc)
        elif 'play music' in query:
            speak("opening music")
            webbrowser.open("spotify.com")
        elif 'local disk d' in query:
            speak("opening local disk D")
            webbrowser.open("D://")
        elif 'local disk c' in query:
            speak("opening local disk C")
            webbrowser.open("C://")
        elif 'local disk e' in query:
            speak("opening local disk E")
            webbrowser.open("E://")
        elif 'sleep' in query:
            exit(0)
