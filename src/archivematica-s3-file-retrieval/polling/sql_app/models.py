# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 28-05-2022 12:33:44
# @Description: 

# custom imports
from sql_app.database import Base

# generic imports
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)



class FileToRetrieveRequest(Base):
    __tablename__ = "file_to_retrieve_request"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("file_to_retrieve.id"), index=True)
    requesters_email = Column(String(255), index=True)
    request_timestamp = Column(DateTime, default=datetime.datetime.now())
    requester_informed_timestamp = Column(DateTime, nullable=True, default=None)

    def as_dict(self):
        return {c.name: getattr(self, c.name) if not isinstance(getattr(self, c.name), \
            datetime.datetime) else str(getattr(self, c.name)) for c in self.__table__.columns}


class FileToRetrieve(Base):
    __tablename__ = "file_to_retrieve"
    id = Column(Integer, primary_key=True, index=True)
    bucket_name = Column(String(255), index=True)
    file_key = Column(String(255), index=True)
    last_retrieval_request_time = Column(DateTime,default=None)
    last_retrieved_timestamp = Column(DateTime, default=None)
    timestamp_of_file_removal = Column(DateTime, default=None)
    was_deleted = Column(Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) if not isinstance(getattr(self, c.name), \
            datetime.datetime) else str(getattr(self, c.name)) for c in self.__table__.columns}


class FileToRetrieveStatus(Base):
    __tablename__ = "file_to_retrieve_status"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("file_to_retrieve.id"), index=True)
    status = Column(String(255), index=True)
    timestamp = Column(DateTime, default=datetime.datetime.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) if not isinstance(getattr(self, c.name), \
            datetime.datetime) else str(getattr(self, c.name)) for c in self.__table__.columns}
