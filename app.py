from flask import Flask, render_template, request, send_from_directory, jsonify, send_file
from PIL import Image, ImageEnhance
import cv2
import numpy as np
import base64
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/mine/bhaiya/uploads/'

# Load the pre-trained face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize the camera
# cap = cv2.VideoCapture(0)

# Global variable to store the captured image
captured_image = None

captured_byte_image = None

# Route to serve static files (like CSS and JS)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('templates', path)

@app.route('/')
def index():
    return render_template('indexJs.html')

@app.route('/upload_image', methods=['POST'])
def upload_image():
    global captured_image
    global captured_byte_image
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'})

    image_data = image_file.read()
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # sharpened_image = getClacheImage(gray_image)
    faces = face_cascade.detectMultiScale(gray_image, 1.4, 3)

    cropped_images = []

    for (x, y, w, h) in faces:
        cropped_image = image[y-95:y+h+95, x-75:x+w+75]
        image_width=360
        image_height=440

        if not cropped_image.size == 0:
            enhanced_image = add_black_border(cropped_image, top=5, bottom=5, left=5, right=5)
            cropped_images.append(getEnhancedImage(enhanced_image, image_width, image_height))
            captured_byte_image = cropped_image

    if cropped_images:
        # Save the captured image in-memory
        show_image = Image.new('RGB', (image_width+100, image_height+100), color='white')
        # sharpened_image = getClacheImage(cropped_images[0])
        # show_image.paste(sharpened_image)
        show_image.paste(cropped_images[0])
        img_bytes = io.BytesIO()
        show_image.save(img_bytes, format='JPEG')
        captured_image = base64.b64encode(img_bytes.getvalue()).decode('utf-8')


    if captured_image :
        image_base64 = captured_image
    else :
        image_base64 = base64.b64encode(image_data).decode('utf-8')

    # cv2.destroyAllWindows()
    
    # You can now process or save the image data as needed
    # For example, you can save it to a file or a database

    return jsonify({'message': 'Image uploaded successfully', 'image_base64': image_base64})

# def getClacheImage(image):
#     # Check if the image is already in grayscale
#     if len(image.shape) == 2:
#         gray_image = image
#     else:
#         # Convert the image to grayscale
#         gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Apply histogram equalization
#     equalized_image = cv2.equalizeHist(gray_image)

#     # Apply CLAHE
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     clahe_image = clahe.apply(equalized_image)

#     # Apply sharpening
#     sharpened_image = cv2.detailEnhance(cv2.cvtColor(clahe_image, cv2.COLOR_BGR2GRAY), sigma_s=10, sigma_r=0.15)

#     # Convert the image back to RGB
#     return cv2.cvtColor(sharpened_image, cv2.COLOR_GRAY2RGB)

# def gen_frames():
#     while True:
#         ret, frame = cap.read()

#         if ret:
#             #flip horizontal
#             frame = cv2.flip(frame, 1)

#             # Convert the frame to grayscale for face and eye detection
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#             # Detect faces in the frame
#             faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#             for (x, y, w, h) in faces:
#                 # Draw a rectangle around the face
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# def getEnhancedImage(cropped_image, image_width, image_height):
#     resized_image_pil = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)).resize((image_width, image_height), resample=Image.LANCZOS)
#     enh = ImageEnhance.Brightness(resized_image_pil)
#     enhanced_image = enh.enhance(1.3)

#     # enh = ImageEnhance.Sharpness(resized_image_pil)
#     # enhanced_image = enh.enhance(1.2)


#     return enhanced_image

def getEnhancedImage(cropped_image, image_width, image_height):
    # Convert the image to RGB mode
    cropped_image_rgb = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB)
    # Resize the image using Lanczos resampling
    resized_image_pil = Image.fromarray(cropped_image_rgb).resize((image_width, image_height), resample=Image.LANCZOS)
    # Enhance the brightness of the resized image
    enh = ImageEnhance.Brightness(resized_image_pil)
    enhanced_image = enh.enhance(1.3)
    # Enhance the sharpness of the resized image
    enh = ImageEnhance.Sharpness(enhanced_image)
    enhanced_image = enh.enhance(1.3)
    # Convert the enhanced image back to NumPy array
    # enhanced_image_np = np.array(enhanced_image)
    return enhanced_image

# @app.route('/capture_photo', methods=['POST'])
# def capture_photo():
#     global captured_image
#     global captured_byte_image
#     ret, frame = cap.read()
#     #flip horizontal to not show mirror image
#     frame = cv2.flip(frame, 1)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#     cropped_images = []

#     for (x, y, w, h) in faces:
#         cropped_image = frame[y-95:y+h+95, x-75:x+w+75]
#         image_height = 400
#         image_width = 328

#         if not cropped_image.size == 0:
#             cropped_images.append(getEnhancedImage(cropped_image, image_width, image_height))
#             captured_byte_image = cropped_image

#     if cropped_images:
#         # Save the captured image in-memory
#         show_image = Image.new('RGB', (image_height + 100, image_width + 100), color='white')
#         show_image.paste(cropped_images[0])
#         img_bytes = io.BytesIO()
#         show_image.save(img_bytes, format='JPEG')
#         captured_image = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

#     return 'OK'

# @app.route('/get_captured_image')
# def get_captured_image():
#     global captured_image
#     if captured_image:
#         return captured_image
#     else:
#         return ''

def add_black_border(image, top, bottom, left, right):
    # Define the border color (black color)
    border_color = [0, 0, 0]

    # Add black border to the image
    bordered_image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)

    return bordered_image


@app.route('/save_image', methods=['POST'])
def save_image():
    global captured_byte_image
    data = request.get_json()
    if not captured_byte_image.size == 0:
        enhanceAndSaveImage(data, captured_byte_image)
        return 'Image saved successfully!'
    else:
        return 'No image to save.'

@app.route('/save_cropped_image', methods=['POST'])
def save_cropped_image():
    data = request.get_json()
    img_src = data['imgSrc']
    # Decode the base64 image
    img_data = base64.b64decode(img_src.split(',')[1])
    np_img = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    if not img.size == 0:
        enhanceAndSaveImage(data, img)
        return 'Image saved successfully!'
    else:
        return 'No image to save.'

def enhanceAndSaveImage(data, img):
    image_width=380
    image_height=435
    enhanced_image = add_black_border(img, top=5, bottom=5, left=5, right=5)
    enhanced_image = getEnhancedImage(enhanced_image, image_width, image_height)
    a4_canvas = Image.new('RGB', (2480, 3509), color='white')
    start_x = 28
    start_y = 28
    spacing = 28

    numberOfImages = data.get('numberOfImages')

    for i in range(int(numberOfImages)):
        row = i // 6 #6 is number of images in a row
        col = i % 6  #6 is number of images in a col
        x_offset = start_x + col * (image_width + spacing)
        y_offset = start_y + row * (image_height + spacing)
        a4_canvas.paste(enhanced_image, (x_offset, y_offset))
    
    img_bytes = io.BytesIO()
    a4_canvas.save(img_bytes, format='JPEG', quality=100)
    captured_image2 = img_bytes.getvalue()

    # # Save the captured image to the local uploads folder
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.jpg')

    with open(image_path, 'wb') as f:
        f.write(captured_image2)
    # send_file(captured_image2, mimetype='image/jpeg', as_attachment=True, download_name='captured_image.jpg')

if __name__ == '__main__':
    upload_folder = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    app.run(debug=True)