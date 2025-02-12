class JobPosting:

    """
    JobPosting class is used to store the information of a job posting.

    Attributes:
        job_title (str): The job title of the job posting.
        company_name (str): The company name of the job posting.
        company_location (str): The company location of the job posting.
        job_description (str): The job description of the job posting.
        salary_information (str): The salary information of the job posting.
    """

    def __init__(self, job_title, company_name, company_location, job_description, salary_information):
        self.job_title = job_title
        self.company_name = company_name
        self.company_location = company_location
        self.job_description = job_description
        self.salary_information = salary_information

    def to_dict(self):
        """
        Convert the JobPosting object to a dictionary.

        Returns:
            dict: A dictionary representation of the JobPosting object.
        """
        return {
            'job_title': self.job_title,
            'company_name': self.company_name,
            'company_location': self.company_location,
            'job_description': self.job_description,
            'salary_information': self.salary_information
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a JobPosting object from a dictionary.

        Args:
            data (dict): A dictionary containing job posting information.

        Returns:
            JobPosting: A new JobPosting object.
        """
        return cls(
            job_title=data.get('job_title'),
            company_name=data.get('company_name'),
            company_location=data.get('company_location'),
            job_description=data.get('job_description'),
            salary_information=data.get('salary_information')
        )

    @staticmethod
    def generate_random_job_posting():
        """
        Generate a random job posting.

        Returns:
            JobPosting: A job posting with random attributes.
        """
        job_title = "Software Engineer"
        company_name = "Google"
        company_location = "Mountain View, CA"
        job_description = "Develop software for Google products."
        salary_information = "100,000"

        return JobPosting(job_title, company_name, company_location, job_description, salary_information)

    def __str__(self):
        return f"Job Title: {self.job_title}\nCompany Name: {self.company_name}\nCompany Location: {self.company_location}\nJob Description: {self.job_description}\nSalary Information: {self.salary_information}"
