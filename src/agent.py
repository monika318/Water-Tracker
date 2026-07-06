import os
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4", temperature=0.5)

class WaterIntakeAgent:

    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml):
        prompt = f"""You are a hydration assistant. A user has consumed {intake_ml} ml of water today.
        provide a hydration statis and siuggest if they need to drink more water
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        
        return response.content
    


if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500  # Example water intake in milliliters
    analysis = agent.analyze_intake(intake)
    print(analysis)