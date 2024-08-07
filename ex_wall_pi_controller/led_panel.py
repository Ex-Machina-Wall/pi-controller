from ex_wall_pi_controller.image_handling.image_handler import ImageHandler
from ex_wall_pi_controller.effects import TwoColorRandom, ImageEffect, AudioEffect
from ex_wall_pi_controller.http_listener import HTTPListener
from ex_wall_pi_controller.frame import Frames

from ex_wall_frame_transmitter import FrameTransmitter
from ex_wall_frame_transmitter.constants import NUM_PIXELS
from time import sleep, perf_counter
import logging
import struct
from decouple import config


class Panel:
    NUM_PIXELS = 73
    TARGET_FRAME_TIME = 1/40

    def __init__(self):
        self.logger = logging.getLogger("Panel")
        self.frame_transmitter = FrameTransmitter(destination_uri=config("DESTINATION_URI"))
        self.frame_transmitter.start()
        self.ntfy_listener = HTTPListener()
        self.ntfy_listener.start_thread()
        self.image_handler = ImageHandler()
        self.effects_list = [
            ImageEffect(),
            TwoColorRandom()
        ]
        self.modifiers_list = [
            AudioEffect()
        ]
        self.accepted_commands = {
            "SET_ARDUINO_PGAIN": self.set_arduino_p_gain
        }
        self.arduino_ramp_rate = 10

    def handle_commands(self):
        """
        Get the commands out of the NTFY listener
        and pass them on to the effects that need them
        """
        # Get commands out of ntfy listener
        commands = self.ntfy_listener.get_queue()

        # iterate through the commands
        for command in commands:

            # Iterate through each effect we have
            # check if they listen to that command
            for effect in self.effects_list + self.modifiers_list:
                for accepted_command in effect.accepted_commands:
                    if accepted_command in command:
                        # If an effect listens to one of those commands
                        # pass it on in the relevant function
                        effect.accepted_commands[accepted_command](command)

            # Check if any of the commands are for this panel directly
            #  rather than the effects
            for accepted_command in self.accepted_commands:
                if accepted_command in command:
                    self.accepted_commands[accepted_command](command)

            # for accepted_command in self.audio_effect.accepted_commands:
            #     if accepted_command in command:
            #         self.audio_effect.accepted_commands[accepted_command](command)

    def set_arduino_p_gain(self, command: str):
        """
        This is a command handler
        In each message there is a gain param for how quickly the arduino
        should reach the target color
        Parse the command and se
        """
        try:
            ramp_rate = int(command.split("-")[1])
            self.arduino_ramp_rate = ramp_rate
            self.logger.info(f"Ramp rate Updated to: {ramp_rate}")
        except Exception as e:
            self.logger.error("Failed to parse Arduino P Gain Command")
            self.logger.error(f"'{command}' was not a valid command. '{e}'")
            self.logger.debug("Setting Arduino P Gain to default value of 20")
            self.arduino_ramp_rate = 20

    def run(self):
        while True:
            start_time = perf_counter()
            # Handle all the latest commands that have arrived from NTFY server
            self.handle_commands()

            # Create a single frame from all the frame generators
            frame = Frames(
                frames=[effect.get_frame() for effect in self.effects_list]
            )
  
            # Let the frame modifiers modify the total frame
            for modifier in self.modifiers_list:
                frame = modifier.get_frame(current_frame=frame.pixel_array)

            # Turn the frame into the LED string data
            end_time = perf_counter()

            # Generate binary payload and send over the websocket
            self.frame_transmitter.send_numpy_frame(pid_gain=self.arduino_ramp_rate, np_frame=frame.pixel_array)

            duration = end_time - start_time
            # self.logger.debug(f"Frame Time: {duration:.4f}s")
            if duration < self.TARGET_FRAME_TIME:
                sleep(self.TARGET_FRAME_TIME - duration)

    def power_down(self):
        self.logger.info("Attempting to power down")
        self.ntfy_listener.stop_thread()
