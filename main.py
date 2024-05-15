from backend import *

try:
    @bot.message_handler(commands=['start'])
    def bot_start(message):
        bot.send_message(message.chat.id, start_msg)

    @bot.message_handler(commands=['create'])
    def create_profile(message):
        user_id = message.from_user.id
        if user_exists(user_id):
            bot.send_message(message.chat.id, user_exist_msg)
        else:
            sent_msg = bot.send_message(message.chat.id, name_msg)
            bot.register_next_step_handler(sent_msg, reg_name_step)

    def reg_name_step(message):
        user_id = message.from_user.id
        name = message.text
        process_name(user_id, name)

        sent_msg = bot.send_message(message.chat.id, age_msg)
        bot.register_next_step_handler(sent_msg, reg_age_step)

    def reg_age_step(message):
        user_id = message.from_user.id
        age = message.text
        process_age(user_id, age)

        bot.send_message(message.chat.id, show_user(user_id, age))

    @bot.message_handler(commands=['delete'])
    def delete_profile(message):
        user_id = message.from_user.id
        if user_exists(user_id):
            delete_user(user_id)
            bot.send_message(message.chat.id, delete_msg)
        else:
            bot.send_message(message.chat.id, not_found_msg)

    @bot.message_handler(commands=['update'])
    def update_profile(message):
        user_id = message.from_user.id
        if user_exists(user_id):
            sent_msg = bot.send_message(message.chat.id, to_update_msg)
            bot.register_next_step_handler(sent_msg, update_profile_step)
        else:
            bot.send_message(message.chat.id, not_found_create_msg)

    def update_profile_step(message):
        user_id = message.from_user.id
        try:
            name, age = message.text.split(", ")
            update_user(user_id, name, age)
            bot.send_message(message.chat.id, profile_updated_msg)
        except Exception as e:
            bot.send_message(message.chat.id, e)

    @bot.message_handler(commands=['admin'])
    def admin_actions(message):
        bot.send_message(message.chat.id, admin_msg)
        bot.register_next_step_handler(message, process_admin_command)

    def process_admin_command(message):
        cmd = message.text
        if cmd == "/view_all":
            bot.send_message(message.chat.id, view_all_msg(get_all_users()))
            admin_actions(message)
        elif cmd == "/delete_all":
            delete_all_users()
            bot.send_message(message.chat.id, users_deleted_msg)
            admin_actions(message)
        else:
            bot_start(message)

    bot.polling()
except redis.exceptions.ConnectionError:
    print(err_db_msg)
except redis.exceptions.TimeoutError:
    print(err_timeout_msg)
except redis.exceptions.AuthenticationError:
    print(err_auth_msg)
except Exception as e:
    print(f"Ошибка: {e}")