# -*- coding: utf-8 -*-
# @Author: Rafael Direito
# @Date:   10-05-2022 10:52:27
# @Email:  rdireito@av.it.pt
# @Last Modified by:   Rafael Direito
# @Last Modified time: 12-05-2022 16:17:53
# @Description: 

import datetime

import sql_app
# custom imports
from sql_app.database import Base
# generic imports
from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import relationship


class User(Base):
	__tablename__ = "user"
	id = Column(Integer, primary_key=True, index=True)    
	username = Column(String(255), unique=True, index=True)
	hashed_password = Column(String(255), nullable=False)
	is_active = Column(Boolean, nullable=False)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User_Role(Base):
	__tablename__ = "user_role"
	id = Column(Integer, primary_key=True, index=True)    
	user = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
	role = Column(Integer, ForeignKey("role.id"), nullable=False)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Role(Base):
	__tablename__ = "role"
	id = Column(Integer, primary_key=True, index=True)    
	role = Column(String(255), unique=True)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}
