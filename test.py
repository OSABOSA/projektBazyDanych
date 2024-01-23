import flet as ft
import requests

logged_in = False


username = ft.TextField(hint_text='Enter username', width=200, height=30)
password = ft.TextField(hint_text='Enter password', width=200, height=30)
email = ft.TextField(hint_text='Enter email', width=200, height=30)
phone = ft.TextField(hint_text='Enter phone', width=200, height=30)
sport = ft.TextField(hint_text='Enter sport', width=200, height=30)
elo = ft.TextField(hint_text='Enter elo', width=200, height=30)
opponent = ft.TextField(hint_text='Enter opponent', width=200, height=30)
result = ft.TextField(hint_text='Enter result', width=200, height=30)


def create_user(e):
    url = 'http://127.0.0.1:8000/app_frontend/create_user/'
    data = {'name': username.value, 'email': email, 'password': password.value, 'phone': phone.value}

    # Use the post function from the requests library
    post_response = requests.post(url, data=data)

    if post_response.status_code == 200:
        print(post_response.json())  # Display the response in console or update your Flet UI

    response = requests.post('http://127.0.0.1:8000/app_frontend/create_table_and_add_entries/',
                             data={'table_name': username.value})

    if response.status_code == 200:
        print('Table created and populated successfully')
    else:
        print(f'Error: {response.json()}')




def delete_user(e):
    urls = ['http://127.0.0.1:8000/app_frontend/drop_table_by_name/',
            'http://127.0.0.1:8000/app_frontend/clear_entries_by_username/',
            'http://127.0.0.1:8000/app_frontend/delete_user/']
    data = {'name': username.value}
    for url in urls:
        post_response = requests.post(url, data=data)

        if post_response.status_code == 200:
            print(post_response.json())
        else:
            print(f'Error: {post_response.json()}')


def add_activity(e):
    urls = ['http://127.0.0.1:8000/app_frontend/create_activity_entry/']
    data = {'username': username.value, 'sport': sport.value, 'elo': elo.value}
    for url in urls:
        post_response = requests.post(url, data=data)

        if post_response.status_code == 200:
            print(post_response.json())
        else:
            print(f'Error: {post_response.json()}')


def delete_activity(e):
    urls = ['http://127.0.0.1:8000/app_frontend/remove_activity_entry/']
    data = {'username': username.value, 'sport': sport.value}
    for url in urls:
        post_response = requests.post(url, data=data)

        if post_response.status_code == 200:
            print(post_response.json())
        else:
            print(f'Error: {post_response.json()}')


def search_activity(e):
    urls = ['http://127.0.0.1:8000/app_frontend/get_activities_by_discipline_name/']
    data = {'sport': sport.value}
    for url in urls:
        post_response = requests.get(url, data=data)

        if post_response.status_code == 200:
            print(post_response.json())
        else:
            print(f'Error: {post_response.json()}')


def create_game(e):
    urls = ['http://127.0.0.1:8000/app_frontend/add_entries_to_history/']
    data = {'username': username.value, 'opponent': opponent.value, 'result': result.value, 'sport': sport.value}
    for url in urls:
        post_response = requests.post(url, data=data)

        if post_response.status_code == 200:
            print(post_response.json())
        else:
            print(f'Error: {post_response.json()}')


def update_elo(e):
    urls = ['http://127.0.0.1:8000/app_frontend/update_elo/']
    data = {'username': username.value, 'elo': elo.value, 'result': result.value, 'sport': sport.value}
    for url in urls:
        post_response = requests.post(url, data=data)

        if post_response.status_code == 200:
            print(post_response.json())
        else:
            print(f'Error: {post_response.json()}')


bt_create_user = ft.FloatingActionButton(text='create user', on_click=create_user)
bt_delete_user = ft.FloatingActionButton(text='delete user', on_click=delete_user)

bt_add_activity = ft.FloatingActionButton(text='add activity', on_click=add_activity)
bt_delete_activity = ft.FloatingActionButton(text='delete activity', on_click=delete_activity)
bt_search_activity = ft.FloatingActionButton(text='search activity', on_click=search_activity)
bt_create_game = ft.FloatingActionButton(text='create game', on_click=create_game)
bt_update_elo = ft.FloatingActionButton(text='update elo', on_click=update_elo)


user_list_label = ft.Text('User List:')
user_list = ft.Text('')  # This label will display the user list


def main(page: ft.Page):

    # def get(e):
    #     # Make a GET request to fetch users
    #     response = requests.get('http://127.0.0.1:8000/app_frontend/get_users/')
    #     if response.status_code == 200:
    #         users = response.json()
    #         user_list.text = '\n'.join([f"{user['name']}" for user in users])
    #         page.update()  # Refresh the entire page
    #         print(users)  # Display users in console or update your Flet UI
    #
    # def post(e):
    #     # Make a POST request to add a user
    #     name = tf.value
    #     email = tf2.value
    #     url = 'http://127.0.0.1:8000/app_frontend/add_user/'
    #     data = {'name': name, 'email': email}
    #
    #     # Use the post function from the requests library
    #     post_response = requests.post(url, data=data)
    #
    #     if post_response.status_code == 200:
    #         print(post_response.json())  # Display the response in console or update your Flet UI
    #         get(None)  # Reuse the 'get' function to update the user list
    #
    # def create_table_and_add_entries(e):
    #     table_name = tf3.value
    #     response = requests.post('http://127.0.0.1:8000/app_frontend/create_table_and_add_entries/',
    #                              data={'table_name': table_name})
    #
    #     if response.status_code == 200:
    #         print('Table created and populated successfully')
    #     else:
    #         print(f'Error: {response.json()}')

    page.add(
        ft.Column(controls=[
            username,
            password,
            email,
            phone,
            ft.Row(controls=[
                bt_create_user,
                bt_delete_user,
            ]),
            sport,
            elo,
            ft.Row(controls=[
                bt_add_activity,
                bt_delete_activity,
                bt_search_activity,
            ]),
            opponent,
            result,
            bt_create_game,
            bt_update_elo,
        ]))


ft.app(target=main, view=ft.WEB_BROWSER)
