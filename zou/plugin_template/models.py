from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class Count(db.Model, BaseMixin, SerializerMixin):
    """
    Describe a plugin.
    """

    __table_args__ = {"extend_existing": True}
    count = db.Column(db.Integer, nullable=False, default=0)
