import flet as ft

class UI:
    def __init__(self):
        self.title = ft.Text("Русская рулетка", size=26, weight="bold")
        self.drum = ft.Text("🔫", size=60)
        self.hearts = ft.Text("❤️❤️❤️", size=30)
        self.status = ft.Text("Нажми выстрел", size=18)
        self.round = ft.Text("Раунд: 1", size=16)
        self.shoot_btn = ft.ElevatedButton("🔫 Выстрел")
        self.reset_btn = ft.ElevatedButton("🔃 Перезарядка")

    def update_hearts(self, lives):
        self.hearts.value = "❤️" * lives + "🖤" * (3 - lives)

    def build(self):
        return [
            ft.Column(
                controls=[
                    self.title,
                    self.drum,
                    self.hearts,
                    self.status,
                    self.round,
                    ft.Row(
                        controls=[self.shoot_btn, self.reset_btn],
                        spacing=10
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        ]