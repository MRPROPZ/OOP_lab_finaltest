import sqlite3

class SqliteBMI:
    def __init__(self, dbname=None):
        self.conn = None
        self.cursor = None
        if dbname:
            self.open(dbname)

    def open(self, dbname):
        try:
            self.conn = sqlite3.connect(dbname)
            self.cursor = self.conn.cursor()
            print(sqlite3.version)
        except sqlite3.Error as e:
            print("Failed to connect db...")

    def insert(self, query, datainsert):
        c = self.cursor
        c.execute(query, datainsert)
        self.conn.commit()

    def delete(self, query):
        c = self.cursor
        c.execute(query)
        self.conn.commit()

    def select(self, query):
        c = self.cursor
        c.execute(query)
        return c.fetchall()

    def edit(self, query, dataupdate):
        c = self.cursor
        c.execute(query, dataupdate)
        self.conn.commit()

#test = SqliteUser("test.db")
#test.insert("INSERT INTO users(name,year,admin) "
#            "VALUES('BB',2010,0)")
#print(test.select("SELECT * FROM users"))

class BMI:
    def __init__(self, name, sex, wei, hei):
        self.name = name
        self.sex = sex
        self.weight = wei
        self.height = hei
        self.bmi = 0.0

    def getBMI(self):
        hei = self.height
        if self.sex == 1:
            hei = hei-10
        hei_m = hei/100
        self.bmi = self.weight/(hei_m*hei_m)
        return self.bmi

    def getBMImeaning(self):
        if self.bmi >30.0:
            return "Obese"
        elif self.bmi>25.0:
            return "Overweight"
        elif self.bmi>18.5:
            return "Normal"
        else:
            return "Underweight"

    def getName(self):
        return self.name

    def getSex(self):
        return self.sex

    def getWeight(self):
        return self.weight

    def getHeight(self):
        return self.height


#b = BMI("aa", 1, 60, 165)
#print(b.name, b.sex, b.weight, b.bmi)
#print(b.getBMI())