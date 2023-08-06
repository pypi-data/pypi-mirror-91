class Student:
    def __init__(self,name): #ฟังกชันพิเศษ เพื่อให้สามารถรันได้ self คำพิเศษ เพื่อใช้เเทนตัวมันเอง ใช้คำอืนเเทน self ได้
        self.name=name
        self.exp=0
        self.lesson=0
        self.AddEXP(10)


    def Hello(self):
        print('สวัสดี  เราชื่อ {}'.format(self.name))

    def Coding(self):
        print('{} กำลังเขียนโปนเเกรม'.format(self.name))
        self.exp +=5
        self.lesson +=1
    def ShowExp(self):
        print('{} exp {}'.format(self.name, self.exp))
        print('เรียนไป {} ครั้ง'.format(self.lesson))
    def AddEXP(self,score):
        self.lesson +=1
        self.exp +=score

class SpecialStudent(Student):
    def __init__(self,name,father):
        super().__init__(name) #ฟังชันพิเศษ กำหนด __init__ เรียกคล่าส student เเละเอ่ name เข้าไป
        self.father=father
        mafia=['Gates','Tomas Edison']
        if father in mafia:
            self.exp +=100
    def AddEXP(self,score):
        self.lesson += 1
        self.exp += (score*3)
    def AskEXP(self,score=10):
        print('ครู ! ขอคะเเนนผมหน่อยสิสัก {} EXP'.format(score))
        self.AddEXP(10)

print(__name__)
if __name__=='__main__': #เชคว่าอยุ่ในไฟล์ main ไหม

    jack = Student('spadun')  # st = ออปเจค
    print(jack.name)
    jack.Hello()
    student2 = Student('Steve')
    print(student2.name)
    student2.Hello()

    jack.AddEXP(10)

    print(jack.name, jack.exp)
    print(student2.name, student2.exp)

    for i in range(5):
        student2.Coding()

    jack.ShowExp()
    student2.ShowExp()
