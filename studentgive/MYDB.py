import pymssql

server = "LAPTOP-KS13NLRE"
user = "hyy"
password = "1234567"
database = "Studentgive"
charset = "utf8"


class MyDBHelper:

    def GetuserInfo(self):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        userinfor = cs.execute("SELECT * FROM register ")
        userinfor = cs.fetchall()
        conn.commit()
        return userinfor

    def CreateDatabase(self, sql):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute(sql)
        print("成功")
        conn.close()
    #返回了一个username所有的信息
    def Checkusersame(self, name):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute("SELECT * FROM register where username=%s", name)
        username = cs.fetchall()
        conn.commit()
        return username
    #返回了一个tusername所有的信息
    def Checktusersame(self, name):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute("SELECT * FROM tregister where tusername=%s", name)
        username = cs.fetchall()
        conn.commit()
        return username
    #加入user
    def adduser(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("INSERT INTO register(username,password) values(%s,%s)", args)
        row=cs.rowcount
        print(type(row))
        conn.commit()
        return row
    #加入tuser
    def addtuser(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("INSERT INTO tregister(tusername,tpassword) values(%s,%s)", args)
        row = cs.rowcount
        print(type(row))
        conn.commit()
        return row
    #添加file
    def addshenhefile(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("INSERT INTO shenhe(username,filename,myorder,realname) values(%s,%s,%s,%s)",args)
        row = cs.rowcount
        print(type(row))
        conn.commit()
        return row

    def GettPassword(self, username):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(username)
        cs.execute("SELECT * FROM tregister where tusername=%s",username)
        password2=cs.fetchall()
        conn.commit()
        return  password2[0][1]

    def GetPassword(self, username):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(username)
        cs.execute("SELECT * FROM register where username=%s", username)
        password2 = cs.fetchall()
        conn.commit()
        return password2[0][1]
    def Gettinform(self,username):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(username)
        cs.execute("SELECT * FROM tregister where tusername=%s", username)
        password2 = cs.fetchall()
        conn.commit()
        return password2

    def checkfile(self,username):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(username)
        cs.execute("SELECT * FROM shenhe where username=%s", username)
        password2 = cs.fetchall()
        conn.commit()
        return password2


    def addtext(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("UPDATE tregister set tinform='%s' where tusername='%s'"%args)
        row=cs.rowcount
        print(row)
        conn.commit()
        return  row

    def addtrealname(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("UPDATE register set trealname='%s' where username='%s'"%args)
        row=cs.rowcount
        print(row)
        conn.commit()
        return row

    def addtusername(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("UPDATE register set tusername='%s' where username='%s'"%args)
        row=cs.rowcount
        print(row)
        conn.commit()
        return row

    def addrealname(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("UPDATE register set realname='%s' where username='%s'" %args )
        row = cs.rowcount
        print(row)
        conn.commit()
        return row
    def getshenhern(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("SELECT realname from register where username='%s'" %args )
        list = cs.fetchall()
        conn.commit()
        return list


    #从里面得到realname和username
    def getallstudent(self):
        conn = pymssql.connect(server, user, password, database, charset)
        cs=conn.cursor()
        cs.execute("SELECT username,realname from register")
        list=cs.fetchall()
        conn.commit()
        return list



    def addshenhetn(self, args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("UPDATE shenhe set tusername='%s' where username='%s'" %args)
        row = cs.rowcount
        print(row)
        conn.commit()
        return row

    def getaudit(self, stname):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute("SELECT audit from shenhe where username='%s'"%stname)
        list = cs.fetchall()
        conn.commit()
        return list

    def addaudit(self,args):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        print(args)
        cs.execute("UPDATE shenhe set audit='%s' where username='%s'and myorder='%s'" %args)
        row = cs.rowcount
        print(row)
        conn.commit()
        return row

    def getfilename(self, sargs):
            conn = pymssql.connect(server, user, password, database, charset)
            cs = conn.cursor()
            print(sargs)
            cs.execute("SELECT * FROM shenhe where username='%s' and myorder='%s'"%sargs)
            password2 = cs.fetchall()
            conn.commit()
            return password2

    def getallshenhe(self, args):
            conn = pymssql.connect(server, user, password, database, charset)
            cs = conn.cursor()
            cs.execute("SELECT username,realname,audit,myorder from shenhe where username='%s'"%args)
            list = cs.fetchall()
            print(type(list))
            conn.commit()
            return list

    def getshenhelist(self):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute("SELECT username,realname,audit,myorder from shenhe")
        list = cs.fetchall()
        conn.commit()
        return list

    def deleteuser(self, stname):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute("DELETE from register where username='%s'"%stname)
        row = cs.rowcount
        print(row)
        conn.commit()
        return row
    def deleteusershenhe(self, stname):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute("DELETE from shenhe where username='%s'"%stname)
        row = cs.rowcount
        print(row)
        conn.commit()
        return row

    def getsthistorylist(self, username):
        conn = pymssql.connect(server, user, password, database, charset)
        cs = conn.cursor()
        cs.execute("SELECT username,realname,audit,myorder from shenhe where username='%s'"%username)
        list = cs.fetchall()
        conn.commit()
        return list
