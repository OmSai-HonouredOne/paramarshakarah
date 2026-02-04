from google import genai
from dotenv import load_dotenv
import os


def llm(skills, target_jobs):
    load_dotenv()
    env = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=env)
    prompt = f'''
    there is a list of skills: {skills}
    and there is a list of target jobs: {target_jobs}
    now give an output of a python list in which there will be 5 lists,(keep in mind that the skill choices should be semantic, for example if one knows pytorch, he definitely knows about machine learning, so dont suggest machine learning as a skill to learn in that case, keep this throughly in mind while suggesting skills to learn)
    1st list will contain boolean values of if he is [eligible(write 2 in string in the list) or close(write 1 in string in the list) or not eligible(write 0 in stringin the list)] for now in the same indexes of target jobs according to list of skills
    2nd list is the list of containing all the required skills needed to learn(at max 5-6) for the target jobs that are not in the skills list
    3rd list will be the list of one course corresponding to the 2nd list but just one course for each skill with same index of the skill in 2nd list.(just the links only, can be from youtube, udemy or coursera)
    4th list will be the list of bonus skills(4-5) which are not neccessary but good to know
    5th list will be the list of one course corresponding to the 4th list but just one course for each skill with same index of the skill in 4th list.
    give these 5 lists in a list(in the same order as I gave to you) and in output give nothing else except the list, so that I can just eval(output you gave) and get the list... remember give not an extra character not even a backtick, dont even write python code block, just the list only
    '''
    response = client.models.generate_content(
        model="gemma-3-12b-it", contents=prompt
    )
    return eval(response.text)