import time
import sys
import os.path
#define the database building API
def build_db(path, mode=0):
    if mode == 0:
        
        db = {}
        if os.path.exists('contacts.txt') == False:
            with open('contacts.txt', 'w') as f:
                f.write('CONTACT: DEV')
                f.write('\n    First Name: FELIX')
                f.write('\n    Last Name: MARTIN')
                f.write('\n    Number: N/A')
                f.write('\n    Address: N/A')
            print("Please re-run the program.")
            quit()
        else:
            #while opening contacts.txt as f
            with open(path) as f:
                for line in f:
                    #strip the file and split each line from the 'CATEGORY' and the 'VALUE'
                    #e.g. split 'CONTACT: YOU' to 'CONTACT', 'YOU'
                    category, value = map(str.strip, line.split(":"))
                    #if the stripped line is the CONTACT line
                    if category == "CONTACT":
                        #set the current contact to start a new dictionary with the value of the contact
                        cur_contact = value
                        db[value] = {}
                    #if the stripped line is the data within the CONTACT line
                    else:
                        #set the previously set dictionarys data with another dictionary
                        db.get(cur_contact, {})[category] = value
            #return the database when its called
            return db
    #unless debug mode is set to 1
    
    else:
        #do everything as before, except print data for debugging
        db = {}
        with open(path) as f:
            for line in f:
                category, value = map(str.strip, line.split(":"))
                mapDebug = map(str.strip, line.split(":"))
                print("Printing mapDebug\n")
                print(mapDebug)
                print("Printing category, value\n") 
                print(category, value)
                if category == "CONTACT":
                    cur_contact = value
                    db[value] = {}
                    print("Printing db[value]\n")
                    print(db[value])
                else:
                    print("Printing db.get(cur_contact, {})[category]\n")
                    print(db.get(cur_contact, {})[category])
                    db.get(cur_contact, {})[category] = value
        print(db)
        return db        
#finally, build the database off of the local contacts.txt file
db = build_db("contacts.txt")
#Application

class App:
    #initialize the Application
    def __init__(self):
        #print info
        print("Contact Manager - Felix Martin V2.8.1")
        print("LOADING . . .")
        print("LOADED!")
        self.contact_manager(db)
    
    #format function
    def format_contact_info(self, contact_info):
        formatting = """CONTACT:{contact}
    First Name: {First Name}
    Last Name: {Last Name}
    Number: {Number}
    Address: {Address}"""

        return formatting.format(**contact_info)
    
    #add contact function
    def add_contact_to_db(self, db, contact_name, contact_fname, contact_lname, contact_number, contact_address):
        #set the contact_info to be empty
        contact_info = {}
        #also check to see if the contact name already exists
        contact_info_cmd = db.get(contact_name)

        #if the contact_info_cmd is not None, or has existing data
        if contact_info_cmd is not None:
            raise KeyError("Contact already exists: {}".format(contact_name))
        # check if any of the fields are empty
        if contact_name == "" or contact_name == None:
            print("Error! Contact Reference name cannot be blank!")
            self.contact_manager(db)
        if contact_fname == "" or contact_fname == None:
            print("Error! Contact First Name cannot be blank!")
            self.contact_manager(db)
        if contact_lname == "" or contact_lname == None:
            print("Error! Contact Last Name cannot be blank!")
            self.contact_manager(db)
        if contact_number == "" or contact_number == None:
            print("Error! Contact Number cannot be blank!")
            self.contact_manager(db)
        if contact_address == "" or contact_address == None:
            print("Error! Contact Address cannot be blank!")
            self.contact_manager(db)
        #set uppercase data equal to user input
        contact_info['contact'] = contact_name.upper()
        contact_info['First Name'] = contact_fname.upper()
        contact_info['Last Name'] = contact_lname.upper()
        contact_info['Number'] = contact_number.upper()
        contact_info['Address'] = contact_address.upper()
        
        #open up the file
        with open('contacts.txt', 'a+') as f:
            #write the data
            f.write("\n"+self.format_contact_info(contact_info))
            #rebuild the db
        db = build_db("contacts.txt")
        self.contact_manager(db)
        
    #debug function
    def clear_file(self, db):
        f = open('contacts.txt', 'r')
        i = 0
        for line in f:
            i += 1
            p = f.readlines()
            print(p[i])
        self.contact_manager(db)
    #search contact function
    def search_contact(self, db, contact_name):
        #grab user input
        contact_name = contact_name.upper()
        contact_info = db.get(contact_name)
        #if userinput isnt a valid a contact        
        if contact_info is None:
            raise KeyError("No such contact: {}".format(contact_name))
        #set the data equal to the user input
        contact_info['contact'] = contact_name
        #finally, print the found contact and its values following the format
        print(self.format_contact_info(**contact_info))
        self.contact_manager(db)
        
    #replicate search_contact function, however return the value for write_db_to_file
    def read_contact(self, db, contact_name):
        #grab user input
        contact_name = contact_name.upper()
        contact_info = db.get(contact_name)
        #if userinput isnt a valid a contact        
        if contact_info is None:
            raise KeyError("No such contact: {}".format(contact_name))
        #set the data equal to the user input
        contact_info['contact'] = contact_name
        #finally, return the found contact and its values following the format
        return self.format_contact_info(**contact_info)
    
    #write_db_to_file function
    def write_db_to_file(self, db, out_path):
        with open(out_path, 'w+') as outf:
            for contact_name in db:
                this_contact = self.extract(contact_name.upper(), db) 
                outf.write(self.format_contact_info(this_contact))
                outf.write('\n')
        self.contact_manager(db)
        
    #extract function
    def extract(self, contact_name, db):
        contact_name = contact_name.upper()
        contact_info = db.get(contact_name)
        contact_info['contact'] = contact_name 
        return contact_info
        
    #remove_user function
    def remove_user_from_db(self, db, contact_name):
        #check to see if they are deleting default contact
        if contact_name.upper() == "DEV":
            print("Cannot delete that contact!")
            self.contact_manager(db)
        else:
            #try searching for the given contact
            try:
                del db[contact_name.upper()]
            #but if there is no such contact
            except KeyError or contact_name.upper() is "dev":
                raise KeyError("No such contact: {}".format(contact_name))
            self.contact_manager(db)
    
    #main menu function
    def contact_manager(self, db):

        #init the menu
        print("Type a command, help or quit to exit the program.")
        cmd = input("")
        #if the cmd is help
        if cmd.upper() == "HELP":
            print("Available commands are: addContact, delContact, writeFile, readFile, help, quit")
            
            self.contact_manager(db)
        #or if the cmd is addcontact
        elif cmd.upper() == "ADDCONTACT":
            
            self.add_contact_to_db(db, input("What is the contacts reference name?\n").upper(), input("What is the contacts first name?\n").upper(), input("What is the contacts last name?\n").upper(), input("What is the contacts (cell/main/home/etc) number?\n").upper(), input("What is the contacts address?\n").upper())
        #or if the cmd is writefile...
        elif cmd.upper() == "WRITEFILE":
            
            self.write_db_to_file(db, "contacts.txt")
        #... etc etc etc
        elif cmd.upper() == "READFILE":
            
            self.search_contact(db, input("What contact shall you search?\n").upper())
        
        elif cmd.upper() == "DELCONTACT":
            
            self.remove_user_from_db(db, input("What contact shall you delete?\n"))
            
        elif cmd.upper() == "CLRFILE":
            
            self.clear_file(db)
            
        #if the cmd is quit
        elif cmd.upper() == "QUIT":
            #thank the user for using my program
            print("Thank you for using Contact Manager.")
            #delay2 seconds
            time.sleep(2)
            quit()

        #if the user activates the secret command
        elif cmd.upper() == "DEBUG()":
            
            print("Activating DEBUG Function.\n")
            print("Nothing set to debug.\n")
            self.contact_manager(db)
        #finally, if it is none of these
        else:
            print("Unknown command.")
            self.contact_manager(db)
            
#run the app    
App()
