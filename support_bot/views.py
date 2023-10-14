import json, sys, os, time
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from support_bot.telega import Telega
from config.settings import STATIC_DIR
from django.views.generic.base import TemplateView

from .models import Chat, Bot


logging.basicConfig(
    level = logging.DEBUG, 
    filename = f'{STATIC_DIR}/text.log', 
    format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s", 
    datefmt = '%H:%M:%S',
)

logger = logging.getLogger(__name__)

@require_POST
def api_support(request, token):
    
    method = request.method
    chat_id_arr = [hid.chat_id for hid in Chat.objects.all()] # id chat for admin message,
    gram = Telega(token = token, path = STATIC_DIR, filename = "data.json")

    try:    
        data_unicode = request.body.decode('utf-8')

        if data_unicode is None:
            return JsonResponse({'error':True, 'method':method})
            
        data = json.loads(data_unicode)
        # gram.write_json(data = data, filename = f'{STATIC_DIR}/data_json.json')
        # logger.debug(data)
        
        if 'message' not in data:
            return JsonResponse({'error':True, 'method':method})
        
        chat_id = data['message']['chat']['id']
        message_id = data['message']['message_id']
        from_id = data['message']['from']['id']
        is_admin = chat_id in chat_id_arr
        chat_text = data['message']['text']        
        first_name = data['message']['from']['first_name'] if data['message']['from']['first_name'] else ''
        last_name = data['message']['from']['last_name'] if data['message']['from']['last_name'] else ''
        username = data['message']['from']['username'] if data['message']['from']['username'] else ''
        language_code = data['message']['from']['language_code']
        
        m = []
        m.append(f'chat_id: {chat_id}')
        m.append(f'{first_name}, {last_name}')
        m.append(f'{username}, {language_code}')
        m.append(chat_text)
        
        if chat_text == '/getchatid':
            """ help return """
            gram.sendMessage(chat_id, text="\n".join([f'chat_id: {chat_id}', f'message_id: {message_id}', f'from_id: {from_id}']))
            return main_view_json(request)
        
        if is_admin is True:
            """ is admin """
            if 'reply_to_message' in data['message']:
                reply_to_message = data['message']['reply_to_message']['text']
                rm_arr = reply_to_message.split('\n')
                old_chat_id = rm_arr[0].replace('chat_id:','',1).strip()
                gram.sendMessage(old_chat_id, text=chat_text)            
            else:                
                for c_id in chat_id_arr:
                    gram.sendMessage(c_id, text="\n".join(m))
        
        if is_admin is False:
            """ is user """
            for c_id in chat_id_arr:
                gram.sendMessage(c_id, text="\n".join(m))
        
    except Exception as e:
        logger.error(sys.exc_info()[1])    

    return main_view_json(request)

def main_view_json(request):    
    response = JsonResponse({'ok':True, 'result':True, 'method':request.method})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
    
    return response

class MainView(TemplateView):
    """ main page """    
    template_name = "main/main_list.html"