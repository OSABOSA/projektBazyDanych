import flet as ft
import requests

tf_username = ft.TextField(hint_text="Username")
tf_password = ft.TextField(hint_text="Password")
tf_email = ft.TextField(hint_text="Email")
tf_phone = ft.TextField(hint_text="Phone")
t_login_message = ft.Text("")

user_id = None
username = None

lv_disciplines = ft.ListView(expand=True, spacing=10)
lv_requested = ft.ListView(expand=True, spacing=10)
lv_ongoing = ft.ListView(expand=True, spacing=10)
lv_history = ft.ListView(expand=True, spacing=10)


dd_disciplines_search = ft.Dropdown(options=[],)
req = requests.get("http://localhost:8000/api/get_disciplines/").json()
dd_disciplines_search.options = [ft.dropdown.Option(discipline) for discipline in req['disciplines']]
dd_disciplines_settings = ft.Dropdown(options=[],)
req = requests.get("http://localhost:8000/api/get_disciplines/").json()
dd_disciplines_settings.options = [ft.dropdown.Option(discipline) for discipline in req['disciplines']]


def main(page: ft.Page):
    global tf_username, tf_password, tf_email, tf_phone, t_login_message, user_id, username, lv_disciplines, dd_disciplines
    page.title = "Routes Example"

    def route_change(e):
        global tf_username, tf_password, tf_email, tf_phone, t_login_message, user_id, username, lv_disciplines, dd_disciplines
        print("Route change:", e.route)
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app")),
                    ft.ElevatedButton("Login", on_click=lambda e: page.go("/login")),
                    ft.ElevatedButton("Register", on_click=lambda e: page.go("/register")),
                ],
            )
        )

        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Login!"),
                        tf_username,
                        tf_password,
                        ft.ElevatedButton("Login", on_click=check_login),
                        t_login_message
                    ],
                )
            )

        if page.route == "/register":
            page.views.append(
                ft.View(
                    "/register",
                    [
                        ft.AppBar(title=ft.Text("Register"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Register!"),
                        tf_username,
                        tf_password,
                        tf_email,
                        tf_phone,
                        ft.ElevatedButton("Register", on_click=check_register),
                    ],
                )
            )

        if page.route == "/games":
            get_games(user_id)
            page.views.append(
                ft.View(
                    "/games",
                    [
                        ft.AppBar(title=ft.Text("Games"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Requested games!"),
                        lv_requested,
                        ft.Text("Ongoing games!"),
                        lv_ongoing,
                        ft.Text("History!"),
                        lv_history,
                        ft.Row(controls=[ft.ElevatedButton("Settings", on_click=lambda e: page.go("/settings")),
                    ft.ElevatedButton("Search", on_click=lambda e: page.go("/search"))])
                    ],
                )
            )

        if page.route == "/settings":
            page.views.append(
                ft.View(
                    "/settings",
                    [
                        ft.AppBar(title=ft.Text("Settings"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Settings!"),
                        dd_disciplines_settings,
                        ft.ElevatedButton("Add discipline", on_click=add_activity),
                        ft.ElevatedButton("Remove discipline", on_click=remove_activity),
                        ft.Row(controls=[ft.ElevatedButton("Games", on_click=lambda e: page.go("/games")),
                                         ft.ElevatedButton("Search", on_click=lambda e: page.go("/search"))])
                    ],
                )
            )

        if page.route == "/search":
            page.views.append(
                ft.View(
                    "/search",
                    [
                        ft.AppBar(title=ft.Text("Search"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Search!"),
                        dd_disciplines_search,
                        ft.ElevatedButton("Search", on_click=player_search),
                        lv_disciplines,
                        ft.Row(controls=[ft.ElevatedButton("Settings", on_click=lambda e: page.go("/settings")),
                                         ft.ElevatedButton("Games", on_click=lambda e: page.go("/games"))])
                    ],
                )
            )

        page.update()

    def view_pop(e):
        print("ft.View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    def check_login(e):
        global tf_username, tf_password, t_login_message, user_id, username
        url = " http://localhost:8000/api/get_user/"
        data = {
            "username": tf_username.value,
            "password": tf_password.value
        }
        req = requests.post(url, data=data)
        response = req.json()
        print(response)
        if 'error' in response:
            t_login_message.text = response['error']
        else:
            username = response['username']
            user_id = response['user_id']
            page.go("/games")

    def check_register(e):
        global tf_username, tf_password, tf_email, tf_phone
        url = "http://localhost:8000/api/create_user/"
        data = {
            "username": tf_username.value,
            "password": tf_password.value,
            "email": tf_email.value,
            "phone": tf_phone.value
        }
        req = requests.post(url, data=data)
        response = req.json()
        print(response)
        if 'error' in response:
            t_login_message.text = response['error']
        else:
            page.go("/login")

    def player_search(e):
        global dd_disciplines_search, lv_disciplines
        url = "http://localhost:8000/api/get_activities/"
        data = {
            "discipline": dd_disciplines_search.value
        }
        req = requests.post(url, data=data)
        response = req.json()
        print(response)
        if 'error' in response:
            t_login_message.text = response['error']
        else:
            lv_disciplines.controls.clear()
            for item in response['activities']:
                username = item['username']
                elo = item['elo']

                # Create a Text control for user information
                user_info_text = ft.Text(f"User: {username} - ELO: {elo}")

                # Create a Button control that passes the username when clicked
                button = ft.ElevatedButton("Click Me", on_click=lambda _, x=username: request_match(x))

                # Append the Text and Button controls to lv_disciplines
                lv_disciplines.controls.append(ft.Row(controls=[user_info_text, button]))

            page.update()

    def add_activity(e):
        global dd_disciplines_settings, user_id
        url = "http://localhost:8000/api/add_activity/"
        data = {
            "discipline": dd_disciplines_settings.value,
            "user_id": user_id
        }
        req = requests.post(url, data=data)
        response = req.json()
        print(response)
        if 'error' in response:
            t_login_message.text = response['error']
        else:
            page.update()

    def remove_activity(e):
        global dd_disciplines_settings, user_id
        url = "http://localhost:8000/api/remove_activity/"
        data = {
            "discipline": dd_disciplines_settings.value,
            "user_id": user_id
        }
        req = requests.post(url, data=data)
        response = req.json()
        print(response)
        if 'error' in response:
            t_login_message.text = response['error']
        else:
            page.update()

    def request_match(opponent):
        global user_id, dd_disciplines_search
        url = "http://localhost:8000/api/request_match/"
        data = {
            "sender_id": user_id,
            "receiver": opponent,
            "discipline": dd_disciplines_search.value
        }
        req = requests.post(url, data=data)
        response = req.json()
        print(response)
        if 'error' in response:
            t_login_message.text = response['error']
        else:
            page.update()

    def get_games(user_id):
        global lv_requested, lv_ongoing, lv_history
        url = "http://localhost:8000/api/get_games/"
        data = {
            "user_id": user_id
        }
        req = requests.post(url, data=data)
        response = req.json()
        print(response)
        if 'error' in response:
            pass
        else:
            lv_requested.controls.clear()
            lv_ongoing.controls.clear()
            lv_history.controls.clear()
            for item in response['requested']:
                username = item['username']
                discipline = item['discipline']
                elo = item['elo']

                # Create a Text control for user information
                user_info_text = ft.Text(f"User: {username} - ELO: {elo} - Discipline: {discipline}")

                # Create a Button control that passes the username when clicked
                accept = ft.ElevatedButton("V", on_click=lambda _, u=username, d=discipline: accept_game(u, d))
                deny = ft.ElevatedButton("X", on_click=lambda _, u=username, d=discipline: reject_game(u, d))

                # Append the Text and Button controls to lv_disciplines
                lv_requested.controls.append(ft.Row(controls=[user_info_text, accept, deny]))

            for item in response['ongoing']:
                username = item['username']
                discipline = item['discipline']
                opponent = item['opponent']

                # Create a Text control for user information
                user_info_text = ft.Text(f"User: {opponent}  - Discipline: {discipline}")

                # Create a Button control that passes the opponent when clicked
                end_game = ft.ElevatedButton("Finish", on_click=lambda _, u=opponent, d=discipline: avengers(u, d))

                # Append the Text and Button controls to lv_disciplines
                lv_ongoing.controls.append(ft.Row(controls=[user_info_text, end_game]))

            for item in response['history']:
                username = item['username']
                discipline = item['discipline']
                opponent = item['opponent']

                # Create a Text control for user information
                user_info_text = ft.Text(f"User: {opponent} - Discipline: {discipline}")

                # Append the Text and Button controls to lv_disciplines
                lv_history.controls.append(ft.Row(controls=[user_info_text]))

            page.update()

            def accept_game(opponent, discipline):
                global user_id, dd_disciplines_search
                url = "http://localhost:8000/api/accept_game/"
                data = {
                    "sender_id": user_id,
                    "receiver": opponent,
                    "discipline": discipline
                }
                req = requests.post(url, data=data)
                response = req.json()
                print(response)
                if 'error' in response:
                    t_login_message.text = response['error']
                else:
                    page.update()


            def reject_game(opponent, discipline):
                global user_id, dd_disciplines_search
                url = "http://localhost:8000/api/reject_game/"
                data = {
                    "sender_id": user_id,
                    "receiver": opponent,
                    "discipline": discipline
                }
                req = requests.post(url, data=data)
                response = req.json()
                print(response)
                if 'error' in response:
                    t_login_message.text = response['error']
                else:
                    page.update()

            def avengers(opponent, discipline):
                global user_id, dd_disciplines_search
                url = "http://localhost:8000/api/avengers/"
                data = {
                    "sender_id": user_id,
                    "receiver": opponent,
                    "discipline": discipline
                }
                req = requests.post(url, data=data)
                response = req.json()
                print(response)
                if 'error' in response:
                    t_login_message.text = response['error']
                else:
                    page.update()

    page.go(page.route)


ft.app(target=main, view=ft.WEB_BROWSER)
