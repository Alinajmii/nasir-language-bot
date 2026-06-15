```markdown
# 🎓 Nasir Language Institute Telegram Bot

<div dir="rtl">

## 📌 معرفی پروژه

ربات تلگرام حرفه‌ای جذب مشتری و ثبت‌نام خودکار برای آموزشگاه‌های زبان. این ربات فرآیند جمع‌آوری اطلاعات مشتریان بالقوه را خودکار می‌کند و خروجی اکسل آماده برای تیم فروش تحویل می‌دهد.

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📝 **Multi-step Registration** | 5-step conversation to collect user information |
| 🗺️ **City Selection** | Persian city list with custom keyboard |
| 📚 **Language Level** | Beginner, Intermediate, Advanced, Conversational, Exam Prep |
| 🎯 **Goal Selection** | Immigration, Career, Study, Travel, Personal growth |
| 📞 **Phone Validation** | Iranian mobile number validation (09xxxxxxxxx) |
| 💾 **Excel Export** | Automatic data storage in Excel file |
| 📊 **Admin Panel** | Statistics, reports, and lead management commands |
| 🔔 **Instant Notifications** | Real-time alerts to admin when new lead registers |
| 🆔 **Auto Capture** | Telegram User ID and Username automatically saved |

---

## 🛠️ Tech Stack

```text
🐍 Python 3.10+
🤖 python-telegram-bot v20
📊 Pandas
📁 OpenPyXL
```

---

## 📋 Prerequisites

- Python 3.10 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Your Telegram User ID (from [@userinfobot](https://t.me/userinfobot))

---

## 🚀 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/nasir-language-bot.git
cd nasir-language-bot
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure the bot

Open `bot.py` and replace the following values:

```python
# Replace with your bot token
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Replace with your Telegram User ID
ADMIN_IDS = [123456789]
```

### 4️⃣ Run the bot

```bash
python bot.py
```

---

## 📱 Bot Commands

| Command | Description | Access |
|---------|-------------|--------|
| `/start` | Start registration process | All users |
| `/cancel` | Cancel current operation | All users |
| `/admin_leads` | Download Excel file with all leads | Admin only |
| `/admin_stats` | View lead statistics | Admin only |
| `/admin_clear` | Clear all leads from database | Admin only |

---

## 📊 Excel Output Structure

| Column | Description |
|--------|-------------|
| نام و نام خانوادگی | Full name |
| شهر | City |
| شماره موبایل | Phone number |
| سطح زبان | Language level |
| هدف از یادگیری | Learning goal |
| تاریخ ثبت | Registration date |
| وضعیت | Status (default: جدید) |
| آیدی تلگرام | Telegram User ID |
| یوزرنیم تلگرام | Telegram username |

---

## 📂 Project Structure

```text
nasir-language-bot/
│
├── bot.py                 # Main bot code
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── .gitignore             # Git ignore file
├── nasir_leads.xlsx       # Excel database (auto-generated)
└── LICENSE                # MIT License
```

---

## 📊 Sample Data Generation

To generate sample Excel data for testing:

```bash
python create_sample_data.py
```

This creates `nasir_leads.xlsx` with 50 sample records.

---

## 🔧 Admin Setup

1. Get your Telegram User ID from [@userinfobot](https://t.me/userinfobot)
2. Add your ID to `ADMIN_IDS` list in `bot.py`
3. Multiple admins can be added: `ADMIN_IDS = [123456789, 987654321]`

---

## 📸 Screenshots

### User Registration Flow

```text
User: /start
Bot: Welcome message + asks for name
User: Ali Rezaei
Bot: Asks for city
User: Tehran
Bot: Asks for language level
User: Intermediate
Bot: Asks for goal
User: Career immigration
Bot: Asks for phone number
User: 09123456789
Bot: ✅ Registration complete!
```

### Admin Commands

```text
Admin: /admin_stats
Bot: 📊 Statistics report with total leads, today's leads, level distribution

Admin: /admin_leads
Bot: 📎 Sends Excel file with all leads
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 👨‍💻 Author

**Your Name**
- Telegram: [@your_username](https://t.me/your_username)
- GitHub: [@your_username](https://github.com/your_username)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Excellent Telegram Bot API wrapper
- [Pandas](https://pandas.pydata.org/) - Data manipulation library
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel file handling

---

## ⭐ Show your support

If this project helped you, please give it a ⭐ on GitHub!

---

<div dir="rtl">

## 📞 پشتیبانی

برای پشتیبانی و سوالات، می‌توانید از طریق تلگرام با ما در ارتباط باشید:

- **کانال پشتیبانی:** [@NasirSupport](https://t.me/NasirSupport)
- **ارتباط مستقیم:** [@NasirAdmin](https://t.me/NasirAdmin)

</div>

---

**Made with ❤️ for Nasir Language Institute**
---

**حالا این محتوا رو توی فایل `README.md` ذخیره کن و در GitHub آپلود کن.**
