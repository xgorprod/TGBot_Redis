import telebot
import redis

bot = telebot.TeleBot('')
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
admin_panel = False

start_msg = '''Привет! Я телеграм бот для управления профилями пользователей.'''
name_msg = "Введите ваше имя:"
age_msg = "Введите ваш возраст:"
delete_msg = "Ваш профиль удален."
not_found_msg = "Профиль не найден."
user_exist_msg = "Профиль уже существует. Используйте команду /update для изменения профиля."
to_update_msg = "Введите новую информацию (формат: имя, возраст):"
not_found_create_msg = "Профиль не найден. Используйте команду /create для создания нового профиля."
profile_updated_msg = "Ваш профиль обновлен."
format_error_msg = "Неверный формат. Попробуйте еще раз."
users_deleted_msg = "Все профили удалены."
unk_msg = "Неизвестная команда. Попробуйте еще раз."
admin_msg = '''Доступные команды:
/view_all 
/delete_all'''

err_db_msg = "Ошибка подключения к базе данных."
err_timeout_msg = "Превышено время ожидания."
err_auth_msg = "Ошибка аутентификации."

def user_exists(user_id):
    return r.hexists(f"user:{user_id}", "name")

def show_user(user_id, age):
    return f"Профиль создан. Ваше имя: {r.hget(f'user:{user_id}', 'name')}, возраст: {age}."

def process_name(user_id, name):
    r.hset(f"user:{user_id}", "name", name)

def process_age(user_id, age):
    r.hset(f"user:{user_id}", "age", age)

def delete_user(user_id):
    r.delete(f"user:{user_id}")

def update_user(user_id, name, age):
    r.hset(f"user:{user_id}", "name", name)
    r.hset(f"user:{user_id}", "age", age)

def view_all_msg(users):
    return f"Все пользователи:\n" + "\n".join([f"{key}: {value}" for key, value in users.items()])

def get_all_users():
    keys = r.keys("user:*")
    users = {key: r.hgetall(key) for key in keys}
    return users

def delete_all_users():
    keys = r.keys("user:*")
    for key in keys:
        r.delete(key)
