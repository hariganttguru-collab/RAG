# Project Management Learning Portal

A Django-based learning portal that simulates a project management environment where students can interact with AI-powered stakeholders to learn project estimation and budgeting.

## Features

- **User Authentication**: Registration and login system
- **Virtual Office Dashboard**: View online stakeholders and notifications
- **Real-time Chat**: WebSocket-based chat with AI stakeholders
- **AI Stakeholders**: LangChain-powered conversational agents with distinct personas
- **Notifications**: In-app notification system
- **Document Management**: Upload and view project documents

## Technology Stack

- Django 4.2.7
- Django Channels (WebSockets)
- LangChain + OpenAI API
- Bootstrap 5
- SQLite (development)

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```
   SECRET_KEY="i8laj*j^%vn@vp0=e6=(#lis12wu^y1risbj)f&m)%g^hvaz3%"
   OPENAI_API_KEY="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"
   DEBUG=True
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Initialize Stakeholders**
   ```bash
   python manage.py init_stakeholders
   ```

5. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**
   
   **Easy way (recommended):**
   - Double-click `start_server.bat` (Windows)
   - Or run `start_server.ps1` in PowerShell
   
   **Manual way:**
   ```bash
   python manage.py runserver
   ```
   
   For WebSocket support (required for chat), use Daphne:
   ```bash
   daphne -b 127.0.0.1 -p 8000 config.asgi:application
   ```
   
   Or simply use the provided startup scripts which use Daphne automatically.

## Usage Flow

1. **Register/Login**: Create an account or login
2. **Virtual Office**: After login, you'll see the dashboard with online stakeholders
3. **Notification**: You'll receive a notification from the Senior Manager about a new project
4. **Chat**: Click on any stakeholder to start a conversation
5. **Project Kickoff**: The Senior Manager will guide you through project initiation
6. **Estimation**: Chat with different stakeholders to gather information for project estimation and budgeting

## Project Structure

```
project_management_portal/
├── apps/
│   ├── authentication/    # User registration/login
│   ├── office/            # Virtual office dashboard
│   ├── chat/              # Real-time chat with WebSockets
│   ├── notifications/    # Notification system
│   ├── documents/         # Document management
│   └── ai/                # LangChain AI agents
├── config/                # Django project settings
├── templates/             # HTML templates
└── static/               # Static files (CSS, JS)
```

## AI Stakeholders

- **Sarah Chen** (Senior Manager): Initiates projects and guides the team
- **Mike Rodriguez** (Team Lead): Provides technical estimates
- **Alex Kim** (Developer): Estimates development work
- **Emma Watson** (Designer): Provides design estimates
- **David Park** (QA Engineer): Estimates testing efforts
- **Robert Johnson** (Client): Represents business needs

## Notes

- Make sure to set your OpenAI API key in the `.env` file for AI functionality
- The portal uses InMemoryChannelLayer for development. For production, configure Redis.
- All stakeholders are AI-powered using LangChain and OpenAI GPT models

