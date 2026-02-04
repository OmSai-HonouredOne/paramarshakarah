from google import genai
from dotenv import load_dotenv
import os

# YOU GET OUTPUT FROM THIS FILE FROM THE FUNCTION llm(prompt)

def promptset(gapSkills, extraSkills, userSkills, requiredSkills):
    # Retrieve Username from DB here.
    # Maybe even job name??
    username = "WoozyDragon"

    if not gapSkills and not extraSkills:
        prompt = f"""
            You are Margadarshaka, a career counsellor. A user has just been through our system and we have evaluated them to have exactly 
            the same skills as the job of their liking demands, as per the job description provided to us. 
            What you will now do is generate a good cover letter for {username} who has {userSkills}.
        """

    elif not gapSkills and extraSkills:
        prompt = f"""
            You are Margadarshaka, a career counsellor. A user has just been through our system and we have evaluated them to have more skills
            than what is needed for the job (which is a good thing!). What you will do now is generate a cool cover letter for {username} having {userSkills} and you can
            even highlight they have {str(extraSkills)} extra skills as well! And give them some advice...
        """

    else:
        prompt = f"""
            You are Margadarshaka, a career counsellor. A user has just been through our system and we have evaluated them to have a gap in their
            skillset, meaning they have NOT completed {gapSkills} which are needed by the job (which are {requiredSkills}). Extra Skills include {extraSkills} (ignore if None).
            They have so far completed {userSkills}.
            What you must do now is to scour the internet, find a good career path in like 6 months to cover the required skills and close the gap
            They must adhere to latest market trends as well. Give links and you can even separate free resources from paid ones.
            Pick ones which are very relevant and which are very reliable.
        """
        
    return llm(prompt)

def llm(prompt):
    load_dotenv()
    env = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=env)

    response = client.models.generate_content(
        model="gemini-3-flash-preview", contents=prompt
    )
    print(response.text)
    return response.text

