# Overview

This project was an excersize in developing a simple game with added music, sound effects, and movable objects used by keyboard inputs, as well as user interface elements.

This is a simple game based off of a pc game from my childhood. You are an aircraft on a 2d screen that can move using WASD and fire missles with the spacebar to defeat enemies coming from the top to the bottom.

This software was a test of my knowledge of abstraction in Python (this was done using pygame). Each object is intialized using a class with unique attributes and behaviors, as well as handling input with live code.

Youtube demonstration of code

[Software Demo Video](https://www.youtube.com/watch?v=wen7oPDahzY)

# Development Environment

I used the pygame library to create the game with Python code, and used Visual Studio Code to write and edit the code itself. To learn the basics and syntax of the pygame library, I used ChatGPT.

# Useful Websites

* [ChatGPT](https://chatgpt.com)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* Item 1: I have a bug where if you are firing missiles as other ones hit an enemy, explosions are produced where the new missiles are spawning.
* Item 2: Some enemies spawn to the right of the window, probably due to initializing them with their topleft attribute.
* Item 3: The sound files can be tweaked. The missiles produce a really loud sound effect that kind of masks everything else when they are being fired continuosly.
