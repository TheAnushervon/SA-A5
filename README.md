# SA-A5

TEAM 03

## Team Members

Anushervon Qodirzoda | Ilias Dzhabbarov  |  Muhammad Allayarov

## Installation

1. Clone the repo
2. Create an environment and activate
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r pip-requirements.txt
4. Run services (if you want to run by hand or you can use start.bat script for Win)
uvicorn message.message:app --reload
uvicorn user.auth:app --reload
uvicorn feed.feed:app --reload

## Structure

Our application consists of 3 services: User, Message and Feed with single database.

In user service we handle registration and further authentication with logout. In message there is message creation and liking/unliking logic. In feed there is code for 10 last messages showig to users. 

Each service is independent and can be scaled, at least by adding feature for possibility to handle multiple instances (proxying via Nginx, after containerizaton).

## Demo

[Link]()
