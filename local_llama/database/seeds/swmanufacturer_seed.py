from sqlmodel import Session, create_engine, select
from local_llama.models.sw_manufacturer import SWManufacturer
import os
from dotenv import load_dotenv

load_dotenv()

def seed_sw_manufacturers():
    """Seed the SWManufacturer table with predefined software manufacturer data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Software manufacturer data to insert (name, weblink, contact)
    sw_manufacturers_data = [
        {"swmanu_name": "Adobe", "weblink": "https://www.adobe.com", "swmanu_contact": "1-800-833-6687"},
        {"swmanu_name": "Microsoft", "weblink": "https://www.microsoft.com", "swmanu_contact": "1-800-426-9400"},
        {"swmanu_name": "Oracle", "weblink": "https://www.oracle.com", "swmanu_contact": "1-800-392-2999"},
        {"swmanu_name": "SAP", "weblink": "https://www.sap.com", "swmanu_contact": "1-800-872-1727"},
        {"swmanu_name": "Salesforce", "weblink": "https://www.salesforce.com", "swmanu_contact": "1-800-667-6389"},
        {"swmanu_name": "IBM", "weblink": "https://www.ibm.com", "swmanu_contact": "1-800-426-4968"},
        {"swmanu_name": "Intuit", "weblink": "https://www.intuit.com", "swmanu_contact": "1-800-446-8848"},
        {"swmanu_name": "ServiceNow", "weblink": "https://www.servicenow.com", "swmanu_contact": "1-888-914-9661"},
        {"swmanu_name": "Workday", "weblink": "https://www.workday.com", "swmanu_contact": "1-877-967-5329"},
        {"swmanu_name": "Autodesk", "weblink": "https://www.autodesk.com", "swmanu_contact": "1-855-301-1941"},
        {"swmanu_name": "VMware", "weblink": "https://www.vmware.com", "swmanu_contact": "1-877-486-9273"},
        {"swmanu_name": "Red Hat", "weblink": "https://www.redhat.com", "swmanu_contact": "1-888-733-4281"},
        {"swmanu_name": "Atlassian", "weblink": "https://www.atlassian.com", "swmanu_contact": "1-866-660-6456"},
        {"swmanu_name": "Epicor Software Corporation", "weblink": "https://www.epicor.com", "swmanu_contact": "1-800-999-6995"},
        {"swmanu_name": "Infor", "weblink": "https://www.infor.com", "swmanu_contact": "1-800-260-2640"},
        {"swmanu_name": "Sage", "weblink": "https://www.sage.com", "swmanu_contact": "1-866-996-7243"},
        {"swmanu_name": "NetSuite", "weblink": "https://www.netsuite.com", "swmanu_contact": "1-877-638-7848"},
        {"swmanu_name": "Zoho Corporation", "weblink": "https://www.zoho.com", "swmanu_contact": "1-888-900-9646"},
        {"swmanu_name": "Splunk", "weblink": "https://www.splunk.com", "swmanu_contact": "1-888-773-5865"},
        {"swmanu_name": "Palo Alto Networks", "weblink": "https://www.paloaltonetworks.com", "swmanu_contact": "1-866-320-4788"},
        {"swmanu_name": "Cisco", "weblink": "https://www.cisco.com", "swmanu_contact": "1-800-553-2447"},
        {"swmanu_name": "Symantec", "weblink": "https://www.broadcom.com", "swmanu_contact": "1-800-441-7234"},
        {"swmanu_name": "McAfee", "weblink": "https://www.mcafee.com", "swmanu_contact": "1-888-847-8766"},
        {"swmanu_name": "Fortinet", "weblink": "https://www.fortinet.com", "swmanu_contact": "1-866-868-3678"},
        {"swmanu_name": "Crowdstrike", "weblink": "https://www.crowdstrike.com", "swmanu_contact": "1-888-510-3623"},
        {"swmanu_name": "Okta", "weblink": "https://www.okta.com", "swmanu_contact": "1-888-722-7871"},
        {"swmanu_name": "Zendesk", "weblink": "https://www.zendesk.com", "swmanu_contact": "1-888-670-4887"},
        {"swmanu_name": "HubSpot", "weblink": "https://www.hubspot.com", "swmanu_contact": "1-888-482-7768"},
        {"swmanu_name": "Slack", "weblink": "https://slack.com", "swmanu_contact": "1-855-980-5920"},
        {"swmanu_name": "Tableau", "weblink": "https://www.tableau.com", "swmanu_contact": "1-833-559-0075"},
        {"swmanu_name": "Snowflake", "weblink": "https://www.snowflake.com", "swmanu_contact": "1-844-766-9355"},
        {"swmanu_name": "Databricks", "weblink": "https://www.databricks.com", "swmanu_contact": "1-866-330-0121"},
        {"swmanu_name": "MongoDB", "weblink": "https://www.mongodb.com", "swmanu_contact": "1-844-666-4632"},
        {"swmanu_name": "Cloudera", "weblink": "https://www.cloudera.com", "swmanu_contact": "1-888-789-1488"},
        {"swmanu_name": "Teradata", "weblink": "https://www.teradata.com", "swmanu_contact": "1-866-548-8348"},
        {"swmanu_name": "SAS", "weblink": "https://www.sas.com", "swmanu_contact": "1-800-727-0025"},
        {"swmanu_name": "Informatica", "weblink": "https://www.informatica.com", "swmanu_contact": "1-650-385-5000"},
        {"swmanu_name": "Talend", "weblink": "https://www.talend.com", "swmanu_contact": "1-650-485-2730"},
        {"swmanu_name": "Google Cloud", "weblink": "https://cloud.google.com", "swmanu_contact": "1-844-613-7589"},
        {"swmanu_name": "Amazon Web Services", "weblink": "https://aws.amazon.com", "swmanu_contact": "1-800-257-1778"},
        {"swmanu_name": "Azure", "weblink": "https://azure.microsoft.com", "swmanu_contact": "1-800-867-1389"},
        {"swmanu_name": "GitLab", "weblink": "https://about.gitlab.com", "swmanu_contact": "1-415-689-8249"},
        {"swmanu_name": "GitHub", "weblink": "https://github.com", "swmanu_contact": "1-877-448-4820"},
        {"swmanu_name": "Bitbucket", "weblink": "https://bitbucket.org", "swmanu_contact": "1-866-660-6456"},
        {"swmanu_name": "Freshworks", "weblink": "https://www.freshworks.com", "swmanu_contact": "1-855-818-1151"},
        {"swmanu_name": "Monday.com", "weblink": "https://monday.com", "swmanu_contact": "1-201-778-4567"},
        {"swmanu_name": "Asana", "weblink": "https://asana.com", "swmanu_contact": "1-415-525-8474"},
        {"swmanu_name": "Trello", "weblink": "https://trello.com", "swmanu_contact": "1-866-660-6456"},
        {"swmanu_name": "QuickBooks", "weblink": "https://quickbooks.intuit.com", "swmanu_contact": "1-800-446-8848"},
        {"swmanu_name": "Xero", "weblink": "https://www.xero.com", "swmanu_contact": "1-844-829-3726"},
        {"swmanu_name": "Wave", "weblink": "https://www.waveapps.com", "swmanu_contact": "1-833-928-3424"},
    ]
    
    with Session(engine) as session:
        # Check if software manufacturers already exist to avoid duplicates
        existing_manufacturers = session.exec(select(SWManufacturer)).all()
        existing_names = {manufacturer.swmanu_name for manufacturer in existing_manufacturers}
        
        manufacturers_to_add = []
        for manufacturer_data in sw_manufacturers_data:
            if manufacturer_data["swmanu_name"] not in existing_names:
                manufacturers_to_add.append(SWManufacturer(**manufacturer_data))
        
        if manufacturers_to_add:
            session.add_all(manufacturers_to_add)
            session.commit()
            print(f"Added {len(manufacturers_to_add)} software manufacturers to the database.")
        else:
            print("All software manufacturers already exist in the database.")

if __name__ == "__main__":
    seed_sw_manufacturers()