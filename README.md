# Interview System

A modern, web-based recruitment and interview management system built with Django.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- Candidate registration and profile management
- Job position management (create, edit, activate/deactivate)
- Application submission and tracking
- Interview scheduling and management
- Role-based access for HR, interviewers, and candidates
- Dashboard for HR and interviewers
- Responsive UI with modern design
- Secure authentication and authorization

## Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Tailwind CSS or Bootstrap), JavaScript
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)
- **Other:** Git, GitHub Actions (optional for CI/CD)

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Git

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/interview-system.git
    cd interview-system
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the application:**

    Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage

- HR staff can manage job positions, review applications, and schedule interviews.
- Candidates can register, apply for positions, and track their application status.
- Interviewers can view assigned interviews and provide feedback.

## Project Structure

<pre> 
interview_system/
│
├── recruitment/           # Main Django app
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── ...
├── interview_system/      # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
├── requirements.txt
└── README.md
</pre>


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [tyhuynh172003@gmail.com](mailto:tyhuynh172003@gmail.com) or open an issue on GitHub.

---

*Thank you for using Interview System!*