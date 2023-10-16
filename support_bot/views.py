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
    tid = Bot.objects.filter(token=token).first()
    
    if tid is None:
        return main_view_json(request)
    
    chat_id_arr = [hid.chat_id for hid in Chat.objects.filter(token=tid.id)] # id chat for admin message,    
    bots = Telega(token = token, path = STATIC_DIR, filename = "data.json")
 
    reply_markup = {'force_reply':True, 'input_field_placeholder':'Reply', 'selective':False}

    try:    
        data_unicode = request.body.decode('utf-8')

        if data_unicode is None:
            return JsonResponse({'error':True, 'method':method})

        data = json.loads(data_unicode)
        # bots.write_json(data = data, filename = f'{STATIC_DIR}/data_json.json')  # this is loging data json files
        # logger.debug(data)

        if 'message' not in data:
            return JsonResponse({'error':True, 'method':method})

        chat_id = data['message']['chat']['id']
        message_id = data['message']['message_id']
        from_id = data['message']['from']['id']
        is_admin = chat_id in chat_id_arr
        chat_text = data['message']['text'] if 'text' in data['message'] else False
        photo = data['message']['photo'][0]['file_id'] if 'photo' in data['message'] else False
        caption = data['message']['caption'] if 'caption' in data['message'] else False
        first_name = data['message']['from']['first_name'] if 'first_name' in data['message']['from'] else ''
        last_name = data['message']['from']['last_name'] if 'last_name' in data['message']['from'] else ''
        username = data['message']['from']['username'] if 'username' in data['message']['from'] else ''
        language_code = data['message']['from']['language_code'] if 'language_code' in data['message']['from'] else 'ru'
        # reply_markup_button = {'inline_keyboard':[[{'text':'Reply', 'callback_data':f'cid: {chat_id}'},]], 'resize_keyboard':True, 'one_time_keyboard':False}

        m = []
        m.append(f'cid: {chat_id}')
        m.append(f'{first_name}, {last_name}, @{username}, {language_code}')
        if chat_text is not False:
            m.append(chat_text)

        if caption is not False:
            m.append(caption)
        
        if chat_text == '/getchatid':
            """ help return """
            bots.sendMessage(chat_id, text="\n".join([f'cid: {chat_id}', f'mid: {message_id}', f'fid: {from_id}']))
            return main_view_json(request)

        if is_admin is True:
            """ is admin """
            if 'reply_to_message' in data['message']:
                reply_to_message_text = data['message']['reply_to_message']['text'] if 'text' in data['message']['reply_to_message'] else ''
                reply_to_message_caption = data['message']['reply_to_message']['caption'] if 'caption' in data['message']['reply_to_message'] else ''
                rm_arr = (reply_to_message_text+reply_to_message_caption).split('\n')
                old_chat_id = rm_arr[0].replace('cid:','',1).strip()
                bots.sendMessage(old_chat_id, text=chat_text)
            else:
                if chat_text is not False:
                    for cid in chat_id_arr:
                        bots.sendMessage(cid, text="\n".join(m), parse_mode='html', reply_markup=reply_markup)

                if photo is not False:
                    for cid in chat_id_arr:
                        bots.sendPhoto(cid, photo=photo, caption="\n".join(m), parse_mode='html', reply_markup=reply_markup)

        if is_admin is False:
            """ is user """
            if chat_text is not False:
                for cid in chat_id_arr:
                    bots.sendMessage(cid, text="\n".join(m), parse_mode='html', reply_markup=reply_markup)

            if photo is not False:
                for cid in chat_id_arr:
                    bots.sendPhoto(cid, photo=photo, caption="\n".join(m), parse_mode='html', reply_markup=reply_markup)
        
    except Exception as e:
        logger.error(sys.exc_info()[1])    

    return main_view_json(request)

def main_view_json(request):    
    response = JsonResponse({'ok':True, 'result':True, 'method':request.method, 'vid':'0.1.9'})
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    # response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"

    return response

class MainView(TemplateView):
    """ main page """    
    template_name = "main/main_list.html"