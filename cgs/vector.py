# import psycopg2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import askLLM

# INPUT GOES TO THIS PROGRAM...

def skillAnalysis():
    # def get_connection():
    #     return psycopg2.connect(
    #         user="???",
    #         password="???",
    #         database="???",
    #         host="???"
    #     )

    # conn = get_connection()
    # cursor = conn.cursor()

    # FETCHED DATA
    # Assumed format?
    # userid, username, skills
    # and skills are in the string like uhh "python, pytorch, postgresql, tensorflow"

    # cursor.execute("SELECT skills FROM databaseName WHERE username=%s", (???, ))
    # skills = cursor.fetchone()
    # conn.close()

    #placeholder skills lists
    skillsUser = "python"
    skillsRequired = "python, java, pytorch, tensorflow"

    set_skillsUser = set([x.lower() for x in skillsUser.split(", ")])
    set_skillsReq = set([x.lower() for x in skillsRequired.split(", ")])

    gapSkills = set_skillsReq - set_skillsUser
    extraSkills = set_skillsUser - set_skillsReq

    if not gapSkills and not extraSkills:
        print("Match! (100%)")
    elif not gapSkills and extraSkills:
        print(f"Overqualified lmfao: {extraSkills}")
    else:
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        vectorUser = model.encode(skillsUser)
        vectorRequired = model.encode(skillsRequired)

        score = cosine_similarity([vectorUser], [vectorRequired])
        scorePct = score[0][0] * 100

        print(f"Skill gaps found: {str(gapSkills)} with a match score of {scorePct:.4f}")
    return askLLM.promptset(gapSkills, extraSkills, set_skillsUser, set_skillsReq)

skillAnalysis()