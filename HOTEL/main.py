import math
import tkinter as tk
from tkinter import ttk
import random
import sqlite3
import datetime
import tkcalendar
from datetime import *
from tkcalendar import *
from HotelAPI import *
import tkinter.messagebox as mb


#Назначение HotelAPI (Дополнительные функций)
HAPI = HotelAPI(update_callback=lambda: Hotel.UpdateDB())



def CreateDB():
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    conn2 = sqlite3.connect('rooms.db')
    c2 = conn2.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              FullName TEXT,
              Passport TEXT,
              BirthDate DATE,
              PhoneNumber TEXT,
              Arrival DATE,
              Flight TEXT,
              AllInclusive BOOLEAN,
              Comments TEXT,
              LiveRoom TEXT,
              TimeLive DATE )''')

    c2.execute('''CREATE TABLE IF NOT EXISTS rooms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  RoomNumber TEXT UNIQUE,
                  RoomType TEXT,
                  Capacity INTEGER,
                  PricePerNight REAL,
                  IsOccupied BOOLEAN,
                  LiveID INTEGER)''')
    conn.commit()
    conn.close()
    conn2.commit()
    conn2.close()


class Hotel:
    def Main():
        print("Hello!")

    def Time():
        time = datetime.now()
        print(time)


    def Module():
        print("Bye")

    def AddClient():
        def SaveClient():
            conn = sqlite3.connect('hotel.db')
            c = conn.cursor()
            #Подсчёт времени выезда
            TLive = int(Days.get())
            ADate = Arrival.get_date()
            DDate = ADate + timedelta(days=TLive)
            Departure = DDate.strftime("%Y-%m-%d")

            birth_date = BirthDate.get_date().strftime("%d-%m-%Y")
            arrival_date = Arrival.get_date().strftime("%d-%m-%Y")
            c.execute("INSERT INTO clients (FullName, Passport, BirthDate, PhoneNumber, Arrival, Flight, AllInclusive, Comments, LiveRoom, TimeLive) VALUES (?, ?, ?, ?, ?, ?, ?,?,?,?)",
                      (FullName.get(),
                       Passport.get(),
                       birth_date,
                       PhoneNumber.get(),
                       arrival_date,
                       Flight.get(),
                       vip.get(),
                       Comments.get(),
                       Room.get(),
                       Departure))  # Используем значение из чекбокса
            conn.commit()

            new_client_id = c.lastrowid


            RoomNumbers = Room.get().split()[1]
            conn2 = sqlite3.connect('rooms.db')
            c2 = conn2.cursor()
            c2.execute("UPDATE rooms SET IsOccupied = 1, LiveID = ? WHERE RoomNumber = ?", (new_client_id,RoomNumbers,))
            conn2.commit()
            conn2.close()
            addclient.destroy()
            Hotel.UpdateDB()
            conn.close()

        addclient = tk.Toplevel()
        addclient.resizable(False, False)
        addclient.geometry("512x512")
        addclient.title("New Client")
        addclient.configure(bg="#9dfcfc")
        vip = tk.BooleanVar(value=False)

        conn = sqlite3.connect('rooms.db')
        c = conn.cursor()
        c.execute("SELECT RoomNumber, RoomType FROM rooms WHERE IsOccupied = 0")
        FreeRooms = [f"{room[1]} {room[0]}" for room in c.fetchall()]
        conn.close()

        # Кнопка сохранения
        bt1 = ttk.Button(addclient, text="Внести в базу", command=SaveClient)
        bt1.place(x=220, y=480)

        # Чекбокс All Inclusive
        vipcheck = ttk.Checkbutton(addclient, text="AllInclusive", variable=vip)
        vipcheck.place(x=128,y=240)

        # Метки
        Txt1 = ttk.Label(addclient, text="Новый клиент")
        Txt2 = ttk.Label(addclient, text="ФИО")
        Txt3 = ttk.Label(addclient, text="Паспорт")
        Txt4 = ttk.Label(addclient, text="Дата Рождения")
        Txt5 = ttk.Label(addclient, text="Номер телефона")
        Txt6 = ttk.Label(addclient, text="Дата прибытия")
        Txt7 = ttk.Label(addclient, text="Номер рейса")
        Txt8 = ttk.Label(addclient, text="Особенности")
        Txt9 = ttk.Label(addclient, text="Номер")
        Txt10 = ttk.Label(addclient, text="Кол-во дней")

        # Поля ввода
        FullName = ttk.Entry(addclient, width=30)
        Passport = ttk.Entry(addclient, width=30)
        BirthDate = DateEntry(addclient, width=27, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy') # DateEntry для даты рождения
        PhoneNumber = ttk.Entry(addclient, width=30)
        Arrival = DateEntry(addclient, width=27, background='darkblue',
                        foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy') # DateEntry для даты прибытия
        Flight = ttk.Entry(addclient, width=30)
        Comments = ttk.Entry(addclient, width=50)
        Room = ttk.Combobox(addclient,values=FreeRooms, state="readonly")
        Days = ttk.Spinbox(addclient, from_=1.0, to=999, state="readonly")

        # Расположение элементов
        Txt1.place(x=256, y=0)
        Txt2.place(x=90, y=100)
        Txt3.place(x=70, y=120)
        Txt4.place(x=35, y=140)
        Txt5.place(x=25, y=160)
        Txt6.place(x=35, y=180)
        Txt7.place(x=45, y=200)
        Txt8.place(x=45, y=220)
        Txt9.place(x=380,y=50)
        Txt10.place(x=380,y=270)

        FullName.place(x=128, y=100)
        Passport.place(x=128, y=120)
        BirthDate.place(x=128, y=140)
        PhoneNumber.place(x=128, y=160)
        Arrival.place(x=128, y=180)
        Flight.place(x=128, y=200)
        Comments.place(x=128,y=220)
        Room.place(x=340,y=80)
        Days.place(x=340,y=300)


    def AddRoom():
        def SaveRoom():
            conn = sqlite3.connect('rooms.db')
            c = conn.cursor()
            c.execute("INSERT INTO rooms (RoomNumber, RoomType, Capacity, PricePerNight, IsOccupied) VALUES (?, ?, ?, ?, ?)",
                      (RoomNumber.get(),
                       RoomType.get(),
                       Capacity.get(),
                       PricePerNight.get(),False))  # Используем значение из чекбокса
            conn.commit()
            conn.close()
            addroom.destroy()
            Hotel.UpdateDB()


        addroom = tk.Toplevel()
        addroom.resizable(False, False)
        addroom.geometry("512x512")
        addroom.title("Add Room")
        roomtype = ["Люкс","Стандарт","Полу-люкс"]
        #Thanks Strelok432 for UI


        bt1 = ttk.Button(addroom, text="Внести в базу",command=SaveRoom)
        bt1.place(x=220,y=480)

        RoomNumber = ttk.Entry(addroom)
        RoomNumber.place(x=100,y=100)
        RoomType = ttk.Combobox(addroom,value=roomtype, state="readonly")
        RoomType.place(x=100,y=120)
        Capacity = ttk.Entry(addroom)
        Capacity.place(x=350,y=100)
        PricePerNight = ttk.Entry(addroom)
        PricePerNight.place(x=100,y=200)

        txt1 = ttk.Label(addroom, text="Номер комнаты")
        txt1.place(x=-1, y=100)
        txt2 = ttk.Label(addroom, text="Тип комнаты")
        txt2.place(x=-1, y=120)
        txt3 = ttk.Label(addroom, text="Цена за ночь")
        txt3.place(x=-1, y=200)
        txt4 = ttk.Label(addroom, text="Кол-во мест")
        txt4.place(x=275, y=100)
        txt5 = ttk.Label(addroom, text="Добавить номер")
        txt5.place(x=150, y=1)

    def UpdateDB():
        text_widg1.delete(0, tk.END)
        text_widg2.delete(0, tk.END)
        text_widg3.delete(0, tk.END)
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        c.execute("SELECT * FROM clients")
        rows = c.fetchall()
        conn.close() 

        today = datetime.now().date() 

        for row in rows:
            try:
                birth_date = datetime.strptime(str(row[3]), "%d-%m-%Y").strftime("%d.%m.%Y")
            except (ValueError, TypeError):
                 birth_date = "N/A"

            try:
                 arrival_date = datetime.strptime(str(row[5]), "%d-%m-%Y").strftime("%d.%m.%Y")
            except (ValueError, TypeError):
                 arrival_date = "N/A"

            all_inclusive = "Yes" if row[7] else "No"
            timelive_date_str = row[10]
            is_expired = False
            if timelive_date_str:
                try:
                    timelive_date_dt = datetime.strptime(str(timelive_date_str), "%Y-%m-%d").date()
                    if timelive_date_dt <= today:
                        is_expired = True
                except (ValueError, TypeError):
                    pass

            item_text = f"ID: {row[0]}, ФИО: {row[1]}, Телефон: {row[4]}, All Inclusive: {all_inclusive}, Дата Рождения: {birth_date}, Дата Прибытия: {arrival_date}, Комната: {row[9]}"

            text_widg1.insert(tk.END, item_text)

            current_index = text_widg1.size() - 1

            if is_expired:
                text_widg1.itemconfigure(current_index, background='red')


        conn2 = sqlite3.connect('rooms.db')
        c2 = conn2.cursor()

        # Свободные номера
        c2.execute("SELECT RoomNumber, RoomType FROM rooms WHERE IsOccupied = 0")
        for room in c2.fetchall():
            text_widg2.insert(tk.END, f"{room[1]} {room[0]}")

        # Занятые номера
        c2.execute("SELECT RoomNumber, RoomType FROM rooms WHERE IsOccupied = 1")
        for room in c2.fetchall():
            text_widg3.insert(tk.END, f"{room[1]} {room[0]}")
        conn2.close() # Закрываем соединение с rooms.db


    def EditClient():
        def LoadClientForEdit():
            selected_item = text_widg1.curselection()
            if not selected_item:
                return

            selected_client_text = text_widg1.get(selected_item[0])
            client_id_str = selected_client_text.split(',')[0].split(':')[1].strip()
            client_id = int(client_id_str)

            conn = sqlite3.connect('hotel.db')
            c = conn.cursor()
            c.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            client_data = c.fetchone()
            conn.close()

            if not client_data:
                return 

            ewin = tk.Toplevel()
            ewin.resizable(False, False)
            ewin.geometry("512x600")
            ewin.title(f"Edit Client ID: {client_id}")
            ewin.configure(bg="#9dfcfc")

            ewin.client_id = client_id

            ttk.Label(ewin, text="Редактировать клиента").place(x=200, y=10)

            ttk.Label(ewin, text="ФИО").place(x=90, y=50)
            edit_FullName = ttk.Entry(ewin, width=30)
            edit_FullName.place(x=180, y=50)
            edit_FullName.insert(0, client_data[1]) # FullName

            ttk.Label(ewin, text="Паспорт").place(x=70, y=80)
            edit_Passport = ttk.Entry(ewin, width=30)
            edit_Passport.place(x=180, y=80)
            edit_Passport.insert(0, client_data[2]) # Passport

            ttk.Label(ewin, text="Дата Рождения").place(x=35, y=110)
            edit_BirthDate = DateEntry(ewin, width=27, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
            edit_BirthDate.place(x=180, y=110)
            try:
                 edit_BirthDate.set_date(datetime.strptime(str(client_data[3]), "%d-%m-%Y"))
            except (ValueError, TypeError):
                 pass


            ttk.Label(ewin, text="Номер телефона").place(x=25, y=140)
            edit_PhoneNumber = ttk.Entry(ewin, width=30)
            edit_PhoneNumber.place(x=180, y=140)
            edit_PhoneNumber.insert(0, client_data[4]) # PhoneNumber

            ttk.Label(ewin, text="Дата прибытия").place(x=35, y=170)
            edit_Arrival = DateEntry(ewin, width=27, background='darkblue',
                                 foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
            edit_Arrival.place(x=180, y=170)
            try:
                 edit_Arrival.set_date(datetime.strptime(str(client_data[5]), "%d-%m-%Y"))
            except (ValueError, TypeError):
                 pass

            ttk.Label(ewin, text="Номер рейса").place(x=45, y=200)
            edit_Flight = ttk.Entry(ewin, width=30)
            edit_Flight.place(x=180, y=200)
            edit_Flight.insert(0, client_data[6]) # Flight

            edit_AllInclusive = tk.BooleanVar(value=client_data[7])
            ttk.Checkbutton(ewin, text="AllInclusive", variable=edit_AllInclusive).place(x=180, y=230)

            ttk.Label(ewin, text="Особенности").place(x=45, y=260)
            edit_Comments = ttk.Entry(ewin, width=50)
            edit_Comments.place(x=180, y=260)
            edit_Comments.insert(0, client_data[8]) # Comments

            ttk.Label(ewin, text="Номер").place(x=45, y=290)
            conn_rooms = sqlite3.connect('rooms.db')
            c_rooms = conn_rooms.cursor()
            c_rooms.execute("SELECT RoomNumber, RoomType FROM rooms WHERE IsOccupied = 0 UNION SELECT RoomNumber, RoomType FROM rooms WHERE LiveID = ?", (client_id,))
            AvailableRooms = [f"{room[1]} {room[0]}" for room in c_rooms.fetchall()]
            conn_rooms.close()

            edit_Room = ttk.Combobox(ewin, values=AvailableRooms, state="readonly")
            edit_Room.place(x=180, y=290)
            current_room = client_data[9]
            if current_room in AvailableRooms:
                edit_Room.set(current_room)

            ttk.Label(ewin, text="Кол-во дней").place(x=45, y=320)
            current_arrival_str = client_data[5]
            current_timelive_str = client_data[10]
            current_days = 0
            if current_arrival_str and current_timelive_str:
                 try:
                      arrival_date_dt = datetime.strptime(str(current_arrival_str), "%d-%m-%Y")
                      timelive_date_dt = datetime.strptime(str(current_timelive_str), "%Y-%m-%d") # Assuming YYYY-MM-DD format from SaveClient
                      current_days = (timelive_date_dt - arrival_date_dt).days
                 except (ValueError, TypeError):
                      pass


            edit_Days = ttk.Spinbox(ewin, from_=1.0, to=999, state="readonly")
            edit_Days.place(x=180, y=320)
            if current_days > 0:
                 edit_Days.set(current_days)
            else:
                 edit_Days.set(1)



            ttk.Button(ewin, text="Сохранить изменения", command=lambda: SaveEditedClient(
                ewin, client_id, edit_FullName, edit_Passport, edit_BirthDate,
                edit_PhoneNumber, edit_Arrival, edit_Flight, edit_AllInclusive,
                edit_Comments, edit_Room, edit_Days, client_data[9]
            )).place(x=200, y=550)

        def SaveEditedClient(window, client_id, FullName_entry, Passport_entry, BirthDate_dateentry,
                             PhoneNumber_entry, Arrival_dateentry, Flight_entry, AllInclusive_var,
                             Comments_entry, Room_combobox, Days_spinbox, old_room_str):

            conn = sqlite3.connect('hotel.db')
            c = conn.cursor()
            conn_rooms = sqlite3.connect('rooms.db')
            c_rooms = conn_rooms.cursor()


            try:
                TLive_days = int(Days_spinbox.get())
                Arrival_date = Arrival_dateentry.get_date()
                Departure_date = Arrival_date + timedelta(days=TLive_days)
                Departure_str = Departure_date.strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                Departure_str = None 

            try:
                 birth_date_str = BirthDate_dateentry.get_date().strftime("%d-%m-%Y")
            except (ValueError, TypeError):
                 birth_date_str = None

            try:
                 arrival_date_str = Arrival_dateentry.get_date().strftime("%d-%m-%Y")
            except (ValueError, TypeError):
                 arrival_date_str = None


            new_room_str = Room_combobox.get()
            old_room_number = None
            new_room_number = None


            if old_room_str and " " in old_room_str:
                old_room_number = old_room_str.split(" ")[1]


            if new_room_str and " " in new_room_str:
                 new_room_number = new_room_str.split(" ")[1]



            if new_room_number != old_room_number:

                 if old_room_number:
                      c_rooms.execute("UPDATE rooms SET IsOccupied = 0, LiveID = NULL WHERE RoomNumber = ?", (old_room_number,))

                 if new_room_number:
                      c_rooms.execute("UPDATE rooms SET IsOccupied = 1, LiveID = ? WHERE RoomNumber = ?", (client_id, new_room_number,))

            c.execute("""UPDATE clients SET
                         FullName = ?,
                         Passport = ?,
                         BirthDate = ?,
                         PhoneNumber = ?,
                         Arrival = ?,
                         Flight = ?,
                         AllInclusive = ?,
                         Comments = ?,
                         LiveRoom = ?,
                         TimeLive = ?
                         WHERE id = ?""",
                      (FullName_entry.get(),
                       Passport_entry.get(),
                       birth_date_str,
                       PhoneNumber_entry.get(),
                       arrival_date_str,
                       Flight_entry.get(),
                       AllInclusive_var.get(),
                       Comments_entry.get(),
                       new_room_str,
                       Departure_str,
                       client_id))

            conn.commit()
            conn_rooms.commit()

            conn.close()
            conn_rooms.close()

            window.destroy() 
            Hotel.UpdateDB() 

        LoadClientForEdit()

    def UpdateDB():
        text_widg1.delete(0, tk.END)
        text_widg2.delete(0, tk.END)
        text_widg3.delete(0, tk.END)

        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        c.execute("SELECT * FROM clients")
        rows = c.fetchall()
        conn.close()

        today = datetime.now().date()

        for row in rows:
            try:
                birth_date = datetime.strptime(str(row[3]), "%d-%m-%Y").strftime("%d.%m.%Y")
            except (ValueError, TypeError):
                 birth_date = "N/A"

            try:
                 arrival_date = datetime.strptime(str(row[5]), "%d-%m-%Y").strftime("%d.%m.%Y")
            except (ValueError, TypeError):
                 arrival_date = "N/A"

            all_inclusive = "Yes" if row[7] else "No"


            timelive_date_str = row[10]
            is_expired = False
            if timelive_date_str:
                try:
                    timelive_date_dt = datetime.strptime(str(timelive_date_str), "%Y-%m-%d").date()
                    if timelive_date_dt <= today:
                        is_expired = True
                except (ValueError, TypeError):
                    pass

            item_text = f"ID: {row[0]}, ФИО: {row[1]}, Телефон: {row[4]}, All Inclusive: {all_inclusive}, Дата Рождения: {birth_date}, Дата Прибытия: {arrival_date}, Комната: {row[9]}"


            text_widg1.insert(tk.END, item_text)


            current_index = text_widg1.size() - 1

            if is_expired:
                text_widg1.itemconfigure(current_index, background='red')



        conn2 = sqlite3.connect('rooms.db')
        c2 = conn2.cursor()

        # Свободные номера
        c2.execute("SELECT RoomNumber, RoomType FROM rooms WHERE IsOccupied = 0")
        for room in c2.fetchall():
            text_widg2.insert(tk.END, f"{room[1]} {room[0]}")

        # Занятые номера
        c2.execute("SELECT RoomNumber, RoomType FROM rooms WHERE IsOccupied = 1")
        for room in c2.fetchall():
            text_widg3.insert(tk.END, f"{room[1]} {room[0]}")
        conn2.close()
        
    def DeleteClient():
        selected_item = text_widg1.curselection()
        if not selected_item:
            mb.showwarning("Ошибка", "Выберите клиента для удаления.")
            return

        selected_client_text = text_widg1.get(selected_item[0])
        client_id_str = selected_client_text.split(',')[0].split(':')[1].strip()
        try:
            client_id = int(client_id_str)
        except ValueError:
             mb.showerror("Ошибка", "Не удалось определить ID клиента.")
             return


        confirm = mb.askyesno(
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить клиента с ID: {client_id}?"
        )

        if confirm:
            conn_hotel = sqlite3.connect('hotel.db')
            c_hotel = conn_hotel.cursor()
            conn_rooms = sqlite3.connect('rooms.db')
            c_rooms = conn_rooms.cursor()

            try:

                c_hotel.execute("SELECT LiveRoom FROM clients WHERE id = ?", (client_id,))
                room_info = c_hotel.fetchone()
                old_room_str = room_info[0] if room_info else None


                c_hotel.execute("DELETE FROM clients WHERE id = ?", (client_id,))


                if old_room_str and " " in old_room_str:
                    old_room_number = old_room_str.split(" ")[1]
                    c_rooms.execute("UPDATE rooms SET IsOccupied = 0, LiveID = NULL WHERE RoomNumber = ?", (old_room_number,))

                conn_hotel.commit()
                conn_rooms.commit()
                mb.showinfo("Успех", "Клиент успешно удален.")

            except sqlite3.Error as e:
                conn_hotel.rollback()
                conn_rooms.rollback()
                mb.showerror("Ошибка базы данных", f"Ошибка при удалении клиента: {e}")

            finally:
                conn_hotel.close()
                conn_rooms.close()
                Hotel.UpdateDB()

    def ProcessCheckoutButton():
        selected_item = text_widg1.curselection()
        if not selected_item:
            mb.showwarning("Ошибка", "Выберите клиента для оформления выезда и оплаты.")
            return

        selected_client_text = text_widg1.get(selected_item[0])
        try:
            id_start = selected_client_text.find("ID:") + 3
            id_end = selected_client_text.find(",", id_start)
            if id_end == -1:
                 client_id_str = selected_client_text[id_start:].strip()
            else:
                 client_id_str = selected_client_text[id_start:id_end].strip()

            client_id = int(client_id_str)
        except (ValueError, IndexError):
             mb.showerror("Ошибка", "Не удалось определить ID клиента из выбранной строки.")
             return

        conn_hotel = sqlite3.connect('hotel.db')
        c_hotel = conn_hotel.cursor()
        conn_rooms = sqlite3.connect('rooms.db')
        c_rooms = conn_rooms.cursor()

        total_cost = 0.0
        error_calculating_cost = False

        try:
            c_hotel.execute("SELECT Arrival, TimeLive, LiveRoom FROM clients WHERE id = ?", (client_id,))
            client_row = c_hotel.fetchone()

            if client_row:
                arrival_date_str = client_row[0] # Дата прибытия в формате "%d-%m-%Y"
                timelive_date_str = client_row[1] # Дата выезда (TimeLive) в формате "%Y-%m-%d"
                live_room_str = client_row[2] # Строка с типом и номером комнаты, например "Люкс 101"

                # Рассчитываем количество дней проживания
                num_days = 0
                if arrival_date_str and timelive_date_str:
                    try:
                        arrival_dt = datetime.strptime(str(arrival_date_str), "%d-%m-%Y").date()
                        timelive_dt = datetime.strptime(str(timelive_date_str), "%Y-%m-%d").date()
                        # Количество дней = дата выезда - дата прибытия
                        num_days = (timelive_dt - arrival_dt).days
                        if num_days < 0: num_days = 0 # Если дата выезда раньше прибытия (ошибка в данных), считаем 0 дней
                    except (ValueError, TypeError) as e:
                        print(f"Error parsing dates for client ID {client_id}: {e}")
                        error_calculating_cost = True


                room_number = live_room_str.split(" ")[-1] if " " in live_room_str else None

                if room_number:
                    # Получаем цену за ночь из таблицы rooms
                    c_rooms.execute("SELECT PricePerNight FROM rooms WHERE RoomNumber = ?", (room_number,))
                    room_row = c_rooms.fetchone()

                    if room_row:
                        price_per_night = room_row[0]
                        # Рассчитываем общую стоимость
                        total_cost = price_per_night * num_days
                        print(f"Calculated cost for client ID {client_id}: {price_per_night} * {num_days} = {total_cost}") # Лог для отладки
                    else:
                        print(f"Warning: Room number {room_number} not found in rooms table for price lookup.")
                        error_calculating_cost = True
                else:
                    print(f"Warning: Could not extract room number from LiveRoom string '{live_room_str}' for client ID {client_id} for price lookup.")
                    error_calculating_cost = True
            else:
                print(f"Error: Client with ID {client_id} not found in clients table during cost calculation.")
                error_calculating_cost = True # Клиент не найден, расчет невозможен

        except sqlite3.Error as e:
            print(f"Database error during cost calculation for client ID {client_id}: {e}")
            mb.showerror("Ошибка БД", f"Ошибка при расчете стоимости проживания: {e}")
            return

        finally:
            conn_hotel.close()
            conn_rooms.close()

        if error_calculating_cost:
             mb.showwarning("Предупреждение", "Не удалось рассчитать стоимость проживания автоматически. Пожалуйста, введите сумму вручную.")
             HAPI.Payment(client_id, None)
        else:
             HAPI.Payment(client_id, total_cost)



# Main Menu 
ui = tk.Tk()
ui.resizable(False, False)
ui.geometry("1366x768")
ui.configure(bg="#ffcb73")
ui.title("Hotel Reception")

# Компоненты UI
text_widg1 = tk.Listbox(ui, height=20, width=60)
text_widg2 = tk.Listbox(ui, height=23, width=60)
text_widg3 = tk.Listbox(ui, height=22, width=60)
text_frame = tk.Frame(ui)
text_frame.pack(padx=20, pady=20)

# Кнопки
bt1 = ttk.Button(ui, text="Внести в базу", command=Hotel.AddClient)
bt2 = ttk.Button(ui, text="Редактировать базу",command=Hotel.EditClient)
bt3 = ttk.Button(ui, text="Добавить номер", command=Hotel.AddRoom)
bt4 = ttk.Button(ui, text="Расписание", command=HAPI.Schedule)
bt5 = ttk.Button(ui, text="События", command=HAPI.Events)
bt6 = ttk.Button(ui, text="Уборка и проверка", command=HAPI.Inspect)
bt7 = ttk.Button(ui, text="Удалить клиента", command=Hotel.DeleteClient)
bt8 = ttk.Button(ui, text="Выселение", command=Hotel.ProcessCheckoutButton)

# Списки и меню
scb1 = ttk.Scrollbar(ui, command=text_widg1.yview)
scb2 = ttk.Scrollbar(ui, command=text_widg2.yview,orient=tk.VERTICAL)
scb3 = ttk.Scrollbar(ui, command=text_widg3.yview,orient=tk.VERTICAL)


# Расположение UI
bt1.place(x=0, y=0)
bt2.place(x=83, y=0)
bt3.place(x=200,y=0)
bt4.place(x=300,y=0)
bt5.place(x=375,y=0)
bt6.place(x=990,y=0)
bt7.place(x=450, y=0)
bt8.place(x=1105, y=0)
scb1.pack(side=tk.LEFT, fill=tk.Y)
scb2.place(x=1350,y=40,height=370)
scb3.place(x=1350,y=410,height=360)
text_widg1.pack(side=tk.LEFT, fill=tk.Y, expand=False)
text_widg2.place(x=990,y=40)
text_widg3.place(x=990,y=410)

# Конфиги
text_widg1.config(yscrollcommand=scb1.set)
text_widg2.config(yscrollcommand=scb2.set)
text_widg3.config(yscrollcommand=scb3.set)

#Инициализация БД
CreateDB()
Hotel.UpdateDB()
Hotel.Time()

ui.mainloop()
