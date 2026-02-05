# import psycopg2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import askLLM

# INPUT GOES TO THIS PROGRAM...

def skillAnalysis():
    print("MARGADARSHAKA WORKING (PROTOTYPE):")
    # Skills lists
    skillsUser = input("Please enter what skills you are proficient in:\n")
    jobDesc = input("\nPlease enter the job description/target role that you desire:\n")

    promptSkillsJobDesc = f"""
        STRICTLY OUTPUT IN FORM OF COMMA SEPARATED KEYWORDS AND NOTHING MORE. 
        IDENTIFY 5 (TRY TO KEEP MINIMUM AS POSSIBLE, max 10) SKILLS/TOOLS REQUIRED FOR '{jobDesc}' AND MAINTAIN SKILLS/TOOLS 
        FOR SINGLE PROGRAMMING LANGUAGE ONLY, OUT OF WHAT {skillsUser} SKILLS THE USER has completed. 
        IF user has completed minimum all skills then just output same skills as whatever user has completed.
    """

    # Fetch required skills as per job desc.
    model = "gemma-3-12b-it"
    skillsRequired = askLLM.llm(model, promptSkillsJobDesc)

    set_skillsUser = set([x.lower() for x in skillsUser.split(", ")])
    set_skillsReq = set([x.lower() for x in skillsRequired.split(", ")])
    print(set_skillsReq)

    gapSkills = set_skillsReq - set_skillsUser
    extraSkills = set_skillsUser - set_skillsReq

    model = SentenceTransformer('sentence-transformers/all-miniLM-L6-V2')
    vectorUser = model.encode(skillsUser)
    vectorRequired = model.encode(skillsRequired)

    # Semantic Similarity Check
    score = cosine_similarity([vectorUser], [vectorRequired])
    scorePct = score[0][0] * 100

    if not gapSkills and not extraSkills:
        print("Match! (100%)")
    elif not gapSkills and extraSkills:
        print(f"Extra skills: {extraSkills}")
    else:
        print(f"Skill gaps found: {gapSkills} with a match score of {scorePct:.4f}%")
    print()
    # Output
    return askLLM.promptset(gapSkills, extraSkills, jobDesc, set_skillsUser, set_skillsReq)

skillAnalysis()
