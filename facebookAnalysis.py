#Facebook Message Analysis
#By Jack Markham - 13/04/2020

#import everything required 

import matplotlib.pyplot as plt
import numpy as np
import csv
import datetime
import sys
import os 
import combineFiles

#ask user for location of files to combine and the type 
print("What is the dir of the files to combine?")
fileDir = input()

print("What is the file type?")
fileType = input()

#create file combines the strings, it then gives the input info to another file which combines all the file types so we can anaylise all at once 
createFile = os.path.join(fileDir, "output.txt")
combineFiles.combine(fileDir, fileType)

#open our combined file and start reading the lines
file = open(createFile)
fileNew =  file.readlines()

#set varibles for everything 
participantsNameCount = 0
participantsTotal = 0;
participantsNameCheck = 'false'

messageTotal = 0;

addNameCount = 0
addNameCheck = 'false'
addNameMessage = 0;


messageCheck = 'false'
messageCount = 0
messageTotal = 0

messageCountPP = []

nameArray = []
participantsTotalLoop = 0

missing = 0

reactCheck = 'false'
reactCounter = 0;

#Checks the file for the names of each participants
while participantsNameCheck != 'true':
    
    #if it finds a line with name in it, start a counter from 0, change the the line to match correct index, create a new varibale for that line, and adds a new place in our array to save the name
    if 'name' in fileNew[participantsNameCount]:
        count = 0;
        
        participantsNameCount = participantsNameCount + 1
        newLine = fileNew[participantsNameCount-1]
        nameArray = nameArray + [""]
        
        #count each letter in the line, ignore everything before 16 as thats useless info, read each character after that and save to the array, stop when you reach a "
        for i in newLine:
            count = count + 1
            
            if count >= 16:
                if i == '"':
                    break
                nameArray[participantsTotal] = nameArray[participantsTotal] + i
                        
        participantsTotal = participantsTotal + 1
         #to keep the loop going, if we get to the end of the participants, end loop           
    else:
        participantsNameCount = participantsNameCount + 1
        
        if 'messages' in fileNew[participantsNameCount]:
            participantsNameCheck = 'true'
        
    
#finds overall amount of messages so we know how big to make the list 
while messageCheck != 'true':
    #every message has a senders name section, so we know a message was sent
    if 'sender_name' in fileNew[messageCount]:
        messageTotal = messageTotal + 1
        messageCount = messageCount + 1
    #we add EOF at the end of each file to know when to stop 
    else:
        messageCount = messageCount + 1
        if 'EOF' in fileNew[messageCount]:
            messageCheck = 'true'

#name, time, content, type, reacts, who reacted, type
messageList = [["","","","", -1] for i in range(messageTotal)]


#loop to find what type of message was sent, it finds the senders name and goes down line by line till it finds out what type of message it is then checks to see if it has any reactions
while addNameCheck != 'true':
    
    if 'sender_name' in fileNew[addNameCount]:
        count = 0;
        for i in range(participantsTotal):
            if nameArray[i] in fileNew[addNameCount]:
                messageList[addNameMessage][0] = nameArray[i]
            
            
        newLine = fileNew[addNameCount + 1]
        
        for i in newLine:
            count = count + 1
            
            if count >= 23:
                if i == ',':
                    break
                messageList[addNameMessage][1] = messageList[addNameMessage][1] + i
                
                
        newLine = fileNew[addNameCount + 2]
        
        if 'content' in newLine:
            newLine = fileNew[addNameCount + 2]
            count = 0;
            messageList[addNameMessage][3] = 'Text'
            for i in newLine:
                count = count + 1

                if count >= 19:
                    if i == '"':
                        break
                    messageList[addNameMessage][2] = messageList[addNameMessage][2] + i
        elif 'photos' in newLine:
            newLine = fileNew[addNameCount + 4]
            count = 0;
            messageList[addNameMessage][3] = 'Photo'
            for i in newLine:
                count = count + 1

                if count >= 19:
                    if i == '"':
                        break
                    messageList[addNameMessage][2] = messageList[addNameMessage][2] + i
                    
        elif 'sticker' in newLine:
            newLine = fileNew[addNameCount + 3]
            count = 0;
            messageList[addNameMessage][3] = 'Sticker'
            for i in newLine:
                count = count + 1

                if count >= 17:
                    if i == '"':
                        break
                    messageList[addNameMessage][2] = messageList[addNameMessage][2] + i
        elif 'gifs' in newLine:
            newLine = fileNew[addNameCount + 4]
            count = 0;
            messageList[addNameMessage][3] = 'GIFS'
            for i in newLine:
                count = count + 1

                if count >= 19:
                    if i == '"':
                        break
                    messageList[addNameMessage][2] = messageList[addNameMessage][2] + i
        elif 'videos' in newLine:
            newLine = fileNew[addNameCount + 4]
            count = 0;
            messageList[addNameMessage][3] = 'Videos'
            for i in newLine:
                count = count + 1

                if count >= 19:
                    if i == '"':
                        break
                    messageList[addNameMessage][2] = messageList[addNameMessage][2] + i
        elif 'files' in newLine:
            newLine = fileNew[addNameCount + 4]
            count = 0;
            messageList[addNameMessage][3] = 'Files'
            for i in newLine:
                count = count + 1

                if count >= 19:
                    if i == '"':
                        break
                    messageList[addNameMessage][2] = messageList[addNameMessage][2] + i
        
        secondLoop = 0;   
        reactCheck = 'false'
        while reactCheck != 'true':
            count = 0;
            
            
            newLine = fileNew[addNameCount + secondLoop]
            if 'reaction' in newLine:    
                    messageList[addNameMessage][4] = messageList[addNameMessage][4] + 1
            if 'type' in newLine:
                reactCheck = 'true'
                        
            secondLoop = secondLoop + 1    
        
             
        else: 
            missing = missing + 1
        addNameCount = addNameCount + 1
        addNameMessage = addNameMessage + 1
        
    else:
        
        addNameCount = addNameCount + 1
        if 'EOF' in fileNew[addNameCount]:
            addNameCheck = 'true'
            
#create an array for the amount of messages sent by person and find that info            
messageCountPP = [0] * (participantsTotal)

for i in range(messageTotal):
    for j in range(participantsTotal):
        if messageList[i][0] in nameArray[j-1]:
            messageCountPP[j-1] = messageCountPP[j-1] + 1



            #create an output file which is CSV so we can import into excel if we want 
csvfile = "D:\Desktop\Coding\AlifNathaliWorshipSociety_InmMrlKf-A\outputList.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(messageList)
#output the data to screen
print(nameArray)
#print(sum(messageCountPP))
plt.bar(nameArray, messageCountPP)
plt.ylabel('Message Count')
plt.show()
