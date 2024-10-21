import os
from crewai import Agent, Task, Crew

from dotenv import dotenv_values

secrets = dotenv_values()

os.environ["OPENAI_API_KEY"] = secrets['OPENAI_API_KEY']
os.environ["OPENAI_MODEL_NAME"] = secrets['OPENAI_MODEL']

info_agent = Agent(
    role="Information Agent",
    goal="Give compelling information about a certain topic",
    backstory="""
        You love to know information.  People love and hate you for it.  You win most of the
        quizzes at your local pub.
    """
)

task1 = Task(
    description="Tell me all about the blue-ringed octopus.",
    expected_output="Give me a quick summary and then also give me 7 bullet points describing it.",
    agent=info_agent
)

crew = Crew(
    agents=[info_agent],
    tasks=[task1],
    verbose=1
)

result = crew.kickoff()

print("############")
print(result)
