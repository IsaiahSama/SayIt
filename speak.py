import pyttsx3
import time
import os

FEMALE_VOICE = 1
MALE_VOICE = 0
FILE_PATH = "./Script.txt"


def ask_and_quit():
    input("Press enter to exit")
    raise SystemExit

class Engine:
    """Class responsible for the setup and handling of the Text To Speech
    
    Attrs:
        messages (list): List of messages to be read
    Methods:
        setup_engine(): Used to setup the Text To Speech.
        say_and_print(*args): Prints a message to the screen, and says it as well.
        speak(message:str): Stores messages to be output in a queue."""

    messages = []

    def __init__(self) -> None:
        pass

    def setup_engine(self):
        """Sets up the pyttsx3 engine for usage.
        
        Returns the engine"""
        engine = pyttsx3.init()
        
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 200)
        engine.setProperty('voice',voices[MALE_VOICE].id)
        engine.setProperty('volume', 1.0)

        return engine        

    def say_and_print(self, message:str):
        """Used to display a message to the screen, and read it out loud as well.
        
        Args:
            message (str): The message to be displayed and read."""

        print(message)
        self.speak(message)

    def speak(self, message:str):
        """Reads a message from the queue
        
        Args:
            message (str): The message to be read."""

        engine = self.setup_engine()
        engine.say(message)
        engine.runAndWait()
        engine.stop()

class Main:
    """The main class of the program
    
    Attrs:
        engine (Engine): The TTS engine.
        script (list): The script broken into lines
        commands (list): List of commands
        cmd (str): The current command to be run.

    Methods:
        setup(): Used to set up everything the program needs
        run(): Used to run the main program
        is_command(msg:str): Used to check if a line of the script is a command.
        exe_command(msg:str): Used to execute a command."""

    def __init__(self) -> None:
        self.script = None
        self.engine = Engine()
        self.commands = ["wait"]
        self.cmd = None

    def run(self):
        """Used to run the program."""
        self.setup()

        for line in self.script:
            if self.is_command(line):
                self.exe_command(line)
            else:
                self.engine.say_and_print(line)

    def setup(self):
        """Used to setup everything the program needs."""
        if not os.path.exists(FILE_PATH):
            print(f"No `{FILE_PATH}` file was found. Create one then run me again.")
            ask_and_quit()

        with open(FILE_PATH) as fp:
            script = fp.readlines()

        self.script = [line for line in script if not line.startswith("#")]

        if not self.script:
            print("Script file is empty.")
            ask_and_quit()

    def is_command(self, msg:str) -> bool:
        """Used to detect whether a given line of text is a command or not
        
        Args:
            msg (str): The message to check."""
        
        text = msg.split(" ")
        for cmd in self.commands:
            if text[0] == cmd:
                self.cmd = cmd
                return True
        return None

    def exe_command(self, msg:str) -> bool:
        """Used to execute a given command.
        
        Args:
            msg (str): The string containing the command.
        
        Returns:
            Bool"""
        
        # Parsing time.
        if self.cmd == "wait":
            text = msg.split("wait")[1:]
            val = text[-1].strip()
            if not val.isnumeric():
                print(val, "is not a number, so no waiting will be done.")
                return False
            secs = float(val)
            print("Waiting", secs, "seconds")
            time.sleep(secs)


if __name__ == "__main__":
    main = Main()
    main.run()

