from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext, ConversationHandler
from datetime import datetime
from random import choice
import QueenSolver, asciiArtGen

# Constants
TOKEN : Final = '8139725820:AAGK16aWE69iVut-jw6BdzAALjD7aIZ1Qkc'
BOT_USERNAME : Final = '@IKnow43Bot'
WAIT_FOR_BOARD_SIZE : Final = 0
WAIT_FOR_BOARD : Final = 1
WAIT_FOR_RPS : Final = 1
WAIT_FOR_PHOTO_ASCII : Final = 1
# Variables
queen_board_size : int = 0

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, I am a bot! How can I help you?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""This is a bot that can help you with your daily tasks. You can use the following commands:
    /start - Start the bot
    ...
    """)

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, this is a custom command!')

async def queensolver_init_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Send me the size of the board you want to solve!
    Note that square boards are only supported for now!
    Example: 8 for an 8x8 board''')
    return WAIT_FOR_BOARD_SIZE

async def queensolver_boardsize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global queen_board_size
    size = update.message.text
    try:
        queen_board_size = int(size)
        await update.message.reply_text('Now send me the photo of the board!')
        return WAIT_FOR_BOARD
    except:
        await update.message.reply_text('Invalid board size provided!')
        return WAIT_FOR_BOARD_SIZE

async def queensolver_board_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    solution = None
    image = update.message.photo[-1]
    image_file = await context.bot.get_file(image.file_id)
    file_extension = image_file.file_path.split('.')[-1]
    file_path = f"images/Download-{datetime.now().strftime("%Y%m%d%H%M%S")}.{file_extension}"
    await image_file.download_to_drive(custom_path= file_path)
    color_data = QueenSolver.get_color_data(file_path, queen_board_size, queen_board_size)
    for perm in QueenSolver.possible_permutations(queen_board_size):
        if QueenSolver.check_permutation(perm, color_data, queen_board_size):
            solution = perm
            break
    solution_text = '''Solution:\n'''
    if solution is not None:
        for i in range(queen_board_size):
            for j in range(queen_board_size):
                if j == solution[i]:
                    solution_text += "Q"
                else:
                    solution_text += "*"
            solution_text += "\n"
        await update.message.reply_text(solution_text)
    else:
        await update.message.reply_text('No solution found!')
    await update.message.reply_text('Operation closed')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

async def rock_paper_scissors(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''Rock, paper, scissors?''')
    return WAIT_FOR_RPS

async def rock_paper_scissors_reveal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text.lower()
    bot_choice = choice(['rock', 'paper', 'scissors'])
    if user_choice == bot_choice:
        await update.message.reply_text(f"Both chose {user_choice}. It's a tie!")
    elif (user_choice == 'rock' and bot_choice == 'scissors') or (user_choice == 'paper' and bot_choice == 'rock') or (user_choice == 'scissors' and bot_choice == 'paper'):
        await update.message.reply_text(f"You chose {user_choice} and the bot chose {bot_choice}. You win!")
    elif user_choice not in ['rock', 'paper', 'scissors']:
        await update.message.reply_text('Invalid choice provided, try again!')
        return WAIT_FOR_RPS
    else:
        await update.message.reply_text(f"You chose {user_choice} and the bot chose {bot_choice}. You lose!")
    return ConversationHandler.END

async def ascii_art_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Send me the photo you want to convert to ASCII art!')
    return WAIT_FOR_PHOTO_ASCII

async def ascii_art_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    photo_file = await context.bot.get_file(photo.file_id)
    file_extension = photo_file.file_path.split('.')[-1]
    file_path = f"images/Download-{datetime.now().strftime("%Y%m%d%H%M%S")}.{file_extension}"
    await photo_file.download_to_drive(custom_path= file_path)
    await update.message.reply_text('Photo received!')
    output = asciiArtGen.ascii_art(file_path)
    image_path = f"Sent Images/{update.message.chat_id}-ASCII-ART.png"
    asciiArtGen.ascii_to_image(output, output_path=image_path)
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=open(image_path, 'rb'))
    await update.message.reply_text('Operation closed')
    return ConversationHandler.END

async def toss_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = choice(['Heads', 'Tails'])
    await update.message.reply_text(f"The result is {result}")

# Responses
async def handle_photo(update: Update, context: CallbackContext):
    # Get the largest version of the photo sent by the user
    photo = update.message.photo[-1]  # The last item in the list is the largest resolution
    photo_file = await context.bot.get_file(photo.file_id)  # Retrieve the file object
    file_extension = photo_file.file_path.split('.')[-1]
    file_path = f"images/Download-{datetime.now().strftime("%Y%m%d%H%M%S")}.{file_extension}"
    
    await photo_file.download_to_drive(custom_path= file_path)  # Download the photo to the local file system
    await update.message.reply_text('Photo received!')  # Send a message to the user

def handle_response(text : str) -> str: # Handle the response / input message from the user
    print("Handling response...")
    processed: str = text.lower() 
    print("Processed:", processed)
    if 'hello' in processed:
        return 'Hello! How can I help you?'
    elif processed.startswith('calculate '):
        expression: str = processed.replace('calculate ', '')
        try:
            value: float = eval(expression)
            return f'The result is {value}'
        except:
            return 'Invalid expression provided'
    elif processed.startswith('toss a coin'):
        return 'Heads' if choice([0, 1]) == 0 else 'Tails'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Handling message...")
    message_type: str= update.message.chat.type # Check if private message or group message
    text: str = update.message.text
    print(f"User:{update.message.chat.id} in {message_type} says: {text}")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    if response is not None:
        print(f"Bot says: {response}")
        await update.message.reply_text(response)
    else:
        print("No response generated")
        await update.message.reply_text("I'm sorry, I don't understand that!")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Conversation Handlers
queen_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("queensolver", queensolver_init_command)],
    states={
        WAIT_FOR_BOARD_SIZE : [MessageHandler(filters.TEXT & ~filters.COMMAND, queensolver_boardsize_command)],
        WAIT_FOR_BOARD : [MessageHandler(filters.PHOTO, queensolver_board_command)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

rps_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("rockpaper", rock_paper_scissors)],
    states={
        WAIT_FOR_RPS : [MessageHandler(filters.TEXT & ~filters.COMMAND, rock_paper_scissors_reveal)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

ascii_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("asciiart", ascii_art_command)],
    states={
        WAIT_FOR_PHOTO_ASCII : [MessageHandler(filters.PHOTO, ascii_art_photo)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('tosscoin', toss_coin))

    # Conversations
    app.add_handler(queen_conv_handler)
    app.add_handler(rps_conv_handler)
    app.add_handler(ascii_conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Photos
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    # Error
    app.add_error_handler(error)

    # Polling the bot
    print("Polling...")
    app.run_polling(poll_interval=3)