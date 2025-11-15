
# The GBA's framerate. GBI runs at this exact framerate.
framerate = 59.727500569606
# GBI's TAS system uses audio samples, running at 4096 Hz. Divided by 1000, we get milliseconds.
samples = 4.096
# The milliseconds a frame approximately takes.
frame = 1000/framerate
# The milliseconds from the moment GBI begins counting, until the game starts running, assuming there's 0 frames of delay for Latios in EUR Sapphire.
frame_zero = 2618
# GBI tracks button presses/releases in this exact order, using two bytes. Each button is represented by a bit. e.g. $0001 presses A, then releases all other buttons.
buttons = ("RButton", "LButton", "Right", "Left", "Down", "Up", "Start", "Select", "BButton", "AButton")
# The current state of the buttons in a TAS. It starts at 0 (all buttons released), and will be converted to hex as required
buttons_state = 0
# Since RSE have a static seed (on dead battery for RS, always for E) we can use the same intro. This one was used for an Italian Sapphire TAS, but should work just fine for the rest.
rse_intro = """00008535 0001
0000870F 0000
00009054 0001
000091C0 0000
000096FC 0001
00009899 0000
0000B642 0001
0000B758 0000
0000C92F 0001
0000CA6B 0000
0000D020 0001
0000D191 0000
"""
# The number of frames an encounter is delayed by.
delay = {
        "latias": 286,
        "latios": 313,
        "beldum": 50,
        "wynaut": 51
        }

# The earliest sample from which we'll take inputs in RSE after loading our save. (FRLG has the Previously... section)
first_actionable_sample = 60193

def frame_to_ms(target): # Converts target frame to milliseconds
    return frame_zero + (target * frame)

def samples_to_ms(time): # Converts from GBI samples to milliseconds, rounded to the nearest integer.
    return round(time / samples)

def ms_to_samples(time): # Converts from milliseconds to GBI samples.
    return time * samples

def button_to_bits(button): # Converts button state to be pressed to its hex representation
    return int(str(pow(10, len(buttons) - 1 - buttons.index(button))), 2)

def flip_button(button, current_input = 0): # Presses or releases button, basically an XOR
    return button_to_bits(button) ^ current_input

def press_button(time, button, current_input = 0): # Presses and releases a button, assuming no other buttons were being held. The time inserted here must be in samples.
    return "{}\n{}\n".format(
    (format(round(time), "08X") + " " + format(flip_button(button, current_input), "04X")),
    (format(round(time + 5*frame), "08X") + " " + "0000"))