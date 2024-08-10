# Reciepe

Welcome to your Django Project! This guide will help you set up the project on your local machine. Even if you're new to Django, these steps should be easy to follow.

## Getting Started


### Cloning the Repository

First, clone the repository from GitHub. Open your terminal and run:

```bash
git clone https://github.com/AbhijithMR-403/Reciepe.git
```

### Navigate into the project directory:

```bash
cd Reciepe
```

### Setting Up a Virtual Environment

1. Create a virtual environment:

```bash
python -m venv env
```

2. Activate the virtual environment:

```bash
.\env\Scripts\activate (for windows)

source env/bin/activate (max/linux)
```

### Install the Required Packages
```bash
pip install -r requirements.txt
```

### create .env file

you can get the api key from razorpay site:\
Tutorial: https://razorpay.com/docs/x/dashboard/api-keys/ \
You should create a `.env` file uisng the details from razorpay and with the vaible i have mentioned below

```bash
RAZOR_KEY_ID = ''
RAZOR_KEY_SECRET = ''
```

### Running Migrations
```bash
python manage.py migrate
```

### Running the Development Server
```bash
python manage.py runserver
```