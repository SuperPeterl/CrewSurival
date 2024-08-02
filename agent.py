import os
os.environ["SERPER_API_KEY"] = "75fb28de5dac4a2ef7f2fe9322ec9277b3ee1f5e"  # serper.dev API key
os.environ["EXA_API_KEY"] = "bf4f9f68-845e-4185-9088-db9ca95658ef"
os.environ["OPENAI_API_KEY"] = "sk-proj-1LylPhLMrvJLtVMqYDtGT3BlbkFJuJGr2pxwQ5V4D30DCp38"

from crewai import Agent,Task,Crew
from langchain_groq import ChatGroq

llmx = ChatGroq(api_key="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",
                model= "llama3-groq-70b-8192-tool-use-preview")
from crewai_tools import TXTSearchTool
# Define your agents with roles and goals
class PlayerAgent:
    def __init__(self):
        self.player = Agent(
            role='player',
            goal='from {memory} and information {info} survive as long as possible in the game',
            backstory="""You are a player in a game. You have a limited set of capabilities. They are listed below:""",
            verbose=True,
            allow_delegation=False,
            llm  =  llmx,
            max_iter = 1
            )
        
        self.attention = Agent(
            role='attention',
            goal='from {memory} and information {info} prioritizes game-relevant information, filtering out distractions.',
            backstory="""You are an attention agent. You are here to help the player make a decision""",
            verbose=True,
            allow_delegation=False,
            llm  =  llmx,
            max_iter = 1
            )
        
        self.problemsolver = Agent(
            role='ProblemSolver',
            goal='from {memory} and information {info} overcome challenges and obstacles presented by the game.',
            backstory="""overcome challenges and obstacles presented by the game.""",
            verbose=True,
            allow_delegation=False,
            llm  =  llmx,
            max_iter = 1
            )
        
        self.patternrecognizer = Agent(
            role='PatternRecognizer',
            goal='from {memory} and information {info} identify and learn from recurring elements or strategies in the game.',
            backstory="""identify patterns in the game to help the player make better decisions.""",
            verbose=True,
            allow_delegation=False,
            llm  =  llmx,
            max_iter = 1
            )
        
        self.timemanager = Agent(
            role='TimeManager',
            goal='from {memory} and information {info} manage time effectively to achieve the player’s objectives.',
            backstory="""manage time effectively to achieve the player’s objectives.""",
            verbose=True,
            allow_delegation=False,
            llm  =  llmx,
            max_iter = 1
            )
        
        self.memory = Agent(
            role='Memory',
            goal='from {memory} and information {info} store and retrieve relevant information to assist the player in making decisions.',
            backstory="""store and retrieve relevant information to assist the player in making decisions.
            """,
            verbose=True,
            allow_delegation=False,
            llm  =  llmx,
            max_iter = 1
            )
        
        self.give_attention = Task(
            description='from {memory} and information {info} the information you have, decide what information is most relevant to the player',
            expected_output='A list of the most relevant information to the player',
            agent=self.attention,
        )

        self.solve_problem = Task(
            description='from {memory} and information {info} define a problem, come up with a solution to help the player overcome it',
            expected_output='A solution to the problem in form "problem: " and solution: ""',
            agent=self.problemsolver
        )

        self.recognize_pattern = Task(
            description='from {memory} and information {info} Identify recurring elements or strategies in the game that can help the player make better decisions',
            expected_output='A list of patterns or strategies that can help the player ',
            agent=self.patternrecognizer,
        )

        self.manage_time = Task(
            description='from {memory} and information {info} Given the player’s objectives, come up with a plan to manage time effectively',
            expected_output="list of a action and time usage , and time passed and plan to manage time effectively",
            agent=self.timemanager,
        )

        self.store_memory = Task(
            description='from {memory} and information {info} Given new information, store it in memory for future reference',
            expected_output="""The new information stored in memory
            line of text form is this  by "" mean information you need to store
            you need to store previous memore and new information in the memory max is 5
            id = "" # id of memory max is 5 
            priortize information = "" #information you need to store
            problem and solution =  problem: "" and solution: "" #problem and solution
            pattern = "" #pattern
            time management = "" #time management
            """,
            agent=self.memory,
            output_file="memory.txt",
        )

        self.player_decision = Task(
            description='from {memory} and information {info} Make a decision based on the information you have',
            expected_output='A decision to be executed by the player',
            agent=self.player,
        )

        self.gameinterface = Task(
            description='Make a decision based on the information you have this is your infomation {info} and your last action is {last_action} learn to make a decision ',
            expected_output="""A decision to be executed by the player you output is of this 
             You have a limited set of capabilities. They are listed below:
            * move_left
            * move_right
            * move_up
            * move_down
            * search
            * use
            # Responses
            
            You must supply your responses in the form of list of string .  Your responses will specify which of the above actions you intend to take.
            you answer is planing to do the following actions in the game. must have 10 actions in the list
            The following is an example of a valid response:
                ["move_left", "move_right", "move_up", "move_down", "search", "use", "move_left", "move_right", "move_up", "move_down"]
            """,
            agent=self.player,
            output_file="player_decision.txt",
        )

# Instantiate your crew with a sequential process
        self.crew = Crew(
            agents=[self.player, self.attention, self.problemsolver, self.patternrecognizer, self.timemanager, self.memory],
            tasks=[self.give_attention, self.solve_problem, self.recognize_pattern, self.manage_time, self.store_memory, self.player_decision,self.gameinterface,],
            verbose=2, # You can set it to 1 or 2 to different logging levels
            max_rpm = 30
            )
        
    def get_dicision(self,information,last_action,memory):
        result = self.crew.kickoff({"info" : information, "last_action": last_action, "memory": "memory"})
        return result
    


