from typing import List, Dict  # Import List and Dict for type hints
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import cv2
import numpy as np
from movenet import Movenet
from data import BodyPart, Point  # Import BodyPart and Point from data.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize MoveNet
movenet = Movenet('movenet_thunder.tflite')

# Define correct keypoints for each yoga pose (existing CORRECT_POSES dictionary)
CORRECT_POSES = {
    "Chair Pose": {
        BodyPart.NOSE: Point(0.3741, 0.4990),
        BodyPart.LEFT_EYE: Point(0.3602, 0.5083),
        BodyPart.RIGHT_EYE: Point(0.3597, 0.4900),
        BodyPart.LEFT_EAR: Point(0.3609, 0.5229),
        BodyPart.RIGHT_EAR: Point(0.3594, 0.4765),
        BodyPart.LEFT_SHOULDER: Point(0.4080, 0.5395),
        BodyPart.RIGHT_SHOULDER: Point(0.4090, 0.4555),
        BodyPart.LEFT_ELBOW: Point(0.3313, 0.5629),
        BodyPart.RIGHT_ELBOW: Point(0.3327, 0.4347),
        BodyPart.LEFT_WRIST: Point(0.2416, 0.5612),
        BodyPart.RIGHT_WRIST: Point(0.2422, 0.4364),
        BodyPart.LEFT_HIP: Point(0.6189, 0.5251),
        BodyPart.RIGHT_HIP: Point(0.6186, 0.4721),
        BodyPart.LEFT_KNEE: Point(0.7274, 0.5202),
        BodyPart.RIGHT_KNEE: Point(0.7276, 0.4799),
        BodyPart.LEFT_ANKLE: Point(0.8622, 0.5126),
        BodyPart.RIGHT_ANKLE: Point(0.8628, 0.4847),
    },
    "Cobra Pose": {
        BodyPart.NOSE: Point(0.499, 0.497),
        BodyPart.LEFT_EYE: Point(0.481, 0.509),
        BodyPart.RIGHT_EYE: Point(0.480, 0.485),
        BodyPart.LEFT_EAR: Point(0.473, 0.526),
        BodyPart.RIGHT_EAR: Point(0.472, 0.467),
        BodyPart.LEFT_SHOULDER: Point(0.520, 0.558),
        BodyPart.RIGHT_SHOULDER: Point(0.522, 0.438),
        BodyPart.LEFT_ELBOW: Point(0.574, 0.595),
        BodyPart.RIGHT_ELBOW: Point(0.580, 0.420),
        BodyPart.LEFT_WRIST: Point(0.640, 0.580),
        BodyPart.RIGHT_WRIST: Point(0.645, 0.405),
        BodyPart.LEFT_HIP: Point(0.700, 0.510),
        BodyPart.RIGHT_HIP: Point(0.705, 0.480),
        BodyPart.LEFT_KNEE: Point(0.750, 0.505),
        BodyPart.RIGHT_KNEE: Point(0.755, 0.470),
        BodyPart.LEFT_ANKLE: Point(0.800, 0.490),
        BodyPart.RIGHT_ANKLE: Point(0.805, 0.460),
    },
    "Tree Pose": {
        BodyPart.NOSE: Point(0.5, 0.3),
        BodyPart.LEFT_EYE: Point(0.48, 0.31),
        BodyPart.RIGHT_EYE: Point(0.47, 0.29),
        BodyPart.LEFT_EAR: Point(0.45, 0.32),
        BodyPart.RIGHT_EAR: Point(0.46, 0.27),
        BodyPart.LEFT_SHOULDER: Point(0.52, 0.35),
        BodyPart.RIGHT_SHOULDER: Point(0.53, 0.25),
        BodyPart.LEFT_ELBOW: Point(0.54, 0.38),
        BodyPart.RIGHT_ELBOW: Point(0.55, 0.22),
        BodyPart.LEFT_WRIST: Point(0.40, 0.60),
        BodyPart.RIGHT_WRIST: Point(0.41, 0.20),
        BodyPart.LEFT_HIP: Point(0.60, 0.60),
        BodyPart.RIGHT_HIP: Point(0.61, 0.20),
        BodyPart.LEFT_KNEE: Point(0.50, 0.75),
        BodyPart.RIGHT_KNEE: Point(0.50, 0.55),
        BodyPart.LEFT_ANKLE: Point(0.45, 0.90),
        BodyPart.RIGHT_ANKLE: Point(0.55, 0.90),
    },
    "Shoulder Stand": {
        BodyPart.NOSE: Point(0.5, 0.15),
        BodyPart.LEFT_EYE: Point(0.48, 0.16),
        BodyPart.RIGHT_EYE: Point(0.47, 0.14),
        BodyPart.LEFT_EAR: Point(0.45, 0.17),
        BodyPart.RIGHT_EAR: Point(0.46, 0.13),
        BodyPart.LEFT_SHOULDER: Point(0.55, 0.25),
        BodyPart.RIGHT_SHOULDER: Point(0.54, 0.20),
        BodyPart.LEFT_ELBOW: Point(0.58, 0.40),
        BodyPart.RIGHT_ELBOW: Point(0.57, 0.35),
        BodyPart.LEFT_WRIST: Point(0.60, 0.55),
        BodyPart.RIGHT_WRIST: Point(0.59, 0.50),
        BodyPart.LEFT_HIP: Point(0.55, 0.70),
        BodyPart.RIGHT_HIP: Point(0.56, 0.68),
        BodyPart.LEFT_KNEE: Point(0.53, 0.85),
        BodyPart.RIGHT_KNEE: Point(0.54, 0.83),
        BodyPart.LEFT_ANKLE: Point(0.50, 0.95),
        BodyPart.RIGHT_ANKLE: Point(0.51, 0.94),
    },
    "Triangle Pose": {
        BodyPart.NOSE: Point(0.45, 0.40),
        BodyPart.LEFT_EYE: Point(0.43, 0.42),
        BodyPart.RIGHT_EYE: Point(0.42, 0.38),
        BodyPart.LEFT_EAR: Point(0.41, 0.45),
        BodyPart.RIGHT_EAR: Point(0.40, 0.35),
        BodyPart.LEFT_SHOULDER: Point(0.50, 0.50),
        BodyPart.RIGHT_SHOULDER: Point(0.48, 0.38),
        BodyPart.LEFT_ELBOW: Point(0.55, 0.60),
        BodyPart.RIGHT_ELBOW: Point(0.52, 0.30),
        BodyPart.LEFT_WRIST: Point(0.65, 0.65),
        BodyPart.RIGHT_WRIST: Point(0.58, 0.20),
        BodyPart.LEFT_HIP: Point(0.50, 0.75),
        BodyPart.RIGHT_HIP: Point(0.48, 0.55),
        BodyPart.LEFT_KNEE: Point(0.45, 0.85),
        BodyPart.RIGHT_KNEE: Point(0.40, 0.65),
        BodyPart.LEFT_ANKLE: Point(0.38, 0.95),
        BodyPart.RIGHT_ANKLE: Point(0.30, 0.75),
    }
    
}

# Define critical body parts for each yoga pose (existing CRITICAL_BODY_PARTS dictionary)
CRITICAL_BODY_PARTS = {
    "Tree Pose": [BodyPart.LEFT_KNEE, BodyPart.RIGHT_KNEE, BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER],
    "Downward Dog": [BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP],
    "Chair Pose": [BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP, BodyPart.LEFT_KNEE, BodyPart.RIGHT_KNEE],
    "Cobra Pose": [BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER, BodyPart.LEFT_ELBOW, BodyPart.RIGHT_ELBOW],
    "Shoulder Stand": [BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP],
    "Triangle Pose": [BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP, BodyPart.LEFT_WRIST, BodyPart.RIGHT_WRIST],
    
}

# Define tolerance thresholds for feedback
POSITION_TOLERANCE = 0.1  # 10% deviation is allowed

def normalize_keypoints(keypoints: List, image_width: int, image_height: int) -> Dict[BodyPart, Point]:
    """
    Normalize keypoints from pixel coordinates to 0-1 range
    
    Args:
    keypoints (List): List of keypoint objects
    image_width (int): Width of the image
    image_height (int): Height of the image
    
    Returns:
    Dict: Normalized keypoints
    """
    normalized_keypoints = {}
    for kp in keypoints:
        normalized_x = kp.coordinate.x / image_width
        normalized_y = kp.coordinate.y / image_height
        normalized_keypoints[kp.body_part] = Point(normalized_x, normalized_y)
    
    return normalized_keypoints

def compare_pose(user_keypoints: Dict[BodyPart, Point], 
                 correct_pose: Dict[BodyPart, Point], 
                 critical_body_parts: List[BodyPart]) -> List[str]:
    """
    Compare the user's normalized keypoints with the correct pose and generate simple feedback.
    
    Args:
    user_keypoints (Dict): Normalized user keypoints
    correct_pose (Dict): Normalized correct pose keypoints
    critical_body_parts (List): List of critical body parts to compare
    
    Returns:
    List[str]: Simple, actionable feedback messages
    """
    feedback = []
    for body_part in critical_body_parts:
        if body_part in user_keypoints and body_part in correct_pose:
            user_point = user_keypoints[body_part]
            correct_point = correct_pose[body_part]

            # Calculate the difference between user and correct keypoints
            dx = user_point.x - correct_point.x
            dy = user_point.y - correct_point.y

            # Check if the deviation exceeds the tolerance
            if abs(dx) > POSITION_TOLERANCE or abs(dy) > POSITION_TOLERANCE:
                # Determine movement direction
                if abs(dx) > POSITION_TOLERANCE:
                    if dx > 0:
                        feedback.append(f"Shift your {body_part.name.lower()} slightly to the left")
                    else:
                        feedback.append(f"Shift your {body_part.name.lower()} slightly to the right")
                
                if abs(dy) > POSITION_TOLERANCE:
                    if dy > 0:
                        feedback.append(f"Lift your {body_part.name.lower()} up")
                    else:
                        feedback.append(f"Lower your {body_part.name.lower()} down")

    return feedback

@app.route('/detect-pose', methods=['POST'])
def detect_pose():
    print("Received request at /detect-pose")  # Debug log

    if 'image' not in request.files:
        print("No image received in the request")  # Debug log
        return jsonify({"error": "No image received"}), 400

    file = request.files['image']
    print("Image file received successfully")  # Debug log

    try:
        # Read and preprocess the image
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            print("Failed to decode image")  # Debug log
            return jsonify({"error": "Failed to decode image"}), 400

        input_size = 256
        resized_image = cv2.resize(image, (input_size, input_size))
        normalized_model_input = resized_image.astype(np.float32) / 255.0

        # Detect pose and get keypoints
        result = movenet.detect(normalized_model_input)
        person = result["person"]

        # Print original user detected keypoints
        print("\n--- Original User Detected Keypoints (Pixel Coordinates) ---")
        for kp in person.keypoints:
            print(f"{kp.body_part.name}: x = {kp.coordinate.x:.4f}, y = {kp.coordinate.y:.4f}")

        # Normalize user keypoints
        normalized_user_keypoints = normalize_keypoints(person.keypoints, input_size, input_size)

        # Print normalized user keypoints
        print("\n--- Normalized User Keypoints (0-1 Range) ---")
        for body_part, point in normalized_user_keypoints.items():
            print(f"{body_part.name}: x = {point.x:.4f}, y = {point.y:.4f}")
            
        
        pose = request.form.get('pose', 'Tree Pose')

        # Generate feedback based on the Tree Pose
        feedback = compare_pose(
        normalized_user_keypoints, 
        CORRECT_POSES[pose],  # Use the selected pose
        CRITICAL_BODY_PARTS[pose]  # Use critical body parts for the selected pose
    )

        # Print feedback
        print("\n--- Real-time Feedback ---")
        for fb in feedback:
            print(fb)

        # Return the response
        response = {
            "pose": pose,
            "original_keypoints": [
                {"body_part": kp.body_part.name, "x": kp.coordinate.x, "y": kp.coordinate.y} 
                for kp in person.keypoints
            ],
            "normalized_keypoints": [
                {"body_part": body_part.name, "x": point.x, "y": point.y} 
                for body_part, point in normalized_user_keypoints.items()
            ],
            "feedback": feedback
        }
        return jsonify(response)

    except Exception as e:
        print("Error processing image:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)