import sqlite3
import tkinter as tk
from tkinter import ttk

class Main(tk.Frame):
	
	def __init__(self, root):
		super().__init__() # super это ссылка на род. класс
		#далее создаём главное окно
		self.init_main()
		self.db = db
		self.view_records()

	def init_main(self):
		toolbar = tk.Frame(bg='#d7d7d7', bd=2)  # область с серым фоном и рамкой
		toolbar.pack(side=tk.TOP, fill=tk.X) # сверху по всей ширине окна
	#интерфейс
		self.update_image = tk.PhotoImage(file='./img/update.png')
		button_update = tk.Button(toolbar, bg='#d7d7d7', bd=1, image=self.update_image, command=self.open_update_child) # кнопка вызова
		button_update.pack(side=tk.LEFT) # кнопка с картинкой добавления контакта

		self.add_image = tk.PhotoImage(file='./img/add.png')
		button_add = tk.Button(toolbar, bg='#d7d7d7', bd=1, image=self.add_image, command=self.open_child) # кнопка вызова
		button_add.pack(side=tk.LEFT) # кнопка с картинкой добавления контакта

		self.remove_image = tk.PhotoImage(file='./img/remove.png')
		button_remove = tk.Button(toolbar, bg='#d7d7d7', bd=1, image=self.remove_image, command=self.remove_records) # кнопка вызова
		button_remove.pack(side=tk.LEFT) # кнопка с картинкой добавления контакта

		self.search_image = tk.PhotoImage(file='./img/search.png')
		button_search = tk.Button(toolbar, bg='#d7d7d7', bd=1, image=self.search_image, command=self.open_search) # кнопка вызова
		button_search.pack(side=tk.LEFT) # кнопка с картинкой добавления контакта
		
		self.refresh_image = tk.PhotoImage(file='./img/refresh.png')
		button_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=1, image=self.refresh_image, command=self.view_records) # кнопка вызова
		button_refresh.pack(side=tk.LEFT) # кнопка с картинкой добавления контакта

	#таблица
		#колонки
		self.tree = ttk.Treeview(self, column=('ID', 'name', 'email', 'phone', 'salary'), height=45, show='headings')
		self.tree.column('ID', width=45, anchor=tk.CENTER)
		self.tree.column('name', width=300, anchor=tk.CENTER)
		self.tree.column('phone', width=150, anchor=tk.CENTER)
		self.tree.column('email', width=150, anchor=tk.CENTER)
		self.tree.column('salary', width=150, anchor=tk.CENTER)
	#заголовки
		self.tree.heading('ID', text='ID')
		self.tree.heading('name', text='name')
		self.tree.heading('phone', text='phone')
		self.tree.heading('email', text='email')
		self.tree.heading('salary', text='salary')

		self.tree.pack(side=tk.LEFT)
	def records(self, name, phone, email, salary):
		self.db.insert_data(name, phone, email, salary)
		self.view_records()

	def view_records(self): # прочиттывает все контакты и вставляет их в табличку
		self.db.crs.execute('''SELECT * FROM Contacts''')
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.crs.fetchall()]

	def update_records(self, name, phone, email, salary): # обновляет первый выделенный контакт и причём только один
		id = self.tree.set(self.tree.selection()[0], '#1')
		self.db.crs.execute('UPDATE Contacts SET name=?, phone=?, email=?, salary=? WHERE ID=?', (name, phone, email, salary, id))
		self.db.con.commit()
		self.view_records()
	def remove_records(self): # удаляет все выделеные контакты без создания нового окна (а зачем?)
		for row in self.tree.selection():
			self.db.crs.execute('DELETE FROM Contacts WHERE ID=?', (self.tree.set(row, '#1'),))
		self.db.con.commit()
		self.view_records()

	def search_records(self, name): # рыщет по колонке ФИО согласно введённой информации
		name = (f'%{name}%')
		self.db.crs.execute('SELECT * FROM Contacts WHERE name LIKE ?', (name,))
		[self.tree.delete(i) for i in self.tree.get_children()]
		[self.tree.insert('', 'end', values=row) for row in self.db.crs.fetchall()]
	# эти три метода только для открытия окон
	def open_child(self):
		Child()
	def open_update_child(self):
		UpdateChild()
	def open_search(self):
		Search()
#а теперь дочернее окно
class Child(tk.Toplevel):
	def __init__(self):
		super().__init__(root)
		self.init_child()
		self.view = app

	def init_child(self): # настройки окна
		self.title('Добавить контакт')
		self.geometry('400x220')
		self.resizable(False, False)
		self.grab_set()
		self.focus_set()
	#подсказки
		label_name = tk.Label(self, text='ФИО: ')
		label_name.place(x=50, y=50)

		label_phone = tk.Label(self, text='Телефон: ')
		label_phone.place(x=50, y=80)

		label_email = tk.Label(self, text='E-mail: ')
		label_email.place(x=50, y=110)

		label_salary = tk.Label(self, text='Зарплата: ')
		label_salary.place(x=50, y=140)
	#поля ввода
		self.entry_name = ttk.Entry(self)
		self.entry_name.place(x=200, y=50)

		self.entry_phone = ttk.Entry(self)
		self.entry_phone.place(x=200, y=80)

		self.entry_email = ttk.Entry(self)
		self.entry_email.place(x=200, y=110)

		self.entry_salary = ttk.Entry(self)
		self.entry_salary.place(x=200, y=140)
	#кнопка закрытия
		self.button_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
		self.button_cancel.place(x=300, y=170)
	#и добавления
		self.button_add = ttk.Button(self, text='Добавить')
		self.button_add.place(x=220, y=170)
	#по нажатию записывает контакт
		self.button_add.bind('<Button-1>', lambda e: self.view.records(self.entry_name.get(), self.entry_email.get(), self.entry_phone.get(), self.entry_salary.get()))

class UpdateChild(Child):
	def __init__(self):
		super().__init__()
		self.init_update_child()
		self.db = db
		self.default_data()

	def init_update_child(self):#
		self.title('Редактировать контакт')
		self.button_add.destroy()

		self.button_update = ttk.Button(self, text='Редактировать')
		self.button_update.bind('<Button-1>', lambda e: self.view.update_records(self.entry_name.get(), self.entry_email.get(), self.entry_phone.get(), self.entry_salary.get())) # кнопка обновления
		self.button_update.bind('<Button-1>', lambda e: self.destroy(), add='+') # дополнительная кнопка закрытия
		self.button_update.place(x=200, y=170)
	def default_data(self): # вставка значений по умолчанию, т. е. значения выделенного контакта
		id = self.view.tree.set(self.view.tree.selection()[0], '#1')
		self.db.crs.execute('SELECT * FROM Contacts WHERE ID=?', (id,))
		# запись изменений
		row = self.db.crs.fetchone()
		self.entry_name.insert(0, row[1])
		self.entry_phone.insert(0, row[2])
		self.entry_email.insert(0, row[3])
		self.entry_salary.insert(0, row[4])

class Search(tk.Toplevel): # здесь всё аналогично названиям и комментариям из UpdateChild, только для посика присутствует лишь одно поле
	def __init__(self):
		super().__init__(root)
		self.init_search()
		self.view = app

	def init_search(self):
		self.title('Поиск по контактам')
		self.geometry('300x110')
		self.resizable(False, False)
		self.grab_set()
		self.focus_set()

		label_name = tk.Label(self, text="ФИО")
		label_name.place(x=20, y=20)

		self.entry_name = tk.Entry(self)
		self.entry_name.place(x=70, y=20)

		self.button_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
		self.button_cancel.place(x=200, y=70)

		self.button_search = ttk.Button(self, text='Поиск')
		self.button_search.place(x=70, y=70)
		self.button_search.bind('<Button-1>', lambda e: self.view.search_records(self.entry_name.get()))
		self.button_search.bind('<Button-1>', lambda e: self.destroy(), add='+')
class DataBase(): # БД
	def __init__(self):
		self.con = sqlite3.connect('Contacts.db')
		self.crs = self.con.cursor()
		self.crs.execute('''
			CREATE TABLE IF NOT EXISTS Contacts(
					ID INTEGER PRIMARY KEY NOT NULL,
					name TEXT,
					phone TEXT,
					email TEXT,
					salary INTEGER)
		''')# создание таблицы
	def insert_data(self, name, phone, email, salary): # вставляет контакты
		self.crs.execute('''INSERT INTO Contacts(name, phone, email, salary) VALUES(?, ?, ?, ?)''', (name, phone, email, salary))
		self.con.commit()

if __name__ == '__main__':# при импорте ничего не запуститься
	# инициализация настройки и прочая подготовка
	root = tk.Tk()
	db = DataBase()
	app = Main(root)
	app.pack()
	root.title('Телефонная книга')
	root.geometry('795x450')
	root.resizable(False, False)
	root.configure(bg='white')
	root.mainloop()
