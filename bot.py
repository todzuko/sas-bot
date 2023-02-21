import vk
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk_session = vk_api.VkApi(token='vk1.a.nR8uCUsiWVpQiyRYyVRjXzsJV7Px3WauvpC1NRzoJyOTSLUP4XFTpITH-hCPibNHQeqDRj3STe6J6FlCqLUv2LRfHnCkCIOtsNa0coP0H6kpFMT7Cm2Ymkoh3s_oCypdy3ohWdNBuAvzH8mbQkUq4yl1UPMYmimPfea3_Fpf9plzkBBsDIvQsuqMYyUIgzeHqAeRLOXEGSlN4ji1DH9wvA')

longpoll = VkBotLongPoll(vk_session, 218858137) #ID вашей группы без кавычек
vk = vk_session.get_api()

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Привет', color=VkKeyboardColor.NEGATIVE)
keyboard.add_button('Клавиатура', color=VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_location_button()
keyboard.add_line()
keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=183415444")
longpoll_params = vk.messages.getLongPollServer(group_id=218858137)
key = longpoll_params['key']
server = longpoll_params['server']
ts = longpoll_params['ts']


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if 'tired' in str(event) or 'sleep' in str(event):
            if event.from_chat:
                vk.messages.send(
                    key=key,  # ВСТАВИТЬ ПАРАМЕТРЫ
                    server=server,
                    ts=ts,
                    random_id=get_random_id(),
                    message='Pweasee sleep already',
                    chat_id=event.chat_id
                )
        if 'Клавиатура' in str(event):
            if event.from_chat:
                vk.messages.send(
                    keyboard=keyboard.get_keyboard(),
                    key=key,  # ВСТАВИТЬ ПАРАМЕТРЫ
                    server=server,
                    ts=ts,
                    random_id=get_random_id(),
                    message='Держи',
                    chat_id=event.chat_id
                )