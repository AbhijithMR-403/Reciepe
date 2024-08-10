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

### Running Migrations
```bash
python manage.py migrate
```

### Running the Development Server
```bash
python manage.py runserver
```