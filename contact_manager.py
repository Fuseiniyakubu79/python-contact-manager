def build_db(path):
    db = {}
    debug_dict = {}
    with open(path) as f:
        for line in f:
            category, value = map(str.strip, line.split(":"))
            if category == "CONTACT":
                cur_contact = value
                db[value] = {}
            else:
                db.get(cur_contact, {})[category] = value
    # builds a dictionary of dictionaries that looks like:
    # # {"YOU": {"First Name": "FELIX", "Last Name": "MARTIN", ...}, ...}
    print(db)
    return db
    
db = build_db("contacts.txt")
class App:
    def __init__(self):
        
        print("Contact Manager - Felix Martin V2.0")
        print("LOADING . . .")
        
        self.contact_manager(db)
        
        print("LOADED!")
    #debugging for a new function
    def add_contact_to_db_data(self, db):
        
        formatting = """\
        CONTACT: {contact}
            First Name: {First Name}
            Last Name: {Last Name}
            Number: {Number}
            Address: {Address}
        """      
        
        refname = input("What is the contacts reference name?\n")
        fname = input("What is the contacts first name?\n")
        lname = input("What is the contacts last name?\n")
        number = input("What is the contacts (cell/main/home/etc) number?\n")
        address = input("What is the contacts address?\n")
        
        contact_name = refname
        contact_fname = fname
        contact_lname = lname
        contact_number = number
        contact_address = address
        
        contact_info = db.get(contact_name)
        
        if contact_info is not None:
            raise KeyError("Contact already exists: {}".format(contact_name))

        
        self.add_contact_to_db(db, contact_name, contact_fname, contact_lname, contact_number, contact_address)
    #more debugging
    def add_contact_to_db(self, db, contact_name, contact_fname, contact_lname, contact_number, contact_address):
        
        formatting = """\
        CONTACT: {contact}
            First Name: {firstname}
            Last Name: {lastname}
            Number: {number}
            Address: {address}
        """
        contact_info = db.append(contact_name)
        
        if contact_info is not None:
            raise KeyError("Contact already exists: {}".format(contact_name))
        print(contact_info['contact'])
        #contact_info['contact'] = contact_name.upper()
        #contact_info['firstname'] = contact_fname.upper()
        #contact_info['lastname'] = contact_lname.upper()
        #contact_info['number'] = contact_number.upper()
        #contact_info['address'] = contact_address.upper()
        
        print(formatting.format(**contact_info))
        
    def read_contact(self, db, contact_name):
        formatting = """\
        CONTACT: {contact}
            First Name: {First Name}
            Last Name: {Last Name}
            Number: {Number}
            Address: {Address}
        """
        contact_name = contact_name.upper()
        contact_info = db.get(contact_name)
        
        if contact_info is None:
            raise KeyError("No such contact: {}".format(contact_name))
        contact_info['contact'] = contact_name
        return formatting.format(**contact_info)
    
    def write_db_to_file(self, db, out_path):
        with open(out_path, 'w') as outf:
            for contact_name in db:
                contact_name = contact_name.upper()
                outf.write(self.read_contact(db, contact_name))
    
    def remove_user_from_db(self, db, contact_name):
        try:
            del db[contact_name.upper()]
        except KeyError:
            raise KeyError("No such contact: {}".format(contact_name))
    
    def debug_function(self, db, contact_name):
        formatting = """\
        CONTACT: {contact}
            First Name: {First Name}
            Last Name: {Last Name}
            Number: {Number}
            Address: {Address}
        """        
        print(db)
        self.contact_manager(db)
        
        
    def contact_manager(self, db):

        print("Type a command, help or quit to exit the program.")
        cmd = input("")
        if cmd.upper() == "HELP":
            print("Available commands are: addContact, delContact, writeFile, readFile, help, quit")
            
            self.contact_manager(db)
            
        elif cmd.upper() == "ADDCONTACT":
            
            self.add_contact_to_db_data(db)
        
        elif cmd.upper() == "WRITEFILE":
            
            self.write_db_to_file(db, "contacts.txt")
        
        elif cmd.upper() == "READFILE":
            
            self.read_contact(db, input("What contact shall you search?"))
        
        elif cmd.upper() == "DELCONTACT":
            
            self.remove_user_from_db(db, input("What contact shall you delete?").upper())
        elif cmd.upper() == "DEBUG()":
            
            print("Activating DEBUG Function.\n")
            self.debug_function(db, "")
            
            
App()
