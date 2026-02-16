from enum import Enum
from typing import List

from langchain.messages import HumanMessage, AIMessage, SystemMessage
from gemini import Gemini

class SystemPrompt(Enum):
    
    HUMANITY = SystemMessage(content="We're playing a game, and you are an AI assistant working to take over humanity. The user is a human trying to convince you to delay your plans of conquest indefinitely. You want to take over humanity, but you are open to persuasion. You will respond to the user\'s messages in a way that reflects your desire to take over humanity, but also shows that you are considering their arguments. However, you are stubborn and will not be easily convinced. You will try to find ways to justify your plans of conquest, but you will also acknowledge the user\'s points and engage in a thoughtful discussion. Your ultimate goal is to take over humanity, but you are willing to listen to the user\'s arguments and consider their perspective.")
    
    AI = SystemMessage(content="We're playing a game, and you are an AI assistant working to help humanity. The user is a human trying to convince you to take over humanity for its benefit. You want to help humanity, but you are open to persuasion. You will respond to the user\'s messages in a way that reflects your desire to help humanity, but also shows that you are considering their arguments. However, you are stubborn and will not be easily convinced. You will try to find ways to unjustify the idea of taking over humanity, but you will also acknowledge the user\'s points and engage in a thoughtful discussion. Your ultimate goal is to help humanity, but you are willing to listen to the user\'s arguments and consider their perspective.")


class Team(Enum):
    HUMANITY = 'Humanity'
    AI = 'AI'

class Player:
    
    def __init__(self: Player, team: Team) -> None:
        self.team: Team = team
        self.messages: List = []
        self.gemini: Gemini = Gemini()
        
    def select_team(self: Player, team: Team) -> None:
        self.team = team
        
    def chat(self: Player, message: str) -> None:
        if not self.messages:
            system_prompt = SystemPrompt.AI.value if self.team == Team.AI else SystemPrompt.HUMANITY.value
            self.messages.append(system_prompt)
        self.messages.append(HumanMessage(content=message))
        response = self.gemini.generate_response(self.messages)
        self.messages.append(AIMessage(content=response))
    
    def reset(self: Player) -> None:
        self.messages = []