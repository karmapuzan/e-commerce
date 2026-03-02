from fastapi import APIRouter, Depends, HTTPException, status
from backend.app.auth.security import oauth2_scheme
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.page import Page as PageModel
from backend.app.models.sections import Section as SectionModel
from backend.app.schemas.section import PageWithSections


router = APIRouter(
    prefix="/page", tags=["section"], dependencies=[Depends(oauth2_scheme)]
)


@router.post("")
def create_page(title: str, db: Session = Depends(get_db)):
    page = db.query(PageModel).filter(PageModel.title == title).first()
    if page:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Page is already created"
        )

    new_page = PageModel(slug=title.lower(), title=title)
    db.add(new_page)
    db.commit()

    return {
        "message": "Page has been successfully created",
        page: {"title": title, "slug": title.lower()},
    }


@router.post("/home")
def create_hero_banner(payload: PageWithSections, db: Session = Depends(get_db)):

    page = db.query(PageModel).filter(PageModel.id == payload.page_data.id).first()
    print(page)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Page with title '{payload.page_data.id}' not found",
        )
    created_sections = []

    for section in payload.landing:
        exiting = (
            db.query(SectionModel)
            .filter(
                SectionModel.page_id == page.id,
                SectionModel.type == section.type,
                SectionModel.order == section.order,
            )
            .first()
        )

        if exiting:
            continue

        new_section = SectionModel(
            page_id=page.id,
            type=section.type,
            order=section.order,
            content=section.content.dict(),
        )

        db.add(new_section)
        created_sections.append(new_section)
    db.commit()

    return {
        "message": "Sections created successfully",
        "total_sections": len(created_sections),
    }


@router.get("/page")
def get_page_content(db: Session = Depends(get_db)):
    pass
