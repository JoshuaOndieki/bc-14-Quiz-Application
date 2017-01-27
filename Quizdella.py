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
                try:
                    with open(current_path + "/quizlevel.json") as quizlevels:
                        quiz_levels = json.load(quizlevels)
                    level = quiz_levels[quiz]
                    qlist.add_row([quiz, quizlen, level])
                except:
                    level="None"
                    qlist.add_row([quiz,quizlen,level])
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
            #print(quiz)
            user_score = 0  # score is initialised to zero
            total_questions = int(len(quiz))
            #print(total_questions)
            question_number = 0
            time_out = 10 * total_questions  # assign the quiz a duration according to its number of questions
            # ask questions using a while loop till no other questions are available
            print(Fore.GREEN)
            print("\t\t\t\t\t\t\t\tYou have "+str(round(time_out,2))+" seconds to finish the quiz.")
            print(Style.RESET_ALL)
            timer_start = time.time()  # start the timer
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
                time_remaining = int(time_out - (time.time() - timer_start))
                if time_remaining<=0:
                    print(Fore.RED)
                    print("Sorry timed out!")
                    print(Style.RESET_ALL)
                    time.sleep(2)
                    break
                # if the answer given by user is correct add +1 to score and respond with correct
                if answer == correct_answer:
                    print(Fore.GREEN)
                    time_remaining=(time_out-(time.time()-timer_start))
                    time_remaining=str(round(time_remaining,2))
                    print ("\t\t\t\t\t\t\t\tCorrect!"+"\t\t\t\t\t\t\t\t\t\t\t\t"+time_remaining+" Seconds to go..")
                    print(Style.RESET_ALL)
                    user_score += 1
                else:
                    print(Fore.RED)
                    print("\t\t\t\t\t\t\t\tWrong answer")
                    print("\t\t\t\t\t\t\t\tThe right  answer is "+correct_answer)
                    print(Style.RESET_ALL)
                question_number += 1
                # after every question check whether the time is up before asking another question
                time_remaining = int(time_out - (time.time() - timer_start))
                timer = time.time()
                if time_remaining<=0:
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
        print(Back.GREEN)
        print(Fore.BLUE)
        onlineq_list=PrettyTable(["Quiz","Number of questions","Level"])
        firebases=firebase.FirebaseApplication("https://quizdella.firebaseio.com",None)
        online_quizzes = firebases.get("/della",None)
        for i in tqdm(range(1), ascii=True, desc="Getting all available online quizzes"):
            for quiz in online_quizzes:
                quizlen = len(online_quizzes[quiz])
                try:
                    with open(current_path + "/quizlevel.json","r") as quizlevels:
                        quiz_levels = json.load(quizlevels)
                    level = quiz_levels[quiz]
                except:
                    level="None"
                onlineq_list.add_row([quiz, quizlen, level])
        print(onlineq_list)
        print(Style.RESET_ALL)
    def download(self):
        """
        DESCRIPTION: DOWNLOAD QUIZZES FROM AN ONLINE DATABASE
        Usage: Command: download quiz
        :return:
        """
        quiz_name=input("Type the name of an online quiz to download >> ")
        firebases=firebase.FirebaseApplication("https://quizdella.firebaseio.com",None)
        online_quiz=firebases.get("/della",quiz_name)
        with open(current_path + "/dellas/quizzes.json", "r") as quizzes:
            local_quizzes = json.load(quizzes)
        local_quizzes[quiz_name] = online_quiz
        with open(current_path + "/dellas/quizzes.json", "w") as quizzes:
            json.dump(local_quizzes, quizzes)
        print("The quiz was downloaded successfully, you can now view and take the quiz")

    def upload(self):
        """
        DESCRIPTION: UPLOAD QUIZZES TO ONLINE DATABASE
        Usage: Command: upload quiz
        :return:
        """
        """
        quiz_name=input("Type the name of a local quiz to upload >> ")
        with open(current_path+"/dellas/quizzes.json","r") as quizzes:
            local_quizzes=json.load(quizzes)
        quiz=local_quizzes[quiz_name]
        firebases = firebase.FirebaseApplication("https://quizdella.firebaseio.com", None)
        online_quizzes = firebases.get("/della", None)
        online_quizzes[quiz_name]=quiz
        firebases.delete("/della",None)
        online_quizzes=firebases.post("/della",online_quizzes)
        print(quiz_name+" was successfully uploaded to online database. ")
        """
        print(Fore.RED)
        print(Back.WHITE)
        print("\t\t\t\t\t\t\t\tDEAR USER QUIZ UPLOAD IS NOT AVAILABLE AT THE MOMENT.QUIZDELLA DATABASE IS UNDER MAINTAINANCE. NOTE THAT THE DOWNLOAD SERVICE IS STILL AVAILABLE.")
        print(Style.RESET_ALL)


    def view_stats(self):
        """
        DESCRIPTION: DISPLAY STATISTICS FOR QUIZZES TAKEN BY USER.
        Usage: Command: view stats
        :return:
        """
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
    commands_table.add_row(["download quiz","Download a quiz from the online database to local. "])
    commands_table.add_row(["upload quiz","upload quizzes to the online database from your computer"])
    commands_table.add_row(["view stats","view your performance"])
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
    elif command=="view stats":
        app.view_stats()
    elif command=="download quiz":
        app.download()
    elif command=="upload quiz":
        app.upload()
    #if user command is unknown, print a regret message
    else:
        print(Back.BLACK)
        print(Fore.RED)
        print("Sorry,, Quizdella didn't recognize your command.")
        print(Style.RESET_ALL)