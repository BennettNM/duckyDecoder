# duckyDecoder
The 'Ducky Decoder' program was created to allow a user to take programs written for 'ducky' devices, convert the code into a human readable format, allowing the user to see exactly what the program is designed to do (what actions it will perform on the target system). Additionally, the 'Ducky Decoder' will also allow the user to make changes to the ducky code such as editing existing code, however, it is NOT designed to allow the user to extend the code, so actions such as 'adding additional lines to the code' are out of scope of this program.

A couple of importaint notes: in order for this program to work, the 'Ducky-Decode.json' file is REQUIRED as it contontains the dictionary used to translate operational codes to human readable text, and reverse the process.

There are two main steps needed to use the Ducky Decoder:

Step 1: provide the program with a binary file that contains ducky code (normally called 'inject.bin'). This can be done in two different ways. 

First, it can be passed through as part of calling the program from the command line 'Python duckyDecode.py [name of file including extension]', Second, the user can provide the full path inside the program itself, when prompted to do so, and it will attempt to open the file. 

It should be noted here that the Ducky Decoder will also create a backup of the original file in the home directory (if possible) in a file called ducky_backup as a precautionary step in case the file is altered. (this will be overwritten in any subsequent uses of the program)

Step 2: Select what the user would like to do with the file. There are several options available to the user such as: 
Viewing the human readable version of the ducky program on the screen (option 1).
 
Viewing the ducky operational codes for the program (option 2).

Edit the ducky code, meaning, the user can make actual changes to the code that exists within the program, from a human input level. This includes changing both strings and instructions. This option also includes the ability to present the list of available instructions to the user by entering '-dhelp' WARNING: instructions MUST be entered in capital letters (option 3), 

Remove any changes by restoring to the originally provided file (option 4).

Output the ducky code (as a working '.bin' file) and the human readable code for the program (as a '.txt' file) (option 5).

Finally, terminate the program (option 6 or q).

The program will offer the user the chance to quit or return to the main menu after each of the options has been completed (and will also clear the screen), meaning that the user can view the code, then choose to make changes, then output the files, etc.

Explanation of each option:

Option 1: This option will present the human readable format of the code to the user, allowing them to gain an understanding as to what the program is designed to do or accomplish on the target system.

Option 2: This option allows the user to see the actual operational codes that the Ducky device will use (as the operational codes are flipped from the middle out when used)

Option 3: This option allows the user to change one or many lines within the code, changing instructions or strings as required (for example changing the string 'one' to 'two') but still allowing the program to work. (if required) **NOTE** when entering instructions (a list of instructions is provided by entering 'help') these MUST be entered in UPPERCASE (e.g. DELAY 100, not delay 100)

Option 4: This option allows the user to return to the originally created file, then returns to the menu to allow the user to continue.

Option 5: This option allows the user to output a working '.bin' file of the program and a '.txt' file containing the human readable version of the code, into a file of the users choosing (or the current working directory) 

Option 6: This option terminates the program.

Additionally, there are multiple functions that allow this program to work, each of these can be called externally, if required, by importing the program into other code, then calling the functions required. (If doing this, please be sure to read the code and understand what the functions require to be passed into them)
