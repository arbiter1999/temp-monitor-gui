import subprocess
import tkinter as tk
import threading
import time

WARNING_TEMP = 75.0  # Temperature threshold in Celsius

def get_temp():
    result = subprocess.run(['sensors'], stdout=subprocess.PIPE, text=True)
    for line in result.stdout.split('\n'):
        # This line varies depending on hardware. Adjust if needed.
        if 'Package id 0' in line or 'Tdie' in line:
            parts = line.split('+')
            if len(parts) > 1:
                temp_str = parts[1].split('°')[0]
                try:
                    return float(temp_str)
                except:
                    pass
    return None

def update_temp():
    while True:
        temp = get_temp()
        if temp:
            label.config(text=f"🌡️ Current Temp: {temp:.1f}°C")
            if temp > WARNING_TEMP:
                warning_label.config(text="⚠️ Warning: Temperature too high!", fg="red")
            else:
                warning_label.config(text="", fg="black")
        else:
            label.config(text="❌ Unable to read temperature")
        time.sleep(5)

# GUI setup
root = tk.Tk()
root.title("System Temperature Monitor")

label = tk.Label(root, font=("Helvetica", 16))
label.pack(pady=10)

warning_label = tk.Label(root, font=("Helvetica", 14))
warning_label.pack(pady=5)

# Run temperature check in background
threading.Thread(target=update_temp, daemon=True).start()
root.mainloop()