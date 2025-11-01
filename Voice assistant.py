import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget, QInputDialog, QMessageBox, QGridLayout, QDialog, QLineEdit, QDialogButtonBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtCore import QObject, pyqtSignal
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import warnings
import datetime
import time
import pywhatkit as kit
import requests
from bs4 import BeautifulSoup
#import psutil
import calendar

warnings.filterwarnings("ignore")

# Initialize pyttsx3
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[0].id)  # 1 for female and 0 for male voice

user_name = None

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish_me():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = f"Hello {user_name}, Good Morning"
        log_emitter.log_updated.emit(greeting)
        speak(greeting)
    elif 12 <= hour < 18:
        greeting = f"Hello {user_name}, Good Afternoon"
        log_emitter.log_updated.emit(greeting)
        speak(greeting)
    else:
        greeting = f"Hello {user_name}, Good Evening"
        log_emitter.log_updated.emit(greeting)
        speak(greeting)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        log_emitter.log_updated.emit("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        log_emitter.log_updated.emit("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        log_emitter.log_updated.emit(f"User said: {query}\n")
    except Exception as e:
        log_emitter.log_updated.emit(f"Error: {e}\n")
        speak("I didn't understand")
        return "None"
    return query

def get_news():
    url = "https://timesofindia.indiatimes.com/home/headlines"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    headlines = soup.find_all('span', {'class': 'w_tle'})
    
    news_list = []
    for headline in headlines[:5]:  # Get the first 5 headlines
        news_list.append(headline.text.strip())
    
    return news_list

def read_news():
    news_list = get_news()
    for i, news in enumerate(news_list, 1):
        log_emitter.log_updated.emit(f"News {i}: {news}")
        speak(f"News {i}: {news}")

'''def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    system_info = f"CPU usage is at {cpu_usage}%. Memory usage is at {memory_info.percent}%. Disk usage is at {disk_info.percent}%."
    log_emitter.log_updated.emit(system_info)
    speak(system_info)
    elif 'system info' in query:
            get_system_info()
    '''

def tell_date():
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    log_emitter.log_updated.emit(f"Today's date is: {current_date}")
    speak(f"Today's date is {current_date}")

def show_calendar(month=None, year=None):
    if month is None or year is None:
        now = datetime.datetime.now()
        month = now.month
        year = now.year
    
    cal = calendar.TextCalendar(calendar.SUNDAY)
    cal_str = cal.formatmonth(year, month)
    
    log_emitter.log_updated.emit(f"Calendar for {calendar.month_name[month]} {year}:\n{cal_str}")
    speak(f"Here is the calendar for {calendar.month_name[month]} {year}")
    print(cal_str)


def run_assistant():
    wish_me()
    log_emitter.log_updated.emit("Loading your personal voice assistant Amigo")
    speak("Loading your personal voice assistant Amigo")
    log_emitter.log_updated.emit("Amigo assistance activated")
    speak("Amigo assistance activated")
    speak(f"How can I help you, {user_name}?")
    speak("I can help you with certain tasks such as getting information from Wikipedia, opening YouTube, Google, GitHub, Chrome browser, Amazon shopping, playing multimedia, BMSIT website, VTU website, VS Code, playing music, reading news headlines and even opening storage disks from your device.")
    while True:
        query = take_command().lower()
        if 'wikipedia' in query:
            speak("Searching Wikipedia ...")
            query = query.replace("wikipedia", '')
            try:
                results = wikipedia.summary(query, sentences=5)
                speak("According to Wikipedia")
                log_emitter.log_updated.emit(results)
                speak(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak("Sorry, your query is ambiguous. Please provide more details.")
                log_emitter.log_updated.emit(f"DisambiguationError: {e}")
            except wikipedia.exceptions.PageError as e:
                speak("Sorry, I couldn't find any information on that.")
                log_emitter.log_updated.emit(f"PageError: {e}")
        elif 'who are you' in query:
            speak("I am Amigo, a voice assistant")
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("google.com")
        elif 'open github' in query:
            speak("Opening GitHub")
            webbrowser.open("github.com")
        elif 'bmsit' in query:
            speak("Opening BMSIT website")
            webbrowser.open("bmsit.ac.in")
        elif 'play music' in query:
            speak("Opening Wynk Music")
            webbrowser.open("wynk.in")
        elif 'amazon shopping' in query:
            speak("Opening amazon shopping")
            webbrowser.open("amazon.in")
        elif 'play' in query:
            song = query.replace('play', "")
            speak("Playing " + song)
            kit.playonyt(song)
        elif 'open chrome' in query:
            speak("Opening Chrome")
            loc = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            os.startfile(loc)
        elif 'search' in query:
            s = query.replace('search', '')
            speak("searching for"+ s)
            kit.search(s)
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"the time is {strTime}")
            log_emitter.log_updated.emit(strTime)
        elif 'open weather' in query:
            speak("Opening weather")
            webbrowser.open("accuweather.com")
        elif 'vtu' in query:
            speak("Opening VTU website")
            webbrowser.open("vtu.ac.in")
        elif 'vs code' in query:
            speak("Opening VS Code")
            loc = r'C:\Users\Surajkrishnan\AppData\Local\Programs\Microsoft VS Code\Code.exe'
            os.startfile(loc)
        elif 'c drive' in query:
            speak("Opening Local Disk C")
            os.startfile("C://")
        elif 'e drive' in query:
            speak("Opening Local Disk E")
            os.startfile("E://")
        elif 'date' in query:
            tell_date()
        elif 'calendar' in query:
            month = None
            year = None
            # Extract month name and year from query if specified
            if 'for' in query:
                try:
                    parts = query.split('for')[-1].strip().split()
                    if len(parts) == 2:
                        month_name = parts[0].capitalize()
                        year = int(parts[1])
                        month = list(calendar.month_name).index(month_name)
                except ValueError:
                    speak("Please specify the month and year correctly, for example: 'calendar for March 2024'.")
                    log_emitter.log_updated.emit("Error in parsing month/year for calendar.")
            show_calendar(month, year)
        elif 'news' in query:
            speak("Fetching the latest news")
            webbrowser.open_new_tab("timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India, happy reading')
            read_news()
            time.sleep(10)
        elif "goodbye" in query or "ok bye" in query or "stop" in query or "exit" in query:
            log_emitter.log_updated.emit(f'Your personal assistant Amigo is shutting down. Goodbye {user_name}!')
            speak(f'Your personal assistant Amigo is shutting down. Goodbye {user_name}!')
            break

class AssistantThread(QThread):
    def run(self):
        run_assistant()

class LogEmitter(QObject):
    log_updated = pyqtSignal(str)

log_emitter = LogEmitter()

class UserNameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("User Name")
        self.setGeometry(400, 300, 300, 100)  # Set the geometry for the dialog

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Please enter your name:", self)
        self.layout.addWidget(self.label)

        self.textbox = QLineEdit(self)
        self.layout.addWidget(self.textbox)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_name(self):
        return self.textbox.text()

class AmigoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AMIGO - Your Personal Voice Assistant")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowState(Qt.WindowMaximized)

        self.bg_label = QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setPixmap(QPixmap("wallpaperflare.com_wallpaper.jpg").scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.content_frame = QWidget(self.central_widget)
        self.content_frame.setGeometry(int(self.width() * 0.125), int(self.height() * 0.1), int(self.width() * 0.75), int(self.height() * 0.8))
        self.content_frame.setStyleSheet("background: rgba(46, 63, 79, 150); border-radius: 10px;")

        self.layout = QVBoxLayout(self.content_frame)

        self.title_label = QLabel("AMIGO - Voice Assistant", self.content_frame)
        self.title_label.setStyleSheet("font-size: 45px; font-weight: bold; color: white;background: none; border-radius: 0px;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        grid_layout = QGridLayout()

        self.start_button = QPushButton("START ASSISSTANT", self.content_frame)
        self.start_button.setStyleSheet("font-size: 20px; background-color: violet; color: white;")
        self.start_button.clicked.connect(self.start_assistant)
        grid_layout.addWidget(self.start_button, 0, 0)

        self.exit_button = QPushButton("EXIT", self.content_frame)
        self.exit_button.setStyleSheet("font-size: 20px; background-color: violet; color: white;")
        self.exit_button.clicked.connect(self.close)
        grid_layout.addWidget(self.exit_button, 0, 1)

        self.console_label = QLabel("CONSOLE OUTPUT", self.content_frame)
        self.console_label.setStyleSheet("font-size: 30px; color: white;background: none; border-radius: 0px;")
        grid_layout.addWidget(self.console_label, 1, 0, 1, 2, alignment=Qt.AlignCenter)

        self.console_text = QTextEdit(self.content_frame)
        self.console_text.setReadOnly(True)
        self.console_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.console_text.setStyleSheet("background-color: rgba(28, 28, 28, 150); color: #e0e0e0; font-family: Courier; font-size: 24px;")
        grid_layout.addWidget(self.console_text, 2, 0, 1, 2)

        self.layout.addLayout(grid_layout)

        global user_name
        dialog = UserNameDialog()
        if dialog.exec_() == QDialog.Accepted:
            user_name = dialog.get_name()
        if not user_name:
            user_name = "User"

        self.assistant_thread = None

        self.resize_event()  # Initial call to set sizes

    def resize_event(self):
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setPixmap(QPixmap("wallpaperflare.com_wallpaper.jpg").scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.content_frame.setGeometry(int(self.width() * 0.125), int(self.height() * 0.1), int(self.width() * 0.75), int(self.height() * 0.8))

    def resizeEvent(self, event):
        self.resize_event()
        super().resizeEvent(event)

    def start_assistant(self):
        try:
            log_emitter.log_updated.disconnect(self.log)  # Disconnect the signal from the log function
        except TypeError:
            pass  # Ignore if the signal was not connected

        self.assistant_thread = AssistantThread()
        self.assistant_thread.start()
        log_emitter.log_updated.connect(self.log)

   
    def log(self, message):
        self.console_text.append(str(message))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', "Do you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def log(message):
    app_instance.log(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_instance = AmigoApp()
    app_instance.show()
    sys.exit(app.exec_())

