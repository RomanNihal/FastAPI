import uvicorn
import math
import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

# --- Models ---
class OrganizationCreate(BaseModel):
    name: str
    status: str 
    description: Optional[str] = None

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None

# --- Fake Database ---
fake_db = []

# --- GET List ---
@app.get("/organizations")
def get_organizations(
    page: int = 1, 
    limit: int = 10, 
    sortBy: str = "createdAt", 
    sortOrder: str = "desc",
    status: Optional[str] = None
):
    filtered_data = fake_db.copy()

    if status:
        filtered_data = [org for org in filtered_data if org["status"] == status]

    is_descending = (sortOrder.lower() == "desc")
    filtered_data.sort(key=lambda x: x.get(sortBy, ""), reverse=is_descending)

    start_index = (page - 1) * limit
    end_index = start_index + limit
    page_data = filtered_data[start_index : end_index]

    total_items = len(filtered_data)
    total_pages = math.ceil(total_items / limit) if limit > 0 else 0

    return {
        "data": page_data,
        "total": total_items,
        "page": page,
        "totalPages": total_pages
    }

# --- GET Single Item ---
@app.get("/organizations/{org_id}")
def get_organization(org_id: str):
    for org in fake_db:
        if org["id"] == org_id:
            return org
    raise HTTPException(status_code=404, detail="Organization not found")

# --- POST Create ---
@app.post("/organizations", status_code=status.HTTP_201_CREATED)
def create_organization(org: OrganizationCreate):
    new_org = {
        "id": str(uuid.uuid4()),
        "name": org.name,
        "status": org.status,
        "description": org.description,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    fake_db.append(new_org)
    return new_org

# --- CUSTOM ACTION Endpoint (New) ---
@app.post("/organizations/{org_id}/archive")
def archive_organization(org_id: str):
    found_org = None
    for org in fake_db:
        if org["id"] == org_id:
            found_org = org
            break
    
    if not found_org:
        raise HTTPException(status_code=404, detail="Organization not found")

    found_org["status"] = "custom action"
    found_org["updatedAt"] = datetime.now().isoformat()
    
    return found_org

# --- PATCH Update ---
@app.patch("/organizations/{org_id}")
def update_organization(org_id: str, update_data: OrganizationUpdate):
    found_org = None
    for org in fake_db:
        if org["id"] == org_id:
            found_org = org
            break
    
    if not found_org:
        raise HTTPException(status_code=404, detail="Organization not found")

    update_dict = update_data.dict(exclude_unset=True)
    
    for key, value in update_dict.items():
        found_org[key] = value

    found_org["updatedAt"] = datetime.now().isoformat()
    
    return found_org

# --- DELETE Endpoint ---
@app.delete("/organizations/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(org_id: str):
    target_index = -1
    for index, org in enumerate(fake_db):
        if org["id"] == org_id:
            target_index = index
            break
    
    if target_index == -1:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    fake_db.pop(target_index)
    return

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)