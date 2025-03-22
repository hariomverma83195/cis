import torch
import torchvision.transforms as transforms
import cv2
import numpy as np

# Load the pretrained CodeFormer model
model = torch.load('codeformer.pth')  # Load the model using torch.load()

# Define image preprocessing
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def preprocess_image(image_path):
    # Read image and preprocess it
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    image = preprocess(image)
    return image

def postprocess_image(image):
    # Postprocess the deblurred image
    image = (image * 255).astype(np.uint8)  # Denormalize pixel values
    return image

def deblur_image(image_path):
    # Preprocess the input image
    preprocessed_image = preprocess_image(image_path)
    
    # Expand dimensions to match model input shape
    preprocessed_image = torch.unsqueeze(preprocessed_image, 0)
    
    # Deblur the image using the pretrained model
    with torch.no_grad():
        deblurred_image = model(preprocessed_image)
    
    # Postprocess the deblurred image
    deblurred_image = postprocess_image(deblurred_image[0].permute(1, 2, 0).cpu().numpy())
    
    return deblurred_image

# Example usage:
input_image_path = 'img_15_cropped.jpg'
output_image = deblur_image(input_image_path)
cv2.imwrite('deblurred_image.jpg', cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))  # Save deblurred image
