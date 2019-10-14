import numpy as np

import matplotlib.pyplot as plt

from tkinter import *
import tkinter as ttk
from tkinter import ttk

infilename="fixed2.txt"
#infilename="testfixed.txt"

#infile=open(infilename,"r")

big_table={}
#big_table["test"]=np.empty(0)


with open(infilename) as f:
	content = f.readlines()
	for i in range(len(content)): #loop through each line
		start_of_data=0
		location=0 #0=time,1=id,2=data
		time1=0
		time2=0
		mid=""
		tempstore=np.empty(0)
		
		for j in range(len(content[i])):	#loop through characters in a line
				if(location==0):
					if(content[i][j]=="\t"):
						location=1
						time1=float(content[i][start_of_data:j])
						start_of_data=j+1
						tempstore=np.append(tempstore,time1)
				elif(location==1):
					if(content[i][j]=="\t"):
						location=2
						mid=content[i][start_of_data:j]
						start_of_data=j+1
				elif(location==2):
					if(content[i][j]=="\t"):
						location=3
						time2=float(content[i][start_of_data:j])
						start_of_data=j+1
				else:
					if(content[i][j]=="\t"):
						
						tempstring=content[i][start_of_data:j]
						if(len(tempstring)==1):
							tempstring="0"+tempstring
						tempstore=np.append(tempstore,tempstring)
						start_of_data=j+1
		
		
		if(not(mid in big_table)):
			big_table[mid]=tempstore	
		else:
			#print("OR ELSE")
			#print(big_table[mid])
			#print(tempstore)
			#print(big_table[mid].shape)
			#print(tempstore.shape)
			if(len(big_table[mid].shape)==1 or (big_table[mid].shape[1])==len(tempstore)):
				big_table[mid]=np.vstack((big_table[mid],tempstore))

print(big_table)


root = Tk()
root.title("CAN rev-eng GUI")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

# Create a Tkinter variable
tkvar = StringVar(root)
tkvar2 = StringVar(root) 

# Dictionary with options
choices=list(big_table.keys())
#choices = { 'Pizza','Lasagne','Fries','Fish','Potatoe'}
tkvar.set(choices[0]) # set the default option

tkvar2.set(1)
choices2={1,2,3,4,5,6,7,8,12,23,34,45,56,67,78}
popupMenu2= OptionMenu(mainframe, tkvar2, *choices2)
Label(mainframe, text="Choose a byte or combo").grid(row = 3, column = 1)
popupMenu2.grid(row = 3, column =3)

popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Choose a message ID").grid(row = 1, column = 1)
popupMenu.grid(row = 1, column =3)

# on change dropdown value
def change_dropdown(*args):
	#tkvar2.set(1)
	#
	print( tkvar.get() )
	
def change_dropdown2(*args):
	print(tkvar2.get())
	

# link function to change dropdown
tkvar.trace('w', change_dropdown)
tkvar2.trace('w', change_dropdown2)



def callback():
	
	indexes=[]
	print(tkvar)
	keyforhash=tkvar.get()
	indexes_to_examine=float(tkvar2.get())
	if(indexes_to_examine>9):
		indexes=(int((indexes_to_examine-indexes_to_examine%10)/10),int(indexes_to_examine%10))
	else:
		indexes=[int(indexes_to_examine)]
	table=big_table[keyforhash]
	
	if(len(table.shape)==1):
		if(indexes[-1]>=len(table)):
			ccc.config(text="No data for that byte combo.")
			
		else:
			
			if(len(indexes)==1):
				print(indexes[0])
				value=int(table[indexes[0]], 16)
			else:
				print
				value=int(table[indexes[0]]+table[indexes[1]], 16)
			ccc.config(text="Just 1 message with value "+str(value)+" at time "+str(table[0])+"s.")
	else:#have an actual table
		print("have an actual table")
		print(indexes)
		print(len(table[0]))
		if(indexes[-1]>=len(table[0])):
			print(len(table[0]))
			print(table[0])
			ccc.config(text="No data for that byte combo.")
		else:
			ccc.config(text="See plot.")
			x=table[:,0]
			y=[]
			if(len(indexes)==1):
				print("ONLY 1 index")
				column_of_interest=table[:,indexes[0]]
				newarray=np.zeros(column_of_interest.shape)
				for r in range(len(newarray)):
					newarray[r]=int(column_of_interest[r],16)
				y=newarray
			else:
				print("COMBO OF INDEXES")
				print(table)
				#column_of_interest=np.concatenate([table[:,indexes[0]], table[:,indexes[1]]], axis=0)
				column_of_interest=list(map(''.join, zip(table[:,indexes[0]], table[:,indexes[1]])))
				print(column_of_interest)
				newarray=np.zeros(len(column_of_interest))
				for r in range(len(newarray)):
					newarray[r]=int(column_of_interest[r],16)
				y=newarray
				print(y)
			print(table)
			print(y)
			plt.plot(x,y)
			plt.ylabel('Integer Value')
			plt.xlabel('Time (s)')
			plt.show()
		
	print(len(table.shape))


ccc=Label(mainframe, text="")
ccc.grid(row = 5, column = 1)
b = Button(root, text="DRAW", command=callback)

b.pack()

root.mainloop()

			
	
	