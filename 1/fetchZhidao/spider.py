#coding:gbk
__author__ = 'ub'
import pylibmc as memcache
import urllib
from bs4 import BeautifulSoup
from models import ZhidaoQuestion





def startFetch():
    mc = memcache.Client()
    zhidaono = mc.get("zhidaono")



    resultHtml = urllib.urlopen("http://zhidao.baidu.com/question/"
                             + str(zhidaono) + ".html")
    xx = resultHtml.read()
    uni = xx.decode('gbk')
    utf = uni.encode('utf8')

    #soup = BeautifulSoup(resultHtml)
    return utf

def FetchStart():
    mc = memcache.Client()
    mc.set("errorcount",0)
    # questionid = 773
    #
    # resultHtml = urllib.urlopen("http://zhidao.baidu.com/question/"
    #                          + str(questionid) + ".html").read()
    # ErrorStr = '知道宝贝找不到问题了'
    # nPos = resultHtml.find(ErrorStr)
    # soup = BeautifulSoup(resultHtml)
    # if( soup.find("div", class_="wgt-best ") != None ):
    #         if( soup.find("div", class_="wgt-best ").find("pre",class_="best-text mb-10") != None ):
    #             bestanster = soup.find("div", class_="wgt-best ").find("pre",class_="best-text mb-10").text
    #         elif( soup.find("div", class_="wgt-best ").find("div", class_="bd answer").find("pre",class_="best-text expand-exp mb-10") != None ):
    #             bestanster = soup.find("div", class_="wgt-best ").find("div", class_="bd answer").find("pre",class_="best-text expand-exp mb-10").text
    # elif ( soup.find("div", class_="bd answer") != None ):
    #     bestanster = soup.find("div", class_="bd answer").find("pre",class_="recommend-text mb-10").text
    # elif( soup.find("div", class_="wgt-best ") != None ):
    #     bestanster = soup.find("div", class_="wgt-best ").find("pre",class_="best-text mb-10").text
    # else:
    #     bestanster = None
    # return bestanster


def fetchzhidao():
    passcount = 0
    trycount = 10
    incrcount = 1
    errorcount = 0
    while(True):
        mc = memcache.Client()
        questionid = mc.get("zhidaono")
        mc.set("zhidaono",(questionid + incrcount))
        resultHtml = urllib.urlopen("http://zhidao.baidu.com/question/"
                                 + str(questionid) + ".html").read()
        ErrorStr = '知道宝贝找不到问题了'
        nPos = resultHtml.find(ErrorStr)
        if( nPos > 0 ):
            passcount += 1
            if(trycount > 0):
                trycount -= 1
                continue
            if(passcount < 100):
                trycount = 10
                incrcount += (passcount/8)*6
            elif(passcount < 200):
                trycount = 10
                incrcount += (passcount/6)*6
            elif(passcount < 300):
                trycount = 10
                incrcount += (passcount/4)*7
            elif(passcount < 400):
                trycount = 10
                incrcount += (passcount/2)*7
            else:
                trycount = 10
                incrcount += passcount*7
            continue
        else:
            passcount = 0
            trycount = 10
            incrcount = 1
            if ( parseHtml(resultHtml,questionid) == 1):
                mc.incr("errorcount")

def parseHtml(resultHtml,questionid):
    soup = BeautifulSoup(resultHtml)
    if( soup.find("span", class_="ask-title  ") != None ):
        questiontitle = soup.find("span", class_="ask-title  ").text
    else:
        questiontitle = None
    if( soup.find("pre", class_="line mt-10 q-content") != None ):
        fullquestion = soup.find("pre", class_="line mt-10 q-content").text
    else:
        fullquestion = None
    if( soup.find("span", class_="grid-r ask-time") != None ):
        asktime = soup.find("span", class_="grid-r ask-time").text
    else:
        asktime = None
    if( soup.find("div", class_="wgt-best ") != None ):
        if( soup.find("div", class_="wgt-best ").find("pre",class_="best-text mb-10") != None ):
            bestanster = soup.find("div", class_="wgt-best ").find("pre",class_="best-text mb-10").text
        elif( soup.find("div", class_="wgt-best ").find("div", class_="bd answer").find("pre",class_="best-text expand-exp mb-10") != None ):
            bestanster = soup.find("div", class_="wgt-best ").find("div", class_="bd answer").find("pre",class_="best-text expand-exp mb-10").text
    elif ( soup.find("div", class_="wgt-recommend ") != None ):
        if( soup.find("div", class_="wgt-recommend ").find("div", class_="bd answer").find("pre",class_="recommend-text mb-10") != None ):
            bestanster = soup.find("div", class_="wgt-recommend ").find("div", class_="bd answer").find("pre",class_="recommend-text mb-10").text
        elif( soup.find("div", class_="wgt-recommend ").find("div", class_="bd answer").find("pre",class_="recommend-text expand-exp mb-10") != None ):
            bestanster = soup.find("div", class_="wgt-recommend ").find("div", class_="bd answer").find("pre",class_="recommend-text expand-exp mb-10").text
    else:
        bestanster = None

    if ( soup.find("div", class_="wgt-answers") != None ):
        otherDiv = soup.find("div", class_="wgt-answers")
        if(otherDiv.find("div", class_="bd answer answer-first    ") != None ):
            anster1 = otherDiv.find("div", class_="bd answer answer-first    ")\
            .find("pre", class_="answer-text mb-10").text
        elif(otherDiv.find("div", class_="bd answer answer-first   answer-fold ") != None ):
            anster1 = otherDiv.find("div", class_="bd answer answer-first   answer-fold ")\
            .find("pre", class_="answer-text mb-10").text
        else:
            anster1 = None
            anster2 = None
            anster3 = None
        if(otherDiv.find("div", class_="bd answer    answer-fold ") != None ):
                answerfold = otherDiv.find_all("div", class_="bd answer    answer-fold ")
                if( len(answerfold) >1 ):
                    anster2 = answerfold[0].find("pre", class_="answer-text mb-10").text
                    anster3 = answerfold[1].find("pre", class_="answer-text mb-10").text
                else:
                    anster2 = answerfold[0].find("pre", class_="answer-text mb-10").text
                    if(otherDiv.find("div", class_="bd answer  answer-last  answer-fold ") != None  ):
                        anster3 = otherDiv.find("div", class_="bd answer  answer-last  answer-fold ")\
                        .find("pre", class_="answer-text mb-10").text
                    elif(otherDiv.find("div", class_="bd answer  answer-last   ") != None ):
                        anster3 = otherDiv.find("div", class_="bd answer  answer-last   ")\
                        .find("pre", class_="answer-text mb-10").text
                    else:
                        anster3 = None
        elif(otherDiv.find("div", class_="bd answer     ") != None ):
                answerfold = otherDiv.find_all("div", class_="bd answer     ")
                if( len(answerfold) >1 ):
                    anster2 = answerfold[0].find("pre", class_="answer-text mb-10").text
                    anster3 = answerfold[1].find("pre", class_="answer-text mb-10").text
                else:
                    anster2 = answerfold[0].find("pre", class_="answer-text mb-10").text
                    if(otherDiv.find("div", class_="bd answer  answer-last  answer-fold ") != None ):
                        anster3 = otherDiv.find("div", class_="bd answer  answer-last  answer-fold ")\
                        .find("pre", class_="answer-text mb-10").text
                    elif(otherDiv.find("div", class_="bd answer  answer-last   ") != None ):
                        anster3 = otherDiv.find("div", class_="bd answer  answer-last   ")\
                        .find("pre", class_="answer-text mb-10").text
                    else:
                        anster3 = None
        elif(otherDiv.find("div", class_="bd answer  answer-last  answer-fold ") != None ):
            anster2 = otherDiv.find("div", class_="bd answer  answer-last  answer-fold ")\
            .find("pre", class_="answer-text mb-10").text
            anster3 = None
        else:
            anster2 = None
            anster3 = None
    else:
        anster1 = None
        anster2 = None
        anster3 = None
    if( ( id == None ) or ( questiontitle == None) or ( asktime == None) ):
        return 1
    p = ZhidaoQuestion(id = questionid,
                       questiontitle = questiontitle,
                       fulllquestion = fullquestion,
                       asktime = asktime,
                       bestanster = bestanster,
                       anster1 = anster1,
                       anster2 = anster2,
                       anster3 = anster3,
    )
    p.save()
    return 0

