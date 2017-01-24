import os
import json
import cmd
import time
from termcolor import *
from pyfiglet import *
from prettytable import *
from firebase import *
from colorama import *


cprint(figlet_format('Quiz', font='poison'),'red', "on_green")
cprint(figlet_format("Della", font="poison"), "red", "on_green")

current_path = os.path.dirname(os.path.abspath(__file__))
della_path = current_path + "/dellas/"
users={}
class QuizApp(cmd.Cmd):
    def quiz_list(self):
        print(Back.GREEN)
        print(Fore.BLUE)
        qlist=PrettyTable(["Quiz","Origin"])
        quiz_list_path = current_path+"/dellas/"
        for file in os.listdir(quiz_list_path):
            qlist.add_row([file,"Quizdella"])
        print(qlist)
        print(Style.RESET_ALL)

    def take_quiz(self , quiz):

        quiz_path=current_path+"/dellas/"+quiz+".json"
        with open(quiz_path) as quiz:
            della = json.load(quiz)
        questions=list(della.keys())
        user_score=0
        total_questions=int(len(questions))
        print(total_questions)
        question_number=0
        time_out=10*total_questions
        timer_start=time.time()
        while question_number < total_questions:
            print(Back.YELLOW)
            print(Fore.BLUE)
            print(questions[question_number])
            answer = input("Type your answer: ")
            print(Style.RESET_ALL)
            if answer == della[questions[question_number]]:
                print(Fore.GREEN)
                print("Correct!")
                print(Style.RESET_ALL)
                user_score += 1
            else:
                print(Fore.RED)
                print("Wrong answer")
                print(Style.RESET_ALL)
            question_number += 1
            timer=time.time()
            if time_out<(timer-timer_start):
                print(Fore.RED)
                print("Sorry timed out!")
                print(Style.RESET_ALL)
                time.sleep(2)
                break
        user_score=str(user_score)
        print ("Your score is "+user_score)
app=QuizApp()
app.quiz_list()