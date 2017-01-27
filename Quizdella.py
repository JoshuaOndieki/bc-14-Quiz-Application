#import libraries
from tqdm import tqdm
#use json to store and read .json files
import json
#cmd--make the app run in console with no hustle
import cmd
#use time to time quizzes
import time
#make the console interface more appealing
from termcolor import *
from pyfiglet import *
from prettytable import *
from colorama import *
#access firebase database to import and export quizzes to and from the database
from firebase import firebase



for i in tqdm(range(100),ascii=True,desc="Quizdella loading..."):
    pass
#print out a Quizdella logo
cprint(figlet_format('Quiz\nDella', font='poison'),'red', "on_green")

current_path = os.path.dirname(os.path.abspath(__file__)) #get the current path of the app and use to access other app folders
della_path = current_path + "/dellas/" #this will be the path of the quizzes(delllas)


#app functions defined inside a class QuizApp
class QuizApp(cmd.Cmd):

    def create_quiz(self):
        """
        DESCRIPTION: HELPS USERS TO CREATE QUIZZES EASILY IN THE APP WITHOUT LEARNING THE QUIZ JSON STRUCTURE
        :return: NEW QUIZ
        """
        print(Fore.GREEN)
        print("\t\t\t\t\t\t\t\tCREATE A QUIZ WIZARD")
        print(Style.RESET_ALL)
        quiz_name=input("Give your new quiz a name>> ")
        new_quiz={}
        num_que=int(input("Type the number of questions you would like to add in your quiz >> "))
        while num_que>0:
            question=input("Type your question>> ")
            answer_a=input("Answer A). ")
            answer_b=input("Answer B). ")
            answer_c=input("Answer C). ")
            answer_d=input("Answer D). ")
            correct_answer=input("Choose a letter for correct answer. (A B C D) >> ")
            answer_a="A. "+answer_a
            answer_b="B. "+answer_b
            answer_c="C. "+answer_c
            answer_d="D. "+answer_d
            #initialize dict items
            with open(current_path+"/"+"dellas/quizzes.json","r") as quizzes_list:
                quiz_dict=json.load(quizzes_list)
                quiz_dict[quiz_name]={question:{"Answers":[answer_a,answer_b,answer_c,answer_d],"Correct":correct_answer}}
            with open(current_path+"/"+"dellas/quizzes.json","w") as quizzes_list:
                json.dump(quiz_dict, quizzes_list)
            num_que-=1
        level=input("Choose a level for your quiz, e.g beginner,intermediate etc")
        new_quiz_level={}
        new_quiz_level[quiz_name] = level
        with open(current_path+"/"+"quizlevel.json","w") as quiz_levels:
            json.dump(new_quiz_level,quiz_levels)

        print("\t\t\t\t\t\t\t\tYour quiz "+quiz_name+" was created successfully!")

    def quiz_list(self):
        """
        DESCRIPTION: THIS FUNCTIONS PRINTS OUT THE LIST OF QUIZZES AVAILABLE IN A TABLE FORMAT
        Usage: Command: quiz list
        :return: LIST OF QUIZZES
        """
        print(Back.GREEN)
        print(Fore.BLUE)
        qlist=PrettyTable(["Quiz","Number of questions","Level"])
        quiz_list_path = current_path + "/dellas/quizzes.json"
        with open(quiz_list_path,"r") as quiz:
            quiz_dict = json.load(quiz)
        for i in tqdm(range(1), ascii=True, desc="Getting all available local quizzes"):
            for quiz in quiz_dict:
                quizlen = len(quiz_dict[quiz])
                with open(current_path + "/quizlevel.json") as quizlevels:
                    quiz_levels = json.load(quizlevels)
                level = quiz_levels[quiz]
                qlist.add_row([quiz, quizlen, level])
        print(qlist)
        print(Style.RESET_ALL)



    def take_quiz(self):
        """
        DESCRIPTION: THIS FUNCTIONS ALLOWS ONE TO TAKE A QUIZ AND DISPLAYS THE SCORE AFTER THE QUIZ IS TAKEN
        Usage: Command: take quiz
        :param quiz: THE NAME OF THE QUIZ
        :return: SCORE
        """
        quiz_name=input("Type the name of quiz: ")
        try:
            # search for the full path of quiz chosen
            quiz_path = current_path + "/dellas/quizzes.json"
            # load the quizzes into a dict variable to be used
            with open(quiz_path, encoding="utf-8") as quiz:
                della = json.load(quiz)
            quiz = della[quiz_name]
            questions=list(quiz.keys())
            print(quiz)
            user_score = 0  # score is initialised to zero
            total_questions = int(len(quiz))
            print(total_questions)
            question_number = 0
            time_out = 10 * total_questions  # assign the quiz a duration according to its number of questions
            timer_start = time.time()  # start the timer
            # ask questions using a while loop till no other questions are available
            while question_number < total_questions:
                print(Back.YELLOW)
                print(Fore.BLUE)
                print(questions[question_number])
                print(Style.RESET_ALL)
                question = questions[question_number]
                marking_scheme = quiz[question]
                answers = marking_scheme["Answers"]
                correct_answer = marking_scheme["Correct"]
                for choice in answers:
                    print(choice + "                                             ")
                answer = input("Type your answer: ")
                print(Style.RESET_ALL)
                timer = time.time()
                if time_out < (timer - timer_start):
                    print(Fore.RED)
                    print("Sorry timed out!")
                    print(Style.RESET_ALL)
                    time.sleep(2)
                    break
                # if the answer given by user is correct add +1 to score and respond with correct
                if answer == correct_answer:
                    print(Fore.GREEN)
                    time_remaining=(time.time()-timer_start)
                    time_remaining=str(round(time_remaining,2))
                    print ("\t\t\t\t\t\t\t\tCorrect!"+"\t\t\t\t"+time_remaining+" Seconds to go..")
                    print(Style.RESET_ALL)
                    user_score += 1
                else:
                    print(Fore.RED)
                    print("\t\t\t\t\t\t\t\tWrong answer")
                    print(Style.RESET_ALL)
                question_number += 1
                # after every question check whether the time is up before asking another question
                timer = time.time()
                if time_out < (timer - timer_start):
                    print(Fore.RED)
                    print("Sorry timed out!")
                    print(Style.RESET_ALL)
                    time.sleep(2)
                    break
            user_score = user_score
            # on break loop or finished quiz, display the score
            percent_score = (int(user_score) / total_questions) * 100
            print(Fore.GREEN)
            print("\t\t\t\t\t\t\t\tYour score is " + str(percent_score) + "%")
            print(Style.RESET_ALL)
            user_name="Josh"
            with open(current_path+"/"+"scorebd.json",encoding="utf-8") as scorebd:
                user_stat=json.load(scorebd)
            user_info=user_stat[user_name]
            score_update=user_info["Score"]
            score_update = score_update+user_score
            quizzes_update = user_info["Quizzes taken"]
            quizzes_update= quizzes_update+1
            max_score_update=user_info["Max score"]
            max_score_update=max_score_update+total_questions
            percent_update=(score_update/max_score_update)*100
            user = {user_name:{"Score": score_update, "Quizzes taken": quizzes_update,"Max score":max_score_update,"Percent":percent_update}}
            with open(current_path+"/"+"scorebd.json","w") as scorebd:
                json.dump(user,scorebd)
            print("Scores updated successfully")
        except FileNotFoundError:
            print(Fore.RED)
            print(Back.WHITE)
            print("\t\t\t\t\t\tThe quiz you are trying to take is not available\n\t\t\t\t\t\tPlease type 'quiz list' to see available quizzes.")
            print(Style.RESET_ALL)

    def import_quiz(self):
        """
        DESCRIPTION: IMPORT QUIZZES FROM EXTERNAL SOURCE TO THE APP
        Usage: Command: import quiz
        :return: IMPORTED QUIZ
        """
        #prompt for the location of file to be imported and new name for imported file
        quizdir = input("Enter the path of file to be imported: ")
        quizname = input("Give your imported quiz a name: ")
        try:
            # read data from existing file
            with open(quizdir, encoding="utf-8") as copyfile:
                copy_data = json.load(copyfile)  # store read data in copy_data variable
            # create a new file in dellas and save the data from imported file to new file
            with open(current_path+"/"+"dellas/quizzes.json","r") as quiz_file:
                quiz_data=json.load(quiz_file)
            quiz_data[quizname]=copy_data
            with open(current_path + "/dellas/" +"quizzes.json", "w") as new_file:
                json.dump(quiz_data, new_file)  # store data in new file
            print(Fore.GREEN)
            print("Quiz import successful")
            print(Style.RESET_ALL)
        except FileNotFoundError:
            print(Fore.RED)
            print(Back.WHITE)
            print("\t\t\t\t\t\t\t\tSorry, Quizdella was unable to find the file you are trying to import. \n\t\t\t\t\t\t\t\tPlease type an existing file path, e.g C:\Documents\your_file")
            print(Style.RESET_ALL)
        except json.JSONDecodeError:
            print(Fore.RED)
            print(Back.WHITE)
            print("\t\t\t\t\t\t\t\tSorry, the format of the quiz you are trying to import is unsupported. \n\t\t\t\t\t\t\t\tPlease use the create quiz wizard to create a new quiz instead.")
            print(Style.RESET_ALL)
    def list_online(self):
        """
        DESCRIPTION: LIST ONLINE QUIZZES
        Usage: Command: online quizzes
        :return: A LIST OF AVAILABLE ONLINE QUIZZES
        """
        firebases=firebase.FirebaseApplication("https://quizdella.firebaseio.com",None)
        result = firebases.get("/della",None)
        print (result)
    def view_stats(self):
        tblstat=PrettyTable(["----------------------------------------------","Score","Max score","Percentage","Quizzes done","----------------------"])
        with open(current_path+"/"+"scorebd.json","r") as scorebd:
            stats=json.load(scorebd)
        stats=stats["Josh"]
        tblstat.add_row(["----------------------------------------------",stats["Score"],stats["Max score"],stats["Percent"],stats["Quizzes taken"],"----------------------"])
        print(tblstat)

app=QuizApp()

#Manual loop
while True:
    #create a table of commands that can be executed
    print(Back.WHITE)
    print(Fore.RED)
    commands_table=PrettyTable(["Command","Description"])
    commands_table.add_row(["quiz list","Use this command to view available quizzes"])
    commands_table.add_row(["quiz take","Use this command to take a quiz"])
    commands_table.add_row(["quiz import","Import quizzes from external sources. Note that quizzes with a foreign format will not be compatible with the application"])
    commands_table.add_row(["online quizzes","View quizzes that are available to download from online database"])
    commands_table.add_row(["Create quiz","Create a new quiz using a wizard."])
    commands_table.add_row(["view stats","view your performance"])
    commands_table.add_row(["quit","Save and quit app"])
    print(commands_table)
    command=str(input("Please type a command from the above table>> "))
    print(Style.RESET_ALL)
    #call a function according to the command given by user
    if command=="quiz list":
        app.quiz_list()
    elif command=="quiz take":
        app.take_quiz()
    elif command=="quiz import":
        app.import_quiz()
    elif command=="online quizzes":
        app.list_online()
    elif command=="create quiz":
        app.create_quiz()
    elif command=="view stats":
        app.view_stats()
    elif command=="quit":
        """
        print(Fore.GREEN)
        print(Back.LIGHTBLUE_EX)
        for i in tqdm(range(1), ascii=True, desc="SAVING DATA AND EXITING APP!"):
            pass
        print(Style.RESET_ALL)
        """
        print("Quit not implemented yet")
    #if user command is unknown, print a regret message
    else:
        print(Back.BLACK)
        print(Fore.RED)
        print("Sorry,, Quizdella didn't recognize your command.")
        print(Style.RESET_ALL)