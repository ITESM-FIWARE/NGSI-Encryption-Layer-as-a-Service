# -*- coding: utf-8 -*-
class Mongomodel:

	def __init__(self, user, email, hashed_pw):
		self.user = user
		self.email = email
		#self.out_url = out_url
		self.password = hashed_pw

	def toDBCollection (self):
		return{
			"user":self.user,
			"email":self.email,
			#"out_url":self.out_url, 
			"password":self.password
		}

	def __str__(self):
		return "User: %s - Email: %s - password: %s" \
			%(self.user, self.email, self.password)

class MongomodelRegister:

	def __init__(self, user, service, hour, date, urlFrom,idEntity, typeEntity, urlTo):
		self.user = user
		self.service = service
		self.hour = hour
		self.date = date
		self.urlFrom = urlFrom
		self.idEntity = idEntity
		self.typeEntity = typeEntity
		self.urlTo = urlTo
	def toDBCollection (self):
		return{
			"user":self.user,
			"service":self.service,
			"hour":self.hour,
			"date":self.date,
			"urlFrom":self.urlFrom,
			"idEntity":self.idEntity,
			"typeEntity":self.typeEntity,
			"urlTo":self.urlTo
		}

	def __str__(self):
		return "user: %s - service: %s - hour: %s - date: %s - urlFrom: %s - idEntity %s - typeEntity %s - urlTo %s" \
			%(self.user, self.service, self.hour, self.date, self.urlFrom, self.idEntity, self.typeEntity, self.urlTo)