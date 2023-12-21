#!/usr/bin/python3

# Filename: m3p1.py
# Author: Ezra Fast
# Course: ITSC 203
# Details: This code is the solution for problem 1, lab assignment 3a, ITSC 203

import random
import string                                               # the string module was used so that the possible sequence characters did not have to be manually declared.

def sequenceLengthSolicitor():                              # this function solicits the length of the non-repeating sequence to generate.
    lengthOfSequence = 0
    while (lengthOfSequence < 100 or lengthOfSequence > 1024):
        lengthOfSequence = int(input('Enter the length of the random sequence: ' ))
        if (lengthOfSequence > 100 and lengthOfSequence < 1024):
            break
        else:
            print('Usage: Enter a sequence length between 100 and 1024 inclusive.\n')
    return lengthOfSequence 

def addressLengthSolicitor():                               # This function solicits the length of the address subsequence (either 4 or 8 bytes) 
    lengthOfAddress = 0
    while (lengthOfAddress != 4 and lengthOfAddress != 8):
        lengthOfAddress = int(input('Enter the size of the address: '))
        if (lengthOfAddress == 4 or lengthOfAddress == 8):
            break
        else:
            print('\nUsage: Enter an address length of either 4 or 8.\n')
    return lengthOfAddress    

def generateAndShowSequence(sequenceLength):                                                        # string.punctuation is included as the lab specifies punctuation should be included
    listOfPossibleCharacters = string.digits + string.punctuation + string.ascii_letters            # this seemed more efficient than using the ascii range
    listOfPossibleCharacters = list(listOfPossibleCharacters)
    rawSequenceList = []
    for i in range(0, sequenceLength + 1):
        rawSequenceList.append(listOfPossibleCharacters[random.randint(0, len(listOfPossibleCharacters) - 1)])
    rawSequenceString = ''.join(rawSequenceList)
    print(f'The generated sequence: \n\n{rawSequenceString}')
    return rawSequenceString 

def subSequenceSolicitor(addressLength):                                                            # This function solicits the user entered sub sequence of the non-repeating sequence.
    subSequenceString = ''
    while (len(subSequenceString) is not addressLength):
        subSequenceString = input('\nEnter a subsequence of the generated sequence: ')
        if (len(subSequenceString) == addressLength):
            break
        else:
            print('\nUsage: Enter a subsequence of the same length as the address length specified above.')
    return subSequenceString

def scanAndReportSubSequenceOccurence(subSequenceString, rawSequenceString):                        # This function identifies and reports the occurence of the subsequence in the generated sequence.
    try:
        subSequenceOffset = rawSequenceString.find(subSequenceString)
        if subSequenceOffset == -1:
            print('Your subsequence does not occur in the generated sequence. Exiting...')
            exit(-2)
        print(f'\nYour subsequence occurs at offset {subSequenceOffset} of the sequence.\n')
    except:
        print('Your subsequence was not found in the generated sequence. Exiting...')
        exit(-1)

def findAndReportNumberOfSubSequenceOccurences(subSequenceString, rawSequenceString):               # This function counts the number of times the provided subsequence occurs in the larger sequence.
    numberOfOccurences = 0
    listOfOccurences = [sequence for sequence in range(0, len(rawSequenceString) + 1) if rawSequenceString.startswith(subSequenceString, sequence)]
    if (len(listOfOccurences) == 1):
        print(f'Your subsequence occurred {len(listOfOccurences)} time in the generated sequence.\n')
    else:
        print(f'Your subsequence occurred {len(listOfOccurences)} times in the generated sequence.\n')
    return len(listOfOccurences)

def colorCodeOutput(subSequenceString, rawSequenceString):                                          # This function color codes the subsequence in the last part of output.
    yellowCode = "\033[93m"
    resetCode = "\033[0m"
    rawSequenceStringCopy = rawSequenceString
    rawSequenceStringCopy = rawSequenceStringCopy.replace(subSequenceString, yellowCode + subSequenceString + resetCode)
    print(f'Your subsequence in the generated sequence:\n\n{rawSequenceStringCopy}\n')

def formatSeparator():
    print('-'*50)

def mainFunction():                                                                                 # This is the main function. This code is very modularized.
    sequenceLength = sequenceLengthSolicitor() 
    addressLength = addressLengthSolicitor()                # both input values have been variablized.
    rawSequenceString = generateAndShowSequence(sequenceLength)
    subSequenceString = subSequenceSolicitor(addressLength)
    scanAndReportSubSequenceOccurence(subSequenceString, rawSequenceString)
    findAndReportNumberOfSubSequenceOccurences(subSequenceString, rawSequenceString)
    colorCodeOutput(subSequenceString, rawSequenceString)
    exit(0)

if __name__ == '__main__':                                                                          # Calling the main function
    mainFunction()
