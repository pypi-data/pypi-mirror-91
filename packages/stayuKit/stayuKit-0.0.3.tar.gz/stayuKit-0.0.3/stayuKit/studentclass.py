# studentclass.py

class Student:
	def __init__(self,name): # self คือคำพิเศษใช้แทนตัวมันเอง ใช้คำอื่นได้
		self.name=name # 1.ตั้ง name
		self.exp=0
		self.lesson=0

	def Hello(self):
		print('สวัสดีจ้า ผมชื่อ {}'.format(self.name))

	def Coding(self):
		print('{} ตอนนี้กำลังเขียนโปรแกรม...'.format(self.name))
		self.exp+=5
		self.lesson+=1

	def ShowEXP(self):
		print('ตอนนี้ {} มีประสบการณ์ {} EXP'.format(self.name,self.exp))
		print('- เรียนไป {} ครั้งแล้ว'.format(self.lesson))

	def PassLesson(self,score):
		self.exp += score
		self.lesson+=1


class SpecialStudent(Student): # ทำแบบ inheritant (สืบทอด) ใน cheat

	def __init__(self,name,father): # บัคับให้ใส่ name กับ father
		super().__init__(name) # super เป็น fn พิเศษกำหนด init /double underscroll, dundle
		self.father=father
		mafia=['Bill Gates','Indiana Jones']
		if father in mafia:
			self.exp+=100

	def PassLesson(self,score):
		self.exp += score*3
		self.lesson+=1

	def AskEXP(self,score=10):
		print('ครู ผมขอคะแนนเพิ่มหน่อยสัก {} คะแนน'.format(score))
		self.PassLesson(score)

# print(__name__)
if __name__ == '__main__': # พิมพ์ ifmain กด enter

	print('======1 Jan======')
	student0=SpecialStudent('Mark Zuckerberg','Bill Gates')
	student0.ShowEXP()
	student0.AskEXP()
	student0.ShowEXP()
	student1=Student('Albert') # คือตัวแปรประเภท object
	print(student1.name)
	student1.Hello() #Calling method

	student2=Student('Steve') # คือตัวแปรประเภท object
	print(student2.name)
	student2.Hello()

	print('======2 Jan======')
	print('----ใครอยากเรียน coding บ้าง ได้ 10 exp')
	student1.PassLesson(10) #Calling method

	print('======3 Jan======')
	student1.name='Albert Ei' # Modify attribute
	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่แล้ว')

	print(student1.name,student1.exp)
	print(student2.name,student2.exp)

	print('======4 Jan======')
	for i in range(5):
		student2.Coding()

	student1.ShowEXP()
	student2.ShowEXP()

