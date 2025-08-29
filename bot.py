import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from monopoly.game import Game
from monopoly.board_image import draw_board, get_board_image_bytes

TOKEN = "8324318371:AAGTWZgvkDGQ59-1iO299FZFx6nZmbsl7Fg"
games = {}  # chat_id -> Game
game_creators = {}  # chat_id -> user_id

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def get_start_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Начать игру", callback_data="new_game")]
    ])

def get_lobby_keyboard(joined, max_players, can_start):
    buttons = [
        [InlineKeyboardButton("Присоединиться", callback_data="join_game")]
    ]
    if can_start:
        buttons.append([InlineKeyboardButton("Начать игру", callback_data="begin_game")])
    return InlineKeyboardMarkup(buttons)

def get_game_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Бросить кости 🎲", callback_data="roll_dice"),
         InlineKeyboardButton("Купить клетку 🏠", callback_data="buy_property")]
    ])

def format_status(game: Game):
    lines = []
    for player in game.players:
        # Замените 'balance' на правильное поле для денег!
        lines.append(f"@{player.username}: {player.balance}₽")
    lines.append("")
    lines.append(f"Следующий ход: @{game.get_current_player().username}")
    return "\n".join(lines)

async def send_game_status_with_board(context, chat_id, game, extra_text=None, reply_markup=None):
    img = draw_board(game)
    bio = get_board_image_bytes(img)
    caption = format_status(game)
    if extra_text:
        caption += "\n\n" + extra_text
    await context.bot.send_photo(chat_id=chat_id, photo=bio, caption=caption, reply_markup=reply_markup, parse_mode=None)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = (
        "Вассап капиталисты, это игра про наш загнивающий запад, под названием \"монополия\"\n"
        "Тыкай на кнопки чтобы выбрать действие."
    )
    keyboard = get_start_keyboard()
    if update.message:
        await update.message.reply_text(text, reply_markup=keyboard, parse_mode=None)
    else:
        await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode=None)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    chat_id = query.message.chat.id

    await query.answer()
    data = query.data

    if data == "new_game":
        games[chat_id] = Game(chat_id)
        game_creators[chat_id] = user.id
        await query.edit_message_text(
            f"Чтоб присоединится к игре тыкни на кнопку \"Присоединиться\"\nИгроков присоединилось: 0/6",
            reply_markup=get_lobby_keyboard(0, 6, False),
            parse_mode=None
        )

    elif data == "join_game":
        if chat_id not in games:
            await query.edit_message_text("Сначала создайте игру!", parse_mode=None)
            return
        game = games[chat_id]
        joined = len(game.players)
        if user.id not in [p.user_id for p in game.players]:
            ok = game.add_player(user.id, user.username or user.full_name, "")
            joined += 1
        can_start = joined >= 2
        if joined >= 6:
            game.start()
            await send_game_status_with_board(context, chat_id, game, reply_markup=get_game_keyboard())
        else:
            await query.edit_message_text(
                f"Чтоб присоединится к игре тыкни на кнопку \"Присоединиться\"\nИгроков присоединилось: {joined}/6",
                reply_markup=get_lobby_keyboard(joined, 6, can_start),
                parse_mode=None
            )

    elif data == "begin_game":
        game = games.get(chat_id)
        if not game:
            await query.edit_message_text("Нет активной игры.", parse_mode=None)
            return
        joined = len(game.players)
        if joined < 2:
            await query.edit_message_text("Минимум 2 игрока для старта!", parse_mode=None)
            return
        if user.id == game_creators.get(chat_id):
            game.start()
            await send_game_status_with_board(context, chat_id, game, reply_markup=get_game_keyboard())
        else:
            await query.edit_message_text("Только создатель игры может начать!", parse_mode=None)

    elif data == "roll_dice":
        game = games.get(chat_id)
        cp = game.get_current_player()
        if user.id != cp.user_id:
            await query.answer("Сейчас не ваш ход!", show_alert=True)
            return
        dice = game.roll_dice()
        ok, msg = game.process_turn(user.id, dice)
        extra_text = f"Вы выбросили: {dice[0]} и {dice[1]}\n{msg}"
        await send_game_status_with_board(context, chat_id, game, extra_text, reply_markup=get_game_keyboard())
        if ok:
            game.next_turn()
            await send_game_status_with_board(context, chat_id, game, reply_markup=get_game_keyboard())

    elif data == "buy_property":
        game = games.get(chat_id)
        cp = game.get_current_player()
        if user.id != cp.user_id:
            await query.answer("Сейчас не ваш ход!", show_alert=True)
            return
        ok, msg = game.buy_property(user.id)
        await send_game_status_with_board(context, chat_id, game, msg, reply_markup=get_game_keyboard())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()