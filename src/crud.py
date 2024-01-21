from sqlalchemy.orm import Session
from ua_parser import user_agent_parser

from src import keygen, models, schemas


def create_db_url(db: Session, url: schemas.LinkBase) -> models.Link:
    key = keygen.create_unique_random_key(db)
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.Link(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_link_by_url(db: Session, url: str) -> models.Link:
    return (
        db.query(models.Link)
        .filter(models.Link.target_url == url, models.Link.is_active)
        .first()
    )


def get_browser(db: Session, ua_string: str) -> models.Browser:
    browser = (
        db.query(models.Browser).filter(models.Browser.user_agent == ua_string).first()
    )
    if not browser:
        agent = user_agent_parser.Parse(ua_string)
        browser = models.Browser(
            user_agent=ua_string,
            browser_family="%s/%s"
            % (agent["user_agent"]["family"], agent["user_agent"]["major"]),
            os="%s/%s" % (agent["os"]["family"], agent["os"]["major"]),
            device="%s/%s" % (agent["device"]["brand"], agent["device"]["family"]),
        )
        db.add(browser)
        db.commit()
    return browser


def register_visit(
    db: Session, link: models.Link, ip_addr: str | None, ua_string: str | None
) -> models.Visit:
    browser = get_browser(db, ua_string) if ua_string else None
    visit = models.Visit(
        link_id=link.id, browser_id=browser.id if browser else None, ip_address=ip_addr
    )
    db.add(visit)
    db.commit()
    return visit


def get_link_by_short_code(db: Session, short_code: str) -> models.Link:
    return (
        db.query(models.Link)
        .filter(models.Link.key == short_code, models.Link.is_active)
        .first()
    )


def get_link_by_secret_key(db: Session, secret_key: str) -> models.Link:
    return (
        db.query(models.Link)
        .filter(models.Link.secret_key == secret_key, models.Link.is_active)
        .first()
    )


def update_db_clicks(db: Session, link: schemas.Link) -> models.Link:
    link.clicks += 1
    db.commit()
    db.refresh(link)
    return link


def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> models.Link:
    db_url = get_link_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
