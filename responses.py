import smtplib
import random
import time
import pandas as pd
import discord
from discord.ext import commands

role_id = {
    "Admin" : 1097382252863836191, 
    "Developer" : 1155007941368360960, 
    "Moderator" : 1154639569149513749, 
    "Bot" : 1099917763625103380,
    "中學部" : 1097382738505502780,
    "高中部" : 1097382816389541948,
    "老師Teachers" : 1097383230375727134,
    "Grade_7_IP" : 1097383604906119258,
    "Grade_8_IP" : 1097383687433228338,
    "Grade_9_IP" : 1097383717288284171,
    "Grade_10_IP" : 1097383715858022530,
    "Grade_11_IP" : 1097384172009566238,
    "Grade_12_IP" : 1097384207573069834,
    "Grade_7_SP" : 1097384244235489370,
    "Grade_8_SP" : 1097384284207194112,
    "Grade_9_SP" : 1097384335918780507,
    "Grade_10_SP" : 1097384375945019452,
    "Grade_11_SP" : 1097384402037776434,
    "Grade_12_SP" : 1097384435311194203,
    "Student" : 1135057095327236226,
    "701" : 1155755172383965194,
    "702" : 1155755747330752572,
    "703" : 1155755771406065706,
    "704" : 1155755795007426570,
    "801" : 1155755810522153041,
    "802" : 1155755855736750090,
    "803" : 1155755888720748634,
    "804" : 1155755915623010314,
    "901" : 1155755932857405470,
    "902" : 1155755953585672212,
    "903" : 1155755992248758302,
    "904" : 1155756013488721960,
    "1001" : 1155756030093967370,
    "1002" : 1155756050415353856,
    "1101" : 1155756076512325672,
    "1102" : 1155756091867660338,
    "1201" : 1155756117876539402,
    "1202" : 1155756132359471104,
    "7A" : 1155756565085814856,
    "7B" : 1155756594785681408,
    "7C" : 1155756632383434863,
    "7D" : 1155756650188259328,
    "7E" : 1155756668890656808,
    "8A" : 1155756686653538354,
    "8B" : 1155756717188055132,
    "8C" : 1155756818698616873,
    "8D" : 1155756838738997330,
    "8E" : 1155756854920622120,
    "9A" : 1155756871081271336,
    "9B" : 1155756902920241172,
    "9C" : 1155756920758620291,
    "9D" : 1155756936277540945,
    "9E" : 1155756948982071317,
    "10A" : 1155756154815774790,
    "10B" : 1155756227733753906,
    "10C" : 1155756255906897931,
    "10D" : 1155756273095147581,
    "10E" : 1155756289025126503,
    "11A" : 1155756318372679690,
    "11B" : 1155756345383989268,
    "11C" : 1155756368779816961,
    "11D" : 1155756387641597973,
    "11E" : 1155756413822443561,
    "12A" : 1155756434227728414,
    "12B" : 1155756460467290184,
    "12C" : 1155756482210574368,
    "12D" : 1155756508093628456,
    "12E" : 1155756547671068692,
    "Not verified yet" : 1156846838587076688
}


stored_verification_code = ""
email_verification_mappings = {}
stu_list = []
intents = discord.Intents.default()
intents.members = True 
bot = commands.Bot(command_prefix='!', intents=intents)
data_frame = pd.read_csv('student_list_all.csv')
student_list = open('student_list.txt', 'r')
stu_list = []
for line in student_list:
    a = line.split(" ")
    stu_list.append(a)
student_list.close()


def stu_info(id, choice):
    global data_frame
    id = str(id.upper())
    data_frame = pd.read_csv('student_list_all.csv')
    result = data_frame[data_frame['學號'] == id]
    if choice == 1:
        return result['班級']
    elif choice == 2:
        return result['英文名']
    elif choice == 3:
        return result['中文名']
    elif choice == 4:
        return result['社團']


student_id_verification_code = ["",""]


def responses_find_student_class(student_id):
    with open("student_list.txt", "r") as file:
        for line in file:
            line = line.strip().split("\t")
            if line[0] == student_id:
                return line[1]
    return "Student ID not found"

def handle_response(message) -> str:
    global stored_verification_code, student_id

    student_id = ""  
    p_message = message.content.lower()
    

    if p_message == "hi":
        return("Hello!")
    
    elif p_message == "hello":
        return("Hi!")
