


### Item auto generation
Example:
```python
from pydantic import Field
from iqt.components.data_view.item import BaseDataItem


class Supply(BaseDataItem):
    _view_widgets: dict = {}
    _sort_fields: str = ["name", "slug", "category"]

    id: int = None
    rating: float = Field(None, description="Average rating")
    category: str = Field(None, description="Category")
    name: str = Field(None, description="Strain name")
    image: str = Field(None, description="<preview>")
    slug: str = Field(None)
    subtitle: str = Field(None, description="<item_name>")
```
- <b>_view_widgets</b> - You can specify a widget for each display type: "flow", "vertical", "horizont".
- <b>_sort_fields</b> - You can explicitly indicate which fields are allowed for sorting.
