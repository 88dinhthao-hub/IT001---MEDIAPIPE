import cv2
import mediapipe as mp
import time
import math

MORSE_DICT = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
}

MORSE_LIST = list(MORSE_DICT.items())

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cv2.namedWindow("Morse Hand App", cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)

current_morse = ""
decoded_text = ""
TOUCH_THRESHOLD = 0.05

prev_touch = {"index": False, "middle": False, "ring": False, "pinky": False}
last_ring_touch_time = 0
pinky_touch_start_time = None
pinky_held_cleared = False


def calc_distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    current_time = time.time()

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark

            thumb_tip = lm[4]
            index_tip = lm[8]
            middle_tip = lm[12]
            ring_tip = lm[16]
            pinky_tip = lm[20]

            touch_index = calc_distance(thumb_tip, index_tip) < TOUCH_THRESHOLD
            touch_middle = calc_distance(thumb_tip, middle_tip) < TOUCH_THRESHOLD
            touch_ring = calc_distance(thumb_tip, ring_tip) < TOUCH_THRESHOLD
            touch_pinky = calc_distance(thumb_tip, pinky_tip) < TOUCH_THRESHOLD

            if touch_index and not prev_touch["index"]:
                current_morse += "."
            prev_touch["index"] = touch_index

            if touch_middle and not prev_touch["middle"]:
                current_morse += "-"
            prev_touch["middle"] = touch_middle

            if touch_ring and not prev_touch["ring"]:
                if current_time - last_ring_touch_time < 0.4:
                    decoded_text += " "
                    current_morse = ""
                else:
                    if current_morse:
                        char = MORSE_DICT.get(current_morse, "?")
                        decoded_text += char
                        current_morse = ""
                last_ring_touch_time = current_time
            prev_touch["ring"] = touch_ring

            if touch_pinky:
                if pinky_touch_start_time is None:
                    pinky_touch_start_time = current_time
                    pinky_held_cleared = False
                elif (
                    current_time - pinky_touch_start_time > 1.2
                ) and not pinky_held_cleared:
                    decoded_text = ""
                    current_morse = ""
                    pinky_held_cleared = True
            else:
                if pinky_touch_start_time is not None:
                    if not pinky_held_cleared:
                        if current_morse:
                            current_morse = current_morse[:-1]
                        elif decoded_text:
                            decoded_text = decoded_text[:-1]
                    pinky_touch_start_time = None
            prev_touch["pinky"] = touch_pinky

    overlay = frame.copy()

    fg_x, fg_y, fg_w, fg_h = 20, 20, 240, 160
    cv2.rectangle(overlay, (fg_x, fg_y), (fg_x + fg_w, fg_y + fg_h), (35, 35, 40), -1)

    chart_w, chart_h = 260, 325
    chart_x = w - chart_w - 20
    chart_y = 20
    cv2.rectangle(
        overlay, (chart_x, chart_y), (w - 20, chart_y + chart_h), (35, 35, 40), -1
    )

    bottom_y = h - 130
    cv2.rectangle(overlay, (20, bottom_y), (w - 20, h - 15), (35, 35, 40), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)
    y_offset = fg_y + 32
    fingers = [
        ("Index", "dot", (255, 255, 0)), 
        ("Middle", "dash", (255, 100, 150)),  
        ("Ring", "end . x2 space", (0, 200, 255)),  
        ("Pinky", "delete . hold clear", (100, 100, 255)), 
    ]
    for name, action, color in fingers:
        cv2.circle(frame, (fg_x + 20, y_offset - 4), 5, color, -1)
        cv2.putText(
            frame,
            name,
            (fg_x + 35, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
        )
        text_size = cv2.getTextSize(action, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)[0]
        cv2.putText(
            frame,
            action,
            (fg_x + fg_w - 15 - text_size[0], y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.42,
            (150, 150, 150),
            1,
        )
        y_offset += 32

    cv2.putText(
        frame,
        "MORSE CHART",
        (chart_x + 18, chart_y + 26),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 200, 100),
        1,
    )
    for i, (morse, char) in enumerate(MORSE_LIST):
        col = i // 12
        row = i % 12
        x = chart_x + 18 + col * 82
        y = chart_y + 52 + row * 22

        is_match = morse == current_morse
        color = (255, 200, 100) if is_match else (100, 100, 100)

        cv2.putText(frame, char, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        cv2.putText(
            frame,
            morse,
            (x + 15, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            color,
            2 if is_match else 1,
        )

    cv2.putText(
        frame,
        "CURRENT LETTER",
        (40, bottom_y + 26),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (150, 150, 150),
        1,
    )

    draw_x = 40
    for symbol in current_morse:
        if symbol == ".":
            cv2.circle(frame, (draw_x + 10, bottom_y + 50), 8, (255, 255, 0), -1)
            draw_x += 30
        elif symbol == "-":
            cv2.circle(frame, (draw_x + 8, bottom_y + 50), 8, (255, 100, 150), -1)
            cv2.rectangle(
                frame,
                (draw_x + 8, bottom_y + 42),
                (draw_x + 32, bottom_y + 58),
                (255, 100, 150),
                -1,
            )
            cv2.circle(frame, (draw_x + 32, bottom_y + 50), 8, (255, 100, 150), -1)
            draw_x += 50

    cv2.putText(
        frame,
        "MESSAGE",
        (40, bottom_y + 78),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (150, 150, 150),
        1,
    )
    cv2.putText(
        frame,
        decoded_text,
        (40, bottom_y + 103),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (255, 255, 255),
        2,
    )

    cv2.imshow("Morse Hand App", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
