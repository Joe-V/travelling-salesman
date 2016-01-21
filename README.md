#Description
This is a basic implementation of [the travelling salesman problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem); a salesman wants to visit a number of cities while travelling the shortest possible distance and finishing in the same city they started in.

This algorithm attempts to find the shortest path by randomly swapping the order in which cities are visited until no shorter path can be found after a certain number of attempts.

# Usage
This is known to work under [Python 3.4.0](https://www.python.org/download/releases/3.4.0/).

The Python script may be run from the command line as follows:

	python main.py <width> <height>

The width and height parameters are optional and specify the dimensions of the field used.

Click *Generate* to create the given number of cities and distribute them on the field at random. The salesman's "home city" is  highlighted in red.

Check the *Toggle swapping* box to begin swapping the order in which these cities are visited to try and minimise the total distance of visiting each one in turn.
