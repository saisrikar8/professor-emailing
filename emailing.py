from EmailSomeone import EmailSender
from ContactPageAnalysis import getContacts
import tkinter
from tkinter import filedialog
import os

root = tkinter.Tk()
root.withdraw()
def search_for_file_path ():
    currdir = os.getcwd()
    tempdir = filedialog.askopenfilenames(parent=root, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print("You chose: " + str(tempdir))
    return tempdir

def main():
    print("Welcome! Start sending email immediately by entering some of your info!")
    contacts = getContacts()
    to_addrs = contacts['Email'].tolist()
    username = 'insert-email-here'
    password = 'insert-password-here'
    subject = 'Projects or Research Opportunities'
    print("Loading...")
    attachments = tuple()
    while True:
        attachmentPrompt = input("Would you like to add any attachments?(Y or N): ")
        if (attachmentPrompt.upper() == 'Y'):
            attachments = search_for_file_path()
            break
        elif (attachmentPrompt.upper() == 'N'):
            print("There aren't going to be any attachments to your email")
            break
        else:
            print("That input was invalid. Let's try again.")
    for to_addr in to_addrs:
        sender = EmailSender(username, password)
        body = open('message.txt').read()

        sender.send_email(body, subject, to_addr, attachments)

if (__name__ == '__main__'):
    main()


