# coding=utf-8

from sqlalchemy import text as _text

from elastic_graph import db


class BaseEntity(db.Model):
    __tablename__ = 'base_entity'

    id = db.Column(db.String(255), primary_key=True)
    local_id = db.Column(db.String(255), unique=True, index=True)
    entity_type = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, server_default=_text("CURRENT_TIMESTAMP"), default=db.func.now())
    update_time = db.Column(db.DateTime, server_default=_text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), default=db.func.now(), onupdate=db.func.now())
