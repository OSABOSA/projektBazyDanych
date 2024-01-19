import flet as ft
import requests

tf = ft.TextField(hint_text='Enter your name', width=200, height=30)
tf2 = ft.TextField(hint_text='Enter your email', width=200, height=30)

user_list_label = ft.Text('User List:')

user_list = ft.Text('')  # This label will display the user list


def main(page: ft.Page):

    def get(e):
        # Make a GET request to fetch users
        response = requests.get('http://127.0.0.1:8000/app_frontend/get_users/')
        if response.status_code == 200:
            # Assuming your users are in response.json()
            users = response.json()
            print(users)  # Display users in console or update your Flet UI
            user_list.text = '\n'.join([f"{user['name']}" for user in users])
            # user_list.update()
            # page.update()

    def post(e):
        # Make a POST request to add a user
        name = tf.value
        url = 'http://127.0.0.1:8000/frontend/add_user/'
        csrf_token = requests.get('http://127.0.0.1:8000/app_frontend/get_csrf_token/')['csrf_token']

        # Include the CSRF token in the headers
        headers = {'X-CSRFToken': csrf_token}

        # Include the CSRF token in the form data
        data = {'name': name, 'csrfmiddlewaretoken': csrf_token}

        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            print(response.json())  # Display the response in console or update your Flet UI
            get(None)  # Reuse the 'get' function to update the user list

    def post(e):
        # Make a POST request to add a user
        name = tf.value
        email = tf2.value
        response = requests.post('http://127.0.0.1:8000/app_frontend/add_user/', data={'name': name, 'email': email})
        if response.status_code == 200:
            print('xdd')
            print(response.json())  # Display the response in console or update your Flet UI
            user_list.update()
            page.update()


    page.add(
        ft.Column(controls=[
            tf,
            tf2,
            ft.FloatingActionButton(text='get', on_click=get),
            ft.FloatingActionButton(text='post', on_click=post),
            user_list_label,
            user_list
        ]))


ft.app(target=main, view=ft.WEB_BROWSER)
