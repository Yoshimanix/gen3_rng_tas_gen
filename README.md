# Pokémon Gen 3 RNG TAS Generator

## What the hey is this?

This is a web app for creating TAS files compatible with the Game Boy Interface.
With this, you can do RNG manipulation on a retail copy of a main series Generation 3 Pokémon game, without any of the trial and error needed!

## What do I need to use this?

You will need a homebrew-capable Nintendo GameCube, a Game Boy Player attached to it, and the main series Generation 3 Pokémon game of your choice. 

## Which games is this compatible with?

Currently, it's compatible with Ruby, Sapphire, and Emerald. Support for Fire Red and Leaf Green is planned in the future.

(This tool has been tested with English Ruby and Italian Sapphire so far, but it should work for all Hoenn games in all languages.)

## Which encounter types are TASable in this way?

Currently, the following encounters have been implemented.

- Beldum (Gift in Mossdeep City)
- Latios and Latias (Southern Island, requires Eon Ticket to access)
- Wynaut Egg (Gift in Lavaridge City)

## How do I use this?

To run the code:
- Clone this repository
- Install Python if you haven't yet
- Open a command prompt in the repository's directory
- Run `pip install -r requirements.txt`
- Run `python run.py`
- Visit `http://127.0.0.1:5000` with the web browser of your choice

Now, fill out the form in the web page, then hit `Generate!` to create a TAS file.
The `gbi_movie.txt` that will be downloaded should be placed in the `GBI/` directory of the SD card in your Nintendo GameCube.
Afterwards, you need to create a .cli file with the same filename as your GBI executable, for example `gbi.cli`.
If you already have one, add a command parameter, as seen in the below example:

```
--format=ntsc,no-border
--movie=./gbi_movie.txt
--
```

## What prep work should I do with my save file?

Generally, you should prepare your save file the same way you would if you were to RNG manip manually. To specify per method:

For static encounters, save in a spot where you need one input to trigger the encounter. (e.g. the A Button for Deoxys).

(The rest have yet to be implemented, so stay tuned!)

~~For the Kanto starters, save in front of the Poke Ball of the desired Pokémon.~~

~~For the Hoenn starters, save in front of Prof. Birch's bag, and use the "Desired Hoenn Starter" option to select which one you want.~~

~~For Field Move encounters, ensure your lead Pokémon (which you must specify in "Field Move User") can use your desired field move,
then save in front of a boulder for Rock Smash, or in tall grass, a cave, or in water for Sweet Scent.~~

## What is the "Field Move User" field for?

When using a field move such as Rock Smash or Sweet Scent, the Pokémon's cry is played after the last input before the encounter.
This causes the Encounter Frame to be offset by the time it takes for the cry to play out. Use this option to choose the user of the field move.
Make sure this Pokémon is in the lead of your party.

## What is the "Desired Hoenn Starter" field for?

In Ruby, Sapphire, and Emerald, when selecting Prof. Birch's bag at the start of the game, the player is placed into a unique UI for selecting their starter Pokémon.
With this option, the extra optional input is added for selecting either Treecko or Mudkip, since the game defaults to Torchic.

## RNG Manipulation? What's that?

I recommend checking [this website](www.retailrng.com) for more info!

## How is this even possible?

Basically, the Game Boy Interface has the capability to run movie files.
The intended function of this is to verify tool-assisted speedruns on real hardware.
I simply learned how the format of the movie files works, and figured out how to make custom movie files without an emulator.
This web app was made to simplify and streamline this process.
The source code of this web app should give you further info on how this was done.

## I'd like to contribute to this project, or use it in my own project.

You're more than welcome! The whole point of this project is to be used by everyone.
