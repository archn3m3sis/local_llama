# Generation Scripts

This directory contains scripts that were used to generate the offline app setup. They are kept for reference but are no longer needed for running the application.

## Scripts:

- `setup_offline_app.py` - Main script that creates the offline_app directory
- `init_offline_db.py` - Database initialization script
- `run_offline.sh` - Original offline runner script
- `run_offline_uv.sh` - UV-based offline runner
- `rxconfig_offline.py` - Offline configuration template
- `requirements-*.txt` - Various requirements files used during setup

## Note:

These scripts have already been used to create the `offline_app` directory. You don't need to run them again unless you want to recreate the offline setup.

To run the offline demo, use:
```bash
cd ../offline_app
./run.sh
```

Or from the main directory:
```bash
./start_offline_demo.sh
```