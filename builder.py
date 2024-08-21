#softbuilder tkinter
#discord: xahma.
#pastaebiryam ne smotret(shutka)

import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox
import json
import pyperclip


class DraggableWidget:
    def __init__(self, canvas, widget, x, y, widget_type="button"):
        self.canvas = canvas
        self.widget = widget
        self.widget_type = widget_type
        self.widget_id = self.canvas.create_window(x, y, window=self.widget, anchor="nw")
        self.widget.bind("<Button-1>", self.start_drag)
        self.widget.bind("<B1-Motion>", self.on_drag)
        self.widget.bind("<Button-3>", self.show_context_menu)

    def start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.canvas.move(self.widget_id, dx, dy)

    def show_context_menu(self, event):
        context_menu = tk.Menu(self.widget, tearoff=0)
        context_menu.add_command(label="Изменить текст", command=self.change_text)
        context_menu.add_command(label="Изменить цвет", command=self.change_color)
        context_menu.add_command(label="Изменить размер", command=self.change_size)
        context_menu.add_command(label="Добавить рамку", command=self.add_border)
        context_menu.add_separator()
        context_menu.add_command(label="Удалить элемент", command=self.delete_widget)
        context_menu.tk_popup(event.x_root, event.y_root)

    def change_text(self):
        new_text = simpledialog.askstring("Изменить текст", "Введите новый текст", initialvalue=self.get_text())
        if new_text is not None:
            self.set_text(new_text)

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.widget.config(bg=color)

    def change_size(self):
        width = simpledialog.askinteger("Размер", "Введите ширину", initialvalue=self.widget.winfo_width())
        height = simpledialog.askinteger("Размер", "Введите высоту", initialvalue=self.widget.winfo_height())
        if width and height:
            self.widget.config(width=width, height=height)

    def add_border(self):
        border_width = simpledialog.askinteger("Ширина рамки", "Введите ширину рамки (в пикселях)", initialvalue=2)
        border_color = colorchooser.askcolor()[1]
        if border_width is not None and border_color:
            self.widget.config(bd=border_width, relief="solid", highlightbackground=border_color,
                               highlightthickness=border_width)

    def get_text(self):
        if isinstance(self.widget, tk.Label) or isinstance(self.widget, tk.Button):
            return self.widget.cget("text")
        elif isinstance(self.widget, tk.Scale):
            return str(self.widget.cget("label"))

    def set_text(self, text):
        if isinstance(self.widget, tk.Label) or isinstance(self.widget, tk.Button):
            self.widget.config(text=text)
        elif isinstance(self.widget, tk.Scale):
            self.widget.config(label=text)

    def delete_widget(self):
        self.canvas.delete(self.widget_id)


class SoftsTkniterBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("SoftsTkniterBuilder")
        self.root.geometry("800x600")

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save_menu)
        file_menu.add_command(label="Generate Code", command=self.generate_code)
        menubar.add_cascade(label="File", menu=file_menu)

        self.control_panel = tk.Frame(self.root, bg='#34495e', width=200, height=600)
        self.control_panel.pack(side='left', fill='y')

        self.add_window_button = tk.Button(self.control_panel, text="Добавить окно", command=self.add_window)
        self.add_window_button.pack(pady=10)

        self.add_button_button = tk.Button(self.control_panel, text="Добавить кнопку", command=self.add_button)
        self.add_button_button.pack(pady=10)

        self.add_slider_button = tk.Button(self.control_panel, text="Добавить слайдер", command=self.add_slider)
        self.add_slider_button.pack(pady=10)

        self.add_text_button = tk.Button(self.control_panel, text="Добавить текст", command=self.add_text)
        self.add_text_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root, bg='#ecf0f1')
        self.canvas.pack(side='right', expand=True, fill='both')

        self.widgets = []
        self.background_widget = None

    def add_window(self):
        window = tk.Frame(self.canvas, bg='#bdc3c7', width=300, height=200, bd=2, relief='groove')
        draggable = DraggableWidget(self.canvas, window, 100, 100, widget_type="frame")
        self.widgets.append(draggable)

        if self.background_widget is None:
            self.background_widget = draggable

    def add_button(self):
        button = tk.Button(self.canvas, text="Button")
        draggable = DraggableWidget(self.canvas, button, 100, 100, widget_type="button")
        self.widgets.append(draggable)

    def add_slider(self):
        slider = tk.Scale(self.canvas, from_=0, to=100, orient=tk.HORIZONTAL)
        draggable = DraggableWidget(self.canvas, slider, 100, 100, widget_type="scale")
        self.widgets.append(draggable)

    def add_text(self):
        label = tk.Label(self.canvas, text="Text", bg="white", width=10, height=2)
        draggable = DraggableWidget(self.canvas, label, 100, 100, widget_type="label")
        self.widgets.append(draggable)

    def save_menu(self):
        data = []
        for widget in self.widgets:
            x, y = self.canvas.coords(widget.widget_id)
            widget_data = {
                "type": widget.widget_type,
                "x": x,
                "y": y,
                "text": widget.get_text(),
                "bg": widget.widget.cget("bg"),
                "width": widget.widget.winfo_width(),
                "height": widget.widget.winfo_height()
            }
            data.append(widget_data)

        with open("menu_config.json", "w") as f:
            json.dump(data, f)

        messagebox.showinfo("Save", "Menu configuration has been saved.")

    def generate_code(self):
        generated_code = "import tkinter as tk\n\nroot = tk.Tk()\nroot.geometry('800x600')\n\n"

        if self.background_widget:
            x, y = self.canvas.coords(self.background_widget.widget_id)
            widget_name = "background_frame"
            generated_code += f"{widget_name} = tk.Frame(root, bg='{self.background_widget.widget.cget('bg')}', width={self.background_widget.widget.winfo_width()}, height={self.background_widget.widget.winfo_height()})\n"
            generated_code += f"{widget_name}.place(x={int(x)}, y={int(y)}, width={self.background_widget.widget.winfo_width()}, height={self.background_widget.widget.winfo_height()})\n\n"

        for widget in self.widgets:
            if widget == self.background_widget:
                continue

            x, y = self.canvas.coords(widget.widget_id)
            widget_type = widget.widget_type
            widget_name = f"widget_{self.widgets.index(widget)}"
            if widget_type == "button":
                generated_code += f"{widget_name} = tk.Button({widget_name}, text='{widget.get_text()}', bg='{widget.widget.cget('bg')}')\n"
            elif widget_type == "label":
                generated_code += f"{widget_name} = tk.Label({widget_name}, text='{widget.get_text()}', bg='{widget.widget.cget('bg')}', width={widget.widget.winfo_width()}, height={widget.widget.winfo_height()})\n"
            elif widget_type == "scale":
                generated_code += f"{widget_name} = tk.Scale({widget_name}, from_=0, to=100, orient=tk.HORIZONTAL)\n"
            elif widget_type == "frame":
                generated_code += f"{widget_name} = tk.Frame({widget_name}, bg='{widget.widget.cget('bg')}', width={widget.widget.winfo_width()}, height={widget.widget.winfo_height()})\n"

            generated_code += f"{widget_name}.place(x={int(x)}, y={int(y)}, width={widget.widget.winfo_width()}, height={widget.widget.winfo_height()})\n\n"

        generated_code += "root.mainloop()"

        pyperclip.copy(generated_code)
        messagebox.showinfo("Generate Code", "Generated code has been copied to clipboard.")

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    builder = SoftsTkniterBuilder(root)
    builder.run()
