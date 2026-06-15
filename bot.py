
"""
Member Acquisition Bot - Nasir Language Institute
جذب مخاطب و ثبت نام مشتریان برای آموزشگاه زبان نصیر
با قابلیت دریافت خودکار آیدی تلگرام
"""

import os
import logging
import re
from datetime import datetime
import pandas as pd
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ============================================================
# CONFIGURATION
# ============================================================
# TOKEN = "توکن_ربات_خودت_اینجا"
TOKEN = "********************************"

# Excel file path
EXCEL_FILE = "nasir_leads.xlsx"

# Admin IDs (Telegram ID ادمین‌ها)
ADMIN_IDS = [123456789]  # آیدی عددی خودت رو اینجا بذار

# Conversation states
NAME, CITY, PHONE, LANGUAGE_LEVEL, GOAL = range(5)

# Create Excel file if not exists
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=[
        "نام و نام خانوادگی", "شهر", "شماره موبایل", "سطح زبان", 
        "هدف از یادگیری", "تاریخ ثبت", "وضعیت", "آیدی تلگرام", "یوزرنیم تلگرام"
    ])
    df.to_excel(EXCEL_FILE, index=False)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def save_to_excel(user_data):
    """Save user data to Excel file."""
    try:
        df = pd.read_excel(EXCEL_FILE)
        new_row = pd.DataFrame([{
            "نام و نام خانوادگی": user_data.get('name', ''),
            "شهر": user_data.get('city', ''),
            "شماره موبایل": user_data.get('phone', ''),
            "سطح زبان": user_data.get('level', ''),
            "هدف از یادگیری": user_data.get('goal', ''),
            "تاریخ ثبت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "وضعیت": "جدید",
            "آیدی تلگرام": user_data.get('user_id', ''),
            "یوزرنیم تلگرام": user_data.get('username', '')
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return True
    except Exception as e:
        print(f"Error saving to Excel: {e}")
        return False


def is_valid_phone(phone):
    """Validate Iranian phone number."""
    pattern = r'^09[0-9]{9}$'
    return re.match(pattern, phone) is not None


# ============================================================
# BOT HANDLERS
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message and start conversation."""
    user = update.effective_user
    
    # دریافت خودکار اطلاعات کاربر از تلگرام
    user_id = user.id
    username = user.username if user.username else "ندارد"
    first_name = user.first_name if user.first_name else ""
    last_name = user.last_name if user.last_name else ""
    full_name = f"{first_name} {last_name}".strip()
    
    # ذخیره اطلاعات اولیه در context
    context.user_data['user_id'] = user_id
    context.user_data['username'] = username
    context.user_data['telegram_name'] = full_name if full_name else first_name
    
    welcome_text = (
        f"🎓 *به آموزشگاه زبان نصیر خوش آمدید!*\n\n"
        f"👋 سلام {first_name} جان\n\n"
        f"🌟 *چرا نصیر؟*\n"
        f"• اساتید مجرب و حرفه‌ای\n"
        f"• روش‌های نوین آموزش زبان\n"
        f"• کلاس‌های آنلاین و حضوری\n"
        f"• مدارک معتبر بین‌المللی\n\n"
        f"📚 *زبان‌های تدریس:*\n"
        f"🇬🇧 انگلیسی | 🇩🇪 آلمانی | 🇫🇷 فرانسوی\n"
        f"🇪🇸 اسپانیایی | 🇮🇹 ایتالیایی | 🇨🇳 چینی\n\n"
        f"✅ *برای دریافت مشاوره رایگان، لطفاً اطلاعات زیر را وارد کنید:*\n\n"
        f"🔹 *نام و نام خانوادگی خود را وارد کنید:*"
    )
    
    await update.message.reply_text(welcome_text, parse_mode="Markdown")
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's name."""
    name = update.message.text.strip()
    
    if len(name.split()) < 2:
        await update.message.reply_text("❌ لطفاً *نام و نام خانوادگی کامل* خود را وارد کنید:")
        return NAME
    
    context.user_data['name'] = name
    
    # City selection keyboard
    cities_keyboard = [
        ["تهران", "کرج", "اصفهان", "مشهد"],
        ["شیراز", "تبریز", "قم", "اهواز"],
        ["کرمانشاه", "ارومیه", "رشت", "زاهدان"],
        ["همدان", "یزد", "اردبیل", "بندرعباس"],
        ["سایر شهرها", "شهر من در لیست نیست"]
    ]
    reply_markup = ReplyKeyboardMarkup(cities_keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "📍 *شهر محل سکونت خود را انتخاب کنید:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    return CITY


async def get_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's city."""
    city = update.message.text.strip()
    
    if city == "شهر من در لیست نیست":
        await update.message.reply_text(
            "📍 *لطفاً نام شهر خود را وارد کنید:*",
            parse_mode="Markdown",
            reply_markup=None
        )
        return CITY
    
    context.user_data['city'] = city
    
    # Language level keyboard
    level_keyboard = [
        ["🌱 مبتدی (مقدماتی)", "📘 متوسط (Intermediate)"],
        ["🎓 پیشرفته (Advanced)", "🗣️ مکالمه محور"],
        ["📚 آمادگی آزمون (IELTS/TOEFL)"]
    ]
    reply_markup = ReplyKeyboardMarkup(level_keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "📖 *سطح زبان خود را انتخاب کنید:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    return LANGUAGE_LEVEL


async def get_language_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's language level."""
    level = update.message.text.strip()
    context.user_data['level'] = level
    
    # Goal keyboard
    goal_keyboard = [
        ["🎯 مهاجرت تحصیلی", "🎯 مهاجرت کاری"],
        ["💼 ارتقاء شغلی", "✈️ سفر و گردشگری"],
        ["🎓 تحصیل در دانشگاه", "📈 پیشرفت شخصی"],
        ["سایر اهداف"]
    ]
    reply_markup = ReplyKeyboardMarkup(goal_keyboard, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "🎯 *هدف خود از یادگیری زبان را انتخاب کنید:*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    return GOAL


async def get_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's goal."""
    goal = update.message.text.strip()
    
    if goal == "سایر اهداف":
        await update.message.reply_text(
            "🎯 *لطفاً هدف خود را توضیح دهید:*",
            parse_mode="Markdown",
            reply_markup=None
        )
        return GOAL
    
    context.user_data['goal'] = goal
    
    await update.message.reply_text(
        "📞 *شماره موبایل خود را وارد کنید:*\n\n"
        "مثال: 09123456789\n\n"
        "🔒 اطلاعات شما کاملاً محرمانه است.",
        parse_mode="Markdown",
        reply_markup=None
    )
    return PHONE


async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user's phone number and save all data."""
    phone = update.message.text.strip()
    
    if not is_valid_phone(phone):
        await update.message.reply_text(
            "❌ *شماره موبایل نامعتبر است!*\n\n"
            "لطفاً یک شماره 11 رقمی Iranian معتبر وارد کنید:\n"
            "مثال: 09123456789",
            parse_mode="Markdown"
        )
        return PHONE
    
    context.user_data['phone'] = phone
    
    # Save to Excel
    if save_to_excel(context.user_data):
        # Get user info for success message
        name = context.user_data.get('name', '')
        city = context.user_data.get('city', '')
        level = context.user_data.get('level', '')
        goal = context.user_data.get('goal', '')
        
        # Send success message
        success_text = (
            f"✅ *اطلاعات شما با موفقیت ثبت شد!*\n\n"
            f"👤 نام: {name}\n"
            f"📍 شهر: {city}\n"
            f"📖 سطح: {level}\n"
            f"🎯 هدف: {goal}\n"
            f"📞 شماره تماس: {phone}\n"
            f"🆔 آیدی تلگرام: {context.user_data.get('user_id', '')}\n\n"
            f"🎯 *کارشناسان آموزشگاه نصیر به زودی با شما تماس خواهند گرفت.*\n\n"
            f"🌟 در ضمن، شما می‌توانید یک جلسه رایگان مشاوره دریافت کنید!\n\n"
            f"📚 برای اطلاعات بیشتر به وب‌سایت ما مراجعه کنید:\n"
            f"🌐 www.nasirlanguage.com\n\n"
            f"💬 سوالی دارید؟ بپرسید!"
        )
        await update.message.reply_text(success_text, parse_mode="Markdown")
        
        # Send notification to admin
        for admin_id in ADMIN_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=f"🆕 *لید جدید آموزشگاه نصیر!*\n\n"
                         f"👤 نام: {name}\n"
                         f"📍 شهر: {city}\n"
                         f"📖 سطح: {level}\n"
                         f"🎯 هدف: {goal}\n"
                         f"📞 موبایل: {phone}\n"
                         f"🆔 آیدی: {context.user_data.get('user_id', '')}\n"
                         f"👤 یوزرنیم: @{context.user_data.get('username', '')}\n"
                         f"🕐 زمان: {datetime.now().strftime('%H:%M:%S')}",
                    parse_mode="Markdown"
                )
            except:
                pass
        
    else:
        await update.message.reply_text(
            "❌ متأسفانه خطایی رخ داد. لطفاً مجدداً تلاش کنید یا با پشتیبانی تماس بگیرید.\n\n"
            "📞 پشتیبانی: ۰۲۱-۱۲۳۴۵۶۷۸"
        )
    
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel conversation."""
    await update.message.reply_text(
        "❌ *فرآیند ثبت‌نام لغو شد.*\n\n"
        "برای شروع مجدد، دستور /start را ارسال کنید.\n\n"
        "🎓 منتظر شما در آموزشگاه زبان نصیر هستیم!",
        parse_mode="Markdown"
    )
    return ConversationHandler.END


# ============================================================
# ADMIN COMMANDS
# ============================================================

async def admin_leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send Excel file with all leads (admin only)."""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🔒 *شما دسترسی به این بخش ندارید.*", parse_mode="Markdown")
        return
    
    if os.path.exists(EXCEL_FILE):
        with open(EXCEL_FILE, 'rb') as f:
            await update.message.reply_document(
                document=f,
                filename=f"nasir_leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                caption="📊 *گزارش کامل لیدهای آموزشگاه زبان نصیر*\n\n"
                        f"📅 تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
    else:
        await update.message.reply_text("📭 *هنوز هیچ لیدی ثبت نشده است.*", parse_mode="Markdown")


async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send statistics about leads (admin only)."""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🔒 *شما دسترسی به این بخش ندارید.*", parse_mode="Markdown")
        return
    
    try:
        df = pd.read_excel(EXCEL_FILE)
        total_leads = len(df)
        
        if total_leads == 0:
            await update.message.reply_text("📭 *هنوز هیچ لیدی ثبت نشده است.*", parse_mode="Markdown")
            return
        
        # Level statistics
        level_counts = df["سطح زبان"].value_counts()
        
        # City statistics
        city_counts = df["شهر"].value_counts().head(10)
        
        # Goal statistics
        goal_counts = df["هدف از یادگیری"].value_counts().head(5)
        
        # Today's leads
        today = datetime.now().strftime("%Y-%m-%d")
        today_leads = df[df["تاریخ ثبت"].str.contains(today)].shape[0] if not df.empty else 0
        
        stats_text = (
            f"📊 *آمار لیدهای آموزشگاه زبان نصیر*\n\n"
            f"📈 *تعداد کل لیدها:* {total_leads}\n"
            f"🆕 *لیدهای امروز:* {today_leads}\n\n"
            f"📖 *توزیع سطوح زبان:*\n"
        )
        
        for level, count in level_counts.head(5).items():
            stats_text += f"   • {level}: {count}\n"
        
        stats_text += f"\n🏙️ *پرتکرارترین شهرها:*\n"
        for city, count in city_counts.items():
            stats_text += f"   • {city}: {count}\n"
        
        stats_text += f"\n🎯 *اهداف کاربران:*\n"
        for goal, count in goal_counts.items():
            stats_text += f"   • {goal}: {count}\n"
        
        await update.message.reply_text(stats_text, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {str(e)}")


async def admin_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Clear all leads (admin only)."""
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text("🔒 *شما دسترسی به این بخش ندارید.*", parse_mode="Markdown")
        return
    
    try:
        # Create new empty DataFrame
        df = pd.DataFrame(columns=[
            "نام و نام خانوادگی", "شهر", "شماره موبایل", "سطح زبان", 
            "هدف از یادگیری", "تاریخ ثبت", "وضعیت", "آیدی تلگرام", "یوزرنیم تلگرام"
        ])
        df.to_excel(EXCEL_FILE, index=False)
        await update.message.reply_text("✅ *تمامی لیدها با موفقیت پاک شدند.*", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"❌ خطا: {str(e)}")


# ============================================================
# MAIN
# ============================================================

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_city)],
            LANGUAGE_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_language_level)],
            GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_goal)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("admin_leads", admin_leads))
    application.add_handler(CommandHandler("admin_stats", admin_stats))
    application.add_handler(CommandHandler("admin_clear", admin_clear))
    
    print("🤖 Nasir Language Institute Bot is running...")
    print("📊 Waiting for users...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()