# EHBC Church Website & Web Application


**Live Website:** [http://129.121.84.30](http://129.121.84.30)



## Overview
This is a custom full-stack web application built to serve as the main website and digital newsletter for our church. 
It handles dynamic content delivery, custom routing for members-only pages, and a responsive frontend interface.

## Key Features
* **Dynamic Content:** Pages are populated using JSON data structures, allowing for easily updatable content
* (sermons, announcements, staff bios, etc.) without having to alter the backend codebase.
* **Members-Only Access:** Custom URL parameter routing is implemented to securely display internal church resources,
* such as a hidden Volunteer dashboard for staff members.
* **Media Integration:** Built-in support for embedding dynamic YouTube videos and sharing formatted scripture outlines.
* **Custom Deployment Pipeline:** Designed and implemented a custom PowerShell-to-Bash deployment script
* (`publish_to_vps.ps1`) to package, transfer via SCP, and deploy the application to a live Linux VPS.

## Tech Stack
* **Backend:** Python, Flask
* **Frontend:** HTML5, CSS3, JavaScript, Jinja2 Templating
* **Data Storage:** JSON-based data structures (for lightweight, fast data retrieval)
* **Server & Hosting:** 
  * Hosted on a Bluehost VPS (Virtual Private Server)
  * OS: Linux (Ubuntu)
  * WSGI Server: Gunicorn
  * Web Server / Reverse Proxy: Nginx

## What I Learned
I learned how to automate updates from staff members and complete a deadline on time. I learned all about setting up Virtual
environments and automatically uploading my updates to bluehost. I never have to log in to bluehost and publish them manually.
I advanced my learning of PYTHON and how to develop a web site based on PYTHON using a framework FLASK. I also learned how to 
integrate jinga2 into the webgsite and build templates for HTML, CSS, and JAASCRIPT. I have also taught myself PHP, MYSQL, SQL, 
amd BOOTSTRAP 3 - 5. i have completed course at IVYTECH Community College online which include: Data Anylitics using Azure 
Icloud, and Python. 
Building this project allowed me to take a full-stack application from just an idea all the way to a live production server. I gained hands-on experience not just with writing Python and Flask code, but with crucial DevOps skills like SSH, SCP, setting up Nginx configuration files, managing Linux permissions, and writing automation scripts.

