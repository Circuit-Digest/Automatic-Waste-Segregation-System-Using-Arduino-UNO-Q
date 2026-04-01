from arduino.app_utils import App, Bridge
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC
import time

ui = WebUI()

detection_stream = VideoObjectDetection(confidence=0.5, debounce_sec=0.5)  # increased debounce

ui.on_message("override_th", lambda sid, threshold: detection_stream.override_threshold(threshold))

classes = ["Paper", "Plastic", "Cardboard", "Battery"]

stable_counts    = {cls: 0 for cls in classes}
last_action_time = {cls: 0 for cls in classes}
in_progress      = {cls: False for cls in classes}   # prevent overlap

# Cooldowns in seconds
COOLDOWN_NORMAL  = 8.0   # Paper, Plastic, Cardboard
COOLDOWN_BATTERY = 10.0  # longer for Battery (no servo wait)

def send_detections_to_ui(detections: dict):
    global stable_counts, last_action_time, in_progress

    detected_this_frame = {cls: 0.0 for cls in classes}
    now = time.time()

    for key, values in detections.items():
        for value in values:
            entry = {
                "content": key,
                "confidence": value.get("confidence"),
                "timestamp": datetime.now(UTC).isoformat()
            }
            ui.send_message("detection", message=entry)

        if key in classes:
            max_conf = max(v.get("confidence", 0.0) for v in values)
            detected_this_frame[key] = max_conf

    CONF_THRESHOLD = 0.82
    BATTERY_THRESHOLD = 0.88   # stricter for Battery to reduce repeats
    STABLE_FRAMES = 2

    for cls in classes:
        conf = detected_this_frame[cls]
        cooldown = COOLDOWN_BATTERY if cls == "Battery" else COOLDOWN_NORMAL

        # Debug only when relevant
        if conf > 0.7:
            print(f"{cls} conf={conf:.3f} stable={stable_counts[cls]} cooldown_left={max(0, last_action_time[cls] + cooldown - now):.1f}s in_progress={in_progress[cls]}")

        if conf >= (BATTERY_THRESHOLD if cls == "Battery" else CONF_THRESHOLD):
            stable_counts[cls] += 1
        else:
            stable_counts[cls] = 0

        try:
            if stable_counts[cls] >= STABLE_FRAMES and not in_progress[cls] and now - last_action_time[cls] > cooldown:
                in_progress[cls] = True
                last_action_time[cls] = now

                if cls == "Paper" or cls == "Cardboard":
                    Bridge.call("set_servo", 0)
                    print(f"{cls} → servo to 0°")
                    time.sleep(5)
                    Bridge.call("set_servo", 90)
                    print(f"→ back to 90° ({cls})")
                elif cls == "Plastic":
                    Bridge.call("set_servo", 180)
                    print(f"Plastic → servo to 180°")
                    time.sleep(5)
                    Bridge.call("set_servo", 90)
                    print(f"→ back to 90° (Plastic)")
                elif cls == "Battery":
                    Bridge.call("buzz", 2000)
                    print("Battery → buzzer 2s")
                    time.sleep(5)  # wait same duration for consistency
                    print("Battery action finished")

                in_progress[cls] = False

        except Exception as e:
            print(f"Bridge failed for {cls}: {e}")
            in_progress[cls] = False  # reset on error

detection_stream.on_detect_all(send_detections_to_ui)

App.run()
