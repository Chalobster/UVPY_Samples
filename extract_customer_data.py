import sys
from datetime import datetime, date, timedelta
import uopy

savedListName = "SAVED_CUST"

def makeconnection(user, password):
    config = {
             'user': user,
             'password': password,
             'service': 'uvcs',
             'host':    'localhost',
             'account': 'HS.SALES',
             #'encoding': 'GB18030',
         }
    try:
        status = 0
        thissession = uopy.connect(**config)
    except uopy.UOError as e:
        print(str(e.code))
        status = e.code
        thissession = "not connected"
    return status, thissession

def selectitems():
    # this is a UniVerse SELECT command -- no semi-colon at end!
    cmd1 = uopy.Command("SELECT CUSTOMER @ID WITH BUY_DATE EQ '01/08/1991'")
    cmd1.run()
    print(cmd1.response)
    #if cmd1.response.startswith("0 Record(s)"):
    #   print("No items selected")
    #   sys.exit()

    # save the IDs selected above
    cmd2 = uopy.Command("SAVE-LIST " + savedListName)
    cmd2.run()
    print(cmd2.response)
    #if "record(s) SAVEd to SELECT list" not in cmd2.response:
        #   print("No items saved to &SAVEDLISTS&")
        #   sys.exit()


    with uopy.File("&SAVEDLISTS&") as savedListsFile:
        try:
            savedList = savedListsFile.read(savedListName)
        except uopy.UOError as e:
            print("Error reading &SAVEDLISTS& " + savedListName)
            sys.exit()
        return savedList

def getrealdate(uvdate):
	# Pick/U2 epoch date
    return datetime(1967, 12, 31, 0, 0) + timedelta(days=uvdate)

status, session = makeconnection('xxxxx', '......')
print ("STATUS: " + str(status))
print("SESSION: " + str(session))

if status != 0:
    sys.exit()

itemslist = selectitems()
if itemslist.count == 0:
    sys.exit()

with uopy.File("CUSTOMER") as custFile:
    for custid in itemslist:
        print("ID: " + str(custid))
        cust = custFile.read(custid)
        # attrNbr = 0
        # for attr in cust:
        #     attrNbr += 1
        #     print(str(attrNbr) + " " + str(attr))
        print(cust[1] + " " + cust[2] + " ProdIDs: " + str(cust[10]) )
        for buydate in uopy.DynArray( cust[13]):
            print("    buy_date: " + buydate + " - " + str(getrealdate(int(buydate))))

#todo:see about closing session before exiting
