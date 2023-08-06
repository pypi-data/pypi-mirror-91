# Created by Jan Rummens at 3/12/2020
from nemonet.engines.graph import Graph
from nemonet.engines.sequencer import Sequences
from nemonet.seleniumwebdriver.commands import Command
from nemonet.screencast.recording import ScreenRecorder
from selenium import webdriver
import json
import time

selenium_config = {
    "driver": {
        "headless": False,
        "browser": "chrome",
        "type": "selenium"
    },
    "recording": {
        "switch": False
    }
}

class TestDriver:

    def open(self):
        pass

    def close(self):
        pass

class ChromeTestDriver( TestDriver ):

    def __init__(self):
        self.driver = None

    def open(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def close(self):
        self.driver.close()

    def get_native_driver(self):
        return self.driver


class Runner( object ):

    def __init__( self, runner_config=None):
        self.data = None
        self.driver = None

        if runner_config == None:
            self.data = selenium_config
        else:
            with open(runner_config, 'r') as fp:
                self.data = json.load(fp)

        assert list( self.data.keys() ) == ['driver', 'recording']
        assert list( self.data["driver"].keys() ) == ['headless', 'browser', 'type']
        assert list( self.data["recording"].keys()) == ['switch']

        if self.data["driver"]["type"] == "selenium":
            if self.data["driver"]["browser"] == "chrome":
                self.driver = ChromeTestDriver()
                self.driver.open()

    def turn_on_recording(self):
        if not self.is_recording:
            self.screenrecording.start()
            self.is_recording = True
            time.sleep(0.25)

    def turn_off_recording(self):
        if self.is_recording:
            self.screenrecording.stop()
            time.sleep(0.25)

    def execute_scenario(self, xml_files_name):
        if self.data["recording"]['switch']:
            self.is_recording = False
            self.screenrecording = ScreenRecorder()
            self.turn_on_recording()
        graph = Graph()
        graph.build(xml_files_name)
        seqences = Sequences(graph)
        commands = Command(self.driver.get_native_driver())
        commands.executeSequences(seqences, graph)
        self.driver.close()
