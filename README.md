pyinventory
===========

if you’d like to help out, hop on over to GitHub and send us a pull request!

Windows installation
--------------------

pyinventory is an inventory and billing software developed using python3.2 tkinter and sqlite3. You need only python3x software installed on windows to run this. tkinter and sqlite3 modules are built in python3.x so no need to install these packages


Linux Installation
------------------

For linux os:

Install Python3 Tkinter Package:

	$ sudo apt-get install python3-tk

Run the app:

	$ cd pyinventory
    $ python3 main.py

Demo
----

![demo](https://raw.github.com/suhailvs/pyinventory/master/demo.gif)

Screenshots
-----------

![screeshot1][logo1]

![screeshot2][logo2]

![screeshot3][logo3]


[logo1]: https://raw.github.com/suhailvs/pyinventory/master/images/screenshots/screenshot1.jpg
[logo2]: https://raw.github.com/suhailvs/pyinventory/master/images/screenshots/screenshot2.jpg
[logo3]: https://raw.github.com/suhailvs/pyinventory/master/images/screenshots/screenshot3.jpg


Make Ubuntu Executable file
---------------------------

	pip install pyinstaller
	pyinstaller main.py --onefile
	cp -r images dist/
	./dist/main