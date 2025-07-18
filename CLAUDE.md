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
├── models/                 # SQLModel database models (25+ tables)
├── components/             # Reusable UI components
├── database/               # Database utilities and seeding system
│   └── seeds/              # Database seed files (11 seed scripts)
├── states/                 # Reflex state management
└── alembic/                # Database migration files
    └── versions/           # Migration version files
```

### Authentication
- Uses `reflex-clerk-api` for authentication
- All pages except index are protected via `protected_page()` wrapper
- Authentication state managed through Clerk provider

### Database Models

#### Core Organizational Models
- `Employee`: Staff information with **required** department_id foreign key
- `AppUser`: Application users with **required** department_id and priv_level_id foreign keys
- `Department`: Department information (dept_id, dept_name, dept_description)
- `PrivilegeLevel`: User privilege levels (priv_id, priv_name, priv_description)

#### Project & Location Models
- `Project`: Project management
- `Building`: Building information (building_id, building_name)
- `Floor`: Floor information with building_id foreign key
- `Room`: Room information with floor_id and building_id foreign keys

#### Asset Management Models
- `Asset`: Core asset tracking with multiple foreign keys (project, location, system specs)
- `SysType`: System type lookup (systype_id, sys_type)
- `SysArchitecture`: System architecture lookup (46 architectures: x86_64, ARM, etc.)
- `CPUType`: CPU type lookup (498 CPU types)
- `GPUType`: GPU type lookup (187 GPU types)

#### Operating System Models
- `OperatingSystem`: OS lookup (os_id, os_name)
- `OSEdition`: OS edition lookup (osedition_id, osedition_name)
- `OSVersion`: OS version with foreign keys to OperatingSystem and OSEdition

#### Hardware & Software Models
- `HardwareManufacturer`: Hardware vendor information
- `SWManufacturer`: Software vendor information
- `AVVersion`: Antivirus version information
- `DatVersion`: DAT version with avversion_id foreign key

#### Activity Tracking Models
- `DatUpdate`: DAT update tracking with employee, asset, project foreign keys
- `LogCollection`: Log collection tracking with employee, asset, project, logtype foreign keys
- `ImageCollection`: Image collection tracking with employee, asset, project, imgmethod foreign keys
- `LogType`: Log type lookup
- `ImagingMethod`: Imaging method lookup

#### Support Models
- `TEMTicket`: Test Equipment Maintenance tickets with asset, project, employee foreign keys

### Database Seed Data Directory
- `seeds` is a directory intended to hold the seed data for information that will need to be inserted to the database. this information will contain known good data to prepopulate the database with some baseline data for the initial testing of certain relationships and to be able to display the appropriate data visuals within the application.
- make sure that seeds will not cause relationship errors in the database, please ensure you are raising any concerns to the user as they request seed data additions...
- **IMPORTANT**: Always maintain a `master_seed.py` file that contains all individual seed data files combined into a singular script without errors. This file must be updated after each seed data file addition to ensure all seed data can be executed in one script.

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

### Database Seeding System

The project includes a comprehensive seeding system for populating lookup tables:

#### Available Seed Files
- `master_seed.py`: Master seed script that runs all seeds in dependency order
- `department_seed.py`: 7 departments (System Administrators, Cybersecurity, etc.)
- `privilege_level_seed.py`: 3 privilege levels (Standard User, Power User, Administrator)
- `employee_seed.py`: 9 employees with department foreign keys
- `appuser_seed.py`: 9 app users with employee, department, and privilege level foreign keys
- `avversion_seed.py`: 2 antivirus versions
- `datversion_seed.py`: 2 DAT versions with AV foreign keys
- `sysarchitecture_seed.py`: 46 system architectures
- `cputype_seed.py`: 498 CPU types
- `gputype_seed.py`: 187 GPU types

#### Running Seeds
```bash
# Run all seeds in proper dependency order
python local_llama/database/seeds/master_seed.py

# Run individual seeds
python local_llama/database/seeds/department_seed.py
```

#### Foreign Key Relationships

**Required Foreign Keys (Non-Nullable):**
- `Employee.department_id` → `Department.dept_id`
- `AppUser.department_id` → `Department.dept_id`
- `AppUser.priv_level_id` → `PrivilegeLevel.priv_id`
- `Room.floor_id` → `Floor.floor_id`
- `Room.building_id` → `Building.building_id`
- `OSVersion.os_id` → `OperatingSystem.os_id`
- `OSVersion.osedition_id` → `OSEdition.osedition_id`
- `DatVersion.avversion_id` → `AVVersion.avversion_id`
- All audit trail relationships (DatUpdate, LogCollection, ImageCollection)

**Optional Foreign Keys (Nullable):**
- `AppUser.employee_id` → `Employee.id` (not all users are employees)
- `Asset.cpu_id` → `CPUType.cpu_id` (hardware may be unknown)
- `Asset.gpu_id` → `GPUType.gpu_id` (hardware may be unknown)
- `TEMTicket.response_emp` → `Employee.id` (may not have responder yet)

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

## Common Issues and Solutions

### Database Migration Issues
- **Character Encoding Errors**: If seeding fails with character encoding errors (e.g., Unicode characters), replace problematic characters with ASCII equivalents
- **Migration Dependency Order**: Always run seeds in dependency order - reference tables first, then tables with foreign keys
- **DateTime Field Defaults**: Use `Optional[datetime] = Field(default=None)` instead of `default_factory=datetime.now` to avoid migration errors

### Foreign Key Constraint Management
- **Required vs Optional**: Core organizational relationships (department, privilege level) should be required; optional relationships (hardware specs, assignments) should be nullable
- **Existing Data**: Before making foreign keys required, ensure all existing data has valid relationships
- **Seed Data Updates**: When changing foreign key constraints, update corresponding seed files to match new requirements

### Model Import Issues
- **Missing Model Imports**: When creating new models, add them to `models/__init__.py` and import in main app before running migrations
- **Table Name Conflicts**: Ensure model class names match expected table names in foreign key references

### Database Seeding Best Practices
- **Duplicate Prevention**: All seed scripts should check for existing records before insertion
- **Master Seed Script**: Use `master_seed.py` to run all seeds in proper dependency order
- **Foreign Key Validation**: Seed scripts should validate foreign key relationships before insertion

### Complete Seed File List (21 files)
- `appuser_seed.py` - 9 app users with FK relationships
- `avversion_seed.py` - 2 antivirus versions
- `building_seed.py` - Building data
- `cputype_seed.py` - 498 CPU types
- `datversion_seed.py` - 2 DAT versions with AV FK
- `department_seed.py` - 7 departments
- `employee_seed.py` - 9 employees with department FK
- `floor_seed.py` - Floor data with building FK
- `gputype_seed.py` - 187 GPU types
- `hardware_manufacturer_seed.py` - Hardware manufacturers
- `imagingmethod_seed.py` - Imaging methods
- `logtype_seed.py` - Log types
- `master_seed.py` - Master script running all seeds
- `operating_system_seed.py` - Operating systems
- `osedition_seed.py` - OS editions
- `osversion_seed.py` - OS versions with FK
- `privilegelevel_seed.py` - 3 privilege levels
- `project_seed.py` - Project data
- `swmanufacturer_seed.py` - Software manufacturers
- `sysarchitecture_seed.py` - 46 system architectures
- `systype_seed.py` - System types
