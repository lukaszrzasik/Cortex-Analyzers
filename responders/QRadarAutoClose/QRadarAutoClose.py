#!/usr/bin/env python
# encoding: utf-8

#QRadarAutoClose
#Author: Florian Perret (@cyber_pescadito)

from cortexutils.responder import Responder
import requests

class QRadarAutoClose(Responder):
    def __init__(self):
        Responder.__init__(self)
        self.QRadar_URL = self.get_param('config.QRadar_Url', None, "QRadar URL is Missing")
        self.QRadar_API_Key = self.get_param('config.QRadar_API_Key', None, "QRadar API Key is Missing")
        self.Offense_Id = self.get_param('data.customFields.externalReferences', None, "QRadar Offense ID is Missing")
	self.Cert_Path = self.get_param('config.Cert_Path')

    def run(self):
    	Responder.run(self)
    	h = {'content-type': 'application/json'}
    	h['Version'] = '9.1'
    	h['SEC'] = str(self.QRadar_API_Key)
    	payload = self.Offense_Id['string'] + '?closing_reason_id=3&status=CLOSED'

	if self.Cert_Path == '':
		r=requests.post(self.QRadar_URL + payload, headers=h)
        else:
		r=requests.post(self.QRadar_URL + payload, headers=h, verify=self.Cert_Path)

	if r.status_code == 200 or 202 or 409:
        	self.report({'message': 'QRadar Offense succesfully closed !'})
        else:
        	self.error({'message': r.status_code})

if __name__ == '__main__':
        QRadarAutoClose().run()
