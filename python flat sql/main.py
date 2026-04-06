import flet as ft
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employees.db")

def create_table():
    con = sqlite3.connect(DB_PATH) 
    con.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT,
            position TEXT,
            salary   TEXT
        )
    """)
    con.commit()
    con.close()

def add_employee(name, position, salary):
    con = sqlite3.connect(DB_PATH)  
    con.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", (name, position, salary))
    con.commit()
    con.close()

def get_employees():
    con = sqlite3.connect(DB_PATH) 
    rows = con.execute("SELECT id, name, position, salary FROM employees").fetchall()
    con.close()
    return rows


def main(page: ft.Page):
    page.title = "Сотрудники"

    create_table()
    field_name     = ft.TextField(label="Имя")
    field_position = ft.TextField(label="Должность")
    field_salary   = ft.TextField(label="Зарплата")
    result_list = ft.Column()

    def refresh():
        result_list.controls.clear()
        for row in get_employees():
            result_list.controls.append(
                ft.Text(f"{row[0]}. {row[1]} — {row[2]} — {row[3]}")
            )
        page.update()

    def on_add(e):
        if field_name.value and field_position.value and field_salary.value:
            add_employee(field_name.value, field_position.value, field_salary.value)
            field_name.value = field_position.value = field_salary.value = ""
            refresh()

    page.add(
        ft.Text("Учёт сотрудников", size=22),
        field_name,
        field_position,
        field_salary,
        ft.ElevatedButton("Добавить", on_click=on_add),
        ft.Divider(),
        result_list,
    )

    refresh()

ft.app(target=main)