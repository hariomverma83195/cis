from deepface import DeepFace
import asyncio

async def verify_gender():
    try:
        img_path = "./static/data/output.jpg"
        facial_features = DeepFace.analyze(img_path, actions=['gender'], enforce_detection=False)
    except Exception as e:
        print("Error:", e)
        facial_features = []
    if len(facial_features) > 0:
        genders = [face['gender'] for face in facial_features if 'gender' in face]
        
        if len(genders) > 1:
            return 2
        elif len(genders) == 1:
            man = int(genders[0]['Man'])
            woman = int(genders[0]['Woman'])
            print(man)
            print(woman)
            gender_i = 1 if woman>man else (3 if man==woman else 0)
            gender_v = woman if woman>man else (3 if man==woman else man)
            gender = 3 if gender_v < 60 else gender_i

            return gender
        else:
            return 3