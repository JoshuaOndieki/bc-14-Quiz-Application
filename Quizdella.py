import os
import json
import cmd
current_path = os.path.dirname(os.path.abspath(__file__))

class QuizApp(cmd.Cmd):
    def quiz_list(self):
        quiz_list_path=current_path+"/dellas/"
        for file in os.listdir(quiz_list_path):
            print (file)
    def take_quiz(self,quiz):
        quiz_path=current_path+"/dellas/"+quiz+".json"
        with open(quiz_path) as quiz:
            della = json.load(quiz)
        questions=della.keys()
        user_score=0
        total_questions=int(len(questions))
        question_number=0
        while question_number<total_questions:
            answer=raw_input("Type answer here: ")
            print (della[questions[question_number]])
            if answer==della[questions[question_number]]:
                print("Correct!")
                user_score +=1
            else:
                print("Wrong answer")
            question_number+=1
        print ("Your score is %s")%(str(user_score))
app=QuizApp()