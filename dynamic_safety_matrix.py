"""
KineFit AI - Dynamic Algorithmic Engine
This module adjusts the safety thresholds based on the user's specific biological transitions.
"""

class GestationalMatrix:
    def __init__(self):
        # Baseline pelvic tilt thresholds for pregnant users based on week of pregnancy.
        self.safety_thresholds = {
            "week_12": {"max_pelvic_tilt_angle": 25.0, "lumbar_load_limit": "High"},
            "week_24": {"max_pelvic_tilt_angle": 15.0, "lumbar_load_limit": "Medium"},
            "week_36": {"max_pelvic_tilt_angle": 8.0,  "lumbar_load_limit": "Low"}
        }

    def evaluate_posture(self, current_week, detected_angle):
        """
        Cross-references the live detected angle with the allowed threshold for that specific week.
        """
        week_key = f"week_{current_week}"
        
        # Default fallback if week is not precisely in matrix
        if week_key not in self.safety_thresholds:
            return "✅ Matrix calibrating..."

        allowed_angle = self.safety_thresholds[week_key]["max_pelvic_tilt_angle"]
        
        if detected_angle > allowed_angle:
            return f"⚠️ Warning: Pelvic Overload. Limit is {allowed_angle}°. Shift Center of Gravity Backwards."
        else:
            return f"✅ Posture Optimal - Week {current_week} Safety Matrix Engaged."

if __name__ == "__main__":
    matrix = GestationalMatrix()
    # Simulating a user in Week 24 with a dangerous pelvic angle of 16 degrees
    alert = matrix.evaluate_posture(current_week=24, detected_angle=16.0)
    print(f"Live Alert Status: {alert}")
