import customtkinter as ctk

from bmi_logic import calculate_bmi
from database import (
    create_table,
    save_record,
    get_users,
    get_history,
    get_latest_record,
    get_record_count
)
from graph import show_graph
from export_csv import export_user


# ============================================================
# APP SETTINGS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# COLORS
# ============================================================

BG = "#0B1120"
CARD = "#111827"
CARD_2 = "#172033"

WHITE = "#F8FAFC"
GRAY = "#94A3B8"

BLUE = "#3B82F6"
BLUE_HOVER = "#2563EB"

GREEN = "#00E676"
ORANGE = "#FFA500"
CORAL = "#FF7043"
RED = "#FF3D3D"


# ============================================================
# DATABASE
# ============================================================

database_ready = create_table()


# ============================================================
# APPLICATION
# ============================================================

app = ctk.CTk()

app.title("BMI Dashboard Pro")

app.geometry("1050x760")

app.minsize(850, 650)

app.configure(
    fg_color=BG
)


# ============================================================
# GRID
# ============================================================

app.grid_columnconfigure(
    0,
    weight=1
)

app.grid_rowconfigure(
    1,
    weight=1
)


# ============================================================
# FUNCTIONS
# ============================================================

def show_status(message, success=True):

    if success:

        status_frame.configure(
            fg_color="#123B2A",
            border_color="#00A85A"
        )

        status_label.configure(
            text=f"✓  {message}",
            text_color=GREEN
        )

    else:

        status_frame.configure(
            fg_color="#401A1A",
            border_color="#A83232"
        )

        status_label.configure(
            text=f"⚠  {message}",
            text_color="#FF6B6B"
        )


def live_bmi(event=None):

    weight_text = weight_entry.get().strip()
    height_text = height_entry.get().strip()

    if not weight_text or not height_text:

        result_value.configure(
            text="--",
            text_color=WHITE
        )

        category_value.configure(
            text="Enter weight and height",
            text_color=GRAY
        )

        advice_label.configure(
            text="Your BMI health advice will appear here."
        )

        return

    try:

        weight = float(weight_text)
        height = float(height_text)

        bmi, category, color, advice = calculate_bmi(
            weight,
            height
        )

        result_value.configure(
            text=f"{bmi:.2f}",
            text_color=color
        )

        category_value.configure(
            text=category.upper(),
            text_color=color
        )

        advice_label.configure(
            text=advice
        )

    except ValueError:

        result_value.configure(
            text="--",
            text_color=WHITE
        )

        category_value.configure(
            text="Invalid input",
            text_color=RED
        )

        advice_label.configure(
            text="Enter valid positive numbers."
        )


def refresh_users():

    users = get_users()

    if users:

        user_dropdown.configure(
            values=users
        )

        user_dropdown.set(
            "Select saved user"
        )

    else:

        user_dropdown.configure(
            values=["No saved users"]
        )

        user_dropdown.set(
            "No saved users"
        )


def update_statistics(username):

    count = get_record_count(username)

    latest = get_latest_record(username)

    records_value.configure(
        text=str(count)
    )

    if latest:

        latest_value.configure(
            text=f"{latest[2]:.2f}"
        )

    else:

        latest_value.configure(
            text="--"
        )


def load_selected_user(username):

    if not username:
        return

    if username == "No saved users":
        return

    if username == "Select saved user":
        return

    name_entry.delete(
        0,
        "end"
    )

    name_entry.insert(
        0,
        username
    )

    record = get_latest_record(
        username
    )

    if record:

        weight = record[0]
        height = record[1]

        weight_entry.delete(
            0,
            "end"
        )

        weight_entry.insert(
            0,
            str(weight)
        )

        height_entry.delete(
            0,
            "end"
        )

        height_entry.insert(
            0,
            str(height)
        )

        live_bmi()

        update_statistics(
            username
        )

        show_status(
            f"Loaded {username}'s latest BMI record.",
            True
        )


def save_bmi():

    username = name_entry.get().strip()

    if not username:

        show_status(
            "Please enter a user name.",
            False
        )

        return

    try:

        weight = float(
            weight_entry.get()
        )

        height = float(
            height_entry.get()
        )

    except ValueError:

        show_status(
            "Enter valid numeric weight and height.",
            False
        )

        return

    if weight <= 0:

        show_status(
            "Weight must be greater than zero.",
            False
        )

        return

    if height <= 0:

        show_status(
            "Height must be greater than zero.",
            False
        )

        return

    try:

        bmi, category, color, advice = calculate_bmi(
            weight,
            height
        )

        saved = save_record(
            username,
            weight,
            height,
            bmi,
            category
        )

        if not saved:

            show_status(
                "Database error. Record was not saved.",
                False
            )

            return

        result_value.configure(
            text=f"{bmi:.2f}",
            text_color=color
        )

        category_value.configure(
            text=category.upper(),
            text_color=color
        )

        advice_label.configure(
            text=advice
        )

        refresh_users()

        user_dropdown.set(
            username
        )

        update_statistics(
            username
        )

        show_status(
            "BMI record saved successfully.",
            True
        )

    except Exception as error:

        print("SAVE ERROR:", error)

        show_status(
            "Unable to save BMI record.",
            False
        )


def show_history():

    username = name_entry.get().strip()

    if not username:

        show_status(
            "Enter or select a user first.",
            False
        )

        return

    data = get_history(
        username
    )

    if not data:

        show_status(
            f"No BMI history found for {username}.",
            False
        )

        return

    show_graph(
        data,
        username
    )

    show_status(
        f"BMI trend opened for {username}.",
        True
    )


def export_history():

    username = name_entry.get().strip()

    if not username:

        show_status(
            "Enter or select a user first.",
            False
        )

        return

    success, result = export_user(
        username
    )

    if success:

        show_status(
            "BMI history exported successfully.",
            True
        )

        print(
            "CSV:",
            result
        )

    else:

        show_status(
            result,
            False
        )


def clear_fields():

    name_entry.delete(
        0,
        "end"
    )

    weight_entry.delete(
        0,
        "end"
    )

    height_entry.delete(
        0,
        "end"
    )

    result_value.configure(
        text="--",
        text_color=WHITE
    )

    category_value.configure(
        text="Enter weight and height",
        text_color=GRAY
    )

    advice_label.configure(
        text="Your BMI health advice will appear here."
    )

    latest_value.configure(
        text="--"
    )

    records_value.configure(
        text="0"
    )

    status_frame.configure(
        fg_color=CARD_2,
        border_color="#263449"
    )

    status_label.configure(
        text="● Ready",
        text_color=GRAY
    )


# ============================================================
# HEADER
# ============================================================

header = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=30,
    pady=(25, 10)
)


title = ctk.CTkLabel(
    header,
    text="BMI DASHBOARD PRO",
    font=("Arial", 30, "bold"),
    text_color=WHITE
)

title.pack(
    anchor="w"
)


subtitle = ctk.CTkLabel(
    header,
    text="Personal BMI tracking & health insights",
    font=("Arial", 13),
    text_color=GRAY
)

subtitle.pack(
    anchor="w"
)


# ============================================================
# MAIN
# ============================================================

main = ctk.CTkScrollableFrame(
    app,
    fg_color="transparent"
)

main.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=25,
    pady=5
)


main.grid_columnconfigure(
    0,
    weight=1
)


# ============================================================
# INPUT CARD
# ============================================================

input_card = ctk.CTkFrame(
    main,
    fg_color=CARD,
    corner_radius=20
)

input_card.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=8
)

input_card.grid_columnconfigure(
    0,
    weight=1
)


ctk.CTkLabel(
    input_card,
    text="BMI Calculator",
    font=("Arial", 21, "bold"),
    text_color=WHITE
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=25,
    pady=(20, 15)
)


# ============================================================
# NAME
# ============================================================

ctk.CTkLabel(
    input_card,
    text="User Name",
    text_color=GRAY
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=25
)


name_entry = ctk.CTkEntry(
    input_card,
    height=42,
    placeholder_text="Enter user name"
)

name_entry.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=25,
    pady=(4, 12)
)


# ============================================================
# SAVED USERS
# ============================================================

ctk.CTkLabel(
    input_card,
    text="Saved Users",
    text_color=GRAY
).grid(
    row=3,
    column=0,
    sticky="w",
    padx=25
)


user_dropdown = ctk.CTkComboBox(
    input_card,
    height=42,
    values=["No saved users"],
    command=load_selected_user
)

user_dropdown.grid(
    row=4,
    column=0,
    sticky="ew",
    padx=25,
    pady=(4, 12)
)


# ============================================================
# WEIGHT
# ============================================================

ctk.CTkLabel(
    input_card,
    text="Weight (kg)",
    text_color=GRAY
).grid(
    row=5,
    column=0,
    sticky="w",
    padx=25
)


weight_entry = ctk.CTkEntry(
    input_card,
    height=42,
    placeholder_text="Example: 70"
)

weight_entry.grid(
    row=6,
    column=0,
    sticky="ew",
    padx=25,
    pady=(4, 12)
)


# ============================================================
# HEIGHT
# ============================================================

ctk.CTkLabel(
    input_card,
    text="Height (cm)",
    text_color=GRAY
).grid(
    row=7,
    column=0,
    sticky="w",
    padx=25
)


height_entry = ctk.CTkEntry(
    input_card,
    height=42,
    placeholder_text="Example: 175"
)

height_entry.grid(
    row=8,
    column=0,
    sticky="ew",
    padx=25,
    pady=(4, 20)
)


# ============================================================
# RESULT
# ============================================================

result_card = ctk.CTkFrame(
    main,
    fg_color=CARD,
    corner_radius=20
)

result_card.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=8
)


ctk.CTkLabel(
    result_card,
    text="CURRENT BMI",
    font=("Arial", 12, "bold"),
    text_color=GRAY
).pack(
    pady=(20, 3)
)


result_value = ctk.CTkLabel(
    result_card,
    text="--",
    font=("Arial", 44, "bold"),
    text_color=WHITE
)

result_value.pack()


category_value = ctk.CTkLabel(
    result_card,
    text="Enter weight and height",
    font=("Arial", 20, "bold"),
    text_color=GRAY
)

category_value.pack(
    pady=(0, 20)
)


# ============================================================
# ADVICE
# ============================================================

advice_card = ctk.CTkFrame(
    main,
    fg_color=CARD_2,
    corner_radius=18
)

advice_card.grid(
    row=2,
    column=0,
    sticky="ew",
    pady=8
)


ctk.CTkLabel(
    advice_card,
    text="HEALTH INSIGHT",
    font=("Arial", 12, "bold"),
    text_color=GRAY
).pack(
    pady=(18, 5)
)


advice_label = ctk.CTkLabel(
    advice_card,
    text="Your BMI health advice will appear here.",
    font=("Arial", 14),
    text_color=WHITE,
    wraplength=800
)

advice_label.pack(
    padx=25,
    pady=(0, 20)
)


# ============================================================
# STATISTICS
# ============================================================

stats = ctk.CTkFrame(
    main,
    fg_color=CARD,
    corner_radius=20
)

stats.grid(
    row=3,
    column=0,
    sticky="ew",
    pady=8
)

stats.grid_columnconfigure(
    (0, 1),
    weight=1
)


ctk.CTkLabel(
    stats,
    text="LATEST BMI",
    text_color=GRAY
).grid(
    row=0,
    column=0,
    pady=(18, 3)
)


latest_value = ctk.CTkLabel(
    stats,
    text="--",
    font=("Arial", 22, "bold"),
    text_color=WHITE
)

latest_value.grid(
    row=1,
    column=0,
    pady=(0, 18)
)


ctk.CTkLabel(
    stats,
    text="TOTAL RECORDS",
    text_color=GRAY
).grid(
    row=0,
    column=1,
    pady=(18, 3)
)


records_value = ctk.CTkLabel(
    stats,
    text="0",
    font=("Arial", 22, "bold"),
    text_color=WHITE
)

records_value.grid(
    row=1,
    column=1,
    pady=(0, 18)
)


# ============================================================
# STATUS
# ============================================================

status_frame = ctk.CTkFrame(
    main,
    fg_color=CARD_2,
    corner_radius=14,
    border_width=1,
    border_color="#263449"
)

status_frame.grid(
    row=4,
    column=0,
    sticky="ew",
    pady=8
)


status_label = ctk.CTkLabel(
    status_frame,
    text="● Ready",
    font=("Arial", 14, "bold"),
    text_color=GRAY
)

status_label.pack(
    pady=12
)



# BUTTONS


buttons = ctk.CTkFrame(
    main,
    fg_color="transparent"
)

buttons.grid(
    row=5,
    column=0,
    sticky="ew",
    pady=12
)

buttons.grid_columnconfigure(
    (0, 1, 2, 3),
    weight=1
)


def make_button(
    text,
    command,
    column
):

    button = ctk.CTkButton(
        buttons,
        text=text,
        command=command,
        height=45,
        corner_radius=12,
        font=("Arial", 13, "bold"),
        fg_color=BLUE,
        hover_color=BLUE_HOVER
    )

    button.grid(
        row=0,
        column=column,
        sticky="ew",
        padx=4
    )


make_button(
    "Save BMI",
    save_bmi,
    0
)


make_button(
    "BMI Trend",
    show_history,
    1
)


make_button(
    "Export CSV",
    export_history,
    2
)


make_button(
    "Clear",
    clear_fields,
    3
)



# FOOTER


footer = ctk.CTkLabel(
    app,
    text="Python • CustomTkinter • SQLite • Matplotlib",
    font=("Arial", 11),
    text_color="#64748B"
)

footer.grid(
    row=2,
    column=0,
    pady=(3, 12)
)


#Event

weight_entry.bind(
    "<KeyRelease>",
    live_bmi
)

height_entry.bind(
    "<KeyRelease>",
    live_bmi
)



# STARTUP


refresh_users()

if not database_ready:

    show_status(
        "Database initialization failed.",
        False
    )



# START


app.mainloop()