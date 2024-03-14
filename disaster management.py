import cv2

# Load the pre-trained HOG descriptor and SVM classifier
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Capture video from webcam (replace 0 with video file path if desired)
cap = cv2.VideoCapture(0)

# Initialize list for detected humans
detected_humans = []

while True:
    # Read a frame
    ret, frame = cap.read()

    # Convert frame to grayscale for better detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect humans in the frame
    (rects, weights) = hog.detectMultiScale(gray, winStride=(4, 4), padding=(8, 8))

    # Draw bounding boxes around detected humans
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # Check if the detected human is already in the list
        new_human = True
        for (x0, y0, w0, h0) in detected_humans:
            if abs(x - x0) < w0 and abs(y - y0) < h0:
                new_human = False
                break
        # If it's a new human, add it to the list and update the count
        if new_human:
            detected_humans.append((x, y, w, h))

    # Display the frame with bounding boxes and count of detected humans
    cv2.putText(frame, f'Humans Detected: {len(detected_humans)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Human Detection', frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture and destroy windows
cap.release()
cv2.destroyAllWindows()