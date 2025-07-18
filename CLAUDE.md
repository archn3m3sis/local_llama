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
- `Employee`: Staff information (id, first_name, last_name, email, department)
- `AppUser`: Application users with foreign keys to Department and PrivilegeLevel
- `Project`: Project management (project_id, project_name, created_at, updated_at, is_active)
- `HardwareManufacturer` & `SWManufacturer`: Vendor information
- `AVVersion` & `DatVersion`: Asset versioning
- `PrivilegeLevel`: User privilege levels (priv_id, priv_name, priv_description)
- `Department`: Department information (dept_id, dept_name, dept_description)
- `Building`: Building information (building_id, building_name)
- `Floor`: Floor information (floor_id, floor_name)
- `Room`: Room information (room_id, floor_id, building_id)
- `SysType`: System types (systype_id, systype_name)
- `OperatingSystem`: Operating systems (os_id, os_name)
- `OSEdition`: OS editions (osedition_id, osedition_name)
- `OSVersion`: OS versions (osversion_id, os_id, osedition_id, osversion_name)
- `CPUType`: CPU types (cpu_id, cpu_name)
- `GPUType`: GPU types (gpu_id, gpu_name)
- `Asset`: Main asset table with extensive foreign key relationships to all location, hardware, and OS tables
- `DatUpdate`: DAT file update tracking (datupdate_id, date_of_update, employee_id, datversion_id, asset_id, project_id, datfile_name, update_result, update_comments)
- `LogType`: Log types (logtype_id, logtype)
- `LogCollection`: Log collection tracking (logcollection_id, logcollection_date, employee_id, asset_id, project_id, logtype_id, logcollection_result, logcollection_comments)
- `ImagingMethod`: Imaging methods (imgmethod_id, img_method)
- `ImageCollection`: Image collection tracking (imgcollection_id, imgcollection_date, employee_id, asset_id, project_id, img_size_mb, imgmethod_id, imaging_result, imaging_comments)
- `TEMTicket`: TEM ticket system (temticket_id, submission_date, global_ticket_id, asset_id, project_id, submission_emp, submission_description, response_date, response_emp, response_reference_link, response_result, response_comments, status, resolution_date, time_to_respond, time_to_resolve)

### Database Seed Data Directory
- `seeds` is a directory intended to hold the seed data for information that will need to be inserted to the databsae. this information will contain known good data to prepopulate the database with some baseline data for the initial testing of certain relationships and to be able to display the appropriate data visuals within the application.
- make sure that seeds will not cause relationship errors in the database, please ensure you are raising any concerns to the user as they request seed data additions...

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
- `/analytics`: Analytics and reporting

### Universal Background System
All protected pages now use a universal background system that includes:
- **Animated particle effects** - Interactive smoke/particle system using TSParticles
- **Mouse-following glow effect** - Subtle white glow that follows cursor movement
- **Gradient backgrounds** - Dark themed with subtle overlays
- **Consistent styling** - All pages have the same visual foundation

The universal background is implemented via:
- `components/universal_background.py` - Contains the background components
- `page_wrapper()` function - Wraps page content with universal background
- `protected_page()` function - Automatically applies universal background to all protected pages

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
