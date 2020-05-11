from tkinter import *
from PIL import ImageTk,Image
from datetime import date
from datetime import datetime
from passlib.context import CryptContext
import os
import fileinput
import sys
import time
import Adafruit_DHT

username = ""
password = ""

# username
username_info = []
for line in open('usernames.txt'):
    line = line.strip()
    username_info.append(line)
   
# password
password_info = []
for line in open('passwords.txt'):
    line = line.strip()
    password_info.append(line)
    
# password encryption
pass_context = CryptContext {
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
}
    
username = username_info[0]
password = password_info[0]
counter = 0
background_color = '#000000'
label_color = '#bb1042'
text_color = '#75aa28'
white = '#FFFFFF'
login_w = 360


def launch_home_page():
    
    
    def clock_tick():
        time_string = time.strftime('%H:%M:%S')
        clock.config(text=time_string)
        clock.after(180,clock_tick)
        
    def spawn_clock():
        clock.place(x=600, y=180)
        clock_tick()
        today = date.today()
        today = today.strftime("%b %d, %Y")
        day = datetime.today().strftime('%A')
        day_today = Label(home, font=('Helvetica', 24), bg=background_color, fg=text_color,
                      text=day)
        day_today.place(x=600, y=310)
        date_today = Label(home, font=('Helvetica', 24), bg=background_color, fg=text_color, text=today)
        date_today.place(x=600, y=400)
    
    def spawn_buttons():
        degree_symbol = Button(home, text='Temperature', bg=background_color,
                           fg=label_color, font=("Helvetica", 24), highlightthickness=0,
                           highlightbackground=text_color, disabledforeground=label_color,
                           command=temperature_pressed)
        degree_symbol.place(x=180, y=70)
        humidity_symbol = Button(home, text='Humidity', bg=background_color, fg=label_color,
                            font=("Helvetica", 24), highlightthickness=0)
        humidity_symbol.place(x=180, y=180)
        
    def spawn_temperature():
        dht_sensor = Adafruit_DHT.DHT11
        dht_pin = 18
        while True:
            humidity, temperature = Adafruit_DHT.read(dht_sensor, dht_pin)
            temp_str = str("Temperature={0:0.1f}C".format(temperature))
            display_temp = Label(home, text=temp_str)
            display_temp.place(x=600, y=180)
            time.sleep(3)
            temp_str = "Calculating..."
            display_temp = Label(home, text=temp_str)
            display_temp.place(x=600, y=180)
        
    
    def temperature_pressed():
        for widget in home.winfo_children():
            widget.destroy()
        spawn_buttons()
        spawn_temperature()
    
    home = Tk()
    home.title('Jake\'s Pi')
    home.geometry("1020x700+0+0")
    home.configure(bg=background_color)
    
    clock = Label(home,font=('Helvetica', 48), bg=background_color, fg=text_color)
    spawn_buttons()
    spawn_clock()
    
    degree_val = 00.000
    humidity_val = 00.000

    home.mainloop()
    

def launch_login_page():
    
    def login():
        window.destroy()
        launch_home_page()

    def enter_pressed():
        
        counter = -1
        value_user = False
        un = username_field.get()
        for user in username_info:
            counter = counter + 1
            if user == un:
                valid_user = True
                break
        valid_pass = False
        pw = password_field.get()
        if password_info[counter] == pw:
            valid_pass = True
        
        if valid_user == True and valid_pass == True:
            login()
        else:
            def login_error_pressed():
                incorrect_popup.destroy()
        
            def launch_new_user_page():
                
                def admin_enter_pressed():
                    if admin_user_entry.get() == username and admin_password_entry.get() == password:
                        
                        # def nu_enter_pressed():
                            # if passwords match
                                # popup alert success
                            # else
                                # popup alert failed
                        
                        admin_login_popup.destroy()
                        new_user_popup = Tk()
                        new_user_popup.title("Enter New User Info")
                        new_user_popup.geometry("480x+300+280")
                        new_user_popup.configure(bg=background_color)
                        nu_username_lbl = Label(new_user_popup, text='New Username:', bg=background_color, fg=label_color, justify='center',
                                                font=("Helvetica", 24))
                        nu_username_lbl.place(x=60, y=10)
                        nu_username_entry = Entry(new_user_popup, fg=text_color, font=("Helvetica", 24))
                        nu_username_entry.focus_set()
                        nu_username_entry.place(x=60, y=60)
                        nu_password_lbl = Label(new_user_popup, text="New Password:", bg=background_color, fg=label_color, justify='center',
                                                font=('Helvetica', 24))
                        nu_password_lbl.place(x=60, y=110)
                        nu_password_entry = Entry(new_user_popup, fg=text_color, font=('Helvetica', 24), show='*')
                        nu_password_entry.place(x=60, y=160)
                        nu_confirm_pass_lbl = Label(new_user_popup, text='Confirm Password:', bg=background_color, fg=label_color, justify='center',
                                                    font=('Helvetica', 24))
                        nu_confirm_pass_lbl.place(x=60, y=210)
                        nu_confirm_pass_entry = Entry(new_user_popup, fg=text_color, font=('Helvetica', 24), show='*')
                        nu_confirm_pass_entry.place(x=60, y=260)
                        nu_button = Button(new_user_popup, fg=label_color, bg=white, command=nu_enter_pressed, text='Enter',
                                           font=('Helvetica', 24))
                        nu_button.place(x=60, y=310)
                        new_user_popup.bind('<Return>', lambda event=None: nu_button.invoke())
                    else:
                        admin_user_entry.delete(0, 'end')
                        admin_password_entry.delete(0, 'end')
                
                incorrect_popup.destroy()
                admin_login_popup = Tk()
                admin_login_popup.title("Add New User")
                admin_login_popup.geometry("480x320+300+280")
                admin_login_popup.configure(bg=background_color)
                
                admin_user_lbl = Label(admin_login_popup, text='Admin Username:', bg=background_color, fg=label_color, justify='center',
                         font=("Helvetica", 24))
                admin_user_lbl.place(x=60, y=10)
                admin_user_entry = Entry(admin_login_popup, fg=text_color, font=("Helvetica", 24))
                admin_user_entry.focus_set()
                admin_user_entry.place(x=60, y=70)
                admin_password_lbl = Label(admin_login_popup, text='Admin Password:', bg=background_color, fg=label_color, justify='center',
                                           font=("Helvetica", 24))
                admin_password_lbl.place(x=60, y=130)
                admin_password_entry = Entry(admin_login_popup, fg=text_color, font=("Helvetica", 24), show='*')
                admin_password_entry.place(x=60, y=190)
                admin_enter = Button(admin_login_popup, text="Enter", fg=label_color, bg=white, font=("Helvetica", 24),
                                     command=admin_enter_pressed)
                admin_enter.place(x=60, y=250)
                admin_login_popup.bind('<Return>', lambda event=None: admin_enter.invoke())

            incorrect_popup = Tk()
            incorrect_popup.title("Login Error")
            incorrect_popup.geometry("480x320+300+280")
            incorrect_popup.configure(bg=background_color)
            username_field.delete(0, 'end')
            password_field.delete(0, 'end')
            login_error_lbl = Label(incorrect_popup, text='Username and Password Not Valid:', bg=background_color,
                                    fg=label_color,
                                    justify='center', font=("Helvetica", 16))
            login_error_lbl.place(x=70, y=80)
            login_error_btn = Button(incorrect_popup, text="Okay", fg=label_color, font=("Helvetica", 16),
                                     command=login_error_pressed, bg=white)
            login_error_btn.place(x=210, y=160)
            add_new_user_button = Button(incorrect_popup, text="Add New User", fg=label_color,
                                         font=("Helvetica", 16), command=launch_new_user_page, bg=white)
            add_new_user_button.place(x=165, y=220)

    window = Tk()
    window.title('Login to Jake\'s Pi')
    window.geometry("1020x700+0+0")
    window.configure(bg=background_color)
    window.bind('<Return>', lambda event=None: enter_btn.invoke())
    
    login_canvas = Canvas(window, bg=background_color, width=1020, height=700, highlightthickness=0)
    login_canvas.pack(expand=1, fill=BOTH)
    login_canvas.place(x=740, y=400)
    rasp_img = Image.open('raspberry.png')
    rasp_img = rasp_img.resize((300, 280), Image.ANTIALIAS)
    rasp_img = ImageTk.PhotoImage(rasp_img)
    login_canvas.create_image(0, 0, image=rasp_img, anchor='nw')
    
    username_field = Entry(window, fg=text_color, font=("Helvetica", 24))
    username_field.place(x=login_w, y=300)
    username_field.focus_set()
    username_lbl = Label(window, text='Username:', bg=background_color, fg=label_color, justify='center',
                         font=("Helvetica", 24))
    username_lbl.place(x=login_w, y=240)
    password_field = Entry(window, fg=text_color, font=("Helvetica", 24), show='*')
    password_field.place(x=login_w, y=420)
    password_lbl = Label(window, text='Password:', bg=background_color, fg=label_color, justify='center',
                         font=("Helvetica", 24))
    password_lbl.place(x=login_w, y=360)
    enter_btn = Button(window, text="Enter", fg=label_color, bg=white, font=("Helvetica", 24), command=enter_pressed)
    enter_btn.place(x=480, y=490)

    window.mainloop()


# launch_login_page()
launch_home_page()
