import time
#define the database building API
def build_db(path, mode=0):
    if mode == 0:
        
        db = {}
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

    def add_contact_to_db(self, db, contact_name, contact_fname, contact_lname, contact_number, contact_address):
        #set the contact_info to be empty
        contact_info = {}
        #also check to see if the contact name already exists
        contact_info_cmd = db.get(contact_name)

        #if the contact_info_cmd is not None, or has existing data
        if contact_info_cmd is not None:
            raise KeyError("Contact already exists: {}".format(contact_name))
        #set uppercase data equal to user input
        contact_info['contact'] = contact_name.upper()
        contact_info['First Name'] = contact_fname.upper()
        contact_info['Last Name'] = contact_lname.upper()
        contact_info['Number'] = contact_number.upper()
        contact_info['Address'] = contact_address.upper()
        
        #open up the file
        with open('contacts.txt', 'a+') as f:
            #write the data
            f.write("\nCONTACT: " + contact_info['contact'])
            f.write("\n    First Name: " + contact_info['First Name'])
            f.write("\n    Last Name: " + contact_info['Last Name'])
            f.write("\n    Number: " + contact_info['Number'])
            f.write("\n    Address: " + contact_info['Address'])
            #rebuild the db
        db = build_db("contacts.txt")
            
        self.contact_manager(db)
        
    def read_contact(self, db, contact_name):
        #follow format
        formatting = """\
CONTACT: {contact}
    First Name: {First Name}
    Last Name: {Last Name}
    Number: {Number}
    Address: {Address}
"""
        #grab user input
        contact_name = contact_name.upper()
        contact_info = db.get(contact_name)
        #if userinput isnt a valid a contact        
        if contact_info is None:
            raise KeyError("No such contact: {}".format(contact_name))
        #set the data equal to the user input
        contact_info['contact'] = contact_name
        #finally, print the found contact and its values following the format
        print(formatting.format(**contact_info))
        
        self.contact_manager(db)
    
    def write_db_to_file(self, db, out_path):
        with open(out_path, 'w') as outf:
            for contact_name in db:
                outf.write(self.read_contact(db, contact_name.upper()))
        
        self.contact_manager(db)        
                
    def remove_user_from_db(self, db, contact_name):
        #try to delete specificed contact
        try:
            del db[contact_name.upper()]
        #but if there is no such contact
        except KeyError or contact_name.upper() is "dev":
            raise KeyError("No such contact: {}".format(contact_name))
        self.contact_manager(db)
    
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
            
            self.read_contact(db, input("What contact shall you search?\n").upper())
        
        elif cmd.upper() == "DELCONTACT":
            
            self.remove_user_from_db(db, input("What contact shall you delete?\n"))
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
            print(db)
            self.contact_manager(db)
        #finally, if it is none of these
        else:
            print("Unknown command.")
            self.contact_manager(db)
            
#run the app    
App()
