from typing import Dict, List, Tuple
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager, register_function
from autogen.agentchat.contrib.captainagent import CaptainAgent
from tools.pdf_gen import generate_cover_letter_pdf
from agents.tools.scrapers.linkedin_profile import scrape_linkedin_profile
from agents.tools.scrapers.linkedin_job import scrape_job_posting
from src.models.user_persona import UserPersona
from src.models.job_posting import JobPosting
from dotenv import load_dotenv
import os
from textwrap import dedent
load_dotenv()

# Configuration for the agents
config_list = {
    "model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")
    }

thinker_agent = AssistantAgent(
    name="Thinker",
    llm_config=config_list,
    max_consecutive_auto_reply=10,
    system_message=dedent("""
    You are a thinker agent that can think about the given task and return a plan for the next steps.
    Pass all the necessary information about the job posting and the candidate profile to the writer agent.
    """
    )
)

writer_agent = AssistantAgent(
    name="Writer",
    llm_config=config_list,
    max_consecutive_auto_reply=10,
    system_message="You are a writer agent that can write a cover letter based on the given task and the plan. Generate the cover letter in markdown format, making sure it fits in one page.Return 'TERMINATE' if the task is complete."
)

refiner_agent = AssistantAgent(
    name="Refiner",
    llm_config=config_list,
    max_consecutive_auto_reply=10,
    system_message="You are a refiner agent that can refine the cover letter based on the feedback. Return 'TERMINATE' if the task is complete."
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "work_dir",
        "use_docker": False,
    },
)

register_function(
    scrape_job_posting,
    # caller agent
    caller=thinker_agent,
    # executor agent
    executor=user_proxy,
    name="scrape_job_posting",
    description="Scrapes a job posting from the given URL and returns structured job data."
)

register_function(
    scrape_linkedin_profile,
    caller=thinker_agent,
    executor=user_proxy,
    name="scrape_linkedin_profile",
    description="Scrapes a LinkedIn profile and returns structured user persona data."
)



def main():
    job_url = "https://www.linkedin.com/jobs/view/3766686044/"
    profile_url = "https://www.linkedin.com/in/antonio-castaldo/"
    task = dedent(f"""
    Extract information about the job posting and the candidate profile.
    Write a cover letter for the following job posting:
    Job URL: {job_url}
    Profile URL: {profile_url}
    """)
    
    group_chat = GroupChat(
        agents=[thinker_agent, writer_agent, user_proxy],
        messages=[],
        max_round=6,
        speaker_selection_method="auto",
        allow_repeat_speaker=True,
    )

    group_chat_manager = GroupChatManager(groupchat=group_chat)
    result = user_proxy.initiate_chat(
        group_chat_manager,
        message=task,
    )
    
    summary = result.summary.replace("```markdown", "").replace("```", "")
    with open("cover_letter.md", "w") as f:
        f.write(summary)
    # Generate PDF from the markdown response
    
    success, message = generate_cover_letter_pdf(
        summary,
        "Antonio Castaldo",
        "Cover_Letter.pdf"
    )
    print(message)

if __name__ == "__main__":
    main()

#captain_agent = CaptainAgent(
#    name="captain_agent",
#    llm_config=config_list,
#    code_execution_config={"use_docker": False, "work_dir": "groupchat"},
#    agent_config_save_path=None,  # If you'd like to save the created agents in nested chat for further use, specify the save directory here
#)
#captain_user_proxy = UserProxyAgent(name="captain_user_proxy", human_input_mode="NEVER", code_execution_config={"use_docker": False, "work_dir": "groupchat"})
#
#result = captain_user_proxy.initiate_chat(
#    captain_agent,
#    message=dedent(f"""
#    Generate a PDF from the summary below, using either fpdf or reportlab.
#    Make sure it looks really good, with large borders and a professional look. The final PDF should be well-formatted, aesthetically pleasing and professional.
#    
#    It should also have a signature at the end of the document with the name of the writer.
#    
#    {response.summary}
#    """),
#    max_turns=1,
#)
#
    #print(result)
    
"""
# Register external functions to the scraper agent
register_function(
    scrape_job_posting,
    # caller agent
    caller=self.scraper_agent,
    # executor agent
    executor=self.user_proxy,
    name="scrape_job_posting",
    description="Scrapes a job posting from the given URL and returns structured job data."
)

register_function(
    scrape_linkedin_profile,
    caller=self.scraper_agent,
    executor=self.user_proxy,
    name="scrape_linkedin_profile",
    description="Scrapes a LinkedIn profile and returns structured user persona data."
)
"""
