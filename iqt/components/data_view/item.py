import pydantic


class BaseDataItem(pydantic.BaseModel):
    view_widgets: dict
    id: str
    slug: str
