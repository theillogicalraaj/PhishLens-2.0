from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.deps import current_user
from app.models import Campaign, Event, Recipient, User

router=APIRouter(prefix="/api/v1/dashboard",tags=["dashboard"])

@router.get("")
def dashboard(db:Session=Depends(get_db),user:User=Depends(current_user)):
    campaigns=db.query(Campaign).filter(Campaign.owner_id==user.id).all()
    campaign_ids=[c.id for c in campaigns]
    events=db.query(Event).filter(Event.campaign_id.in_(campaign_ids)).all() if campaign_ids else []
    recipients=db.query(Recipient).filter(Recipient.campaign_id.in_(campaign_ids)).count() if campaign_ids else 0
    uniq=lambda kind: len({e.recipient_id for e in events if e.event_type==kind})
    clicked=uniq("clicked"); reported=uniq("reported"); completed=uniq("completed")
    click_rate=clicked/max(recipients,1)
    report_rate=reported/max(recipients,1)
    return {
        "campaigns":len(campaigns),"recipients":recipients,"clicked":clicked,"reported":reported,"completed":completed,
        "click_rate":round(click_rate*100,1),"report_rate":round(report_rate*100,1),
        "events":dict(Counter(e.event_type for e in events)),
        "principle":"Use simulation metrics to improve awareness; do not collect credentials."
    }
