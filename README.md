# Eureka_Website_Automation_Testing_Case_7

## Overview

This repository contains the Case_7 automation script. It is developed using Python and Selenium to automate Full Books Request (eBooks_Case_1) (only Subscribed Chapters) on the Eureka website. The script was developed in PyCharm IDE.

## Test Case Summary:

This positive test case verifies that a user can successfully access and download assigned ebooks or ebook chapters from the Eureka Website. The user logs in with valid credentials and, after successful authentication, navigates from the homepage by hovering over the Publications menu and selecting By Title under the Books section, and the user navigates using pagination and clicks on the 4th page. then selects a book from the list. If the selected book is assigned by the admin, the user is able to download the permitted content, either specific chapters from the same page or from the detail page. The system ensures that only admin-assigned books or chapters are available for download, and the download process completes successfully.

## Folder Structure

<img width="595" height="346" alt="image" src="https://github.com/user-attachments/assets/b6aea6e2-ec29-40d8-93c1-641fc80895a1" />

## .env File

Install dotenv library:

pip install python-dotenv

Python Code to Load .env File:

import os
from dotenv import load_dotenv

Load .env file
load_dotenv(".env")

Variables
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

.env File Content:

LOGIN CREDENTIALS
EMAIL=(Your Email)
PASSWORD=(Your Password)

SITE URL
BASE_URL=https://www.eurekaselect.com/

Creating Executable (.exe) File

Install PyInstaller:

pip install pyinstaller

Command to Create Executable:

pyinstaller --onefile --collect-all selenium Case_7.py
