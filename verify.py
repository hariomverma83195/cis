from deepface import DeepFace
import asyncio
import os

async def verify(img_path):
    print("Entering")
    models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"] #face verification
    # verification = DeepFace.verify("./inputs/whole_imgs/input.jpg", "./results/res/input.jpg", model_name = models[1], enforce_detection=False)
    # print(verification)
    image_directory = "./static/uploads"
    filename = ""
    for filename in os.listdir(image_directory):
    # Construct the absolute path to the image
        print(filename)
        image_path = os.path.join(image_directory, filename)
        
        # Verify the image with the target image
        result = DeepFace.verify(img_path, image_path, model_name=models[0], enforce_detection=False)

        # Check if the faces match
        if result["verified"]:
            print(f"Match found with image: {filename}")
            return filename
        else:
            print("No match found in the directory.")
    
    return "nomatch"

