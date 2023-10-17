import discord
from discord import option
from discord import interactions
from discord.ext import commands
from discord.utils import get
import time
import random
import responses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from discord_slash import SlashCommand, SlashContext, context
from discord_slash.utils.manage_commands import create_option, create_choice

email_verification_mappings = {}
student_id_verification_code = ["",""]
TOKEN = "MTE1NDY1OTM2Njc1NTEyMzI2MA.GH_ftP.KNasarORC-iMpq9GbwtdQgaI_HzbXRP8Adjb9k"
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

def find_student_class(student_id):
    with open("student_list.txt", "r") as file:
        for line in file:
            line = line.strip().split("\t")
            if line[0] == student_id.upper():
                return line[1]
    return "Student ID not found"

def find_student_name(student_id):
    with open("name_list.txt", "r") as file:
        for line in file:
            line = line.strip().split("\t")
            if line[0] == student_id.upper():
                a = f"{line[1]} {line[2]}"
                b = line[3]
                return a
    return "Student name not found"

def find_student_eca(student_id):
    with open("name_list.txt", "r") as file:
        for line in file:
            line = line.strip().split("\t")
            if line[0] == student_id.upper():
                a = f"{line[1]} {line[2]}"
                b = line[3]
                return b
    return "Student eca not found"

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
    channel = client.get_channel(1157314133713231892)
    member = message.author
    
    if message.channel == channel:
        if p_message == "@account verification#7215":
            await message.channel.send("How can I assist you today?")
            
        elif p_message == "<@!1154659366755123260>":
            await message.channel.send("How can I assist you today?")
            
        elif p_message == "@!1154659366755123260":
            await message.channel.send("How can I assist you today?")
            
        elif p_message[:2] == "lj" and len(p_message) == 7 or p_message[:2] == "ls" and len(p_message) == 7:
            student_id = p_message
            student_id_verification_code[0] = (student_id)
            verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
            student_id_verification_code[1] = (verification_code)
            stored_verification_code = verification_code
            email_verification_mappings[student_id] = (verification_code, time.time())
            
            content = MIMEMultipart()
            content["subject"] = "學生會 Discord 認證碼 / Student council Discord verification code"
            content["from"] = "ls11189@stu.kcislk.ntpc.edu.tw"
            content["to"] = f"{student_id}@stu.kcislk.ntpc.edu.tw"
            content.attach(MIMEText(f"This is your discord verification code: \n{verification_code}\nThis code will only be available for 10 minutes."))
            stored_verification_code = verification_code
            print(verification_code)
            
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login("ls11189@stu.kcislk.ntpc.edu.tw", "pkllawxjlzifttpe")
                    smtp.send_message(content)
                    await message.channel.send(f"<@!{message.author.id}> The **verification code** has already been sent to your **student Gmail**, and it will only be available for **10 minutes**.\n**驗證碼**已發送至您的**學生Gmail**，有效時間為**10分鐘**。")
                    await message.channel.send(f"<@!{message.author.id}> Verification format: `!Verify (your student id) (your verification code)` \n驗證格式：`!Verify (你的學號) (你的驗證碼)`")
                    await message.channel.send(f"<@!{message.author.id}> example: `!Verify ls12345 1234567890123456`")
                    print("Email verification sent successfully")
                    result = find_student_class(student_id.upper())
                    print(f"paired class = \"{result}\"")
                    return result
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.channel.send(f"<@!{message.author.id}> Not being able to sent verification email. Please report the bug or issue to the administrator as soon as possible.\n無法傳送驗證電子郵件。 請盡快向管理員報告錯誤或問題。")
        
        if p_message[:7] == ("!verify"):
            verify, student_id_, verification_code = p_message.split(" ")
            stored_code, timestamp = email_verification_mappings.get(student_id_, (None, 0))
            current_time = time.time()
            
            if stored_code == verification_code and current_time - timestamp <= 600:
                del email_verification_mappings[student_id_]
                print("Email verification successful")
                class_name = find_student_class(student_id_.upper())
                member = message.author
                role = get(member.guild.roles, name=f"{class_name}")
                role_student = get(member.guild.roles, name="Student")
                
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
                role_eca = get(member.guild.roles, name=f"{find_student_eca(student_id)}")
                
                print(f"Now try to add role \"{role}\"")
                
                try:
                    await member.add_roles(role)
                    await message.channel.send(f'<@!{member.id}> Verification successful! You are now verified. Your role `{class_name}`, `{role_grade}`, `{role_big_grade}` and `{find_student_eca(student_id_)}` will be given by the bot automatically in a minute. If there is a problem, please contact the administrator.\n<@!{member.id}> 驗證成功！ 您現已通過驗證。機器人即將自動分配您的身分組`{class_name}`、`{role_grade}`、`{role_big_grade}` 和 `{find_student_eca(student_id_)}`。 如有疑問，請聯絡管理員。')
                    print("Add role successful")
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.channel.send(f'<@!{member.id}> Role "{class_name}" not found.\n<@!{member.id}> {class_name}身分組不存在。')
        
                try:
                    await member.add_roles(role_grade_x)
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.channel.send(f'<@!{member.id}> Role `{role_grade}` not found.\n<@!{member.id}> `{role_grade}` 身分組不存在。')
                
                try:
                    await member.add_roles(role_student)
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.channel.send(f'<@!{member.id}> Role `Student` not found.\n<@!{member.id}> `Student` 身分組不存在。')
                
                try:
                    await member.add_roles(role_big_grade_x)
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.channel.send(f'<@!{member.id}> Role `{role_big_grade}` not found.\n`{role_big_grade}` 身分組不存在。')
                
                try:
                    await member.add_roles(role_eca)
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.channel.send(f'<@!{member.id}> Role `{find_student_eca(student_id)}` not found.\n`{find_student_eca(student_id)}` 身分組不存在。')
                
                try:
                    b = find_student_name(student_id_.upper())
                    print(b)
                    await member.edit(nick=f"{student_id_.upper()} {b}")
                    await message.channel.send(f"<@!{member.id}> Nickname changed successfully into `{student_id_.upper()} {b}`.\n<@!{member.id}> 匿名已成功更改為 `{student_id_.upper()} {b}`。")
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.channel.send(f'<@!{member.id}> Not able to change nickname into `{student_id_.upper()} {b}`.\n<@!{member.id}> 無法更改匿名為 `{student_id_.upper()} {b}`。')
                    
            else:
                await message.channel.send(f"<@!{member.id}> Invalid verification code or expired or incorrect input format. Please try again.\n<@!{member.id}> 過期、無效的驗證碼或是錯誤的輸入格式。請重試。")
        
        else:
            await send_message(message, p_message)
      
@client.slash_command(name="send_email_verification_code", guild_ids=[1097382252863836190])
@option(
    "student_id_",
    str,
    description="Enter your student id, and the verification code will be sent to your gmail."
)
async def send_email_verification_code_command(message, student_id_):
    member = message.author
    p_message = student_id_.lower()
    
    try:
        if (p_message[:2] == "lj" and len(p_message) == 7) or (p_message[:2] == "ls" and len(p_message) == 7) or (p_message[:2] == "LJ" and len(p_message) == 7) or (p_message[:2] == "LS" and len(p_message) == 7) or (p_message[:2] == "Lj" and len(p_message) == 7) or (p_message[:2] == "Ls" and len(p_message) == 7) or (p_message[:2] == "lJ" and len(p_message) == 7) or (p_message[:2] == "lS" and len(p_message) == 7):
            student_id = p_message
            student_id_verification_code[0] = (student_id)
            verification_code = ''.join(str(random.randint(0, 9)) for _ in range(6))
            student_id_verification_code[1] = (verification_code)
            stored_verification_code = verification_code
            email_verification_mappings[student_id] = (verification_code, time.time())
            
            content = MIMEMultipart()
            content["subject"] = "學生會 Discord 認證碼 / Student council Discord verification code"
            content["from"] = "ls11189@stu.kcislk.ntpc.edu.tw"
            content["to"] = f"{p_message}@stu.kcislk.ntpc.edu.tw"
            content.attach(MIMEText(f"This is your discord verification code: \n{verification_code}\nThis code will only be available for 10 minutes."))
            stored_verification_code = verification_code
            print(verification_code)
            print(f"{p_message}@stu.kcislk.ntpc.edu.tw")
            
            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
                try:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login("ls11189@stu.kcislk.ntpc.edu.tw", "pkllawxjlzifttpe")
                    smtp.send_message(content)
                    await message.respond(f"<@!{member.id}> The **verification code** has already been sent to your **student Gmail**, and it will only be available for **10 minutes**.\n**驗證碼**已發送至您的**學生Gmail**，有效時間為**10分鐘**。")
                    await message.respond(f"<@!{member.id}> Please use slash command `/verify` to finish the verification step. \n請使用`/verify`進行驗證。")
                    print("Email verification sent successfully")
                    result = find_student_class(student_id.upper())
                    print(f"paired class = \"{result}\"")
                    return result
                
                except Exception as e:
                    print("Error message: ", e)
                    await message.respond(f"<@!{member.id}> Not being able to sent verification email. Please report the bug or issue to the administrator as soon as possible.\n無法傳送驗證電子郵件。 請盡快向管理員報告錯誤或問題。")
    
    except Exception as e:
        print("Error message: ", e)
        await message.respond(f"<@!{member.id}> Not being able to sent verification email. Please report the bug or issue to the administrator as soon as possible.\n無法傳送驗證電子郵件。 請盡快向管理員報告錯誤或問題。")


@client.slash_command(name="verify", guild_ids=[1097382252863836190])
@option(
    "student_id_",
    str,
    description="Enter your student id."
)
@option(
    "verification_code",
    str,
    description="Enter your verification code."
)
async def verify_command(message, student_id_, verification_code):
    print(f"Received interaction: {message.interaction}")
    member = message.author
    stored_code, timestamp = email_verification_mappings.get(student_id_.lower(), (None, 0))
    current_time = time.time()
    
    if stored_code == verification_code and current_time - timestamp <= 600:
        del email_verification_mappings[student_id_.lower()]
        print("Email verification successful")
        class_name = find_student_class(student_id_.upper())
        role = get(member.guild.roles, name=f"{class_name}")
        role_student = get(member.guild.roles, name="Student")
        
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
        role_eca = get(member.guild.roles, name=f"{find_student_eca(student_id_)}")
        print(f"Now try to add role \"{role}\"")
        
        try:
            await member.add_roles(role)
            await message.respond(f'<@!{member.id}> Verification successful! You are now verified. Your role `{class_name}`, `{role_grade}`, `{role_big_grade}` and `{find_student_eca(student_id_)}` will be given by the bot automatically in a minute. If there is a problem, please contact the administrator.\n<@!{member.id}> 驗證成功！ 您現已通過驗證。機器人即將自動分配您的身分組`{class_name}`、`{role_grade}`、`{role_big_grade}` 和 `{find_student_eca(student_id_)}`。 如有疑問，請聯絡管理員。')
            print("Add role successful")
        
        except Exception as e:
            print("Error message: ", e)
            await message.respond(f'<@!{member.id}> Role `{class_name}` not found.\n<@!{member.id}> `{class_name}` 身分組不存在。')
        
        try:
            await member.add_roles(role_grade_x)
        
        except Exception as e:
            print("Error message: ", e)
            await message.respond(f'<@!{member.id}> Role `{role_grade}` not found.\n<@!{member.id}> `{role_grade}` 身分組不存在。')
        
        try:
            await member.add_roles(role_student)
        
        except Exception as e:
            print("Error message: ", e)
            await message.respond(f'<@!{member.id}> Role `Student` not found.\n<@!{member.id}> `Student` 身分組不存在。')
        
        try:
            await member.add_roles(role_big_grade_x)
        
        except Exception as e:
            print("Error message: ", e)
            await message.respond(f'<@!{member.id}> Role `{role_big_grade}` not found.\n`{role_big_grade}` 身分組不存在。')
        
        try:
            await member.add_roles(role_eca)
        
        except Exception as e:
            print("Error message: ", e)
            await message.respond(f'<@!{member.id}> Role `{find_student_eca(student_id)}` not found.\n`{find_student_eca(student_id)}` 身分組不存在。')
        
        try:
            b = find_student_name(student_id_.upper())
            print(b)
            await member.edit(nick=f"{student_id_.upper()} {b}")
            await message.respond(f"<@!{member.id}> Nickname changed successfully into `{student_id_.upper()} {b}`.\n<@!{member.id}> 匿名已成功更改為 `{student_id_.upper()} {b}`。")
        
        except Exception as e:
            print("Error message: ", e)
            await message.respond(f'<@!{member.id}> Not able to change nickname into `{student_id_.upper()} {b}`.\n<@!{member.id}> 無法更改匿名為 `{student_id_.upper()} {b}`。')
    
    else:
        await message.respond(f"<@!{member.id}> Invalid verification code or expired or incorrect input format. Please try again.\n<@!{member.id}> 過期、無效的驗證碼或是錯誤的輸入格式。請重試。")

@client.event
async def on_ready():
    print(f"{client.user} is now running")
    await slash.sync_all_commands()
    
# client.run(TOKEN)
if __name__ == '__main__':
    client.run(TOKEN)
