from sqlmodel import Session, create_engine, select
from local_llama.models.asset import Asset
import os
from dotenv import load_dotenv

load_dotenv()

def seed_assets():
    """Seed the Asset table with baseline asset data."""
    
    # Create database engine
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url)
    
    # Asset data to insert
    # Format: (asset_name, project_id, building_id, floor_id, room_id, systype_id)
    assets_data = [
        {"asset_name": "ifmc.gets5a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets5b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets6a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets6b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets12a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets12b", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets14a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets14b", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets22a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets22b", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        
        # Assets with unknown room locations - leaving room_id as None
        {"asset_name": "ifmc.gets25a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.gets26a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.gets30a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        {"asset_name": "ifmc.gets35a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets35b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.gets27a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets28a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets29a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.gets39a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets40a", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 27, "systype_id": 1},
        {"asset_name": "ifmc.gets42a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 41, "systype_id": 1},
        {"asset_name": "ifmc.gets42b", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 41, "systype_id": 1},
        {"asset_name": "ifmc.laselec", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 25, "systype_id": 1},
        {"asset_name": "ifmc.defluxleft", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 39, "systype_id": 1},
        {"asset_name": "ifmc.defluxright", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 39, "systype_id": 1},
        {"asset_name": "ifmc.e2ic", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.vmeconsole", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.pfom", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 26, "systype_id": 1},
        {"asset_name": "ifmc.244m", "project_id": 1, "building_id": 1, "floor_id": 8, "room_id": 28, "systype_id": 1},
        {"asset_name": "ifmc.247m", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 45, "systype_id": 1},
        {"asset_name": "ifmc.248a", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 45, "systype_id": 1},
        {"asset_name": "ifmc.2058", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 40, "systype_id": 1},
        {"asset_name": "ifmc.2258", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 42, "systype_id": 1},
        
        # Asset with unknown room location - leaving room_id as None
        {"asset_name": "ifmc.2260", "project_id": 1, "building_id": 1, "floor_id": 7, "room_id": None, "systype_id": 1},
        
        {"asset_name": "ifmc.2259", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 42, "systype_id": 1},
        
        # Assets in other buildings with unknown room locations - leaving room_id as None
        {"asset_name": "ifmc.ftk1", "project_id": 1, "building_id": 3, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.ftk2", "project_id": 1, "building_id": 3, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.ftk3", "project_id": 1, "building_id": 3, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.hydraulic", "project_id": 1, "building_id": 7, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        {"asset_name": "ifmc.termini", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": 33, "systype_id": 1},
        
        # SHIELD project assets
        {"asset_name": "shield.afcc", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 43, "systype_id": 1},
        {"asset_name": "shield.geotest", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ir6100", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 43, "systype_id": 1},
        {"asset_name": "shield.ir6600", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 43, "systype_id": 1},
        {"asset_name": "shield.flir", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 48, "systype_id": 1},
        {"asset_name": "shield.ngats", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ifte1", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ifte2", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        {"asset_name": "shield.ifte3", "project_id": 2, "building_id": 1, "floor_id": 9, "room_id": 47, "systype_id": 1},
        
        # STARE project assets
        {"asset_name": "stare.wirestrip", "project_id": 3, "building_id": 1, "floor_id": 9, "room_id": 36, "systype_id": 1},
        {"asset_name": "stare.piu", "project_id": 3, "building_id": 1, "floor_id": 8, "room_id": 26, "systype_id": 2},
        
        # STORM project assets
        {"asset_name": "storm.chant", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.testek", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 30, "systype_id": 1},
        {"asset_name": "storm.tropel", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 30, "systype_id": 1},
        {"asset_name": "storm.gearbox", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.boom", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.shaker", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": 31, "systype_id": 1},
        {"asset_name": "storm.blue", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": None, "systype_id": 1},
        
        # MULTI project assets  
        {"asset_name": "multi.honeywell", "project_id": 5, "building_id": 2, "floor_id": 9, "room_id": 44, "systype_id": 1},
        
        # TAGM project assets
        {"asset_name": "tagm.tuts", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": 46, "systype_id": 1},
        {"asset_name": "tagm.jsts004", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "tagm.jsts800", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "tagm.mlv", "project_id": 6, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        # Additional STORM assets
        {"asset_name": "storm.pump", "project_id": 4, "building_id": 1, "floor_id": 7, "room_id": None, "systype_id": 1},
        
        # Additional IFMC numbered assets
        {"asset_name": "ifmc.226114", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.226118", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.2271", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.2275", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        # Additional IFMC test equipment
        {"asset_name": "ifmc.actuatortest", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.hoffman", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.legacythermal", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.lts1", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.ltsctc", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.nts1", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.nts2", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.thermal", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.v281", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.v323", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        {"asset_name": "ifmc.vmeprogrammer", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 1},
        
        # IFMC Oscilloscopes (Digital Oscilloscope - systype_id: 4)
        {"asset_name": "ifmc.oscope.aqg485", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.bgv085", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn4024", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn5201", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6242", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6256", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6309", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6310", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6312", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.cn6387", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.hxx865", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.r7057", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zue544", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zuf375", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zug348", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        {"asset_name": "ifmc.oscope.zug356", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 4},
        
        # IFMC Analyzers (Signal Analyzer - systype_id: 5)
        {"asset_name": "ifmc.analyzer.5617", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.bgv083", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn4322", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn5612", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn5625", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn5626", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6111", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6129", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6378", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6473", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.cn6615", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
        {"asset_name": "ifmc.analyzer.hxr172", "project_id": 1, "building_id": 1, "floor_id": 9, "room_id": None, "systype_id": 5},
    ]
    
    with Session(engine) as session:
        # Check if assets already exist to avoid duplicates
        existing_assets = session.exec(select(Asset)).all()
        existing_names = {asset.asset_name for asset in existing_assets}
        
        assets_to_add = []
        skipped_assets = []
        
        for asset_data in assets_data:
            if asset_data["asset_name"] not in existing_names:
                try:
                    assets_to_add.append(Asset(**asset_data))
                except Exception as e:
                    skipped_assets.append((asset_data["asset_name"], str(e)))
            else:
                skipped_assets.append((asset_data["asset_name"], "Already exists"))
        
        if assets_to_add:
            session.add_all(assets_to_add)
            session.commit()
            print(f"Added {len(assets_to_add)} assets to the database.")
        else:
            print("No new assets to add.")
        
        if skipped_assets:
            print(f"\nSkipped {len(skipped_assets)} assets:")
            for name, reason in skipped_assets:
                print(f"  - {name}: {reason}")

if __name__ == "__main__":
    seed_assets()