from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import speech_recognition as sr
import time
import pyttsx3

# Set up the webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Set up text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    print("Only one voice available, using default voice.")

# Set up speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def speak(query):
    engine.say(query)
    engine.runAndWait()


def recognize_speech():
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    response = ""
    speak("Identifying speech..")
    try:
        response = recognizer.recognize_google(audio)
        print(f"Recognized: {response}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        response = "Error"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        response = "Error"
    return response


def open_new_tab(url):
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])


# Main program
time.sleep(3)
speak("Hello Chetan")

while True:
    speak("How can I help you?")
    voice = recognize_speech().lower()
    print(f"Command: {voice}")

    if 'open google' in voice:
        speak('Opening google..')
        open_new_tab('https://google.com')
    elif 'search google' in voice:
        while True:
            speak('I am listening..')
            query = recognize_speech()
            if query != 'Error':
                break
        element = driver.find_element(By.NAME, 'q')
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'open youtube' in voice:
        speak('Opening youtube..')
        open_new_tab('https://youtube.com')
    elif 'search youtube' in voice:
        while True:
            speak('I am listening..')
            query = recognize_speech()
            if query != 'Error':
                break
        element = driver.find_element(By.NAME, 'search_query')
        element.clear()
        element.send_keys(query)
        element.send_keys(Keys.RETURN)
    elif 'switch tab' in voice:
        num_tabs = len(driver.window_handles)
        cur_tab = (driver.window_handles.index(driver.current_window_handle) + 1) % num_tabs
        driver.switch_to.window(driver.window_handles[cur_tab])
    elif 'close tab' in voice:
        speak('Closing Tab..')
        driver.close()
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[-1])
        else:
            break
    elif 'go back' in voice:
        driver.back()
    elif 'go forward' in voice:
        driver.forward()
    elif 'exit' in voice:
        speak('Goodbye Master!')
        driver.quit()
        break
    else:
        speak('Not a valid command. Please try again.')
    time.sleep(2)
