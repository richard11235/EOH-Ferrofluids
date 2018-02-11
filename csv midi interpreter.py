import numpy as np
name = raw_input('Csv name: ')
filename = name + ".csv"
newfilename = name + "track"
file = open(filename, "r")
convertedlist = []
#opening and initializing
for line in file:
    newline = line.split(",") #Read as string. Delimit into list at commas
    if len(newline) != 6:
        continue #If wrong dimensions(like title), skip
    newnewline = [] #Clearing to use as holder
    for element in newline:
        try:
            fuck = float(element) #Numers are still strings
            newnewline.append(fuck) #Add numbers to placeholder
        except:
            pass #Omit non-numerics
    convertedlist.append(newnewline) #Add product to list
#reading file

file.close()
finallist = []
notelist = []
notelists = []
track = 2
convertedlist.append([convertedlist[-1][0]+1,0,0,0,0])
for allnotes in convertedlist: #Doing statistics for notes
    if allnotes[0] < 2:
        continue
    if track != allnotes[0]: #Different stats for every track
        track = allnotes[0]
        notelists.append(notelist) 
        notelist = []
    notelist.append(allnotes[3])

minimumnote = [0,0] #Initializing with indices as tracks
maximumnote = [0,0]
rangenotes = [0,0]
stdev = [0,0]
for track in notelists:
    minimumnote.append(np.min(track)) #Smallest note
    maximumnote.append(np.max(track)) #Largest note
    rangenotes.append(np.max(track)-np.min(track))
    stdev.append(np.std(track))


prevtime = 0
counter = 0
lastlistavg = 0

for sequence in convertedlist[:-1]: #Creating list of [time,note]
    if sequence[1] != prevtime: #When time changes, append final previous averages and reset variables
        if lasttrack == sequence[0]:
            finallist.append([sequence[0],prevtime,(lastlistavg-minimumnote[int(sequence[0])])*int(sequence[4]>0.)])
            counter = 0
            lastlistavg = sequence[3]
            prevtime = sequence[1]
            continue
        if lasttrack != sequence[0]:
            counter = 0
            prevtime = 0
            lastlistavg = 0
        
    counter += 1
    lasttrack = sequence[0]
    lastlistavg = (lastlistavg+sequence[3]/counter)*counter/(counter+1) #averaging notes

#Eliminating redundancies and setting silences to 0
finallist.append([-1])


track = 1 #Writing new files
prevLED = 3
for notes in finallist:
    if notes[0] == -1:
        currenttrack.write(str(timestamps) + '\n' + str(LEDs)) # write string
        currenttrack.close()
        continue
    if track != int(notes[0]): #new track
        try: #handle exception of first iteration
            currenttrack.write(str(timestamps) + '\n' + str(LEDs)) # write string
            currenttrack.close()
        except:
            pass
        prevnote = notes[2]
        prevLED = 3
        currenttrack = open(newfilename+str(int(notes[0]))+'.txt','w+') #new file
        timestamps= []
        LEDs = []
        track = int(notes[0])
    timestamps.append(notes[1])
    if notes[2] == 0:
        LEDs.append('NONE')
        track = int(notes[0]) #Setting track
        continue
    notediff = .5*(notes[2]-prevnote)/stdev[track]
    if notediff < 0: #if negative, floor on differential
        notediff = np.floor(notediff)
    if notediff > 0: #if positive, ceiling
        notediff = np.ceil(notediff)
    currentLED = notediff + prevLED #current LED
    if currentLED > 6: # if greater than LEDs, bring down
        currentLED = 6
    if currentLED < 1: # if smaller than LEDs, bring up
        currentLED = 1    
    prevLED = int(currentLED)
    LEDs.append('LED' + str(int(currentLED)))
    prevnote = notes[2]
    track = int(notes[0]) #Setting track
    
    
    