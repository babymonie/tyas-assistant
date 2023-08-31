import pyaudio
import numpy as np
import speech_recognition as sr
import pywinauto
import datetime
import webbrowser
import math
import json

with open("config.json") as config_file:
    config = json.load(config_file)

LANGUAGE = config.get("language", "en-US")
CHUNK = config.get("chunk_size", 300)
RATE = config.get("rate", 13000)
PREFIX = config.get("prefix", "")

COMMAND_TIMEOUT = 10

p = pyaudio.PyAudio()
COMMANDS = {
    "close": "Close the program.",
    "exit": "Close the program.",
    "pause": "Pause the program.",
    "resume": "Resume the program.",
    "panic": "Switch windows (Alt-Tab).",
    "what day is it": "Display the current day.",
    "what year is it": "Display the current year.",
    "what month is it": "Display the current month.",
    "what day of the week is it": "Display the current day of the week.",
    "what is the date": "Display the current date.",
    "what time is it": "Display the current time.",
    "what time is it in": "Search for the time in a different location.",
    "google": "Search on Google.",
    "youtube": "Search on YouTube.",
    "go to": "Navigate to a website.",
    "netflix": "Search on Netflix.",
    "what's my calendar for today": "Open Google Calendar for today.",
    "what's my calendar for tomorrow": "Open Google Calendar for tomorrow.",
    "what's my calendar for this week": "Open Google Calendar for this week.",
    "what's my calendar for next week": "Open Google Calendar for next week.",
    "play from spotify": "Search and play on Spotify.",
    "say the n word": "Display a message.",
    "say the f word": "Display a message.",
    "say the b word": "Display a message.",
    "china accident": "Display a message.",
    "math": "Perform basic arithmetic calculations.",
    "solve root": "Find the square root of a number.",
    "solve cube root": "Find the cube root of a number.",
    "commands": "Display the list of available commands.",
    "send message": "Send a message.",
}

sp_lg = ["en-US", "en-GB", "en-CA", "en-IN", "en-AU", "en-NZ"]


def change_chunk_size(new_chunk_size):
    global CHUNK
    CHUNK = new_chunk_size
    print(f"Chunk size set to: {CHUNK}")


def change_rate(new_rate):
    global RATE
    RATE = new_rate
    print(f"Rate set to: {RATE}")


def change_prefix(new_prefix):
    global PREFIX
    PREFIX = new_prefix
    print(f"Prefix set to: '{PREFIX}'")


def list_microphones():
    print("Available microphones:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        print(f"Device {i}: {info['name']}")


def choose_microphone():
    while True:
        mic_number = input(
            "Enter the number of the microphone you want to use (or 'q' to quit): "
        )
        if mic_number.lower() == "q":
            return None
        try:
            mic_index = int(mic_number)
            if 0 <= mic_index < p.get_device_count():
                return mic_index
            else:
                print("Invalid microphone number. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


list_microphones()
mic_index = choose_microphone()

while mic_index is not None:
    info = p.get_device_info_by_index(mic_index)
    print(f"Using microphone: {info['name']}")
    if PREFIX:
        print(f"Using prefix: '{PREFIX}'")
    else:
        print("No prefix specified.")

    recognizer = sr.Recognizer()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        input_device_index=mic_index,
        frames_per_buffer=CHUNK,
    )

    while True:
        data = stream.read(CHUNK)
        audio_samples = np.frombuffer(data, dtype=np.int16)

        with sr.Microphone(device_index=mic_index) as source:
            print("Listening for command...")
            audio = recognizer.listen(source, timeout=COMMAND_TIMEOUT)

        try:
            # get the language from the config file and check if it is valid if not then use the default language
            if config.get("language", "en-US") in sp_lg:
                command = recognizer.recognize_google(
                    audio, language=config.get("language", "en-US")
                ).lower()
            if command.startswith(PREFIX):
                # Remove the prefix from the command
                command = command[len(PREFIX) :]

                print(f"Command detected: {command}")

                if "close" in command:
                    print("Closing the program.")
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    exit()
                elif "exit" in command:
                    print("Closing the program.")
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    exit()
                elif "pause" in command:
                    print("Pausing the program.")
                    stream.stop_stream()
                elif "resume" in command:
                    print("Resuming the program.")
                    stream.start_stream()
                elif "panic" in command:
                    print("Panic detected. Switching windows (Alt-Tab)...")
                    pywinauto.keyboard.send_keys("%{TAB}", pause=0)
                elif "what day is it" in command:
                    current_time = datetime.datetime.now()
                    day = current_time.day

                    print(f"It is the {day}th of the month.")

                elif "what year is it" in command:
                    current_time = datetime.datetime.now()
                    year = current_time.year

                    print(f"It is {year}.")

                elif "what month is it" in command:
                    current_time = datetime.datetime.now()
                    month = current_time.month

                    print(f"It is {month}.")

                elif "what day of the week is it" in command:
                    current_time = datetime.datetime.now()
                    weekday = current_time.weekday()

                    print(f"It is {weekday}.")

                elif "what is the date" in command:
                    current_time = datetime.datetime.now()
                    day = current_time.day
                    month = current_time.month
                    year = current_time.year

                    print(f"It is {day}/{month}/{year}.")

                elif "what time is it" in command:
                    current_time = datetime.datetime.now()
                    hour = current_time.hour
                    minute = current_time.minute

                    print(f"It is {hour}:{minute}.")

                elif "what time is it in" in command:
                    print("Opening Google...")

                    pywinauto.keyboard.send_keys(
                        "https://www.google.com/search?q="
                        + command.replace("what time is it in", ""),
                        pause=0,
                    )

                elif "google" in command:
                    print("Opening Google...")
                    webbrowser.open(
                        "https://www.google.com/search?q="
                        + command.replace("google", "")
                    )

                elif "youtube" in command:
                    print("Opening YouTube...")
                    webbrowser.open(
                        "https://www.youtube.com/results?search_query="
                        + command.replace("youtube", "")
                    )
                elif "go to" in command:
                    print(
                        "Opening "
                        + command.replace("go to", "").replace(" ", "")
                        + "..."
                    )
                    # remove spaces
                    webbrowser.open(
                        "https://" + command.replace("go to", "").replace(" ", "")
                    )

                elif "netflix" in command:
                    print("Opening Netflix...")
                    webbrowser.open(
                        "https://www.netflix.com/search?q="
                        + command.replace("netflix", "")
                    )

                elif "what's my calender for today" in command:
                    print("Opening Google Calender...")
                    current_time = datetime.datetime.now()
                    webbrowser.open(
                        "https://calendar.google.com/calendar/u/0/r/day/"
                        + str(current_time.year)
                        + "/"
                        + str(current_time.month)
                        + "/"
                        + str(current_time.day)
                        + "?tab=mc&pli=1"
                    )

                elif "what's my calendar for tomorrow" in command:
                    print("Opening Google Calender...")
                    current_time = datetime.datetime.now()
                    # if day is 31 then just go to 1st of next month
                    if current_time.day == 31:
                        day = 1
                        month = current_time.month + 1
                    else:
                        day = current_time.day + 1
                        month = current_time.month
                    webbrowser.open(
                        "https://calendar.google.com/calendar/u/0/day/"
                        + str(current_time.year)
                        + "/"
                        + str(current_time.month)
                        + "/"
                        + str(day)
                        + "?tab=mc&pli=1"
                    )

                elif "what's my calendar for this week" in command:
                    print("Opening Google Calender...")
                    current_time = datetime.datetime.now()
                    # if day is 31 then just go to 6th of next month
                    if current_time.day == 31:
                        day = 6
                        month = current_time.month + 1
                    else:
                        day = current_time.day + 6
                        month = current_time.month

                    webbrowser.open(
                        "https://calendar.google.com/calendar/u/0/r/day/"
                        + str(current_time.year)
                        + "/"
                        + str(current_time.month)
                        + "/"
                        + str(day)
                        + "?tab=mc&pli=1"
                    )

                elif "what's my calendar for next week" in command:
                    print("Opening Google Calender...")
                    current_time = datetime.datetime.now()
                    # if day is 31 then just go to 13th of next month
                    if current_time.day == 31:
                        day = 13
                        month = current_time.month + 1
                    else:
                        day = current_time.day + 13
                        month = current_time.month

                    webbrowser.open(
                        "https://calendar.google.com/calendar/u/0/r/day/"
                        + str(current_time.year)
                        + "/"
                        + str(current_time.month)
                        + "/"
                        + str(day)
                        + "?tab=mc&pli=1"
                    )

                elif "play from spotify" in command:
                    print("Opening Spotify...")
                    webbrowser.open(
                        "https://open.spotify.com/search/"
                        + command.replace("play from spotify", "")
                    )

                elif "say the n word" in command:
                    print("One N word coming right up!")
                    # This word was copy pasted from the internet because Im not a racist and I dont want to say it out loud or type it

                    pywinauto.keyboard.send_keys(
                        "Sike, you thought", with_spaces=True, pause=0
                    )

                elif "say the f word" in command:
                    print("One F word coming right up!")
                    # This word was copy pasted from the internet because Im not a racist and I dont want to say it out loud or type it

                    pywinauto.keyboard.send_keys(
                        "Woah Calm Down Jamal don't pull out the 9",
                        with_spaces=True,
                        pause=0,
                    )

                elif "say the b word" in command:
                    print(
                        "One B word coming right up! I hope you are not a feminist or else you will get offended"
                    )

                    pywinauto.keyboard.send_keys("Baby", with_spaces=True, pause=0)

                elif "china accident" in command:
                    print(
                        "Woah That Chinese person is really being annoying. Let me help you out with that"
                    )

                    pywinauto.keyboard.send_keys(
                        "动态网自由门 天安門 天安门 法輪功 李洪志 Free Tibet 六四天安門事件 The Tiananmen Square protests of 1989 天安門大屠殺 The Tiananmen Square Massacre 反右派鬥爭 The Anti-Rightist Struggle 大躍進政策 The Great Leap Forward 文化大革命 The Great Proletarian Cultural Revolution 人權 Human Rights 民運 Democratization 自由 Freedom 獨立 Independence 多黨制 Multi-party system 台灣 臺灣 Taiwan Formosa 中華民國 Republic of China 西藏 土伯特 唐古特 Tibet 達賴喇嘛 Dalai Lama 法輪功 Falun Dafa 新疆維吾爾自治區 The Xinjiang Uyghur Autonomous Region 諾貝爾和平獎 Nobel Peace Prize 劉暁波 Liu Xiaobo 民主 言論 思想 反共 反革命 抗議 運動 騷亂 暴亂 騷擾 擾亂 抗暴 平反 維權 示威游行 李洪志 法輪大法 大法弟子 強制斷種 強制堕胎 民族淨化 人體實驗 肅清 胡耀邦 趙紫陽 魏京生 王丹 還政於民 和平演變 激流中國 北京之春 大紀元時報 九評論共産黨 獨裁 專制 壓制 統一 監視 鎮壓 迫害 侵略 掠奪 破壞 拷問 屠殺 活摘器官 誘拐 買賣人口 遊進 走私 毒品 賣淫 春畫 賭博 六合彩 天安門 天安门 法輪功 李洪志 Winnie the Pooh 劉曉波动态网自由门",
                        with_spaces=True,
                        pause=0,
                    )

                elif "math" in command:
                    # convert the symbols to the ones that python can understand like * for multiply and / for divide and etc
                    command = command.replace("x", "*")
                    command = command.replace("÷", "/")
                    command = command.replace("plus", "+")
                    command = command.replace("minus", "-")
                    command = command.replace("times", "*")
                    command = command.replace("divided by", "/")
                    command = command.replace("to the power of", "**")
                    command = command.replace("power of", "**")
                    command = command.replace("power", "**")

                    pywinauto.keyboard.send_keys(
                        str(eval(command.replace("math", ""))), with_spaces=True
                    )

                    print(
                        "Solved! Did you see the answer? make sure you have selected something to type in like a text box or something and try again"
                    )

                elif "commands" in command:
                    print("Available commands:")
                    for cmd, description in COMMANDS.items():
                        print(f"- {cmd}: {description}")

                elif "solve square root" in command:
                    # Extract the number to find the square root of
                    number_to_sqrt = command.replace("solve square root", "").replace(
                        "of", ""
                    )
                    try:
                        number = float(number_to_sqrt)
                        sqrt_result = math.sqrt(number)
                        print(
                            f"Solved! The square root of {number} is {sqrt_result:.2f}"
                        )
                    except ValueError as e:
                        print("Invalid input. Please provide a valid number." + str(e))

                elif "solve cube root" in command:
                    # Extract the number to find the cube root of
                    number_to_cbrt = command.replace("solve cube root", "").replace(
                        "of", ""
                    )
                    try:
                        number = float(number_to_cbrt)
                        cbrt_result = math.pow(number, 1 / 3)
                        print(f"Solved! The cube root of {number} is {cbrt_result:.2f}")

                    except ValueError:
                        print("Invalid input. Please provide a valid number.")
                elif "send message" in command:
                    print("Sending message...")
                    pywinauto.keyboard.send_keys(
                        command.replace("send message", ""), with_spaces=True, pause=0
                    )

                    pywinauto.keyboard.send_keys("{ENTER}", pause=0)

            else:
                print("Unrecognized command or missing prefix.")
        except sr.UnknownValueError:
            print("No command detected.")
        except sr.RequestError as e:
            print(
                f"Could not request results from Google Speech Recognition service; {e}"
            )

    list_microphones()
    mic_index = choose_microphone()

print("Exiting the program.")
