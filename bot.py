import discord
from discord.ext import commands
from discord.utils import get
import time
import random
import responses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os
import openai
email_verification_mappings = {}
student_id_verification_code = ["",""]
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")
openai.api_key = os.getenv('CHATGPT_API_KEY')
def chatgpt_response(prompt):
    response = openai.Completion.create(
        model='gpt-3.5-turbo',
        prompt=prompt,
        temperature=1,
        max_tokens=100
    )
    response_dict = response.get("choice")
    if response_dict and len(response_dict) > 0:
        prompt_response = response_dict[0]["text"]
    try:
        return prompt_response
    except Exception as e:
        print("Error message: ", e)
        return ("Error message: ", e)
def find_student_class(student_id):
    with open("student_list.txt", "r") as file:
        for line in file:
            line = line.strip().split("\t")
            if line[0] == student_id:
                return line[1]
    return "Student ID not found"
TOKEN = "MTE1NDY1OTM2Njc1NTEyMzI2MA.GH_ftP.KNasarORC-iMpq9GbwtdQgaI_HzbXRP8Adjb9k"
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        if not user_message.startswith("?"):
            await message.channel.send(response)
        else:
            await message.author.send(response)
    except Exception as e:
        print("Error message: ", e)
@client.event
async def on_ready():
    print(f"{client.user} is now running")
@client.event
async def on_member_join(member):
    channels = client.get_all_channels()
    print(channels)
    channel = client.get_channel(1157314133713231892)
    print(channel)
    if channel is not None:
        await channel.send(f"<@!{member.id}> Please enter your student id.\n<@!{member.id}>請輸入你的學號。")
        print("invite message sent successfully")
    else:
        print("invite message sent failed")
@client.event
async def on_message(message):
    global stored_verification_code, student_id
    p_message = message.content.lower()
    for text in ['/ai', '/bot', '/chatgpt']:
        if p_message.startswith(text):
            command=p_message.split(' ')[0]
            user_message=p_message.replace(text, '')
            print(f"{command}{user_message}")
    if command == '/ai' or command == '/bot' or command == '/chatgpt':
        bot_response = chatgpt_response(prompt=user_message)
        if bot_response.startswith("Error message: ") == True:
            print(bot_response)
        else: 
            try:
                await message.channel.send("ChatGPT response: ", bot_response)
            except Exception as e:
                print("Error message: ", e)
                await message.channel.send("Error message: ", e)
    elif p_message == "hi":
        await message.channel.send("Hello!")
    elif p_message == "hello":
        await message.channel.send("Hi!")
    elif p_message == "@account verification#7215":
        await message.channel.send("How can I assist you today?")
    elif p_message == "<@!1154659366755123260>":
        await message.channel.send("How can I assist you today?")
    elif p_message[:2] == "lj" and len(p_message) == 7 or p_message[:2] == "ls" and len(p_message) == 7:
        student_id = p_message
        student_id_verification_code[0] = (student_id)
        verification_code = ''.join(str(random.randint(0, 9)) for _ in range(16))
        student_id_verification_code[1] = (verification_code)
        stored_verification_code = verification_code
        email_verification_mappings[student_id] = (verification_code, time.time())
        content = MIMEMultipart()
        content["subject"] = "學生會 Discord 認證碼 / Student council Discord verification code"
        content["from"] = "ls11189@stu.kcislk.ntpc.edu.tw"
        content["to"] = f"{student_id}@stu.kcislk.ntpc.edu.tw"
        content.attach(MIMEText(f"this is your discord verification code {verification_code}. \nThanks for your support 😻💘"))
        stored_verification_code = verification_code
        print(verification_code)
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login("ls11189@stu.kcislk.ntpc.edu.tw", "pkllawxjlzifttpe")
                smtp.send_message(content)
                await message.channel.send("The verification code has already been sent to your student gmail, and it will only be available for 10 minutes, please check your gmail as soon as possible.\n驗證碼已發送至您的學生Gmail，有效期限僅10分鐘，請盡快查看您的學生Gmail帳號。")
                await message.channel.send("Verification input format: \"!Verify (your student id) (your verification code)\", remember to add \"!\" before the word \"verify\"\n驗證輸入格式：\"!Verify(你的學號)(你的驗證碼)\"，記得在\"verify\"前面加上\"!\"")
                await message.channel.send("example: 「!Verify ls12345 1234567890123456」. *** Upper or lower case letters doesn't matter ***\n例子：「!verify ls12345 1234567890123456」。 *** 大寫或小寫字母都可以 ***")
                print("Complete!")
                result = find_student_class(student_id.upper())
                print(result)
                return result
            except Exception as e:
                print("Error message: ", e)
                await message.channel.send("Not being able to sent verification email. Please report the bug or issue to the administrator as soon as possible.\n無法傳送驗證電子郵件。 請盡快向管理員報告錯誤或問題。")
    elif p_message[:7] == ("!verify"):
        verify, student_id_, verification_code = p_message.split(" ")
        stored_code, timestamp = email_verification_mappings.get(student_id_, (None, 0))
        current_time = time.time()
        if stored_code == verification_code and current_time - timestamp <= 600:
            del email_verification_mappings[student_id_]
            print("Email verification successful")
            class_name = find_student_class(student_id_.upper())
            member = message.author
            role = get(member.guild.roles, name=class_name)
            role_student = get(member.guild.roles, name="Student")
            role_grade = ""
            if class_name == "701" or class_name == "702" or class_name == "703" or class_name == "704":
                role_grade = "Grade 7 SP"
            elif class_name == "7A" or class_name == "7B" or class_name == "7C" or class_name == "7D" or class_name == "7E":
                role_grade = "Grade 7 IP"
            elif class_name == "801" or class_name == "802" or class_name == "803" or class_name == "804":
                role_grade = "Grade 8 SP"
            elif class_name == "8A" or class_name == "8B" or class_name == "8C" or class_name == "8D" or class_name == "8E":
                role_grade = "Grade 8 IP"
            elif class_name == "901" or class_name == "902" or class_name == "903" or class_name == "904":
                role_grade = "Grade 9 SP"
            elif class_name == "9A" or class_name == "9B" or class_name == "9C" or class_name == "9D" or class_name == "9E":
                role_grade = "Grade 9 IP"
            elif class_name == "1001" or class_name == "1002":
                role_grade = "Grade 10 SP"
            elif class_name == "10A" or class_name == "10B" or class_name == "10C" or class_name == "10D" or class_name == "10E":
                role_grade = "Grade 10 IP"
            elif class_name == "1101" or class_name == "1102":
                role_grade = "Grade 11 SP"
            elif class_name == "11A" or class_name == "11B" or class_name == "11C" or class_name == "11D" or class_name == "11E":
                role_grade = "Grade 11 IP"
            elif class_name == "1201" or class_name == "1202":
                role_grade = "Grade 12 SP"
            elif class_name == "12A" or class_name == "12B" or class_name == "12C" or class_name == "12D" or class_name == "12E":
                role_grade = "Grade 12 IP"
            role_grade_x = get(member.guild.roles, name=f"{role_grade}")
            if class_name == "701" or class_name == "702" or class_name == "703" or class_name == "704" or class_name == "7A" or class_name == "7B" or class_name == "7C" or class_name == "7D" or class_name == "7E" or class_name == "801" or class_name == "802" or class_name == "803" or class_name == "804" or class_name == "8A" or class_name == "8B" or class_name == "8C" or class_name == "8D" or class_name == "8E" or class_name == "901" or class_name == "902" or class_name == "903" or class_name == "904" or class_name == "9A" or class_name == "9B" or class_name == "9C" or class_name == "9D" or class_name == "9E":
                role_big_grade = "國中部"
            elif class_name == "1001" or class_name == "1002" or class_name == "10A" or class_name == "10B" or class_name == "10C" or class_name == "10D" or class_name == "10E" or class_name == "1101" or class_name == "1102" or class_name == "11A" or class_name == "11B" or class_name == "11C" or class_name == "11D" or class_name == "11E" or class_name == "1201" or class_name == "1202" or class_name == "12A" or class_name == "12B" or class_name == "12C" or class_name == "12D" or class_name == "12E":
                role_big_grade = "高中部"
            role_big_grade_x = get(member.guild.roles, name=f"{role_big_grade}")
            print(f"Now try to add role \"{role}\"")
            try:
                await member.add_roles(role)
                await message.channel.send(f'Verification successful! You are now verified. Your role "{class_name}", "{role_grade}" and "{role_big_grade}" will be given by the bot automatically in a minute. If there is a problem, please contact the administrator.\n驗證成功！ 您現已通過驗證。機器人即將自動分配您的身分組“{class_name}”，"{role_grade}" 和 "{role_big_grade}"。 如有疑問，請聯絡管理員。')
                print("Add role successful")
            except Exception as e:
                print("Error message: ", e)
                await message.channel.send(f'Role "{class_name}" not found.\n{class_name}身分組不存在。')
            try:
                await member.add_roles(role_grade_x)
            except Exception as e:
                print("Error message: ", e)
                await message.channel.send(f'Role "{role_grade}" not found.\n"{role_grade}"身分組不存在。')
            try:
                await member.add_roles(role_student)
            except Exception as e:
                print("Error message: ", e)
                await message.channel.send(f'Role "Student" not found.\n"Student" 身分組不存在。')
            try:
                await member.add_roles(role_big_grade_x)
            except Exception as e:
                print("Error message: ", e)
                await message.channel.send(f'Role "{role_big_grade}" not found.\n"{role_big_grade}"身分組不存在。')
        else:
            await message.channel.send("Invalid verification code or expired or incorrect input format. Please try again.\n過期、無效的驗證碼或是錯誤的輸入格式。請重試。")
    else:
        await send_message(message, p_message)
client.run(TOKEN)
