import sys
import os
import json
import binascii

#this function is designed to produce a list of hex values to be used later in the program
#The main reason for this, when reading directly out of the file, the values are unusable.
def fileHex(file, inst):
    byte = ''
    hexInfo = []
    counter = 0

    #transfer the unusable values into a hex string
    if inst == 'decode':
        hexEncoded = binascii.hexlify(file).decode('utf-8')

        #convert the string of hex values into a usbale list. 
        for i in hexEncoded:
            byte += i
            counter += 1
            if counter == 4:
                hexInfo.append(byte)
                counter = 0
                byte = ''
                
    elif inst == 'encode':
        hexInfo = binascii.unhexlify(file)      
            
    return hexInfo
    

#this function is designed to take the readable text, previously created,
#and return it to a form that can be converted to hex codes, meaning that
#all quality of life revisions are removed. (e.g. changing SPACE to ' ')
def recode(condensedList, dictionary):
    wordList = []
    finalList = []
    for w,x in dictionary.items(): #create a list for ensuring that items entered exist in what can be actioned.
        wordList.append(w)
        
    for h,i in enumerate(condensedList): #recreate the full list
        if i in wordList or i == '00ff':
            finalList.append(i)
            
        else:
            if 'REPEAT' in i: #decompress the 'arrow' revisions made prior
                arrow = condensedList[h-1]#locate what type of 'arrow' it is
                repeatCounter = int(i.replace('REPEAT ', ''))
                while repeatCounter != 0:
                    finalList.append(arrow)
                    repeatCounter -= 1
            else:
                stringList = list(i)#strings contained within the program are converted to a list, to be used later
                                
                for z in stringList:#ensure that correct information is entered to the list, replacing ' ' with SPACE or appending letters
                    if z == ' ':
                        finalList.append('SPACE')
                    else:
                        finalList.append(z)
                
    return finalList

#this function takes a hex string and convertes it to the ducky standard
#by flipping the first and second characters, as well as the third and fourth
def reverse(hexList):
    reversedList = []
    for i in hexList:#move through the list flipping the text characters
        hexSegment = list(i)
        a = hexSegment[0]
        b = hexSegment[1]
        c = hexSegment[2]
        d = hexSegment[3]
        flippedHex = str(b) + str(a) + str(d) + str(c)
        reversedList.append(flippedHex) #append to the final list
    return reversedList

#this function accepts either HEX codes that have been flipped in the 'reverse'
#function, or text, and matches it against a provided dictionary, in order to
#translate between text and hex codes, it also accepts a 'w' or 'r' instruction
#to determine if it is text to hex or hex to text.
def translate(untranslated, inst, dictionary):
    translated = []
    if inst == 'w': #translates from HEX to text, matched against a dictionary
        for segment in untranslated:
            translated.append(next((word for word, HEX in dictionary.items() if HEX == segment), segment))

    else:
        for segment in untranslated:#translates from text to HEX, matched against a dictionary
            translated.append(next((HEX for word, HEX in dictionary.items() if word == segment), segment))

    return translated

#this function accepts a raw list of text that has been converted directly from code.
#It will then move through the list, making the text more readable. E.g. changing SPACE to ' '.
#Additionally, it will also combine strings within the program to be easily read. 
def combine(rawTextList):
    wordString = ''
    combinedList = []
    arrowCount = 0
    arrowList = ('DOWNARROW', 'UPARROW', 'LEFTARROW', 'RIGHTARROW') #list of all possible arrows
    arrowSelect = ''
    for h,i in enumerate(rawTextList):
        if i == None or i == '': #Skip these instructions as they are not needed
            continue
        
        elif len(i) == 1: #catch point for strings, allows them to be combined.
            wordString += i

        elif i in arrowList:#looking for 'arrow' instructions, adding a counter
            arrowCount +=1
            if arrowSelect == '' :#set the type of arrow. e.g. DOWNARROW
                arrowSelect = i
                
            elif i !=  arrowSelect: #check to see if the arrow type has changed, if it has.
                combinedList.append(arrowSelect) #append the previous arrow to the list
                totalArrowCount = 'REPEAT ' + str(arrowCount -1)
                combinedList.append(totalArrowCount)#append the previous arrow count to the list
                arrowCount = 1 #set new arrow count 
                arrowSelect = i #change to new arrow type. e.g. LEFTARROW
                
            if rawTextList[h+1] not in arrowList: #check to see if the next member of the list is not an 'arrow', if true.
                combinedList.append(arrowSelect)#append the current arrow type to the list
                totalArrowCount = 'REPEAT ' + str(arrowCount -1)
                combinedList.append(totalArrowCount)#append the current arrow count to the list
                arrowCount = 0 #reset the arrow count
                arrowSelect = '' #clear the currently selected arrow.
            continue
            
        elif i == 'SPACE': #check for the word SPACE and change it to ' ' for ease of reading.
            wordString += ' '
            continue
   
        elif len(i) != 1 and wordString != '': #check to see if an instruction or string needs to be added to the list
            combinedList.append(wordString) #add the word string first
            combinedList.append(i) #add the instruction
            wordString = '' #reset the wordstring
            
        elif len(i) != 1: #final check to see if there are any instructions to be added
            combinedList.append(i)#add if required.
            
    return combinedList

#this function writes to both a .bin file and a .txt file, this is only used if the user requests for the code to be recompiled.                
def write(humanText, binaryData, *backup):

    filePlural = 'file'
    written = 0
    nameList = []
    filePath = ''

    if backup[0] == '':
        filePath = input('Enter the desired save file path or press enter to use the current directory:\n' + '>>> ')

    else:
        filePath = '\\Ducky_Backup'

    #if the file path contains text, add a \ to the end of it (to continue the path)
    if filePath != '' and filePath[-1] != '\\':
        filePath += '\\'
        
    #check to make sure that the path provided by the user exists 
    if os.path.exists(filePath) == False:
        try: #if it does, create the folder
            os.mkdir(filePath)
            print('File path has been created:\n' + os.path.abspath(filePath))
            
        except: #if not, create a folder in the current operating directory, and create a folder there.
            fullPath = os.getcwd()
            fullPath += '\\createdOutputFolder\\'
            
            try: #try to make the fall back directory, if it already exists, use it'
                os.mkdir(fullPath)
                print('Unable to create desired folder, folder created at:\n' + 
                      fullPath)
                
            except: #if it fails, use the path
                pass
            
            filePath = fullPath
            
    if humanText != '': #make sure that the text exists
        fileNameText = filePath + 'ducky_text.txt' #create the file
        with open(fileNameText, 'w') as file:
            for i in humanText:
                file.write(i + '\n')#write each part of the list to a new line.
            file.close()

        nameList.append('ducky_text.txt')
        written += 1
            
    #create an inject.bin folder in the required file path
    if backup[0] == True:
        fileNameBin = filePath + 'backup_' + 'inject.bin'
        #print('Backup stored at:', os.path.abspath(fileNameBin))

    else: #if not a backup, set the name as 'inject.bin'
        fileNameBin = filePath + 'inject.bin'
        
    if binaryData != '':    
        with open(fileNameBin, 'wb') as file: #Create the inject.bin file
            file.write(binaryData)
            file.close()

        nameList.append('inject.bin')
        written += 1
        
    #for ease of reading, determine if there are many files or just one file written (and avoid a double up with backup)
        
    if written != 0:
        if written > 1:
            filePlural = 'files'
        print(filePlural, 'written:')
        for l, i in enumerate(nameList):
            print(os.path.abspath(filePath + i))

        print('\n')


#this program is designed to accept an input of a .bin file containing HEX codes for a ducky device.
#once provided, it will convert it into proper ducky format, translate it into a human readable version
#and if the user requested to do so, will convert the file back into a program.
def main():
    fileText = []
    hexlist = []
    printed = 0
    hexString = ''
    fileName = ''
    counter = 0
    eight = ''
    selection = ''

    #open needed files for the program to perform work
    if len(sys.argv) == 2 or fileName == '':
        try:
            fileName = sys.argv[1] #command line argument to set file name

        except:
            if fileName == '':
                fileName = input('Please enter a file name, and extension to open:\n' + '>>> ')

    #try to open the file requested by the user
    while True:
        try:
            fileData = open(fileName, 'rb').read() #open the target and create a backup as the target may be edited.
            print('Creating a backup in the home directory')
            write('', fileData, 1) #create backup in the home directory
            break
        
        except: #prompt user to enter a valid file name if opening fails
            fileName = input('no file found, please enter a valid file, or type "q" to end the program: \n' + '>>> ')
            if fileName == 'q': #allow the user to end the program
                exit()
                
    hexTranslated = fileHex(fileData, 'decode') #translate the file into a usable hex list
    
    file = open('Ducky-Decode.json', 'r') #open Json dictionary to assist with decode and encode process.
    dictionary = json.load(file)
    file.close()
    
    readableList = combine(translate(reverse(hexTranslated), 'w', dictionary)) #precreate the readable list as it is used in many places
    
    #check what actions the user would like to perform with the file.
    while True:
        if selection != '':
            selection = input('Press enter to continue or type "q" to quit:\n' + '>>> ')
            os.system('cls')
            
        if selection == '':
            selection = input('What would you like to do with the file? \n(enter the number for the selection) \n' 
                          'Display the code in human readable form? (1) \n' 
                          'Display the Ducky code for the program? (2) \n' 
                          'Edit the code of the program to add or change functionality? (3) \n'
                          'Restore the orignal file (4) \n'
                          'Save a .bin (binary) and .txt (human readable) version of the program (5) \n'
                          'Exit the program (6) or (q) \n'
                          '>>> ')
                      
        if selection == '1':
            #translation of HEX codes to text
            print('Line numbers represent code lines, any skipped lines are "00ff" instructions')
            for l,i in enumerate(readableList): #display text to the user
                if i != '00ff': #excluding 00ff lines as they do not perform any function for the user.
                    print('line ', str(l + 1) + ': ', i)
                    
            selection = input('Would you like to create a ".txt" document with this information? (y/n)\n' + '>>> ')
            
            if selection == 'y':
                write(readableList, '', False)
             
                

        #this area will only show the 'ducky' version of the hex codes, or more accruratly, how the ducky hardware will read them.
        elif selection == '2':
            duckyText = reverse(hexTranslated)
            for i in duckyText:
                eight += i + ' '
                counter += 1
                if counter == 8:# print in lines of 8 to make it easier to read
                    print(eight)
                    counter = 0
                    eight = ''
                
        #the make and change section, this area shows the actual translated code to the user, and allows them to edit the code at will. ONLY edit, not enter new lines.
        elif selection == '3':
            while True: #print the human readable code, as above
                if printed == 0:
                    for l,i in enumerate(readableList):
                        if i != '00ff':
                            print('line ', str(l+1)+': ', i)

                #allow the user to enter a specific line to be changed        
                changeLine = input('Enter the line number you would like to change:\n' + '>>> ')
                while True:
                    try:
                        changeLine = int(changeLine) #make sure that the entered input is a number 
                        if changeLine > len(readableList): #make sure that the entered value is within the program somewhere
                            raise ValueError
                    except:
                        changeLine = input('Please enter a number, representing the line you would like to change:\n' + '>>> ')
                        
                    while True:
                        print('WARNING: instructions MUST be entered in UPPERCASE')
                        changeString = input('Enter the desired text or instruction (or "-dhelp" for a list of instructions):\n' + '>>> ')
                        if i == '-dhelp': #a quick cheatsheet for what values can be entered
                            for h, i in dictionary.items():
                                if len(h) > 1:
                                    print(h)
                            continue
                        
                        elif 'ARROW' in changeString: #check to see if there is an "ARROW" command, and if so, check how many times it is to be repeated.
                            arrowRepeat = input('You have entered an "ARROW" command, how many times would you like to repeat the command?:\n' + '>>> ')
                            while True:
                                try:
                                    arrowRepeat = int(arrowRepeat) #make sure it is a number
                                    arrowRepeat = 'REPEAT ' + str(arrowRepeat) #make the 'repeat' string for use later
                                    readableList.insert(changeLine, arrowRepeat) #amend the list with the new value
                                    break
                                
                                except:
                                    arrowRepeat = input('Please enter the number of times for the arrow command to repeat, as a number:\n' + '>>> ') #if not a number, get a number                           

                        if 'ARROW' in readableList[changeLine-1]:#remove the 'repeat' number from the list for ease of reading.
                            readableList.pop(changeLine)
                            
                        readableList[changeLine-1] = changeString #amend the users input into the list
                        break
                        
                    for l,i in enumerate(readableList): #reprint the new list and instructions that the program has.
                        if i != '00ff':
                            print('line ', str(l+1)+': ', i)
                    printed = 1
                    break
                        
                selection = input('Would you like to change another line? (y/n)\n' + '>>> ')

                if selection == 'y' or selection == 'Y':
                    continue
                elif selection == 'n' or selection == 'N':
                    printed = 0
                    break
                else:
                    print('Unrecognised: returning to menu')
                    break
                
                break
                    
        elif selection == '4':

            hexTranslated = fileHex(fileData, 'decode') #restore the hexTranslated variable
            readableList = combine(translate(reverse(hexTranslated), 'w', dictionary)) #restore the readableList variable
            print('Orignal file restored\n' + 'returning to menue \n') #for ease of reading in code, concatination is used
            selection = '' #skip the users option to immediatly quit
            
        elif selection == '5':
            #translation of text to HEX
            untranslatedText = recode(readableList, dictionary)#undo quality of life changes.
            #first: translate the above text into the hex instructions, then reverse the hex back to normal, then encode the hex for writing to file
            fileText = fileHex(''.join(reverse(translate(untranslatedText, 'r', dictionary))), 'encode')
            print('The files will be output as "Ducky_Text.txt" and "Inject.bin" ')
            write(readableList, fileText, '') #output hex instructions.
                
        #terminate the program.
        elif selection == '6' or selection == 'q':
            exit()

        else:
            continue
               
    
if __name__ == '__main__':
    main()
