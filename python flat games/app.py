import flet as ft
import asyncio
from game import Game
from ui import UI

class RouletteApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Русская рулетка"
        self.page.window_width = 400
        self.page.window_height = 500

        self.game = Game()
        self.ui = UI()

        self.ui.shoot_btn.on_click = self.shoot
        self.ui.reset_btn.on_click = self.restart

        self.page.add(*self.ui.build())

    async def animate_drum(self):
        frames = ["🔫", "🎲", "⚙️", "🔃"]
        for i in range(8):
            self.ui.drum.value = frames[i % len(frames)]
            self.page.update()
            await asyncio.sleep(0.1)
        self.ui.drum.value = "🎯"
        self.page.update()

    async def shoot(self, e):
        if not self.game.alive:
            return

        self.ui.shoot_btn.disabled = True
        self.page.update()

        await self.animate_drum()

        result = self.game.shot()

        if result == "dead":
            self.ui.drum.value = "💀"
            self.ui.status.value = "💀 GAME OVER! Все жизни потрачены"
            self.ui.status.color = "red"
            self.ui.update_hearts(0)
        elif result == "boom":
            self.ui.drum.value = "💥"
            self.ui.status.value = f"💥 БУМ! Осталось жизней: {self.game.lives}"
            self.ui.status.color = "orange"
            self.ui.update_hearts(self.game.lives)
        else:
            self.ui.status.value = "😅 Повезло! Патрона нет"
            self.ui.status.color = "green"

        self.ui.round.value = f"Раунд: {self.game.current_position}"
        self.ui.shoot_btn.disabled = False
        self.page.update()

    def restart(self, e):
        self.game.reset()
        self.ui.drum.value = "🔫"
        self.ui.status.value = "Нажми выстрел"
        self.ui.status.color = "white"
        self.ui.round.value = "Раунд: 1"
        self.ui.update_hearts(3)
        self.page.update()