import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

# -------------------- COLORS --------------------

BG = "#0f172a"
PANEL = "#1e293b"
ENTRY = "#111827"
BLUE = "#2563eb"
TEXT = "#f8fafc"
MUTED = "#94a3b8"

CATEGORIES = [
    "Technical", "Soft Skills", "Management",
    "Research", "Language"
]

MODES = ["Online", "Offline", "Hybrid"]

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Electronics",
    "Mechanical",
    "Civil",
    "Electrical",
    "Biotechnology"
]


class TrainingRegistrationApp:

    def __init__(self, root):
        self.root = root
        self.root.title(
            "Batch 17 - Training Programme Registration System"
        )
        self.root.geometry("1450x850")
        self.root.minsize(1000, 650)

        self.registrations = {}

        self.dark_mode = True

        # Form variables
        self.reg_id = tk.StringVar()
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.phone = tk.StringVar()
        self.department = tk.StringVar(
            value=DEPARTMENTS[0]
        )

        self.programme = tk.StringVar()
        self.duration = tk.StringVar()
        self.category = tk.StringVar(
            value=CATEGORIES[0]
        )
        self.mode = tk.StringVar(value="Online")

        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar(value="All")

        self.setup_style()
        self.build_ui()
        self.display_all()

    # -------------------- STYLE --------------------

    def setup_style(self):

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Treeview",
            background="#1e293b",
            foreground="white",
            fieldbackground="#1e293b",
            rowheight=32,
            font=("Arial", 10)
        )

        self.style.configure(
            "Treeview.Heading",
            background="#1e40af",
            foreground="white",
            font=("Arial", 10, "bold"),
            padding=8
        )

        self.style.map(
            "Treeview",
            background=[("selected", "#2563eb")],
            foreground=[("selected", "white")]
        )

        self.style.configure(
            "TCombobox",
            fieldbackground=ENTRY,
            background=BLUE,
            foreground="white",
            arrowcolor="white"
        )

    # -------------------- MAIN UI --------------------

    def build_ui(self):

        # Header
        self.header = tk.Frame(
            self.root,
            bg="#1e40af",
            height=75
        )
        self.header.pack(fill="x")
        self.header.pack_propagate(False)

        tk.Label(
            self.header,
            text="🎓  Training Programme Registration System  |  Batch 17",
            font=("Arial", 19, "bold"),
            bg="#1e40af",
            fg="white"
        ).pack(side="left", padx=25, pady=20)

        self.theme_btn = tk.Button(
            self.header,
            text="☀ Light Mode",
            command=self.toggle_theme,
            bg="#3b82f6",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=15,
            pady=8
        )
        self.theme_btn.pack(side="right", padx=20)

        # Main container
        self.main_frame = tk.Frame(
            self.root,
            bg=BG
        )
        self.main_frame.pack(
            fill="both",
            expand=True
        )

        self.build_form()
        self.build_table()

        # Status bar
        self.status = tk.Label(
            self.root,
            text="Ready",
            bg="#1e293b",
            fg="#60a5fa",
            anchor="w",
            font=("Arial", 10),
            padx=10
        )
        self.status.pack(
            side="bottom",
            fill="x"
        )

    # -------------------- SCROLLABLE LEFT FORM --------------------

    def build_form(self):

        self.form_panel = tk.Frame(
            self.main_frame,
            bg=BG,
            width=340
        )

        self.form_panel.pack(
            side="left",
            fill="y",
            padx=10,
            pady=10
        )

        self.form_panel.pack_propagate(False)

        # Canvas
        self.left_canvas = tk.Canvas(
            self.form_panel,
            bg=BG,
            highlightthickness=0
        )

        self.left_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Vertical scrollbar
        self.left_scrollbar = ttk.Scrollbar(
            self.form_panel,
            orient="vertical",
            command=self.left_canvas.yview
        )

        self.left_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.left_canvas.configure(
            yscrollcommand=self.left_scrollbar.set
        )

        # Inner frame
        self.form_content = tk.Frame(
            self.left_canvas,
            bg=BG
        )

        self.canvas_window = self.left_canvas.create_window(
            (0, 0),
            window=self.form_content,
            anchor="nw"
        )

        # Automatically update scroll area
        self.form_content.bind(
            "<Configure>",
            lambda event: self.left_canvas.configure(
                scrollregion=self.left_canvas.bbox("all")
            )
        )

        # Keep inner frame width equal to canvas width
        self.left_canvas.bind(
            "<Configure>",
            lambda event: self.left_canvas.itemconfig(
                self.canvas_window,
                width=event.width
            )
        )

        # Mouse wheel scrolling
        self.left_canvas.bind(
            "<Enter>",
            lambda event: self.left_canvas.bind_all(
                "<MouseWheel>",
                self.scroll_left
            )
        )

        self.left_canvas.bind(
            "<Leave>",
            lambda event: self.left_canvas.unbind_all(
                "<MouseWheel>"
            )
        )

        self.create_form_widgets()

    def scroll_left(self, event):

        self.left_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # -------------------- FORM WIDGETS --------------------

    def create_form_widgets(self):

        parent = self.form_content

        # Student identity
        self.section_label(
            parent,
            "👤  Student Identity"
        )

        self.add_label("Registration ID", parent)
        self.add_entry(self.reg_id, parent)

        self.add_label("Full Name *", parent)
        self.add_entry(self.name, parent)

        self.add_label("Email Address", parent)
        self.add_entry(self.email, parent)

        self.add_label("Phone Number", parent)
        self.add_entry(self.phone, parent)

        self.add_label("Department", parent)

        self.department_box = ttk.Combobox(
            parent,
            textvariable=self.department,
            values=DEPARTMENTS,
            state="readonly",
            font=("Arial", 10)
        )
        self.department_box.pack(
            fill="x",
            padx=12,
            pady=5
        )

        # Programme details
        self.section_label(
            parent,
            "📚  Programme Details"
        )

        self.add_label("Programme Name *", parent)
        self.add_entry(self.programme, parent)

        self.add_label("Duration (Weeks) *", parent)
        self.add_entry(self.duration, parent)

        self.add_label("Category", parent)

        self.category_box = ttk.Combobox(
            parent,
            textvariable=self.category,
            values=CATEGORIES,
            state="readonly",
            font=("Arial", 10)
        )
        self.category_box.pack(
            fill="x",
            padx=12,
            pady=5
        )

        # Training mode
        self.add_label("Training Mode", parent)

        mode_frame = tk.Frame(
            parent,
            bg=BG
        )
        mode_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        for m in MODES:

            tk.Radiobutton(
                mode_frame,
                text=m,
                variable=self.mode,
                value=m,
                bg=BG,
                fg=TEXT,
                selectcolor=PANEL,
                activebackground=BG,
                activeforeground="white",
                font=("Arial", 10)
            ).pack(
                side="left",
                padx=5
            )

        # Actions
        self.section_label(
            parent,
            "⚡  Actions"
        )

        buttons = [
            ("➕ Register", self.register, "#3b82f6"),
            ("🔍 Search", self.search, "#0d9488"),
            ("✏ Update", self.update, "#7c3aed"),
            ("🗑 Delete", self.delete, "#ef4444"),
            ("📋 Display All", self.display_all, "#0369a1"),
            ("📊 Statistics", self.statistics, "#c2410c"),
            ("📥 Export CSV", self.export_csv, "#047857"),
            ("🧹 Clear Form", self.clear_form, "#64748b")
        ]

        button_frame = tk.Frame(
            parent,
            bg=BG
        )
        button_frame.pack(
            fill="x",
            padx=8,
            pady=10
        )

        for i, (text, command, color) in enumerate(buttons):

            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                activebackground=color,
                activeforeground="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                cursor="hand2",
                height=2
            )

            btn.grid(
                row=i // 2,
                column=i % 2,
                sticky="ew",
                padx=4,
                pady=4
            )

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Bottom padding
        tk.Frame(
            parent,
            bg=BG,
            height=25
        ).pack()

    # -------------------- FORM HELPERS --------------------

    def section_label(self, parent, text):

        tk.Label(
            parent,
            text=text,
            bg=BG,
            fg="#60a5fa",
            font=("Arial", 13, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(15, 8)
        )

    def add_label(self, text, parent):

        tk.Label(
            parent,
            text=text,
            bg=BG,
            fg=TEXT,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=12,
            pady=(7, 2)
        )

    def add_entry(self, variable, parent):

        tk.Entry(
            parent,
            textvariable=variable,
            bg=ENTRY,
            fg="white",
            insertbackground="white",
            font=("Arial", 11),
            relief="flat"
        ).pack(
            fill="x",
            padx=12,
            ipady=8
        )

    # -------------------- RIGHT TABLE --------------------

    def build_table(self):

        self.table_panel = tk.Frame(
            self.main_frame,
            bg=PANEL
        )

        self.table_panel.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(0, 10),
            pady=10
        )

        # Search and filter
        top = tk.Frame(
            self.table_panel,
            bg=PANEL
        )
        top.pack(
            fill="x",
            padx=10,
            pady=12
        )

        tk.Label(
            top,
            text="🔎 Search:",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 10)
        ).pack(side="left")

        search_entry = tk.Entry(
            top,
            textvariable=self.search_var,
            bg=ENTRY,
            fg="white",
            insertbackground="white",
            font=("Arial", 10),
            width=20
        )
        search_entry.pack(
            side="left",
            padx=8,
            ipady=5
        )

        self.search_var.trace_add(
            "write",
            lambda *args: self.display_all()
        )

        tk.Label(
            top,
            text="Category:",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 10)
        ).pack(
            side="left",
            padx=(15, 5)
        )

        self.filter_box = ttk.Combobox(
            top,
            textvariable=self.filter_var,
            values=["All"] + CATEGORIES,
            state="readonly",
            width=15
        )
        self.filter_box.pack(side="left")

        self.filter_box.bind(
            "<<ComboboxSelected>>",
            lambda event: self.display_all()
        )

        self.count_label = tk.Label(
            top,
            text="Showing: 0 / Total: 0",
            bg=PANEL,
            fg=TEXT,
            font=("Arial", 10)
        )
        self.count_label.pack(side="right")

        # Table container
        table_frame = tk.Frame(
            self.table_panel,
            bg=PANEL
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

        columns = (
            "ID", "Name", "Email", "Phone",
            "Department", "Programme", "Weeks",
            "Category", "Mode"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        widths = {
            "ID": 115,
            "Name": 150,
            "Email": 170,
            "Phone": 110,
            "Department": 145,
            "Programme": 160,
            "Weeks": 65,
            "Category": 110,
            "Mode": 90
        }

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=widths[col],
                minwidth=65,
                anchor="center"
            )

        # Vertical scrollbar
        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        # Horizontal scrollbar
        x_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        y_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        x_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

    # -------------------- VALIDATION --------------------

    def validate(self):

        rid = self.reg_id.get().strip()
        name = self.name.get().strip()
        programme = self.programme.get().strip()
        duration = self.duration.get().strip()

        if not rid:
            messagebox.showerror(
                "Validation Error",
                "Registration ID is mandatory."
            )
            return None

        if not name:
            messagebox.showerror(
                "Validation Error",
                "Student Name is mandatory."
            )
            return None

        if not programme:
            messagebox.showerror(
                "Validation Error",
                "Programme Name is mandatory."
            )
            return None

        if not duration.isdigit() or int(duration) <= 0:
            messagebox.showerror(
                "Validation Error",
                "Duration must be a positive integer."
            )
            return None

        return {
            "id": rid,
            "name": name,
            "email": self.email.get().strip(),
            "phone": self.phone.get().strip(),
            "department": self.department.get(),
            "programme": programme,
            "duration": int(duration),
            "category": self.category.get(),
            "mode": self.mode.get()
        }

    # -------------------- REGISTER --------------------

    def register(self):

        data = self.validate()

        if not data:
            return

        if data["id"] in self.registrations:

            messagebox.showwarning(
                "Duplicate",
                "Registration ID already exists."
            )
            return

        self.registrations[data["id"]] = data

        self.display_all()

        self.set_status(
            f"Successfully registered {data['name']}."
        )

        messagebox.showinfo(
            "Success",
            "Registration completed successfully!"
        )

        self.clear_form()

    # -------------------- SEARCH --------------------

    def search(self):

        rid = self.reg_id.get().strip()

        if not rid:
            messagebox.showerror(
                "Error",
                "Enter Registration ID."
            )
            return

        record = self.registrations.get(rid)

        if not record:

            messagebox.showinfo(
                "Not Found",
                "Registration not found."
            )
            return

        self.fill_form(record)
        self.display_all()
        self.highlight(rid)

        self.set_status(
            f"Record found: {rid}"
        )

    # -------------------- UPDATE --------------------

    def update(self):

        data = self.validate()

        if not data:
            return

        if data["id"] not in self.registrations:

            messagebox.showinfo(
                "Not Found",
                "Registration ID does not exist."
            )
            return

        self.registrations[data["id"]] = data

        self.display_all()
        self.highlight(data["id"])

        self.set_status(
            f"Updated registration {data['id']}."
        )

        messagebox.showinfo(
            "Success",
            "Registration updated successfully!"
        )

    # -------------------- DELETE --------------------

    def delete(self):

        rid = self.reg_id.get().strip()

        if not rid:
            messagebox.showerror(
                "Error",
                "Enter Registration ID."
            )
            return

        if rid not in self.registrations:

            messagebox.showinfo(
                "Not Found",
                "Registration not found."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete registration {rid}?"
        )

        if confirm:

            del self.registrations[rid]

            self.display_all()
            self.clear_form()

            self.set_status(
                f"Deleted registration {rid}."
            )

    # -------------------- DISPLAY ALL --------------------

    def display_all(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        search_text = self.search_var.get().lower()
        category_filter = self.filter_var.get()

        filtered = []

        for record in self.registrations.values():

            if (
                category_filter != "All"
                and record["category"] != category_filter
            ):
                continue

            searchable = " ".join(
                str(value) for value in record.values()
            ).lower()

            if search_text and search_text not in searchable:
                continue

            filtered.append(record)

        for record in filtered:

            self.tree.insert(
                "",
                "end",
                iid=record["id"],
                values=(
                    record["id"],
                    record["name"],
                    record["email"],
                    record["phone"],
                    record["department"],
                    record["programme"],
                    record["duration"],
                    record["category"],
                    record["mode"]
                )
            )

        self.count_label.config(
            text=f"Showing: {len(filtered)} / Total: {len(self.registrations)}"
        )

        self.set_status(
            f"Total registrations: {len(self.registrations)}"
        )

    # -------------------- SELECT RECORD --------------------

    def on_select(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        rid = selected[0]

        record = self.registrations.get(rid)

        if record:
            self.fill_form(record)

    # -------------------- FILL FORM --------------------

    def fill_form(self, record):

        self.reg_id.set(record["id"])
        self.name.set(record["name"])
        self.email.set(record["email"])
        self.phone.set(record["phone"])
        self.department.set(record["department"])

        self.programme.set(record["programme"])
        self.duration.set(str(record["duration"]))
        self.category.set(record["category"])
        self.mode.set(record["mode"])

    # -------------------- HIGHLIGHT --------------------

    def highlight(self, rid):

        if self.tree.exists(rid):

            self.tree.selection_set(rid)
            self.tree.focus(rid)
            self.tree.see(rid)

    # -------------------- CLEAR FORM --------------------

    def clear_form(self):

        self.reg_id.set("")
        self.name.set("")
        self.email.set("")
        self.phone.set("")
        self.department.set(DEPARTMENTS[0])

        self.programme.set("")
        self.duration.set("")
        self.category.set(CATEGORIES[0])
        self.mode.set("Online")

        self.tree.selection_remove(
            self.tree.selection()
        )

        self.set_status("Form cleared.")

    # -------------------- STATISTICS --------------------

    def statistics(self):

        total = len(self.registrations)

        online = sum(
            1 for r in self.registrations.values()
            if r["mode"] == "Online"
        )

        offline = sum(
            1 for r in self.registrations.values()
            if r["mode"] == "Offline"
        )

        hybrid = sum(
            1 for r in self.registrations.values()
            if r["mode"] == "Hybrid"
        )

        messagebox.showinfo(
            "Registration Statistics",
            f"Total Registrations: {total}\n\n"
            f"Online: {online}\n"
            f"Offline: {offline}\n"
            f"Hybrid: {hybrid}"
        )

    # -------------------- EXPORT CSV --------------------

    def export_csv(self):

        if not self.registrations:

            messagebox.showwarning(
                "Empty",
                "No registrations available to export."
            )
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not filename:
            return

        fields = [
            "id", "name", "email", "phone",
            "department", "programme", "duration",
            "category", "mode"
        ]

        try:
            with open(
                filename,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.DictWriter(
                    file,
                    fieldnames=fields
                )

                writer.writeheader()

                writer.writerows(
                    self.registrations.values()
                )

            messagebox.showinfo(
                "Success",
                "CSV exported successfully!"
            )

        except OSError as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )

    # -------------------- STATUS --------------------

    def set_status(self, text):

        self.status.config(text=text)

    # -------------------- THEME SWITCH --------------------

    def toggle_theme(self):

        if self.dark_mode:

            self.dark_mode = False

            bg = "#f1f5f9"
            panel = "#ffffff"
            fg = "#111827"
            entry = "#ffffff"

            self.theme_btn.config(
                text="🌙 Dark Mode"
            )

        else:

            self.dark_mode = True

            bg = "#0f172a"
            panel = "#1e293b"
            fg = "#f8fafc"
            entry = "#111827"

            self.theme_btn.config(
                text="☀ Light Mode"
            )

        self.main_frame.config(bg=bg)
        self.form_panel.config(bg=bg)
        self.form_content.config(bg=bg)
        self.left_canvas.config(bg=bg)
        self.table_panel.config(bg=panel)
        self.status.config(bg=panel, fg=fg)

        # Update all form widgets
        for widget in self.form_content.winfo_children():

            if isinstance(widget, tk.Label):
                widget.config(
                    bg=bg,
                    fg=fg if widget.cget("fg") != "#60a5fa"
                    else "#2563eb"
                )

            elif isinstance(widget, tk.Frame):
                widget.config(bg=bg)

                for child in widget.winfo_children():

                    if isinstance(child, tk.Button):
                        continue

                    if isinstance(child, tk.Radiobutton):
                        child.config(
                            bg=bg,
                            fg=fg,
                            selectcolor=panel,
                            activebackground=bg
                        )

            elif isinstance(widget, tk.Entry):
                widget.config(
                    bg=entry,
                    fg=fg,
                    insertbackground=fg
                )


# -------------------- RUN APPLICATION --------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = TrainingRegistrationApp(root)

    root.mainloop()