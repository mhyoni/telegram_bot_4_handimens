from telegram import Update
from telegram.constants import ParseMode
from telegram.helpers import escape_markdown
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# פונקציה לטיפול בהודעות נכנסות
async def highlight_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text

    # פיצול ההודעה לשורות
    lines = message_text.splitlines()
    title = lines[0]  # הכותרת הראשונה

    # ביצוע escape על הטקסט כדי למנוע בעיות עם Markdown
    escaped_text = escape_markdown(message_text, version=2)

    # הדגשת כותרת (המשפט הראשון)
    highlighted_title = f"*{escaped_text.splitlines()[0]}*"

    # הדגשת המילים 'להזמנות' ו-'הצטרפו אלינו:'
    highlighted_text = highlighted_title + "\n" + "\n".join(lines[1:])
    highlighted_text = highlighted_text.replace("להזמנות", "*להזמנות*").replace("הצטרפו אלינו:", "*הצטרפו אלינו:*")
    
    # Escape התו הנדרש (כמו נקודה, כוכבית, קו תחתון)
    highlighted_text = highlighted_text.replace(".", "\\.").replace("_", "\\_").replace("~", "\\~").replace("`", "\\`").replace("(", "\\(").replace(")", "\\)")

    # בדיקת אם יש תמונה בהודעה
    if update.message.photo:
        photo = update.message.photo[-1].file_id  # בחר את התמונה האחרונה (אחת מהתמונות ששלח המשתמש)
        
        try:
            # שליחת התמונה עם הטקסט המודגש
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=highlighted_text,  # הטקסט המודגש
                parse_mode=ParseMode.MARKDOWN_V2  # השתמש ב-MarkdownV2
            )
        except Exception as e:
            print(f"Error: {e}")
    
    else:
        try:
            # אם אין תמונה, שלח רק את הטקסט המודגש
            await update.message.delete()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=highlighted_text,
                parse_mode=ParseMode.MARKDOWN_V2  # השתמש ב-MarkdownV2
            )
        except Exception as e:
            print(f"Error: {e}")

# פונקציה להפעלת הבוט
def main():
    TOKEN = "8113155684:AAElfE1UfGgCCm08gk2OZ4J47Z8XmILiIgw"  # הכנס את הטוקן שלך כאן

    application = Application.builder().token(TOKEN).build()

    # הוספת Handler להודעות טקסט
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, highlight_word))

    print("Bot is running...")
    application.run_polling()

# הפעלה
if __name__ == "__main__":
    main()
