import cv2
import mediapipe as mp
import pyfirmata
import time
import threading

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Connect to Arduino using pyFirmata
board = pyfirmata.Arduino('COM5')
servo_pin = board.get_pin('d:9:s')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()

def unlock_door():
    servo_pin.write(0)
    print("Door Unlocked")

def lock_door():
    servo_pin.write(180)  
    print("Door Locked")

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv2.CAP_PROP_FPS, 15)

def process_frame():
    last_unlock_time = time.time()
    door_unlocked = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                current_time = time.time()
                if current_time - last_unlock_time > 2:
                    if not door_unlocked:
                        unlock_door()
                        door_unlocked = True
                        last_unlock_time = current_time
        else:
            if door_unlocked:
                lock_door()
                door_unlocked = False

        cv2.imshow('Hand Gesture Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    board.exit()

thread = threading.Thread(target=process_frame)
thread.start()