import google.generativeai as genai

# Setup ApiKey
api_key = open('api_key.txt').read().strip()
genai.configure(api_key=api_key)

# Select Model
model = genai.GenerativeModel("gemini-1.5-flash")


# Chat history
# history=[{"role": "user", "parts": "You are an expert Mathematician"},
# {"role": "assistant", "parts": "Yes, Understood Please Ask your question"}]


def ask_gemini(question, chat_history):
    chat = model.start_chat(
        history=chat_history
    )

    response = chat.send_message(question)
    return response.text


def get_input():
    # Personal Info
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    linkedin = input("Linkedin Profile: ")
    phone = input("Enter Phone: ")
    address = input("Enter address: ")
    
    personal_info = {"name": name, "email": email, "linkedin": linkedin, "phone": phone, "address": address}

    # Company info
    company = input("Enter Company you are applying to: ")
    job_role = input("Enter Job Role you are applying to: ")
    job_position = input("Enter Job Position you are applying to: ")
    
    company_info = {"company": company, "job_role": job_role, "job_position": job_position}

    # Education Info
    education_count = int(input("Enter Number of Education (0 if you have none): "))
    education_info = []

    for i in range(education_count):
        university = input("Enter University/School name: ")
        degree = input("Enter Program Name: ")
        start_date = input("Enter Start Date(Month, Year): ")
        end_date = input("Enter End Date(Month, Year): ")

        education_info.append({"degree": degree, "university": university, "start_date": start_date, "end_date": end_date})

    # Experience Info
    experience_count = int(input("Enter Number of Experiences you want to add (0 if you have none): "))
    experience_info = []

    for i in range(experience_count):
        company = input("Enter Company Name: ")
        position = input("Enter Position: ")
        start_date = input("Enter Start Date(Month, Year): ")
        end_date = input("Enter End Date(Month, Year): ")
        desc = input("Describe what you did as part of the job(2-3 lines): ")


        experience_info.append({"company": company, "position": position, "start_date": start_date, "end_date": end_date, "desc": desc})

    # Project Info
    project_count = int(input("Enter Number of Projects you want to add (0 if you have none): "))
    project_info = []

    for i in range(project_count):
        project = input("Enter Project Name: ")
        desc = input("Describe the project(2-3 lines): ")
        end_date = input("Enter End Date(Month, Year): ")

        project_info.append({"project": project, "desc": desc, "end_date": end_date})

    
    return personal_info, company_info, education_info, experience_info, project_info


def input_from_file():
    with open("input.txt", "r") as f:
        lines = f.readlines()

    name = lines[0].strip()
    email = lines[1].strip()
    linkedin = lines[2].strip()
    phone = lines[3].strip()
    address = lines[4].strip()
    company = lines[5].strip()
    job_role = lines[6].strip()
    job_position = lines[7].strip()

    personal_info = {"name": name, "email": email, "linkedin": linkedin, "phone": phone, "address": address}
    company_info = {"company": company, "job_role": job_role, "job_position": job_position}

    education_info = []
    education_count = int(lines[8].strip())

    index = 9
    for i in range(index, index+education_count):
        university, degree, start_date, end_date = lines[i].split(",")
        education_info.append({"degree": degree, "university": university, "start_date": start_date, "end_date": end_date})
        index += 1
    
    experience_info = []
    experience_count = int(lines[index].strip())
    index += 1

    for i in range(index, index+experience_count):
        company, position, start_date, end_date, desc = lines[i].split(",")
        experience_info.append({"company": company, "position": position, "start_date": start_date, "end_date": end_date, "desc": desc})
        index += 1

    project_info = []
    project_count = int(lines[index].strip())
    index += 1

    for i in range(index, index+project_count):
        project, desc, end_date = lines[i].split(",")
        project_info.append({"project": project, "desc": desc, "end_date": end_date})
        index += 1


    return personal_info, company_info, education_info, experience_info, project_info

def create_prompt(personal_info, company_info, education_info, experience_info, project_info):
    #company_info = {"company": company, "job_role": job_role, "job_position": job_position}
    #education_info = ({"degree": degree, "university": university, "start_date": start_date, "end_date": end_date})
    # experience_info = ({"company": company, "position": position, "start_date": start_date, "end_date": end_date, "desc": desc})
    # project_info = ({"project": project, "desc": desc, "end_date": end_date})
    
    prompt_company= f'''The user wants to apply to a company named {company_info["company"]} for the role of {company_info["job_role"]} at a {company_info["job_position"]} position.'''


    prompt_perosnal = f'''The user's name is {personal_info["name"]}. The user's email is {personal_info["email"]}. The user's address is {personal_info["address"]}'''
    
    prompt_education = ""
    if len(education_info) > 0:
        prompt_education += "The user has the following education background:\n"
        for i in range(len(education_info)):
            prompt_education += f'''The user has a {education_info[i]["degree"]} from {education_info[i]["university"]} from {education_info[i]["start_date"]} to {education_info[i]["end_date"]}'''

    prompt_experience = ""
    if len(experience_info) > 0:
        prompt_experience += "The user has the following work experience:\n"
        for i in range(len(experience_info)):
            prompt_experience += f'''The user has worked at {experience_info[i]["company"]} as a {experience_info[i]["position"]} from {experience_info[i]["start_date"]} to {experience_info[i]["end_date"]}. The user's role was to {experience_info[i]["desc"]}.\n'''

    prompt_project = ""
    if len(project_info) > 0:
        prompt_project += "The user has the following projects:\n"
        for i in range(len(project_info)):
            prompt_project += f'''The user has worked on a project named {project_info[i]["project"]} which was completed by {project_info[i]["end_date"]}. The project was about {project_info[i]["desc"]}.\n'''

    prompt = f'''{prompt_perosnal}\n{prompt_company}\n{prompt_education}\n{prompt_experience}\n{prompt_project}'''

    return prompt


def generate_professional_summary(prompt):
    
    history=[
        {"role": "user", "parts": '''You are an expert who provides a professional summary of a candidate,you get as input the users personal information, company they are applying to, education, experience, and projects. You will output the professional summary of the candidate
        Important points you have to follow:
        0. The professional summary should be less than 100 words
        1. This professional summary is part of the candidates CV keep that in mind while crafting it.
        2. Output only the professional summary of the candidate, nothing else.
        3. You have all the information dosent mean you have to use all of it, use only the relevant information which keeps it professional.
        4. The professional summary should be in the first person
        5. You can add information to the summary if you wish.
        6. Dont directly mention the projects in professional summary unless really required.
        '''},
        {"role": "assistant", "parts": "Yes, Understood Please provide the relevant information and i will output the professional summary of the candidate."}
    ]

    professional_summary = ask_gemini(prompt, history)

    return professional_summary

def generate_email_draft(prompt):
    history=[
    {"role": "user", "parts": '''You are an expert who drafts emails applying for jobs at comapnies,you get as input the users personal information, company they are applying to, education, experience, and projects. You will output the email draft for the user to send to the company.
    Important points you have to follow:
    0. Keep the email professional and to the point
    1. The user will attach his CV along with the email
    2. output just the email and nothing else.
    3. You have all the information dosent mean you have to use all of it, use only the relevant information which keeps it professional and to the point.
    4. You can add information to the email which was not provided to you if required.
    '''},
    {"role": "assistant", "parts": "Yes, Understood Please provide the relevant information and i will output the email draft for the user to send to the company."}
    ]

    email_draft = ask_gemini(chat_history=history, question=prompt)
    return email_draft

# personal_info, company_info, education_info, experience_info, project_info = get_input()
personal_info, company_info, education_info, experience_info, project_info = input_from_file()
prompt = create_prompt(personal_info, company_info, education_info, experience_info, project_info)
proffesional_summary = generate_professional_summary(prompt)
email_draft = generate_email_draft(prompt)

print(proffesional_summary)
print("\n\n")
print(email_draft)





