"""
KineFit AI - Edge Computer Vision Pipeline
Core Pose Estimation & Adaptive Biomechanical Feedback
"""

import cv2
import mediapipe as mp
import numpy as np

def calculate_angle(a, b, c):
    """Calculates the angle between three joints (e.g., Hip, Knee, Ankle)."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

def process_frame(frame, pose_model, profile_type="pregnancy_week_24"):
    """
    Processes a single video frame, extracts 17-point skeletal data,
    and applies the specific dynamic safety matrix based on user profile.
    """
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose_model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    stage = "ANALYZING..."
    color = (255, 255, 255)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        
        # Extract Key Joints
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        # Calculate Biomechanical Angle
        knee_angle = calculate_angle(hip, knee, ankle)

        # Dynamic Safety Engine Logic (Adaptive Thresholds)
        if profile_type == "standard_rehab":
            # Logic for standard users (e.g., deeper squats allowed)
            if knee_angle > 160:
                stage, color = "STANDING", (0, 255, 0)
            elif knee_angle < 90:
                stage, color = "WARNING: JOINT OVERLOAD", (0, 0, 255)
            else:
                stage, color = "OPTIMAL FORM", (0, 255, 0)
                
        elif profile_type == "pregnancy_week_24":
            # Restricted Range of Motion for Prenatal Safety
            if knee_angle > 160:
                stage, color = "STANDING", (0, 255, 0)
            elif knee_angle < 115: # Critical difference: Limits depth for pelvic floor safety
                stage, color = "WARNING: UNSAFE DEPTH FOR PREGNANCY", (0, 0, 255)
            else:
                stage, color = "SAFE MODIFIED SQUAT", (0, 255, 0)

        # Draw UI Overlay
        cv2.rectangle(image, (0, 0), (850, 120), (0, 0, 0), -1)
        cv2.putText(image, f"PROFILE: {profile_type.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        cv2.putText(image, f"ACTION: {stage}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        cv2.putText(image, f"KNEE ANGLE: {int(knee_angle)} DEG", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Render Skeleton Mesh
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
    return image

if __name__ == "__main__":
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    # Example execution (Assuming standard webcam or video input)
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.65, min_tracking_confidence=0.65) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            # Simulate processing a pregnant user in Week 24
            output_frame = process_frame(frame, pose, profile_type="pregnancy_week_24")
            
            cv2.imshow('KineFit AI - Edge Processing', output_frame)
            if cv2.waitKey(10) & 0xFF == ord('q'): break
            
    cap.release()
    cv2.destroyAllWindows()
