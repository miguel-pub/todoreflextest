import reflex as rx
import httpx

class State(rx.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    async def fetch_todos(self):
        async with httpx.AsyncClient() as client:
            response = await client.get("http://127.0.0.1:8000/todos/")
            if response.status_code == 200:
                self.todos = response.json()
            else:
                print("Failed to fetch todos:", response.text)


def index():
    return rx.hstack(
        rx.button(
            "Decrement",
            color_scheme="ruby",
            on_click=State.decrement,
        ),
        rx.heading(State.count, font_size="2em"),
        rx.button(
            "Increment",
            color_scheme="grass",
            on_click=State.fetch_todos,
        ),
        spacing="4",
    )
app = rx.App()
app.add_page(index)