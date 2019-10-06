# the-two-planets
A command line app to show the battle between two armies.

This command line app was developed and tested in the below environment:

OS: Linux
	Distribution: Fedora release 30 (Thirty)

Python Version: 3.7.3

Though this might work in any Linux distro, using the above Python version is recommended.

__________________________

How to run the test cases:
	cd into the parent folder of this project (i.e, 'the-the-two-planets') and run the below command.
		python3.7 -B -m unittest discover -s tests -t .

__________________________

How to run the program:
	Run the the_two_planets.py file in the_two_planets folder
	Example:
		python3.7 -B the_two_planets/the_two_planets.py

__________________________

Continuous Integration:
	CircleCi along with GitHub are used to handle dependencies, build, test and deploy the changes.
	When a change is made and pushed, it automatically triggers the test and build processes.

	You can find this project in GitHub here: https://github.com/sh3ll3y/the-two-planets
	Recent build and test jobs in CircleCI have been successful and they can be seen here: https://circleci.com/gh/sh3ll3y/the-two-planets
