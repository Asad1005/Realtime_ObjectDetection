import cv2
import numpy as np
import os

folder_path="C://Users//HP-PC//OneDrive//Desktop//detected object"

# Load YOLOv3 model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Define classes for YOLOv3 model
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Generate random colors for each class
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Load webcam
cap = cv2.VideoCapture(0)

# Set the resolution of the webcam
cap.set(3, 640)
cap.set(4, 480)

# Loop through webcam frames
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to a blob
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)

    # Set the input to the YOLOv3 model
    net.setInput(blob)

    # Perform object detection on the frame
    outs = net.forward(net.getUnconnectedOutLayersNames())

    # Initialize lists for detected objects
    class_ids = []
    confidences = []
    boxes = []

    # Loop through each detected object
    for out in outs:
        for detection in out:
            # Get class ID and confidence score
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter out weak detections
            if confidence > 0.5:
                # Get center, width, and height of the object
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])

                # Calculate top-left corner of the object
                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                # Add object information to lists
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, width, height])

    # Apply non-maximum suppression to remove overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw boxes around detected objects and save their pictures
    for i in indices:
        i = indices[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        # Draw box around object
        color = colors[class_ids[i]]
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Save object picture
        object_img = frame[y:y + h, x:x + w]
        filename = f'{classes[class_ids[i]]}.jpg'
        filepath = os.path.join(folder_path, filename)
        cv2.imwrite(filepath, object_img)

    # Display the resulting frame
    cv2.imshow("Frame", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
