# -*- coding: utf-8 -*-

import re
import json
from types import SimpleNamespace
# import vk
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from src_bot.db import getQuestions, getAnswer, getKeywords, getKeywordQuestions, getRelatedQuestions, getAnswerById, \
    getQuestionId, getAllowedLinks


def run():
    vk_session = vk_api.VkApi(
        token='')
    longpoll = VkLongPoll(vk_session, 73827394)
    vk = vk_session.get_api()
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_vkpay_button(hash="action=transfer-to-group&group_id=183415444")
    longpoll_params = vk.messages.getLongPollServer(group_id=73827394)
    key = longpoll_params['key']
    server = longpoll_params['server']
    ts = longpoll_params['ts']
    longpoll = VkLongPoll(vk_session)
    try:
        respond(longpoll, vk)
    except Exception as e:
        print(str(e))


def isAllowedLink(requestLink):
    allowedLinks = getAllowedLinks()
    for link in allowedLinks:
        if link['link'] in requestLink:
            return True
    return False


def sendMessageWithButtons(vk, event, message, questions):
    kb = addButtons(vk, event, questions)
    vk.messages.send(
        message=message,
        random_id=get_random_id(),
        user_id=event.user_id,
        keyboard=kb.get_keyboard()
    )


def sendMessage(vk, event, message):
    vk.messages.send(
        message=message,
        random_id=get_random_id(),
        user_id=event.user_id,
        dont_parse_links=1,
    )


def addQuestionKeyboard(vk, event, questions):
    kb = VkKeyboard(one_time=True)
    questionList = ''
    for i, question in enumerate(questions):
        if i == 5:
            break
        if len(question['question']) < 40:
            kb.add_button(question['question'], color=VkKeyboardColor.SECONDARY)
        else:
            kb.add_button(str(i + 1), color=VkKeyboardColor.PRIMARY)
        questionList += str(i + 1) + '. ' + str(question['question']) + '\n'
        if (i < 4) and (i < len(questions) - 1):
            kb.add_line()
    vk.messages.send(
        message=questionList,
        random_id=get_random_id(),
        user_id=event.user_id,
        keyboard=kb.get_keyboard()
    )


def addButtons(vk, event, buttons):
    kb = VkKeyboard(inline=True)
    for i, button in enumerate(buttons):
        kb.add_button(button, color=VkKeyboardColor.PRIMARY)
        if i < len(buttons) - 1:
            kb.add_line()
    return kb

def addQuestionKeyboardId(vk, event, questions):
    kb = VkKeyboard(inline=True)
    questionList = ''
    for i, question in enumerate(questions):
        index = i + 1
        kb.add_button(str(index), color=VkKeyboardColor.PRIMARY, payload=json.dumps({'question': question['id'], 'action': 'answer'}))
        questionList += str(index) + '. ' + str(question['question']) + '\n'
        if index % 4 == 0:
            kb.add_line()
    kb.add_button('Нет нужного вопроса', color=VkKeyboardColor.PRIMARY)
    vk.messages.send(
        message=questionList,
        random_id=get_random_id(),
        user_id=event.user_id,
        keyboard=kb.get_keyboard()
    )


def findURL(string):
    regex=r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return url[0][0] if url else url

def getLinkFromMessage(vk, event):
    info_message = vk.messages.getById(message_ids=event.message_id)['items'][0]
    if info_message['attachments']:
        attachments = info_message['attachments']
        for attachment in attachments:
            if attachment['type'] == 'link':
                link = attachment['link']['url']
                if findURL(link):
                    return findURL(link)
    elif findURL(event.text):
        return findURL(event.text)
    return False


def deleteMessage(vk, event):
    vk.messages.delete(message_ids=event.message_id, delete_for_all=1)

def sendPayloadButtonResponse(vk, event, questions):
    payload = json.loads(event.payload, object_hook=lambda d: SimpleNamespace(**d))
    if payload.action == 'answer':
        questionId = str(payload.question)
        answer = getAnswerById(questionId)
        sendMessage(vk, event, answer)
        related = getRelatedQuestions(questionId)
        if related:
            answer += '\n\nИнтересует ли вас что-то еще?'
            sendMessage(vk, event, 'Чтобы продолжить, введите инетресующую вас тему или выберите один из вопросов')
            addQuestionKeyboardId(vk, event, related)
        else:
            sendMessage(vk, event,
                        'К сожалению, мне нечего больше предложить по данной теме. Попробуйте снова или выберите один из предложенных вопросов')
            addQuestionKeyboardId(vk, event, questions)


def respond(longpoll, vk):
    questions = getQuestions()
    keywords = getKeywords()
    questionList = [q['question'] for q in questions]
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_chat:
                url = getLinkFromMessage(vk, event)
                if url:
                    if not isAllowedLink(url):
                        try:
                            deleteMessage(vk, event)
                        except Exception as e:
                            print(e)
            else:
                if event.to_me:
                    if 'start' in event.text.lower() or 'старт' in event.text.lower() or 'начать' in event.text.lower():
                        sendMessage(vk, event, 'Выберите один из вопросов или введите интересующую вас тему')
                        addQuestionKeyboardId(vk, event, questions)
                    elif event.text in questionList:
                        question = event.text
                        questionId = getQuestionId(question)
                        answer = getAnswer(question)
                        related = getRelatedQuestions(str(questionId))
                        sendMessage(vk, event, answer)
                        if related:
                            sendMessage(vk, event, 'Интересует ли вас что-то еще? Похожие вопросы:')
                            addQuestionKeyboardId(vk, event, related)
                        else:
                            sendMessage(vk, event, 'К сожалению, мне нечего больше предложить по данной теме. Попробуйте снова или выберите один из предложенных вопросов')
                            addQuestionKeyboardId(vk, event, questions)
                    elif event.text in keywords:
                        related = getKeywordQuestions(event.text)
                        if related:
                            sendMessage(vk, event, 'Вот что я могу предложить вам по данной теме')
                            addQuestionKeyboardId(vk, event, related)
                        else:
                            sendMessage(vk, event, 'К сожалению, по данной теме ничего не найдено. Попробуйте снова или выберите один из предложенных вопросов')
                            addQuestionKeyboardId(vk, event, questions)
                    elif event.text == 'Нет нужного вопроса':
                        sendMessageWithButtons(vk, event, 'Cожалею, что не смог вам помочь. Нажмите Старт чтобы начать заново или введите вопрос и дождитесь ответа представителя SAS', ['Старт'])

                    else:
                        try:
                            if event.payload:
                                sendPayloadButtonResponse(vk, event, questions)
                        except Exception as e:
                            print(e)
