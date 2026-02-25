# Smart Parking System  
### License Plate Recognition using PyQt5 + OpenCV + ESP32

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green)
![OpenCV](https://img.shields.io/badge/OpenCV-ComputerVision-red)
![ESP32](https://img.shields.io/badge/ESP32-Serial-orange)
![MySQL](https://img.shields.io/badge/MySQL-Database-blue)

A smart parking management system that uses **computer vision** to recognize vehicle license plates and integrates with **ESP32 hardware** for automated gate control.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Database Setup](#database-setup)
- [ESP32 Communication](#esp32-communication)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Security Notes](#security-notes)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

This project implements an **automatic parking system** that:

- Detects vehicle license plates from camera feeds
- Extracts plate text using OCR
- Stores vehicle entry data in MySQL
- Verifies exit vehicles
- Controls gate via ESP32
- Displays real-time available parking slots

Designed for educational and research purposes.

---

## 🏗 System Architecture

Camera IN ---> OpenCV Detection ---> EasyOCR ---> MySQL Database
|
v
ESP32 <--- Serial Communication <--- Verification Logic
|
v
Camera OUT ---> Plate Check ---> Gate Control ---> Slot Update


---

## Features

- Dual camera system (Entry / Exit)
- License plate detection using Haar Cascade
- OCR recognition with EasyOCR
- MySQL database storage
- Serial communication with ESP32
- Real-time parking slot counter
- GUI built with PyQt5

---

## Technologies Used

- Python 3.x
- PyQt5
- OpenCV
- EasyOCR
- Tesseract OCR
- MySQL
- ESP32
- PySerial

---

## Project Structure

project/
│
├── main.py
├── artboard_qrc.py
├── plates/
│ ├── scanned_img_.jpg
│ ├── checked_img_.jpg
│
├── Training/
│ └── haarcascade_russian_plate_number.xml
│
└── README.md

---

## Installation Guide

### 1️ Clone repository

git clone https://github.com/your-username/smart-parking-system.git
cd smart-parking-system

### 2️ Install dependencies
pip install pyqt5 opencv-python easyocr pytesseract mysql-connector-python pyserial

### 3Install Tesseract OCR

Download and install:

https://github.com/tesseract-ocr/tesseract

Then update path in main.py if needed:

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

### Database Setup
CREATE DATABASE ds_bienso;

USE ds_bienso;

CREATE TABLE ds_bienso (
    stt INT PRIMARY KEY,
    ds_bienso VARCHAR(20)
);
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YOUR_PASSWORD",
    database="ds_bienso"
)

### ESP32 Communication

Update correct COM port:

self.serial_connection = serial.Serial(port='COM9', baudrate=115200, timeout=1)
ESP32 sends:

"Welcome In" → Trigger vehicle entry

"checkout_started" → Trigger vehicle exit

Python responds:

License plate string

1 → Allow exit

0 → Deny exit

### How It Works
🚘 Entry Process

Camera IN captures frame

Plate detected via Haar Cascade

OCR extracts text

Plate saved to MySQL

Plate sent to ESP32

### Exit Process

Camera OUT captures plate

OCR extracts text

System checks MySQL database

If exists → Send 1

If not → Send 0

Update available parking slots

### Configuration
Camera Index
self.cap0 = cv2.VideoCapture(1)
self.cap1 = cv2.VideoCapture(0)

Adjust based on your system.

Haar Cascade Path
harcascade = "C:/Python/Training/haarcascade_russian_plate_number.xml"
### Security Notes

### Do NOT upload:

MySQL password

Serial port configuration

Local absolute paths

Recommended: Use .env file for configuration.

Example:

DB_HOST=localhost
DB_USER=root
DB_PASS=your_password
DB_NAME=ds_bienso
SERIAL_PORT=COM9
### Future Improvements

Improve OCR accuracy with image preprocessing

Replace Haar Cascade with YOLOv8

Add web dashboard

Implement payment system

Store entry/exit timestamps

Docker deployment

Deploy on Raspberry Pi
