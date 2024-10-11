# SA-A5

TEAM 03

## Team Members

Anushervon Qodirzoda | Ilias Dzhabbarov  |  Muhammad Allayarov

## Installation

1. Clone the repo
2. Create an environment and activate
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r pip-requirements.txt
```
4. Run services (if you want to run by hand, but there are start.sh and start.bat scripts both for Linux and Windows)

```bash
uvicorn message.message:app --reload
uvicorn user.auth:app --reload
uvicorn feed.feed:app --reload
```

## Structure

Our application consists of 3 services: User, Message and Feed with single database.

In user service we handle registration and further authentication with logout. In message there is message creation and liking/unliking logic. In feed there is code for 10 last messages showig to users. 

Each service is independent and can be scaled, at least by adding feature for possibility to handle multiple instances (proxying via Nginx, after containerizaton).

## Demo

[Link](https://drive.google.com/file/d/1n0m7WLZGqfgLBs_fF0BE5vgdsVQ9-qAd/view?usp=sharing)
