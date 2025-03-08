from typing import List  # Import List for type hints
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

# Define correct keypoints for each yoga pose
CORRECT_POSES = {
    "Tree Pose": {
        BodyPart.LEFT_SHOULDER: Point(0.2, 0.3),
        BodyPart.RIGHT_SHOULDER: Point(0.8, 0.3),
        BodyPart.LEFT_HIP: Point(0.3, 0.6),
        BodyPart.RIGHT_HIP: Point(0.7, 0.6),
        BodyPart.LEFT_KNEE: Point(0.3, 0.8),
        BodyPart.RIGHT_KNEE: Point(0.7, 0.8),
        BodyPart.LEFT_ANKLE: Point(0.3, 0.95),
        BodyPart.RIGHT_ANKLE: Point(0.7, 0.95),
    },
    "Downward Dog": {
        BodyPart.LEFT_SHOULDER: Point(0.1, 0.2),
        BodyPart.RIGHT_SHOULDER: Point(0.9, 0.2),
        BodyPart.LEFT_HIP: Point(0.2, 0.5),
        BodyPart.RIGHT_HIP: Point(0.8, 0.5),
        BodyPart.LEFT_KNEE: Point(0.2, 0.7),
        BodyPart.RIGHT_KNEE: Point(0.8, 0.7),
        BodyPart.LEFT_ANKLE: Point(0.2, 0.9),
        BodyPart.RIGHT_ANKLE: Point(0.8, 0.9),
    }
}

# Define critical body parts for each yoga pose
CRITICAL_BODY_PARTS = {
    "Tree Pose": [BodyPart.LEFT_KNEE, BodyPart.RIGHT_KNEE, BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER],
    "Downward Dog": [BodyPart.LEFT_SHOULDER, BodyPart.RIGHT_SHOULDER, BodyPart.LEFT_HIP, BodyPart.RIGHT_HIP],
}

# Define tolerance thresholds for feedback
POSITION_TOLERANCE = 0.1  # 10% deviation is allowed

def compare_pose(user_keypoints, correct_pose, critical_body_parts) -> List[str]:
    """
    Compare the user's keypoints with the correct pose and generate feedback.
    Focus only on critical body parts.
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
                if dx > 0:
                    x_direction = "left"
                else:
                    x_direction = "right"

                if dy > 0:
                    y_direction = "down"
                else:
                    y_direction = "up"

                # Normalize feedback to percentage
                x_deviation_percent = abs(dx) * 100
                y_deviation_percent = abs(dy) * 100

                # Generate feedback based on deviations
                if x_direction and y_direction:
                    feedback.append(
                        f"Move your {body_part.name.lower()} {x_direction} by {x_deviation_percent:.0f}% and {y_direction} by {y_deviation_percent:.0f}%."
                    )
                elif x_direction:
                    feedback.append(
                        f"Move your {body_part.name.lower()} {x_direction} by {x_deviation_percent:.0f}%."
                    )
                elif y_direction:
                    feedback.append(
                        f"Move your {body_part.name.lower()} {y_direction} by {y_deviation_percent:.0f}%."
                    )
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
        normalized_image = resized_image.astype(np.float32) / 255.0

        # Detect pose and get keypoints
        result = movenet.detect(normalized_image)
        person = result["person"]

        # Convert keypoints to a dictionary for easier access
        user_keypoints = {kp.body_part: kp.coordinate for kp in person.keypoints}

        # Generate feedback based on the correct pose and critical body parts
        feedback = compare_pose(user_keypoints, CORRECT_POSES["Tree Pose"], CRITICAL_BODY_PARTS["Tree Pose"])

        # Print feedback in the console
        print("Real-time Feedback:")
        for fb in feedback:
            print(fb)

        # Return the response
        response = {
            "keypoints": [{"x": kp.coordinate.x, "y": kp.coordinate.y} for kp in person.keypoints],
            "feedback": feedback
        }
        return jsonify(response)

    except Exception as e:
        print("Error processing image:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)