# YOLO Human Tracking 🎯

**Completed:** March 28, 2026

YOLO Human Tracking is a Python computer vision application that detects and tracks a person in real time using a webcam and the pretrained **YOLOv8n** object detection model.

The program automatically selects a target, attempts to maintain tracking between detections, and calculates directional guidance based on the person's position relative to the center of the camera frame.

I developed this project to explore object detection, real-time tracking, target selection algorithms, coordinate calculations, and computer vision applications that could later be integrated with physical hardware.

## Features

- **Real-time person detection:** Detect people from a live webcam using YOLOv8n.
- **Automatic target selection:** Select the person closest to the center of the camera frame.
- **Position-based tracking:** Follow the selected person across subsequent detections.
- **Target loss handling:** Temporarily remember the previous target when a matching detection is unavailable.
- **Bounding-box persistence:** Intentionally keep the last detected rectangle visible between detection cycles and during brief detection interruptions.
- **Directional guidance:** Calculate LEFT, RIGHT, UP, DOWN, or CENTER corrections based on the target's position.
- **Bounding-box visualization:** Draw a green rectangle around the selected person.
- **Target center visualization:** Mark the center of the target with a red dot.
- **Frame-processing optimization:** Run YOLO detection every fifth frame instead of every frame.
- **Coordinate scaling:** Convert coordinates from the smaller processing image to the original webcam resolution.
- **Modular architecture:** Separate detection, tracking, direction calculations, and visualization into individual Python modules.

## Requirements

- Python 3
- A working webcam
- Ultralytics YOLO
- OpenCV
- NumPy
- Pretrained YOLOv8n model weights

Install the required Python libraries:

```bash
python -m pip install ultralytics opencv-python numpy
```

Ultralytics uses PyTorch for model inference, which is normally installed as a dependency.

## Installation

1. Download or clone this repository.
2. Install the required Python libraries.
3. Create a folder named `modules` inside the project's root directory.
4. Download the official pretrained YOLOv8n model (`yolov8n.pt`).
5. Place the model inside the `modules` folder.
6. Open a terminal in the project's root directory.
7. Run:

   ```bash
   python Camera_run.py
   ```

### Pretrained YOLO Model

**The `modules/` folder and its contents are not included in this repository.**

The application uses a pretrained YOLOv8n model developed by Ultralytics.

Before running the program, create the following directory locally:

```text
modules/
└── yolov8n.pt
```

You can obtain the model from the official Ultralytics resources:

- [YOLOv8 Documentation](https://docs.ultralytics.com/models/yolov8/)
- [Ultralytics GitHub](https://github.com/ultralytics/ultralytics)
- [Ultralytics Model Assets](https://github.com/ultralytics/assets/releases)

Download the pretrained `yolov8n.pt` weights and place them in your newly created `modules/` folder.

The original source code loads the model using:

```python
from ultralytics import YOLO

net = YOLO("modules/yolov8n.pt")
```

Therefore, the model must exist at that relative path.

Run the application from the project's root directory so Python can locate the model correctly.

## How to Use

### 1. Start the Program

Run:

```bash
python Camera_run.py
```

The application opens the default webcam using:

```python
cap = cv2.VideoCapture(0)
```

If the camera is available, the program displays a live video window.

### 2. Detect People

The application analyzes webcam frames using the YOLOv8n object detection model.

It filters detections using:

```python
if clas == 0 and conf > confidence_threshold:
```

Class `0` represents the `person` category in the pretrained COCO object detection model.

The default confidence threshold is:

```python
confidence_threshold = 0.5
```

Only person detections with confidence greater than 50% are considered.

### 3. Automatic Target Selection

If no target has been selected, the program searches through detected people and calculates their distances from the center of the camera frame.

The person closest to the center becomes the selected target.

### 4. Target Tracking

Once a target has been selected, the program attempts to follow the same person by comparing newly detected positions with the previously stored target position.

If no acceptable matching detection is found, the program temporarily preserves the previous target information instead of immediately selecting someone else.

### 5. Bounding-Box Persistence

The program intentionally preserves the last detected bounding box between detection cycles.

Since YOLO does not process every frame, this feature allows the rectangle to remain visible during frames when no new detection calculation takes place.

It also allows the previously detected rectangle to remain visible briefly when the person is temporarily lost.

The main application uses:

```python
if last_faces and frames_without_face < 30:
    draw_rectangle(last_faces, frame, cx, cy)
```

This feature makes the visual output more continuous, rather than immediately removing the rectangle whenever a new detection is unavailable.

**Note:** The stored rectangle uses the previous position and does not predict where the person moved during the missing frames.

### 6. Directional Guidance

The program calculates the position of the selected person relative to a central target area.

It prints horizontal and vertical directional corrections in the terminal.

Possible outputs include:

```text
LEFT
RIGHT
UP
DOWN
CENTER
```

These values are calculated independently for the horizontal and vertical axes.

The current application prints this information but does not control physical motors.

### 7. Exit the Program

Press `Q` to close the application.

The program releases the webcam and closes the OpenCV window.

## How It Works

The application consists of five main Python files, each responsible for a different part of the processing pipeline.

### 1. Camera_run.py — Main Application

Controls webcam capture and the main processing loop.

Its responsibilities include:

- Opening the default webcam.
- Reading video frames.
- Obtaining the original frame dimensions.
- Calling the detection algorithm every fifth frame.
- Maintaining previously detected bounding boxes.
- Drawing tracking information.
- Displaying the live video feed.
- Handling keyboard input.

The detection interval is controlled by:

```python
if number_of_frames % 5 == 0:
```

This means the complete detection algorithm executes once every five video frames.

The program continues displaying the video between detection cycles.

### 2. YOLO/YOLO_human.py — Detection and Tracking

This module contains the main target-selection and position-based tracking algorithm.

It uses the Ultralytics YOLO library:

```python
from ultralytics import YOLO
```

The pretrained model is loaded using:

```python
net = YOLO("modules/yolov8n.pt")
```

The model detects objects in the input image and returns results containing:

- Object class IDs.
- Confidence scores.
- Bounding-box coordinates.

The program filters these results to process only person detections.

#### Initial Target Selection

When no target exists, the program calculates the center of every detected person:

```python
cx = (x1 + x2) // 2
cy = (y1 + y2) // 2
```

It then calculates the distance between the person's center and the center of the frame.

```python
dx = cx - center_x
dy = cy - center_y

distance = dx*dx + dy*dy
```

The person with the smallest calculated distance becomes the selected target.

This is the **squared Euclidean distance**, allowing distances to be compared without calculating square roots.

#### Target Data

The program stores the selected target using a Python dictionary:

```python
target = {
    "x1": x1,
    "y1": y1,
    "x2": x2,
    "y2": y2,
    "cx": cx,
    "cy": cy,
    "lost_frames": 0
}
```

This dictionary contains:

- Bounding-box coordinates.
- Center coordinates.
- A counter for unsuccessful tracking updates.

#### Tracking the Selected Person

When a target already exists, the program compares the center of each new person detection with the previously stored center.

```python
dx = cx - old_cx
dy = cy - old_cy

score = dx*dx + dy*dy
```

The new detection is considered a possible match if:

```python
if score < 10000:
```

This corresponds to a displacement of less than 100 pixels between the old and new target centers in the resized 300 × 300 image.

If multiple detections satisfy the condition, the one with the smallest distance is selected.

The target dictionary is then updated with the new coordinates.

#### Handling a Lost Target

If no acceptable matching detection is found, the program increases the `lost_frames` counter.

```python
old_target["lost_frames"] += 1
```

The target is preserved temporarily.

Once five unsuccessful detection updates occur:

```python
if old_target["lost_frames"] >= 5:
    return None
```

The target is discarded.

The system can then select a new target during a later detection.

This behavior reduces immediate target switching when a person is briefly missed by the detection model.

### 3. face_detaction/face_recognision.py — Coordinate Processing

Despite its filename, this module handles **person detections and coordinate processing**, not facial identity recognition.

Before passing the frame to YOLO, the image is resized:

```python
small_frame = cv2.resize(frame, (300, 300))
```

Using a smaller processing frame reduces the amount of image data analyzed by the model.

The tracking algorithm returns bounding-box coordinates based on this smaller image.

To display the rectangle correctly on the original video, the program calculates scaling factors:

```python
x_scale = org_width / 300
y_scale = org_height / 300
```

These factors are applied to the detected coordinates.

```python
top = int(top * y_scale)
right = int(right * x_scale)
bottom = int(bottom * y_scale)
left = int(left * x_scale)
```

The center coordinates are also scaled.

The module then:

1. Stores the converted coordinates.
2. Calculates directional guidance.
3. Draws tracking information.
4. Returns the processed frame and updated target.

### 4. orientation/routing.py — Directional Guidance

This module calculates the selected person's position relative to the center of the camera frame.

The program defines a central target area:

```python
rect_width = w // 6
rect_height = h // 6
```

This creates a central region with a width equal to one-sixth of the frame width and a height equal to one-sixth of the frame height.

The person's center is then compared against the boundaries of this region.

#### Horizontal Direction

| Target position | Printed correction |
|---|---|
| Left of central area | RIGHT |
| Right of central area | LEFT |
| Inside central area | CENTER |

#### Vertical Direction

| Target position | Printed correction |
|---|---|
| Above central area | DOWN |
| Below central area | UP |
| Inside central area | CENTER |

These values express directions for bringing the target's position toward the center of the displayed frame.

They are currently printed in the terminal and are not transmitted to hardware.

### 5. cv2_draw/cv2_ractangle.py — Visual Output

This module draws the tracking information on the webcam image.

It uses OpenCV to draw a green rectangle around the selected person:

```python
cv2.rectangle(
    frame,
    (left1, top1),
    (right1, bottom1),
    (0, 255, 0),
    2
)
```

When center coordinates are available, the program also draws a red point:

```python
cv2.circle(
    frame,
    (center_x, center_y),
    5,
    (0, 0, 255),
    -1
)
```

The module also supports the program's bounding-box persistence feature by drawing previously stored coordinates.

## Project Structure

The public GitHub repository contains the following files:

```text
YOLO-Human-Tracking/
├── Camera_run.py
├── YOLO/
│   └── YOLO_human.py
├── face_detaction/
│   └── face_recognision.py
├── orientation/
│   └── routing.py
├── cv2_draw/
│   └── cv2_ractangle.py
├── .gitignore
└── README.md
```

The pretrained model must be downloaded separately, as described in the Installation section.

Generated Python `__pycache__/` folders and `.pyc` files are excluded from the repository.

## Known Limitations

- **Person detection only:** The program detects people but does not identify specific individuals.
- **Position-based tracking:** The tracking algorithm compares coordinates rather than using appearance-based re-identification. It may switch targets when people cross paths or move close together.
- **Fixed confidence threshold:** The default detection confidence is `0.5`.
- **Fixed tracking distance:** Possible target matches must satisfy a predefined distance threshold.
- **Intermittent detection:** YOLO processes every fifth frame rather than every frame.
- **Last-known-position display:** The intentional bounding-box persistence feature displays the previously detected position between detection updates. As a result, rectangles may briefly lag behind a moving person.
- **Single target:** The program selects and tracks one person at a time.
- **Repeated drawing:** A rectangle can be drawn twice during certain detection frames.
- **No appearance-based identification:** The system does not generate person identity embeddings.
- **No motor control:** Directional values are displayed in the terminal rather than sent to physical hardware.
- **Default webcam:** The program uses camera index `0`.
- **Limited error handling:** Missing model files, unavailable webcams, or unexpected runtime errors can interrupt execution.
- **No graphical settings:** Detection intervals, tracking thresholds, and other parameters must be changed in the source code.

## Development Note

I developed this project to explore real-time object detection and tracking using Python and a pretrained neural network.

The project allowed me to experiment with target selection, coordinate calculations, positional tracking, lost-target handling, frame-processing optimization, and directional guidance.

One of the implemented features is **bounding-box persistence**, which deliberately keeps the most recently detected rectangle visible between detection cycles and during brief interruptions in detection.

The project also explores how computer vision software can produce directional information that might later be used by a physical tracking system.

The YOLOv8n object detection model was developed and pretrained by Ultralytics. My work focuses on integrating the model into a webcam application and implementing the tracking, target-selection, coordinate transformation, persistence, and directional calculation logic.

This project is an experimental software-based human-tracking system. It does not include motor control or a completed physical robotic implementation.

## Third-Party Software and Model

This project uses **Ultralytics YOLOv8n** for object detection.

Official resources:

- [Ultralytics GitHub](https://github.com/ultralytics/ultralytics)
- [Ultralytics YOLOv8 Documentation](https://docs.ultralytics.com/models/yolov8/)
- [Ultralytics Licensing](https://www.ultralytics.com/license)

Ultralytics offers AGPL-3.0 and Enterprise licensing options. Users should review the applicable licensing conditions before redistribution or deployment.


**Author:** [Nik Berginc](https://github.com/nikberginc)
