from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# all password characters for generating password
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_number = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_list = password_symbol + password_number + password_list
    # shuffling password
    shuffle(password_list)
    password = "".join(password_list)
    # insert the generated password
    password_entry.insert(0, f"{password}")
    # copy password
    pyperclip.copy(password)
    messagebox.showinfo(title=Message, message="A jelszó másolva lett")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    # get the user inputs
    text_email = e_mail_entry.get()
    website_text = website_entry.get()
    password_text = password_entry.get()
    # convert information into json data
    password_data = {website_text: {
        "email": text_email,
        "password": password_text,
    }
    }
    # check if the field is empty
    if len(text_email) < 1 or len(website_text) < 1 or len(password_text) < 1:
        messagebox.showerror(title="Hiba", message="Egy vagy több mező nincs kitöltve.")
    else:
        # check if password length is 8 or greater
        if len(password_text) < 8:
            messagebox.showerror(title="Hiba", message="Túl rövid jelszót adtál meg")
        else:
            # ask the user if the data is ok
            is_ok = messagebox.askokcancel(title=website_text,
                                           message=f"Az általad megadott e-mail és jelszó:\n{text_email}\n{password_text}\nSzeretnéd "
                                                   f"elmenteni?")
            # save data in json
            if is_ok:
                try:
                    with open("data.json", "r") as file:
                        data = json.load(file)
                except FileNotFoundError:
                    # check if json file is already exists, if not, create one
                    with open("data.json", "w") as file:
                        json.dump(password_data, file, indent=4)
                # if json data already exists, save data
                else:
                    data.update(password_data)
                    with open("data.json", "w") as file:
                        json.dump(data, file, indent=4)
                # clear fields
                finally:
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)


def search_password():
    try:
        # try to search file
        with open("data.json") as file:
            website_name = website_entry.get()
            # if file doesn't exists showing error message
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Nem található a fájl.")
        # check if the file exists
    else:
        with open("data.json") as file:
            saved_passwords = json.load(file)
        try:
            # check if the website exists, show error message if not
            searched_password = saved_passwords[website_name]
        except KeyError:
            messagebox.showerror(title="Hiba", message=f"Nem található adat erről az oldalról: {website_name}")
        else:
            # show password if the website exists
            e_mail_name = searched_password["email"]
            password_name = searched_password["password"]
            messagebox.showinfo(title=website_name, message=f"e-mail: {e_mail_name}\njelszó: {password_name}")


# ---------------------------- UI SETUP ------------------------------- #
# config screen
window = Tk()
window.config(padx=50, pady=50)
window.title("Jelszókezelő")
# config the logo
canvas = Canvas(width=200, height=200)
p_manager_pic = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=p_manager_pic)
canvas.grid(column=1, row=0)
# congig text labels
website_label = Label(text="Weboldal")
e_mail_label = Label(text="Email/Felhasználónév:")
password_label = Label(text="Jelszó:")
website_label.grid(column=0, row=1)
e_mail_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)
# config entry labels
website_entry = Entry(width=32)
website_entry.focus()
e_mail_entry = Entry(width=50)
e_mail_entry.insert(0, "example@gmail.com")
password_entry = Entry(width=32)
website_entry.grid(column=1, row=1, columnspan=1)
e_mail_entry.grid(column=1, row=2, columnspan=2)
password_entry.grid(column=1, row=3)
# config buttons
password_button = Button(text="Jelszó generálás", command=generate_password)
add_button = Button(text="Hozzáad", width=43, command=save_password)
search_button = Button(text="Keresés", width=14, command=search_password)
search_button.grid(column=2, row=1)
password_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2)
# infinite loop for screen refresh
window.mainloop()
