import flet

class WorkApp:
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.title = 'Каталог сотрудников'
        self.page.window_width = 500
        self.page.window_height = 800
        self.page.scroll = "auto" 

        self.users = []

        self.build_ui()

    def build_ui(self):
        self.page.add(flet.Text("Добавление сотрудника", size=20, weight='bold'))
        
        # Поля ввода
        self.fname = flet.TextField(label="Имя", width=400)
        self.lname = flet.TextField(label='Фамилия', width=400)
        self.age = flet.TextField(label='Возраст', width=400)
        self.salary = flet.TextField(label='Зарплата', width=400)
        
        self.job = flet.Dropdown(
            label='Должность',
            width=400,
            options=[
                flet.dropdown.Option("Фронтендер"),
                flet.dropdown.Option("Бекендер"),
                flet.dropdown.Option("Менеджер"),
                flet.dropdown.Option("Уборщица"),
            ]
        )

        self.error_text = flet.Text(color="red")
        
        self.people_list = flet.Column()

        add_btn = flet.ElevatedButton('Добавить сотрудника', on_click=self.add_worker)

        self.page.add(
            self.fname,
            self.lname,
            self.age,
            self.salary,
            self.job,
            add_btn,
            self.error_text,
            flet.Divider(),
            flet.Text("Список сотрудников:", size=18, weight="bold"),
            self.people_list
        )

    def add_worker(self, e):
        if not self.fname.value or not self.lname.value or not self.age.value or not self.salary.value or not self.job.value:
            self.error_text.value = "Заполните все поля"
            self.page.update()
            return

        try:
            age_num = int(self.age.value)
            salary_num = float(self.salary.value)
        except ValueError:
            self.error_text.value = "Возраст и зарплата должны быть числами"
            self.page.update()
            return

        new_user = {
            "name": f"{self.fname.value} {self.lname.value}",
            "age": age_num,
            "job": self.job.value,
            "salary": salary_num
        }

        self.users.append(new_user)
        self.error_text.value = "" 
        
        self.update_list()

    def update_list(self):
        self.users.sort(key=lambda x: x['salary'])
        self.people_list.controls.clear()

        for index, user in enumerate(self.users):
            text_color = "green" if user['salary'] > 100000 else "black"
            
            row = flet.Row(
                controls=[
                    flet.Text(f"{user['name']} | {user['job']} | {user['salary']} сом.", color=text_color, size=16),
                    flet.IconButton(
                        icon=flet.icons.DELETE, 
                        icon_color="red",
                        data=index,
                        on_click=self.delete_worker
                    )
                ],
                alignment="spaceBetween"
            )
            self.people_list.controls.append(row)
        
        self.page.update()

    def delete_worker(self, e):
        idx = e.control.data
        self.users.pop(idx)
        self.update_list()

def main(page: flet.Page):
    WorkApp(page)

if __name__ == '__main__':
    flet.app(target=main)