import tkinter as tk
from tkSliderWidget import Slider

root = tk.Tk()

slider = Slider(root, width = 400, height = 60, min_val = 0, max_val = 255, init_lis = [0,255], show_value = True)
slider.pack()
root.title("Slider Widget")
root.mainloop()

print(slider.getValues())
print(slider.getValues()[0])
print(int(slider.getValues()[0]))