
class UserPersona:

    """
    UserPersona class is a class that represents a user persona.

    Attributes:
        name (str): The name of the user persona.
        education (str): The education of the user persona.
        experience (str): The experience of the user persona.
        skills (str): The skills of the user persona.
        certifications (str): The certifications of the user persona.
    """

    def __init__(self, name, education, experience, skills, certifications):
        self.name = name
        self.education = education
        self.experience = experience
        self.skills = skills
        self.certifications = certifications

    def generate_random_user_persona():
        """
        Generate a random user persona.

        Returns:
            UserPersona: A user persona with random attributes.
        """
        name = "John Doe"
        education = "Bachelor's Degree"
        experience = "5 years of experience"
        skills = "Python, SQL, Java"
        certifications = "AWS, Google Cloud"

        return UserPersona(name, education, experience, skills, certifications)

    def to_dict(self):
        """
        Convert the UserPersona object to a dictionary.

        Returns:
            dict: A dictionary representation of the UserPersona object.
        """
        return {
            'name': self.name,
            'education': self.education,
            'experience': self.experience,
            'skills': self.skills,
            'certifications': self.certifications
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a UserPersona object from a dictionary.

        Args:
            data (dict): A dictionary containing user persona information.

        Returns:
            UserPersona: A new UserPersona object.
        """
        return cls(
            name=data.get('name'),
            education=data.get('education'),
            experience=data.get('experience'),
            skills=data.get('skills'),
            certifications=data.get('certifications')
        )


    def __str__(self):
        return f"Name: {self.name}\nEducation: {self.education}\nExperience: {self.experience}\nSkills: {self.skills}\nCertifications: {self.certifications}"