# Overview For IAMS (Next Generation Industrial Asset Management System)

IAMS is a web application that allows users to manage their industrial assets and log the routine care and maintenance of those assets.

## Features

- User Authentication via the reflex-clerk-api integration
- Asset Management via interactive 3D models, tables, and charts shown within the app
    - This will include the ability to perform the following activities:
        - View and edit current asset information
        - View and edit log collections for the assets
        - View and edit recovery image collections for the assets
        - View and edit datfile updates for the assets
        - View and edit the status of TEM (Test Equipment Maintenance Tickets)
        - See relationships between workstation/laptop controller assets oscilloscope/analyzer assets
- Use locally integrated Artificial Intelligence to chat about and     gather more detail about insights gathered from the assets info collected and stored 
- ADMINS only should be able to visit a CRUD ops page to perform most of the database management needed for this type of application
- Track tasks and automatically assign them to one of the cybersecurity employees within the application 
- Integrated Markdown text editor with obsidian like capability for creating playbooks and documentation 
- Download and or print playbook documentation that has been written
- Integrated Code Snippets Vault for storing and reusing code snippets 
- Inventory Management and reporting
- Tracking of asset software packages for detailed change and configuration management ability 
- BEST FEATURE >>> A hotkey controlled universal search feature that allows for the seaarching of assets, logs, images, datfiles, recovery images, playbooks, code snippets, and tasks // this should be an easy to view and detailed compilation of app contents 
- Chat/messaging integration for a sort of 'comms board' type of setup where members of the app can communicate critical information with eachother
- A password vault with FIPS 140-2 compliance for storing critical secrets needed to manage assets within the organization
- A Cradle to Grave Report available for each asset in the organization that shows all details from the time the asset arrived at our organization to the time it was disposed of/retired 
- an intuitive and easy to use vulnerabliity matrix for tracking vulnerabilities found in assets and their severity, which draws from apis to automatically update the matrix with the latest information on threats 
- animations and smooth fluid user experience throughout the entirety of the application 
