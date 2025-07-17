# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IAMS (Industrial Asset Management System) is a Reflex-based web application for managing industrial assets and maintenance logs. The system includes authentication via Clerk, database management with SQLModel/Alembic, and pages for assets, vulnerabilities, playbooks, and more.

## Common Development Commands

### Running the Application
```bash
reflex run           # Start the development server
reflex compile       # Compile the app
reflex init          # Initialize a new Reflex app (if needed)
```

### Database Management
```bash
reflex db makemigrations # create migrations
reflex db migrate # apply migrations
```

### Development Environment
Ensure you have a `.env` file with:
- `DATABASE_URL`: MSSQL connection string
- `CLERK_PUBLISHABLE_KEY`: Clerk authentication key
- `CLERK_SECRET_KEY`: Clerk secret key

## Architecture

### Project Structure
```
local_llama/
├── local_llama.py          # Main app entry point with authentication
├── pages/                  # Page components (dashboard, assets, etc.)
├── models/                 # SQLModel database models
├── components/             # Reusable UI components
├── database/               # Database utilities and data
└── states/                 # Reflex state management
```

### Authentication
- Uses `reflex-clerk-api` for authentication
- All pages except index are protected via `protected_page()` wrapper
- Authentication state managed through Clerk provider

### Database Models
Key models include:
- `Employee`: Staff information
- `AppUser`: Application users with foreign keys to Department and PrivilegeLevel
- `Project`: Project management
- `HardwareManufacturer` & `SWManufacturer`: Vendor information
- `AVVersion` & `DatVersion`: Asset versioning
- `PrivilegeLevel`: User privilege levels (priv_id, priv_name, priv_description)
- `Department`: Department information (dept_id, dept_name, dept_description)

### Page Architecture
Pages are organized by functionality:
- `/dashboard`: Main dashboard view
- `/assets`: Asset management
- `/vulnerabilities`: Vulnerability tracking
- `/playbook`: Documentation and playbooks
- `/software`: Software management
- `/dats`: DAT file management
- `/images`: Image management
- `/logs`: Log viewing
- `/tickets`: Ticket management

### Configuration
- `rxconfig.py`: Reflex configuration with database URL and plugins
- `pyproject.toml`: Python dependencies including AI libraries (langchain, ollama, openai)
- `alembic.ini`: Database migration configuration for MSSQL

## Key Features in Development
Based on the overview, the system will include:
- 3D asset visualization
- AI-powered insights via local LLM integration
- Universal search with hotkey control
- Markdown editor for playbooks
- FIPS 140-2 compliant password vault
- Vulnerability matrix with API integration
- Cradle-to-grave asset reporting

## Development Notes
- The app uses SQLModel for database ORM
- Authentication is handled at the page level, not route level
- Database migrations are managed via Alembic
- The system is designed for cybersecurity and asset management workflows

## User Preference For Workflows 
- Always use reflex db makemigrations and reflex db migrate to manage database migrations
- Always update your CLAUDE.md file with any changes to pages or database schema as well as project tree 
- Always ensure if there are repeated obstacles that are solved after a time, that you log the instructions to properly execute in your claude.md file
