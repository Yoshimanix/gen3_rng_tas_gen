from flask import Flask, request, send_file
import pyvibe as pv
from io import BytesIO
import tas_generator

app = Flask(__name__)
pagename = "Pokémon Gen 3 RNG TAS Generator"


@app.route('/')
def index():
    page = pv.Page(pagename, navbar=None, footer=None)

    with page.add_card() as card:
        card.add_header(pagename, 3)
        with card.add_form(action="generate?") as form:
            form.add_formhidden("version", "RSE")
            form.add_formtext("Encounter Frame", "frame", "42069")
            form.add_formselect("Encounter Type", "encounter", [
                {'value': 'wynaut', 'label': 'Wynaut'},
                {'value': 'beldum', 'label': 'Beldum'},
                {'value': 'latios', 'label': 'Latios'},
                {'value': 'latias', 'label': 'Latias'},
                {'value': 'sweetscent', 'label': 'Field Move'}])
            form.add_formselect("Field Move User", "fieldmoveuser", ["TODO: Add every single Pokémon", "Oddish"])
            form.add_formselect("Desired Hoenn Starter", "hoennstarter", ["Treecko", "Torchic", "Mudkip", "Johto"])
            form.add_formsubmit("Generate!")
        
        """
        with card.add_form(action="generate?") as form:
            form.add_formselect("Game Language", "language", [{'value': 'ENG', 'label': 'English'}, {'value': 'JPN', 'label': 'Japanese'}, {'value': 'EUR', 'label': 'European'}])
            form.add_formselect("Game Version", "version", [{'value': 'RSE', 'label': 'Ruby, Sapphire, Emerald'}, {'value': 'FR10', 'label': 'Fire Red 1.0'}, {'value': 'FR11', 'label': 'Fire Red 1.1'}, {'value': 'LG', 'label': 'Leaf Green'}])
            form.add_formtext("Initial Seed", "seed", "B00B")
            form.add_formtext("Encounter Frame", "frame", "42069")
            form.add_formselect("Encounter Type", "encounter", ["Starters", "Lugia", "Ho-Oh", "Deoxys", "Field Move"])
            form.add_formselect("Field Move User", "fieldmoveuser", ["TODO: Add every single Pokémon", "Oddish"])
            form.add_formselect("Desired Hoenn Starter", "hoennstarter", ["Treecko", "Torchic", "Mudkip", "Johto"])
            form.add_formsubmit("Generate!")
        """
        
    
    with page.add_card() as card2:
        card2.add_header("What the hey is this?", 3)
        card2.add_text("""This is a web app for creating TAS files compatible with the Game Boy Interface.
        With this, you can do RNG manipulation on a retail copy of a main series Generation 3 Pokémon game, without any of the trial and error needed!""")
        card2.add_divider()
        card2.add_header("What do I need to use this?", 3)
        card2.add_text("You will need a homebrew-capable Nintendo GameCube, a Game Boy Player attached to it, and the main series Generation 3 Pokémon game of your choice.")
        card2.add_divider()
        card2.add_header("How do I use this?", 3)
        card2.add_text("""
        First, fill out the form above, then hit \"Generate!\" to create a TAS file.
        The gbi_movie.txt that will be downloaded should be placed in the GBI/ directory of the SD card in your Nintendo GameCube.
        Afterwards, you need to create a .cli file with the same filename as your GBI executable, for example \"gbi.cli\".
        If you already have one, add a command parameter, as seen in the below example:""")
        card2.add_code("""
--format=ntsc,no-border
--movie=./gbi_movie.TXT
--
""")
        card2.add_divider()
        card2.add_header("What prep work should I do with my save file?", 3)
        card2.add_text("""
        Generally, you should prepare your save file the same way you would if you were to RNG manip manually.
        To specify per method:""")
        card2.add_text("For static encounters, save in a spot where you need one input to trigger the encounter. (e.g. the A Button for Deoxys).")
        card2.add_text("For the Kanto starters, save in front of the Poke Ball of the desired Pokémon.")
        card2.add_text("For the Hoenn starters, save in front of Prof. Birch's bag, and use the \"Desired Hoenn Starter\" option to select which one you want. The \"Johto\" option in the list is for the Johto starters given when you complete your Pokedex, where you save in front of your desired starter.")
        card2.add_text("For Field Move encounters, ensure your lead Pokémon (which you must specify in \"Field Move User\") can use your desired field move, then save in front of a boulder for Rock Smash, or in tall grass, a cave, or in water for Sweet Scent.")
        card2.add_divider()
        card2.add_header("What is the \"Field Move User\" field for?", 3)
        card2.add_text("""
        When using a field move such as Rock Smash or Sweet Scent, the Pokémon's cry is played after the last input before the encounter.
        This causes the Encounter Frame to be offset by the time it takes for the cry to play out.
        Use this option to choose the user of the field move. Make sure this Pokémon is in the lead of your party.""")
        card2.add_divider()
        card2.add_header("What is the \"Desired Hoenn Starter\" field for?", 3)
        card2.add_text("""
        In Ruby, Sapphire, and Emerald, when selecting Prof. Birch's bag at the start of the game,
        the player is placed into a unique UI for selecting their starter Pokémon.
        With this option, the extra optional input is added for selecting either Treecko or Mudkip, since the game defaults to Torchic. If you're instead going for a Johto starter, use the \"Johto\" option.""")
        card2.add_divider()
        card2.add_header("RNG Manipulation? What's that?", 3)
        card2.add_text("I recommend checking the website in the link below for more info!")
        card2.add_link("www.retailrng.com", "https://retailrng.com/")
        card2.add_divider()
        card2.add_header("How is this even possible?", 3)
        card2.add_text("""
        Basically, the Game Boy Interface has the capability to run movie files.
        The intended function of this is to verify tool-assisted speedruns on real hardware.
        I simply learned how the format of the movie files works, and figured out how to make custom movie files without an emulator.
        This web app was made to simplify and streamline this process.
        The source code of this web app should give you further info on how this was done.
        """)
    
    # Returns the page, with some manual patches, because PyVibe is finicky...
    # Basically forces dark mode, replaces the favicon, and makes the Initial Seed optional, since RSE don't require it.
    # I should've picked some other library for the frontend, but I can't be bothered. So long as the backend works...
    return page.to_html().replace("<html>", '<html class="dark">').replace("""
    <link rel="apple-touch-icon" sizes="180x180" href="https://cdn.pycob.com/pyvibe/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="https://cdn.pycob.com/pyvibe/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="https://cdn.pycob.com/pyvibe/favicon-16x16.png">
    <link rel="mask-icon" href="https://cdn.pycob.com/pyvibe/safari-pinned-tab.svg" color="#5bbad5">
    <link rel="shortcut icon" href="https://cdn.pycob.com/pyvibe/favicon.ico">""", """
    <link rel="icon" href="https://archives.bulbagarden.net/media/upload/d/dd/Spr_2s_129_s.png" type="image/x-icon">
    <link rel="shortcut icon" href="https://archives.bulbagarden.net/media/upload/d/dd/Spr_2s_129_s.png" type="image/x-icon">""").replace("placeholder=\"B00B\" required", "placeholder=\"B00B\"")

@app.route('/generate')
def generate_movie():
    # Grab URL arguments
    version = request.args.get("version")
    frame = int(request.args.get("frame"))
    encounter = request.args.get("encounter")
    
    # Initialize movie
    output = ""
    
    match version:
        case "RSE":
            output += tas_generator.rse_intro
        case "FRLG":
            pass # Placeholder
        case _:
            return index() #Failsafe
    
    time = tas_generator.frame_to_ms(frame)
    time = tas_generator.ms_to_samples(time)
    
    delay = tas_generator.delay[encounter]*tas_generator.frame
    if delay == None:
        delay = 0
    else:
        delay = tas_generator.ms_to_samples(delay)
    
    match encounter:
        case "latios":
            output += tas_generator.press_button(time-delay, "AButton")
        case "latias":
            output += tas_generator.press_button(time-delay, "AButton")
        case "beldum":
            # We interact with the Poke Ball.
            output += tas_generator.press_button(tas_generator.first_actionable_sample, "AButton")
            # PLAYER checked the POKe BALL.
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096, "AButton")
            # It contained the POKeMON BELDUM.
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096*2, "AButton")
            # Take the POKe BALL? YES/NO (Encounter frame)
            output += tas_generator.press_button(time-delay, "AButton")
        case "wynaut":
            # We interact with the old lady.
            output += tas_generator.press_button(tas_generator.first_actionable_sample, "AButton")
            # I have here an EGG.
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096, "AButton")
            # I'd hoped to hatch it by covering it in
            # hot sand by the hot springs.
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096*3, "AButton")
            # But that doesn't seem to be enough...
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096*4, "AButton")
            # I've heard it would be best if it were
            # kept together with POKeMON and
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096*6, "AButton")
            # carried about.
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096*7, "AButton")
            # You are a TRAINER, yes?
            # And your POKeMON radiate vitality.
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096*9, "AButton")
            # So what say you?
            # Will you take this EGG to hatch? YES/NO
            output += tas_generator.press_button(tas_generator.first_actionable_sample + 4096*11, "AButton")
            # Good! I hope you walk plenty with
            # this here EGG!
            output += tas_generator.press_button(time-delay, "AButton")
        case _:
            return index()
    
    # Return the processed movie as a .txt file to be played on a GBI.
    file = BytesIO(output.encode("UTF-8"))
    return send_file(
        file,
        mimetype="text/plain",
        as_attachment=True,
        download_name="gbi_movie.txt"
    )

if __name__ == '__main__':
    app.run(debug=True)