from pydantic import BaseModel


class LinkBase(BaseModel):
    target_url: str


class Link(LinkBase):
    is_active: bool
    clicks: int

    class Config:
        orm_mode = True


class LinkInfo(Link):
    url: str
    admin_url: str
