# importing required modules
import tkinter
import customtkinter
from PIL import ImageTk, Image

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("light")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("green")

# creating cutstom tkinter window
app = customtkinter.CTk()
app.geometry("600x440")
app.title("Login - GUI")


# img1 = ImageTk.PhotoImage(Image.open("palette.jpg"))

l1 = customtkinter.CTkLabel(master=app, width=600, height=440)

l1.pack()

# creating custom frame
frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)

frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2 = customtkinter.CTkLabel(master=frame, text="Log in", font=("Century Gothic", 20))

l2.place(x=120, y=45)

entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text="Username")

entry1.place(x=50, y=110)

entry2 = customtkinter.CTkEntry(
    master=frame, width=220, placeholder_text="Password", show="*"
)

entry2.place(x=50, y=165)

l3 = customtkinter.CTkLabel(
    master=frame, text="Forget password?", font=("Century Gothic", 12)
)

l3.place(x=155, y=195)

# Create custom button
button1 = customtkinter.CTkButton(
    master=frame, width=220, text="Login", corner_radius=6
)
button1.place(x=50, y=240)

button2 = customtkinter.CTkButton(
    master=frame,
    text="Google",
    width=100,
    height=20,
    compound="left",
    fg_color="white",
    text_color="black",
    hover_color="#AFAFAF",
)

button2.place(x=50, y=290)

button3 = customtkinter.CTkButton(
    master=frame,
    text="Facebook",
    width=100,
    height=20,
    compound="left",
    fg_color="white",
    text_color="black",
    hover_color="#AFAFAF",
)

button3.place(x=170, y=290)

app.mainloop()
