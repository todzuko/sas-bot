import psycopg2
from psycopg2.extras import RealDictCursor

def connect():
    return psycopg2.connect(
        host='localhost',
        user='django',
        password='shieve4aiHei',
        dbname='django_project_db',
    )


def getQuestions():
    conn = connect()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM django_bot_question")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def getAnswer(question):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM django_bot_question WHERE question = %s", (question,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


def getKeywords():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT keyword FROM django_bot_keyword")
    result = cursor.fetchall()
    keywords = [result[0] for result in result]
    cursor.close()
    conn.close()
    return keywords


def getKeywordQuestions(keyword):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT django_bot_question.id, django_bot_question.question FROM django_bot_questionkeyword "
        "LEFT JOIN django_bot_question on django_bot_question.id = django_bot_questionkeyword.question_id "
        "LEFT JOIN django_bot_keyword on django_bot_keyword.id = django_bot_questionkeyword.keyword_id "
        "WHERE django_bot_keyword.keyword = %s",
        (keyword,)
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [q[0] for q in result]


def getQuestionId(question):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM django_bot_question WHERE question = %s",
        (question,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None


def getRelatedQuestions(questionId):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT q.id, q.question "
        "FROM django_bot_question q "
        "JOIN django_bot_questionkeyword qk ON q.id = qk.question_id "
        "JOIN django_bot_keyword k ON qk.keyword_id = k.id "
        "WHERE k.keyword IN ( "
        "SELECT k1.keyword "
        "FROM django_bot_question q1 "
        "JOIN django_bot_questionkeyword qk1 ON q1.id = qk1.question_id "
        "JOIN django_bot_keyword k1 ON qk1.keyword_id = k1.id "
        "WHERE q1.id = %s "
        ") "
        "AND q.id != %s",
        (questionId, questionId)
    )
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    dbcursor.execute("SELECT * FROM django_bot_question")
    result = dbcursor.fetchall()
    return result


def getAnswer(question):
    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    dbcursor.execute("SELECT answer FROM django_bot_question WHERE question = '" + question + "'")
    result = dbcursor.fetchone()
    return result['answer']


def getAnswerById(questionId):
    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    dbcursor.execute("SELECT answer FROM django_bot_question WHERE id = '" + questionId + "'")
    result = dbcursor.fetchone()
    return result['answer']


def getKeywords():
    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    dbcursor.execute("SELECT keyword FROM django_bot_keyword")
    result = dbcursor.fetchall()
    keywords = [result['keyword'] for result in result]
    return keywords


def getKeywordQuestions(keyword):
    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    dbcursor.execute(
        "SELECT DISTINCT django_bot_question.id, django_bot_question.question FROM django_bot_questionkeyword "
        "LEFT JOIN django_bot_question on django_bot_question.id = django_bot_questionkeyword.question_id "
        "LEFT JOIN django_bot_keyword on django_bot_keyword.id = django_bot_questionkeyword.keyword_id "
        "WHERE django_bot_keyword.keyword = '" + keyword + "'"
    )
    result = dbcursor.fetchall()
    return result


def getQuestionId(question):
    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    dbcursor.execute(
        "SELECT django_bot_question.id FROM django_bot_question"
        " "
        "WHERE django_bot_question.question = %s",
        (question, )
    )
    result = dbcursor.fetchone()
    return result['id']


def getRelatedQuestions(question):
    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    qId = question
    dbcursor.execute(
        "SELECT DISTINCT q.id, q.question "
        "FROM django_bot_question q "
        "JOIN django_bot_questionkeyword qk ON q.id = qk.question_id "
        "JOIN django_bot_keyword k ON qk.keyword_id = k.id "
        "WHERE k.keyword IN ( "
        "SELECT k1.keyword "
        "FROM django_bot_question q1 "
        "JOIN django_bot_questionkeyword qk1 ON q1.id = qk1.question_id "
        "JOIN django_bot_keyword k1 ON qk1.keyword_id = k1.id "
        "WHERE q1.id = '" + qId + "' "
                                  ") "
                                  "AND q.id != '" + qId + "'"
    )
    result = dbcursor.fetchall()
    return result


def getAllowedLinks():
    botdb = connect()
    dbcursor = botdb.cursor(cursor_factory=RealDictCursor)
    dbcursor.execute("SELECT link FROM django_bot_allowedlinks")
    allowedLinks = dbcursor.fetchall()
    return allowedLinks
