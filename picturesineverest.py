import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class SpreadsheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Part Number Comparator")
        self.root.geometry("450x300")

        self.path_needs = ""
        self.path_everest = ""

        # --- UI Layout ---
        tk.Label(root, text="Step 1: Select Files", font=("Arial", 12, "bold")).pack(pady=10)

        # File 1: Needs Price
        self.btn_needs = tk.Button(root, text="Select 'Needs Price' File", command=self.load_needs)
        self.btn_needs.pack()
        self.lbl_needs = tk.Label(root, text="No file selected", fg="grey")
        self.lbl_needs.pack(pady=(0, 15))

        # File 2: Pictures in Everest
        self.btn_everest = tk.Button(root, text="Select 'Pictures in Everest' File", command=self.load_everest)
        self.btn_everest.pack()
        self.lbl_everest = tk.Label(root, text="No file selected", fg="grey")
        self.lbl_everest.pack(pady=(0, 20))

        # Action Button
        self.btn_compare = tk.Button(root, text="Run Comparison", command=self.run_logic, 
                                     bg="#2196F3", fg="white", state="disabled", width=20)
        self.btn_compare.pack(pady=10)

    def load_needs(self):
        file = filedialog.askopenfilename(title="Select 'Needs Price'", filetypes=[("Excel", "*.xlsx *.xls")])
        if file:
            self.path_needs = file
            self.lbl_needs.config(text=os.path.basename(file), fg="black")
            self.check_ready()

    def load_everest(self):
        file = filedialog.askopenfilename(title="Select 'Pictures in Everest'", filetypes=[("Excel", "*.xlsx *.xls")])
        if file:
            self.path_everest = file
            self.lbl_everest.config(text=os.path.basename(file), fg="black")
            self.check_ready()

    def check_ready(self):
        # Enable the compare button only when both files are selected
        if self.path_needs and self.path_everest:
            self.btn_compare.config(state="normal")

    def run_logic(self):
        try:
            # Load data
            df_needs = pd.read_excel(self.path_needs)
            df_everest = pd.read_excel(self.path_everest)

            # Logic: Filter Everest for 'T' in PICTURE or NEW PICTURE
            # .astype(str) handles cases where cells might be empty or numbers
            mask = (df_everest['PICTURE'].astype(str).str.upper() == 'T') | \
                   (df_everest['NEW PICTURE'].astype(str).str.upper() == 'T')
            
            everest_matches = df_everest[mask]

            # Find matches in 'Needs Price' based on the 'Code' column
            final_list = df_needs[df_needs['Code'].isin(everest_matches['Code'])]

            if final_list.empty:
                messagebox.showwarning("No Matches", "No matching part numbers with 'T' were found.")
                return

            # Save the result
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", title="Save Result")
            if save_path:
                final_list.to_excel(save_path, index=False)
                messagebox.showinfo("Success", f"Found {len(final_list)} matches!\nSaved to: {save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpreadsheetApp(root)
    root.mainloop()
