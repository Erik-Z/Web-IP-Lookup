import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.constants import INSERT
import time
import datetime
from DNS_Resolver import dnsIPLookup
import validators

def myDig():
    if validators.domain(urlTextField.get()):
        startTime = time.time()
        results = dnsIPLookup(urlTextField.get())
        if results == 'Invalid Domain':
            textArea.insert(INSERT, urlTextField.get() + ' does not exist\n')
            textArea.insert(INSERT, '\n')
            urlTextField.delete(0, 'end')
        else:
            urlTextField.delete(0, 'end')
            endTime = time.time()
            question = str(results[1][0])
            answer = str(results[0][0]).split("\n")
            textArea.insert(INSERT, 'QUESTION\n')
            textArea.insert(INSERT, question + '\n')
            textArea.insert(INSERT, 'ANSWER\n')
            for i in answer:
                textArea.insert(INSERT, i + '\n')
                temp = i
                while temp.split(" ")[-2] == "CNAME":
                    newName = temp.split(" ")[-1]
                    r = dnsIPLookup(newName)[0][0]
                    temp = str(r)
                    textArea.insert(INSERT, temp + '\n')
            textArea.insert(INSERT, "Query time: " + str(round((endTime - startTime) * 1000, 3)) + 'ms\n')
            date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            textArea.insert(INSERT, 'WHEN: ' + date + '\n')
            textArea.insert(INSERT, '\n')
    else:
        textArea.insert(INSERT, urlTextField.get() + ' is an invalid domain\n')
        textArea.insert(INSERT, '\n')
        urlTextField.delete(0, 'end')
def myDigEnter(event):
    myDig()

def printText():
    print(textArea.get("1.0", tk.END))

if __name__=="__main__":
    root = tk.Tk()
    root.title('IP Lookup')
    root.bind('<Return>', myDigEnter)

    urlLabel = tk.Label(root, text='URL', font=('Arial Bold', 12))
    urlLabel.grid(row=0, column=0)

    submitButton = ttk.Button(root, text='Submit', command=myDig)
    submitButton.grid(row=0, column=2, sticky="e")
    # getButton = ttk.Button(root, text='Get', command=printText)
    # getButton.grid(row=0, column=3, sticky="e")

    urlTextField = ttk.Entry(root)
    urlTextField.grid(row=0, column=1, sticky='ew')
    urlTextField.focus()

    textArea = scrolledtext.ScrolledText(root)
    textArea.grid(row=1, column=0, columnspan=3, sticky='ew')

    root.columnconfigure(1, weight=1)
    root.rowconfigure(1, weight=1)
    root.mainloop()