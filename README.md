# Face Anonymizer Application

This is a face anonymization application built using **OpenCV** and **Tkinter**. The application allows you to detect faces in real-time using a webcam and apply various anonymization techniques such as blurring, pixelation, or replacing the face with a custom icon.

## Features

- **Face Detection**: Detects faces in real-time using the Haar Cascade model.
- **Anonymization Methods**:
  - **Blur Faces**: Apply Gaussian blur to detected faces.
  - **Pixelate Faces**: Apply pixelation to detected faces.
  - **Replace Faces with Icon**: Replace the detected faces with a custom icon image.
- **Graphical User Interface (GUI)**: Simple GUI built with Tkinter to adjust blur or pixelation levels.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- Tkinter (comes pre-installed with Python on most platforms)
- Pillow (for handling images in the GUI)
