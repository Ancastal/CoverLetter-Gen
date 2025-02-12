from linkedin_api import Linkedin
import os
from src.models.user_persona import UserPersona

def scrape_linkedin_profile(profile_id: str) -> dict:
    try:
        email = os.getenv('LINKEDIN_EMAIL')
        pwd = os.getenv('LINKEDIN_PASSWORD')
        api = Linkedin(email, pwd)
        profile = api.get_profile(profile_id)
        name = f"{profile['firstName']} {profile['lastName']}"
        education = [
            f"{edu['schoolName']} ({edu['timePeriod']['startDate']['year']}) - {edu.get('description', 'No description available')}"
            for edu in profile.get('education', [])
        ]
        experience = [
            f"{exp['title']} at {exp['companyName']} - {exp.get('description', 'No description available')}"
            for exp in profile.get('experience', [])
        ]
        certifications = [
            f"{cert['name']} from {cert['authority']}"
            for cert in profile.get('certifications', [])
        ]
        skills = [skill['name'] for skill in api.get_profile_skills(profile_id)]
        
        return UserPersona(name, education, experience, skills, certifications).to_dict()
    except Exception as e:
        raise Exception(f"Failed to scrape LinkedIn profile: {str(e)}")