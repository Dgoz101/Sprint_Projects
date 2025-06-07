# Overview

I wanted to challenge myself with a project where I wasn't super familiar with how the software worked. It just so happens that cloud systems are not something that I know a whole lot about, and that cloud systems are becoming more and more essential to many workplaces. I chose to create a Customer Relationship Management system that used to cloud to store information to a database. I decided to stick with python for the language and use the Firebase Admin library to access the cloud provided by Firestore. This project contains a GUI to make tracking, updating, adding, or deleting customer information more accessible and easier to work with. Being new with cloud systems and how they are integrated, there was a lot of bumps in the road where I had to spend time researching what was wrong and why. This provided quite a fun challenge and ultimately, I am quite happy with how it turned out.

[Software Demo Video](http://youtube.link.goes.here)

# Cloud Database

My CRM is on Firebase. I use a service-account key and the Admin SDK to talk to the Cloud in Firestore.Pyrebase does the same to handle user sign-up/login. The database has a top-level customer collection (holds holds a customer’s name, email, and creation timestamp) and under each customer, is their interactions (holds type, details, and timestamp).

# Development Environment

Tools: Cloud (firebase console, Service account JSON, Google Cloud Console)

Language: Python

Libraries: Tkinter, firebase-admin, pyrebase, uuid, datetime

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [Firebase](https://console.firebase.google.com/u/0/)
- [Google Cloud Hub](https://console.cloud.google.com/cloud-hub/)
- [Free Code Camp](https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/)

# Future Work

- Improve GUI
- Add more interaction types
- Improve scalability