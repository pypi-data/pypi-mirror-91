VIVP - Verilog Package Manager 
A simple package manager for all your verilog projects

Installing

Install with pip (python>=3.6):

$ pip install git+https://github.com/AdityaNG/VIVP.git


Creating a Verilog Package

cd into the desired directory run the following; you will be prompted to enter your package Name, list of Authors and an optional remote URL

$ vivp -s .   # setup

To install dependencies : 
$ vivp -i https://github.com/...

To remove dependencies : 
$ vivp -i https://github.com/...

All dependencies are stored at `project_directory/.vpackage/repos/`

Contributing
If you see something that you know you can help fix or implement, do contact me at :
1. Mail : adityang5@gmail.com
2. Discord : to be added

License

This software is released under the [GNU GPL v3 license](LICENSE).