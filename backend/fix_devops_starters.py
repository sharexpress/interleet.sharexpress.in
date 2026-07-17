import os
import json
from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["interleet"]

def fix_starters():
    db = get_db()
    col = db["problems"]
    
    # Query DevOps challenges with devops runtime
    devops_problems = list(col.find({"domain": "DevOps", "runtime": "devops"}))
    print(f"Found {len(devops_problems)} DevOps problems in database.")
    
    updated_count = 0
    for prob in devops_problems:
        starter = prob.get("starter_code", {})
        
        # If it doesn't have "multi" key, convert it
        if "multi" not in starter:
            title = prob.get("title", "DevOps Challenge")
            desc = prob.get("short_description", "Implement the DevOps task.")
            
            multi_files = {
                "setup.sh": "#!/bin/bash\n# TODO: Implement the task requirements\necho 'Running setup.sh...'\n",
                "readme.md": f"# {title}\n\n{desc}\n"
            }
            
            new_starter = {
                "multi": json.dumps(multi_files)
            }
            
            col.update_one({"id": prob["id"]}, {"$set": {"starter_code": new_starter}})
            updated_count += 1
            print(f"  ✓ Updated starter code for DevOps problem: {prob['id']} ({prob['slug']})")
            
    print(f"\nMigration complete. Updated {updated_count} DevOps starter codes.")

if __name__ == "__main__":
    fix_starters()
