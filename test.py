import flet as ft
import requests

tf = ft.TextField(hint_text='Enter your name', width=200, height=30)
tf2 = ft.TextField(hint_text='Enter your email', width=200, height=30)

user_list_label = ft.Text('User List:')

user_list = ft.Text('')  # This label will display the user list



# Function to get the CSRF token from the Django server
def get_csrf_token():
    response = requests.get('http://127.0.0.1:8000/app_frontend/get_csrf_token/')
    return response.json().get('csrf_token')


# Function to make a POST request with CSRF token
def post_with_csrf(url, data, csrf_token):
    headers = {'X-CSRFToken': csrf_token}
    response = requests.post(url, headers=headers, data=data)
    return response


def main(page: ft.Page):
    def get(e):
        # Make a GET request to fetch users
        response = requests.get('http://127.0.0.1:8000/app_frontend/get_users/')
        if response.status_code == 200:
            users = response.json()
            user_list.text = '\n'.join([f"{user['name']}" for user in users])
            user_list.update()  # Trigger a re-render of the text
            page.update()  # Trigger a re-render of the page
            print(users)  # Display users in console or update your Flet UI

    def post(e):
        # Obtain the CSRF token from the Django server
        csrf_token = get_csrf_token()

        # Make a POST request to add a user
        name = tf.value
        email = tf2.value
        url = 'http://127.0.0.1:8000/app_frontend/add_user/'
        data = {'name': name, 'csrfmiddlewaretoken': csrf_token, 'email': email}

        # Use the post_with_csrf function to include the CSRF token in the headers
        post_response = post_with_csrf(url, data, csrf_token)

        if post_response.status_code == 200:
            print(post_response.json())  # Display the response in console or update your Flet UI
            get(None)  # Reuse the 'get' function to update the user list

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
