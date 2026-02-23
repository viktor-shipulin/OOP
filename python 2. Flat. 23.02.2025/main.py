import flet as ft

class Weather:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Погода в областях"
        self.page.window_width = 400
        self.page.window_height = 800 

        self.regions = [
            "Чуйская область",
            "Ошская область",
            "Нарынская область",
            "Иссык-Кульская область",
            "Таласская область",
            "Джалал-Абадская область",
            "Баткенская область",
        ]
        self.inputs = []
        
        self.res_avg = ft.Text(size=18, weight="bold")
        self.res_max = ft.Text(size=16)
        self.res_min = ft.Text(size=16)

        self.build_ui()

    def build_ui(self):
        self.page.add(ft.Text("Введите температуру", size=20))
        
        for name in self.regions:
            field = ft.TextField(label=name, width=350)
            self.inputs.append(field)
            self.page.add(field)  

        btn = ft.ElevatedButton("Показать результат", on_click=self.calculate)
        self.page.add(btn, self.res_avg, self.res_max, self.res_min)

    def calculate(self, e):
        temp_list = []
        try:
            for f in self.inputs:
                if f.value != "":
                    temp_list.append(float(f.value))
                else:
                    self.res_avg.value = "Заполните поля"
                    self.page.update()
                    return

            if temp_list:
                srednyaya = sum(temp_list) / len(temp_list)
                self.res_avg.value = f"Средняя температура: {srednyaya:.2f}"
                
                vysokaya = max(temp_list)
                nizkaya = min(temp_list)
                
                self.res_max.value = f"Самая высокая: {vysokaya}"
                self.res_min.value = f"Самая низкая: {nizkaya}"

                if srednyaya > 20:
                    self.res_avg.color = "green"
                elif srednyaya >= 10:
                    self.res_avg.color = "blue"
                else:
                    self.res_avg.color = "red"
            
        except ValueError:
            self.res_avg.value = "Ошибка пишите только числа"
        
        self.page.update()

def main(page: ft.Page):
    Weather(page)

if __name__ == "__main__":
    ft.app(target=main)