'''
Created on 28/11/2013

@author: Roberto Guimaraes Morati Junior
'''

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.contrib import messages
import json


class ValidateDeletion(object):
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ValidationError as e:
            messages.error(request, "".join(e.messages))
            return HttpResponse(json.dumps({'response': 'exception delete'}), content_type="text")
        return HttpResponse(json.dumps({'response': 'ok'}), content_type="application/json")