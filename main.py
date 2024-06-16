import re
import sqlite3 as sq
from conf import dir

class logg:
    def __init__(self, h: str = None,  t: str = None, r: str = None, s: str = None ):
        self.h = h
        self.t = t
        self.r = r
        self.s = s

    def __repr__(self):
        return f'{self.h}, {self.t}, {self.r}, {self.s}'


def parse():
    f = open("logs.txt", 'r', encoding='UTF-8')
    lines = f.readlines()
    f.close()
    lines = [line.rstrip() for line in lines]
    newArr = []
    pattern = r'(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*)\] "(.*)" (\d*)'
    for line in lines:
        newLog = logg()
        newLog.h, newLog.t, newLog.r, newLog.s = re.split(pattern, line)[1:-1]
        newArr.append(newLog)
    return newArr


logsArr = parse()
print(logsArr)

def writeToDB(data):
    try:
        con = sq.connect('practik.db')
        cursor = con.cursor()
        for log in data:
            cursor.execute("""INSERT OR IGNORE INTO logs
                              (h, t, r, s )
                              VALUES
                              (?, ?, ?, ?);""", [log.h,  log.t, log.r, log.s])
            con.commit()
        cursor.close()

    except sq.Error as error:
        print("Возникла ошибка", error)
    finally:
        if con:
            con.close()
            print("Соединение невозможно")

writeToDB(logsArr)

###############################################################################################

def selectToUser():
    try:
        con = sq.connect('practik.db')
        cursor = con.cursor()
        match input('Вы готовы выбрать временной диапазон? (y или n): '):
            case 'n':
                ans = cursor.execute("""SELECT * FROM logs;""").fetchall()
                con.commit()
                cursor.close()
                print(ans)
            case 'y':
                startTime = input('Введите время (Формат ЧЧ:MM:СС): ')
                endTime = input('Введите  время (Формат ЧЧ:MM:СС): ')
                ans = cursor.execute(f"""select * FROM logs WHERE CAST((substr(t, 13, 2)||substr(t, 16, 2)||substr(t, 19, 2)) AS intege) BETWEEN {startTime.replace(':', '')} AND {endTime.replace(':', '')};""").fetchall()
                con.commit()
                cursor.close()
                print(ans)
    except sq.Error as error:
        print("Ошибка при работе ", error)
    finally:
        if con:
            con.close()
            print("Соединение  закрыто")

selectToUser()