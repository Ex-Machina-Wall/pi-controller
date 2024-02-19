from ex_wall_pi_controller.constants import complement
from ex_wall_pi_controller.frame import Frame
from ex_wall_pi_controller.constants import complement, convert_incoming_color
from ex_wall_pi_controller.effects.abstract_effect import Effect
from ex_wall_audio_reactor.audio_effect import AudioEffect as AudioEffectProcessing
import numpy as np

class AudioEffect(Effect):
    PEAK_AMPLITUDE = 170000
    PEAK_BASS_AMPLITUDE = 300000

    def __init__(self):
        super().__init__()
        self.audio_effect_processor = AudioEffectProcessing()
        self.accepted_commands = {
            "SET_HIGH_FREQUENCY_REACT_STATE": self.set_frequency_react_state,
            "SET_LOW_FREQUENCY_REACT_STATE": self.set_frequency_react_state,
            "SET_HIGH_FREQUENCY_THRESHOLD": self.set_freq_threshold,
            "SET_LOW_FREQUENCY_THRESHOLD": self.set_freq_threshold,
            "SET_PRIMARY_COLOR": self.set_color,
            # "SET_SECONDARY_COLOR": self.set_color,
            "SET_PRIMARY_BRIGHTNESS": self.set_brightness
        }

    """ Incoming command Handlers """

    def set_freq_threshold(self, command: str):
        variable_mapping = {
            "SET_HIGH_FREQUENCY_THRESHOLD": "high_frequency_threshold",
            "SET_LOW_FREQUENCY_THRESHOLD": "low_frequency_threshold"
        }
        try:
            thresh_type, value = command.split("-")
            value = int(value)
            setattr(self.audio_effect_processor, variable_mapping[thresh_type], value)
            self.logger.info(f"Set {variable_mapping[thresh_type]} to {value}")
        except Exception as e:
            self.logger.error(e)
            self.audio_effect_processor.high_frequency_threshold = 170000
            self.audio_effect_processor.low_frequency_threshold = 300000

    def set_brightness(self, command: str):
        try:
            split_command = command.split("-")
            self.audio_effect_processor.brightness = int(split_command[1])
            self.logger.info(f"React Brightness Set: {self.audio_effect_processor.brightness}")
        except Exception as e:
            self.logger.error(e)
            self.audio_effect_processor.brightness = 100

    def set_frequency_react_state(self, command: str):
        variable_mapping = {
            "SET_HIGH_FREQUENCY_REACT_STATE": "high_frequency_react_state",
            "SET_LOW_FREQUENCY_REACT_STATE": "low_frequency_react_state"
        }
        try:
            thresh_type, state = command.split("-")
            state = state == "ON"
            setattr(self.audio_effect_processor, variable_mapping[thresh_type], state)
            self.logger.info(f"Set {variable_mapping[thresh_type]} to {state}")
        except Exception as e:
            self.logger.error(e)
            self.audio_effect_processor.high_frequency_react_state = False
            self.audio_effect_processor.low_frequency_react_state = False

    def set_color(self, command: str):
        variable_mapping = {
            "SET_PRIMARY_COLOR": "primary_color",
            "SET_SECONDARY_COLOR": "primary_color"
        }
        try:
            command, r, g, b = command.split('-')
            r, g, b = convert_incoming_color(r, g, b)
            setattr(self.audio_effect_processor, variable_mapping[command], (r, g, b))
            self.logger.info(f"{variable_mapping[command]}: {(r, g, b)}")
        except Exception as e:
            self.logger.error(e)
            self.audio_effect_processor.secondary_color = (0, 0, 255)
            self.audio_effect_processor.primary_color = (255, 0, 0)
        
        # May want to remove this
        self.audio_effect_processor.secondary_color = complement(*self.audio_effect_processor.primary_color)

    def get_frame(self, current_frame: np.array = None) -> Frame:
        frame = self.audio_effect_processor.get_frame(current_frame=current_frame)
        return Frame(frame)
    