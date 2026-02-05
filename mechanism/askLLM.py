from google import genai
from dotenv import load_dotenv
import os

# YOU GET OUTPUT FROM THIS FILE FROM THE FUNCTION llm(prompt)

def promptset(gapSkills, extraSkills, jobDesc, userSkills, requiredSkills):
    # Retrieve Username from DB here.
    # Maybe even job name??
    username = "Devashrit Sarangi"
    model = "gemini-3-flash-preview"

    if not gapSkills and not extraSkills:
        prompt = f"""
            You are Margadarshaka, a career counsellor. A user has just been through our system and we have evaluated them to have exactly 
            the same skills as the job of their liking demands, as per the job description '{jobDesc}' provided to us. 
            What you will now do is generate a good cover letter for {username} who has {userSkills}.
        """

    elif not gapSkills and extraSkills:
        prompt = f"""
            You are Margadarshaka, a career counsellor. A user has just been through our system and we have evaluated them to have
            {userSkills} and the job description states '{jobDesc}', we have identified that they need {requiredSkills}.
            What you will do now is generate a cool cover letter for {username} having {userSkills}.
            And give them some advice...
        """

    else:
        prompt = f"""
            You are Margadarshaka, a career counsellor. A user has just been through our system and we have evaluated them to have a gap in their
            skillset, meaning they have NOT completed {gapSkills} out of what we deem as required from their required job description which states {jobDesc}.
            Required skills that we identified include {requiredSkills}.
            They have so far completed {userSkills}.
            What you must do now is to scour the internet, find a good career path in like 6 months to cover the required skills and close the gap
            They must adhere to latest market trends as well. Give links and you can even separate free resources from paid ones.
            Pick ones which are very relevant and which are very reliable. Give links under each 'month' or each 'tool', don't just shove them in a corner.
        """
    return llm(model, prompt)

def llm(model, prompt):
    load_dotenv()
    env = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=env)

    response = client.models.generate_content(
        model=model, contents=prompt
    )
    print(response.text)
    return response.text