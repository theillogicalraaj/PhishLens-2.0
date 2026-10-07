from collections import Counter
from datetime import datetime, timezone
import hashlib
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.deps import current_user
from app.models import AuditLog, Campaign, Event, Recipient, RiskSnapshot, User
from app.schemas import CampaignCreate, CaseUpdate, EventIn, RecipientCreate
from app.services.risk import compute_risk

router = APIRouter(prefix="/api/v1/campaigns", tags=["campaigns"])


def owner_campaign(db, user, campaign_id):
    campaign = db.get(Campaign, campaign_id)
    if not campaign or campaign.owner_id != user.id:
        raise HTTPException(404, "Campaign not found")
    return campaign

@router.post("")
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    campaign = Campaign(owner_id=user.id, **payload.model_dump())
    db.add(campaign); db.commit(); db.refresh(campaign)
    db.add(AuditLog(user_id=user.id, action="campaign_created", details=f"campaign_id={campaign.id}")); db.commit()
    return {"id": campaign.id, "name": campaign.name, "status": campaign.status}

@router.get("")
def list_campaigns(db: Session = Depends(get_db), user: User = Depends(current_user)):
    campaigns = db.query(Campaign).filter(Campaign.owner_id == user.id).order_by(Campaign.created_at.desc()).all()
    out=[]
    for c in campaigns:
        events = db.query(Event).filter(Event.campaign_id == c.id).all()
        recipients = db.query(Recipient).filter(Recipient.campaign_id == c.id).count()
        counts = Counter(e.event_type for e in events)
        clicks = len({e.recipient_id for e in events if e.event_type == "clicked"})
        reports = len({e.recipient_id for e in events if e.event_type == "reported"})
        risk = compute_risk(
            min(counts["opened"] / max(recipients,1),1),
            min(clicks / max(recipients,1),1),
            min(reports / max(recipients,1),1),
            0,
            min(len({e.recipient_id for e in events if e.event_type == "completed"}) / max(recipients,1),1),
        )
        out.append({"id": c.id, "name": c.name, "scenario": c.scenario, "status": c.status, "created_at": c.created_at, "recipients": recipients, "clicks": clicks, "reports": reports, "risk": risk})
    return out

@router.get("/{campaign_id}")
def get_campaign(campaign_id: int, db: Session = Depends(get_db), user: User = Depends(current_user)):
    c = owner_campaign(db, user, campaign_id)
    recipients = db.query(Recipient).filter(Recipient.campaign_id == c.id).all()
    events = db.query(Event).filter(Event.campaign_id == c.id).all()
    counts = Counter(e.event_type for e in events)
    recipient_count = len(recipients)
    clickers = len({e.recipient_id for e in events if e.event_type == "clicked"})
    reporters = len({e.recipient_id for e in events if e.event_type == "reported"})
    completers = len({e.recipient_id for e in events if e.event_type == "completed"})
    risk = compute_risk(
        len({e.recipient_id for e in events if e.event_type == "opened"})/max(recipient_count,1),
        clickers/max(recipient_count,1),
        reporters/max(recipient_count,1),
        len([r for r in recipients if sum(1 for e in r.events if e.event_type == "clicked") > 1])/max(recipient_count,1),
        completers/max(recipient_count,1),
    )
    return {
        "id": c.id, "name": c.name, "scenario": c.scenario, "subject": c.subject, "body": c.body,
        "status": c.status, "created_at": c.created_at, "risk": risk,
        "stats": {"recipients": recipient_count, "opened": counts["opened"], "clicked": counts["clicked"], "reported": counts["reported"], "completed": counts["completed"]},
        "recipients": [{"id":r.id,"display_name":r.display_name,"email":r.email,"department":r.department} for r in recipients],
    }

@router.patch("/{campaign_id}/case")
def update_case(campaign_id:int, payload:CaseUpdate, db:Session=Depends(get_db), user:User=Depends(current_user)):
    c=owner_campaign(db,user,campaign_id); c.status=payload.status; db.add(AuditLog(user_id=user.id, action="campaign_status", details=f"campaign_id={c.id};status={c.status}")); db.commit(); return {"status":c.status}

@router.post("/{campaign_id}/recipients")
def add_recipient(campaign_id:int,payload:RecipientCreate,db:Session=Depends(get_db),user:User=Depends(current_user)):
    c=owner_campaign(db,user,campaign_id)
    r=Recipient(campaign_id=c.id,display_name=payload.display_name.strip(),email=payload.email.lower(),department=payload.department.strip())
    db.add(r); db.commit(); db.refresh(r)
    return {"id":r.id,"display_name":r.display_name,"email":r.email,"department":r.department}


@router.post("/{campaign_id}/recipients/import")
async def import_recipients(campaign_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    c = owner_campaign(db, user, campaign_id)
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported")
    raw = await file.read()
    if len(raw) > 1024 * 1024:
        raise HTTPException(413, "CSV too large")
    import csv, io
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    required = {"display_name", "email", "department"}
    if not required.issubset(set(reader.fieldnames or [])):
        raise HTTPException(400, "CSV must contain display_name,email,department columns")
    added = 0
    for row in reader:
        if added >= 500:
            break
        name = (row.get("display_name") or "").strip()
        email = (row.get("email") or "").strip().lower()
        dept = (row.get("department") or "General").strip()
        if not name or "@" not in email:
            continue
        db.add(Recipient(campaign_id=c.id, display_name=name[:160], email=email[:320], department=dept[:100]))
        added += 1
    db.commit()
    return {"imported": added, "limit": 500}

@router.post("/{campaign_id}/simulate")
def simulate_event(campaign_id:int,payload:EventIn,request:Request,db:Session=Depends(get_db)):
    c=db.get(Campaign,campaign_id)
    r=db.get(Recipient,payload.recipient_id)
    if not c or not r or r.campaign_id != c.id:
        raise HTTPException(404,"Simulation target not found")
    ip = request.client.host if request.client else "unknown"
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()
    event=Event(campaign_id=c.id,recipient_id=r.id,event_type=payload.event_type,user_agent=request.headers.get("user-agent"),ip_hash=ip_hash)
    db.add(event); db.commit()
    return {"ok":True,"event":payload.event_type,"message":"Recorded as an internal training simulation event."}

@router.get("/{campaign_id}/report")
def report(campaign_id:int,db:Session=Depends(get_db),user:User=Depends(current_user)):
    from io import BytesIO
    from fastapi.responses import StreamingResponse
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    c=owner_campaign(db,user,campaign_id)
    detail=get_campaign(campaign_id,db,user)
    buf=BytesIO(); pdf=canvas.Canvas(buf,pagesize=A4)
    y=800
    pdf.setFont("Helvetica-Bold",18); pdf.drawString(40,y,"PhishLens 2.0 - Awareness Simulation Report"); y-=35
    pdf.setFont("Helvetica",10)
    lines=[f"Campaign: {c.name}",f"Scenario: {c.scenario}",f"Status: {c.status}",f"Risk: {detail['risk']['score']}/100 ({detail['risk']['severity']})",f"Recipients: {detail['stats']['recipients']}",f"Opened: {detail['stats']['opened']}",f"Clicked: {detail['stats']['clicked']}",f"Reported: {detail['stats']['reported']}",f"Completed: {detail['stats']['completed']}","","Model: Synthetic Logistic Regression baseline","Safety boundary: simulation-only; no credentials are collected."]
    for line in lines:
        pdf.drawString(40,y,line[:115]); y-=18
    pdf.showPage(); pdf.save(); buf.seek(0)
    return StreamingResponse(buf,media_type="application/pdf",headers={"Content-Disposition":f'attachment; filename="phishlens-{c.id}.pdf"'})
