import matplotlib
import matplotlib.pyplot as plt
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler, Filters, Updater

import xperibot.utils as utils

matplotlib.use('Agg')


class ExpBot:
    def __init__(self, token, allowed_users):
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.allowed_users = allowed_users
        self.dispatcher.add_handler(
            CommandHandler('stop', self.stop, filters=Filters.user(username=allowed_users)))

        self.dispatcher.add_handler(
            CommandHandler('raw_scalars', self.get_scalars))
        self.dispatcher.add_handler(
            CommandHandler('draw_scalars', self.get_scalars))
        self.dispatcher.add_handler(CallbackQueryHandler(self.get_scalars))

        self.scalar_dict = {}

        self.current_action = None
        self.selected_scalars = []

    def add_scalar(self, name, x, iteration):
        v = self.scalar_dict.setdefault(name, [])
        v.append((x, iteration))

    def get_scalars_keyboard(self):
        button_list = [InlineKeyboardButton(
            x, callback_data=x) for x in self.scalar_dict if x not in self.selected_scalars]
        keyboard = utils.accept_build_menu(button_list, n_cols=4)
        return InlineKeyboardMarkup(keyboard)

    def get_scalars(self, update, context):
        chat_id = update.effective_chat.id
        if self.current_action is None:
            self.current_action = update.message.text[1:]  # Deleting first '/'
            update.message.reply_text(
                'Scalars selection:', reply_markup=self.get_scalars_keyboard())
        else:
            query = update.callback_query
            query.answer()
            data = query.data
            if data == 'accept':
                if self.current_action == 'raw_scalars':
                    for scalar in self.selected_scalars:
                        value, iteration = self.scalar_dict[scalar][-1]
                        context.bot.send_message(
                            chat_id=chat_id, text="{} {}: {}".format(iteration, scalar, value))
                if self.current_action == 'draw_scalars':
                    fig, ax = plt.subplots(nrows=1, ncols=1)
                    for scalar in self.selected_scalars:
                        y, x = list(zip(*self.scalar_dict[scalar]))
                        ax.plot(x, y, label=scalar)
                    plt.legend()
                    fig.savefig("tmp.png", format='png')
                    plt.close(fig)
                    context.bot.send_photo(chat_id=chat_id, photo=open("tmp.png", 'rb'))
                query.edit_message_text(text="Done")
                self.current_action = None
                self.selected_scalars = []
            elif data == 'cancel':
                self.current_action = None
                query.edit_message_text(text="Cancelled")
            else:
                self.selected_scalars.append(data)
                query.edit_message_text(text="Selected {}".format(
                    self.selected_scalars), reply_markup=self.get_scalars_keyboard())
            # if self.current_action == "draw_scalar":

            #     y, x = list(zip(*self.scalar_dict[scalar]))
            #     fig, ax = plt.subplots(nrows=1, ncols=1)
            #     ax.plot(x, y)
            #     fig.savefig("tmp.png", format='png')
            #     plt.close(fig)
            #     # context.bot.send_photo(
            #     #     chat_id=chat_id, photo=open("tmp.png", 'rb'))
            # elif self.current_action == "raw_scalar":
            #     data = self.scalar_dict[scalar][-1]
            #     # context.bot.send_message(
            #     #     chat_id=chat_id, text="{} {}: {}".format(data[-1], scalar, data[0]))
            # elif self.current_action == "cancel":
            #     update.message.reply_text("Cancel")
            # elif self.current_action == "Accept":
            #     pass

    def start_bot(self):
        self.updater.start_polling()

    def idle_bot(self):
        self.updater.idle()

    def stop(self, update, context):
        self.updater.stop()

    def __enter__(self):
        self.start_bot()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.idle_bot()
