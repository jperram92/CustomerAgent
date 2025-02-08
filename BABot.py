from langchain_openai import OpenAI  # Import from langchain-openai now
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, Tool
from langchain.tools import StructuredTool
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now you can access the OPEN_AI_API_KEY from the environment variables
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

# Initialize the LLM (Large Language Model) with your API key
llm = OpenAI(temperature=0.7, openai_api_key=OPEN_AI_API_KEY)

# Define a tool to gather the requirements
def gather_business_requirements(inputs):
    print(f"Inputs in gather_business_requirements: {inputs}")
    
    # Ensure inputs is a dictionary and not a string
    if isinstance(inputs, str):
        inputs = eval(inputs)  # Convert string back to dictionary if necessary

    business_goals = inputs.get("business_goals", "")
    user_stories = inputs.get("user_stories", "")
    acceptance_criteria = inputs.get("acceptance_criteria", "")
    stakeholders = inputs.get("stakeholders", "")
    
    document = f"""
    # Business Requirements
    ## Business Goals:
    {business_goals}
    
    ## User Stories:
    {user_stories}
    
    ## Acceptance Criteria:
    {acceptance_criteria}
    
    ## Stakeholders:
    {stakeholders}
    """
    return document

# Define a tool to generate User Stories
def generate_user_stories(inputs):
    print(f"Inputs in generate_user_stories: {inputs}")
    
    # Ensure inputs is a dictionary and not a string
    if isinstance(inputs, str):
        inputs = eval(inputs)  # Convert string back to dictionary if necessary

    user_stories = inputs.get("user_stories", "")
    prompt_template = "As a {user_role}, I want {functionality} so that {benefit}"
    stories = "\n".join([prompt_template.format(**story) for story in user_stories])
    return stories

# Define a tool to generate functional requirements
def generate_functional_requirements(inputs):
    print(f"Inputs in generate_functional_requirements: {inputs}")
    
    # Ensure inputs is a dictionary and not a string
    if isinstance(inputs, str):
        inputs = eval(inputs)  # Convert string back to dictionary if necessary
    
    # Extract required values with default fallbacks to prevent missing data
    business_goals = inputs.get("business_goals", "No business goals provided.")
    acceptance_criteria = inputs.get("acceptance_criteria", "No acceptance criteria provided.")
    
    document = f"""
    ## Functional Requirements:
    {business_goals}
    
    ## Acceptance Criteria:
    {acceptance_criteria}
    """
    
    print(f"Generated Functional Requirements:\n{document}")
    return document

# Define a tool to create Stakeholder Analysis
def stakeholder_analysis(inputs):
    print(f"Inputs in stakeholder_analysis: {inputs}")
    
    # Ensure inputs is a dictionary and not a string
    if isinstance(inputs, str):
        inputs = eval(inputs)  # Convert string back to dictionary if necessary

    stakeholders = inputs.get("stakeholders", "")
    report = ""
    for stakeholder in stakeholders:
        report += f"### Stakeholder: {stakeholder['name']}\nRole: {stakeholder['role']}\nNeeds: {stakeholder['needs']}\nPain Points: {stakeholder['pain_points']}\n\n"
    return report

# Create and initialize agent with tools
tools = [
    Tool(func=gather_business_requirements, name="GatherBusinessRequirements", description="Gathers business requirements, user stories, and stakeholder information."),
    Tool(func=generate_user_stories, name="GenerateUserStories", description="Generates user stories from the provided input."),
    Tool(func=generate_functional_requirements, name="GenerateFunctionalRequirements", description="Generates functional requirements document based on input."),
    Tool(func=stakeholder_analysis, name="StakeholderAnalysis", description="Creates a stakeholder analysis report based on provided stakeholder details.")
]

agent = initialize_agent(tools, llm, agent_type="zero_shot", verbose=True)

# Inputs before invoking agent
inputs_with_input_key = {
    "input": {
        "business_goals": "To expand the product line and increase customer reach.",
        "user_stories": [
            {"user_role": "product manager", "functionality": "create new product categories", "benefit": "expand product options for customers"},
            {"user_role": "marketing manager", "functionality": "launch marketing campaigns", "benefit": "increase brand visibility"}
        ],
        "acceptance_criteria": "All product categories should be easy to navigate and marketing campaigns should result in a 10% increase in engagement.",
        "stakeholders": [
            {"name": "Alice", "role": "Product Manager", "needs": "Clear roadmap for new product features", "pain_points": "Slow development cycles"},
            {"name": "Bob", "role": "Marketing Manager", "needs": "Timely data on campaign performance", "pain_points": "Ineffective tracking tools"}
        ]
    }
}


# Print inputs before invoking the agent
print(f"Inputs before invoking agent: {inputs_with_input_key}")

# Run the agent with the corrected inputs structure
output = agent.invoke(inputs_with_input_key)

print(output)
