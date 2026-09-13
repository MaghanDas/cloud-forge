from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CloudForge Demo API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/items", response_model=schemas.ItemResponse)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
):
    db_item = models.Item(
        name=item.name
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


@app.get("/items", response_model=list[schemas.ItemResponse])
def get_items(
    db: Session = Depends(get_db),
):
    return db.query(models.Item).all()