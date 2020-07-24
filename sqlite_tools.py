import sqlite3

class ExportTable:
    def __init__(self, db):
        self.db = db

    def Convete(self, table_name, isTabel = True):
        sql = self.GetSqlCreate(table_name) + ";\n\n"

        if (isTabel):
            sql = sql + self.GetValueFormTable(table_name)

        fo = open(table_name + ".sql", "w")
        fo.write(sql)
        fo.close()

        print(table_name + " --> OK")

    def GetTableList(self):
        con = sqlite3.connect(self.db)
        
        data = con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")

        tables = []

        for row in data:
            tables.append(row[0])

        con.close()
        return tables

    def GetViewList(self):
        con = sqlite3.connect(self.db)

        data = con.execute("SELECT name FROM sqlite_master WHERE type = 'view'")

        Views = []

        for row in data:
            Views.append(row[0])

        con.close()
        return Views

    def GetSqlCreate(self, table_name):
        con = sqlite3.connect(self.db)
        data = con.execute("SELECT sql FROM sqlite_master WHERE name = '" + table_name + "'")
        
        sql = ""

        for row in data:
            sql = row[0]

        con.close()
        return sql

    def GetValueFormTable(self, table_name):
        con = sqlite3.connect(self.db)
        dataName = con.execute("PRAGMA table_info(" + table_name + ")")
        DataCount = con.execute("SELECT count(*) FROM Dyr")
        data = con.execute("SELECT * FROM " + table_name)

        colName = []
        colType = []
        TableCount = 0

        for row in DataCount:
            TableCount = row[0]

        for row in dataName:
            colName.append(row[1])
            colType.append(row[2])

        sql = "INSERT INTO " + table_name + "(" + ",".join(colName) + ") VALUES \n"

        Count = 0

        for row2 in data:
            index = 0
            listDatas = map(str, row2)
            sql = sql + "("
            for listData in listDatas:
                if(listData == "None"):
                    sql = sql + "NULL"
                elif (colType[index] == "TEXT"):
                    sql = sql + "'" + listData + "'"
                else:
                    sql = sql + listData
                
                # Is that the last col?
                # If so, it should not put it ,
                if (index != len(colType) - 1):
                    sql = sql + ","

                
                index = index + 1

            sql = sql + ")"

            if(Count < TableCount - 1):
                sql = sql + ",\n"
            else:
                sql = sql + ";"

            Count = Count + 1

        con.close()
        return sql


if __name__ == "__main__":
    import os.path

    print("\n ######   #######  ##       #### ######## ########     #######      ######   #######  ##       \n##    ## ##     ## ##        ##     ##    ##          ##     ##    ##    ## ##     ## ##       \n##       ##     ## ##        ##     ##    ##                 ##    ##       ##     ## ##       \n ######  ##     ## ##        ##     ##    ######       #######      ######  ##     ## ##       \n      ## ##  ## ## ##        ##     ##    ##          ##                 ## ##  ## ## ##       \n##    ## ##    ##  ##        ##     ##    ##          ##           ##    ## ##    ##  ##       \n ######   ##### ## ######## ####    ##    ########    #########     ######   ##### ## ######## \n")

    dbSti = input("Database path > ")

    if(os.path.isfile(dbSti) == False):
        print("Database not found")
        exit()

    test = ExportTable(dbSti)
    while True:
        print("-------------------------------------------")
        print("[0] Exit")
        print("[1] Table")
        print("[2] View")
        print("-------------------------------------------")
        menuIndex = int(input("Menu > "))

        if (menuIndex == 0):
            break
        elif (menuIndex == 1):
            tableList = test.GetTableList()
            if(len(tableList) != 0):
                print("-------------------------------------------")
                couter = 2
                print("[0] Gå back")
                print("[1] Export everyone on this list")
                for table in tableList:
                    print("[" + str(couter) + "] " + table)
                    couter = couter + 1
                print("-------------------------------------------")
                tableIndex = int(input("Index of table> "))

                if (tableIndex != 0):
                    if (tableIndex == 1):
                        for table in tableList:
                            test.Convete(table)
                    else:
                        test.Convete(tableList[tableIndex - 2])
            else:
                print("-------------------------------------------")
                print("!!! NO TABLE !!!")
        
        elif (menuIndex == 2):
            viewList = test.GetViewList()
            if(len(viewList) != 0):
                print("-------------------------------------------")
                couter = 1
                print("[0] Gå back")
                print("[1] Export everyone on this list")
                for view in viewList:
                    print("[" + str(couter) + "] " + view)
                    couter = couter + 1
                print("-------------------------------------------")
                viewIndex = int(input("Index of view> "))

                if (viewIndex != 0):
                    if(viewIndex == 1):
                        for View in viewList:
                            test.Convete(View)
                    else:
                        test.Convete(viewList[viewIndex - 1], False)
            else:
                print("-------------------------------------------")
                print("!!! NO VIEW !!!")
