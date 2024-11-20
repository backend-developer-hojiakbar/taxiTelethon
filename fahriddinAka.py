from telethon import TelegramClient, events

api_id = 24430906
api_hash = '51e7d9fbda7b2ce4aec07b52ad737839'
phone_number = '+998903434599'

keywords = ['pochta bor', 'odam bor', 'почта бор', 'одам бор']

target_groups = ['https://t.me/+B54YAFQN-5JlZGIy']

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    if not client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input('Tasdiqlash kodini kiriting: ')
        await client.sign_in(phone_number, code)
        if not client.is_user_authorized():
            password = input('Ikki bosqichli tasdiqlash parolini kiriting: ')
            await client.sign_in(password=password)

    # Foydalanuvchi qo'shilgan barcha guruhlarni olish
    dialogs = await client.get_dialogs()
    groups = [dialog for dialog in dialogs if dialog.is_group]

    @client.on(events.NewMessage(chats=[group.id for group in groups]))  # Guruhlar avtomatik aniqlanadi
    async def handler(event):
        message_text = event.raw_text.lower()  # Xabarni kichik harflarga aylantiramiz
        if any(keyword in message_text for keyword in keywords):  # Agar kalit so'z topilsa
            sender = await event.get_sender()  # Xabar yuboruvchining ma'lumotlarini olamiz
            sender_username = sender.username if sender.username else 'Anonim foydalanuvchi'
            group_link = f"https://t.me/{event.chat.username}" if event.chat.username else 'Link yo‘q'
            sender_link = f"https://t.me/{sender_username}"  # Yuboruvchining username havolasi

            # Xabarni har bir maqsadli guruhga yuboramiz
            for target_group in target_groups:
                if sender_username == "Taxi_734" or sender_username == "Azizbek_usta1":
                    pass
                else:
                    await client.send_message(
                        target_group,
                        f'Guruh havolasi: {group_link}\nFoydalanuvchi: @{sender_username}\n\nYolovchi topildi: {event.raw_text}'
                    )

    print("Dastur ishga tushdi. Xabarlarni kutyapman...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())