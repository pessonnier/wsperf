from fastapi import FastAPI
import time
import asyncio
import threading
import multiprocessing

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/plus1/{num}')
async def plus1(num):
    try:
        return { 'value': str(int(num)+1) }
    except:
        return {"message": "paramètre invalide"}

@app.get('/mult/')
async def mult(a:int, b:int):
    return { 'value': str(int(a)*int(b)) }

# consomme du temps mais pas de ressources CPU
@app.get('/pause/{temps}')
async def pause(temps:int):
    await asyncio.sleep(temps)
    return { 'message': 'ok' }

# consomme du temps en appel bloquant mais pas de ressources CPU
@app.get('/pause_sync/{temps}')
def pause_sync(temps:int):
    time.sleep(temps)
    return { 'message': 'ok' }

# consomme du CPU pendant un temps donné
def cpu(stop):
    cpt=0
    while True:
        if stop():
            return
        cpt+=1

@app.get('/cpu/{threads}/{temps}')
async def cpu_thread(threads:int, temps:float):
    debut = time.time()
    signal_stop = False
    ths=[ threading.Thread(target = cpu, name ='cpu_'+ str(i), args =(lambda : signal_stop, )) for i in range(threads) ]
    [ t.start() for t in ths ]
    time.sleep(temps)
    signal_stop = True
    [ t.join() for t in ths ]
    duree = time.time()-debut
    return { 'message': 'ok', 'duree': str(duree) }

def cpux(threads):
    ths=[ threading.Thread(target = cpu, name ='cpu_'+ str(i), args =(lambda : False, )) for i in range(threads) ]
    [ t.start() for t in ths ]

@app.get('/cpux/{proc}/{threads}/{temps}')
async def cpu_proc(proc:int, threads:int, temps:int):
    debut = time.time()
    signal_stop = False
    prs=[ multiprocessing.Process(target = cpux, name ='cpu_'+ str(i), args =(threads, )) for i in range(proc) ]
    [ p.start() for p in prs ]
    time.sleep(temps) # TODO à comparer avec await asyncio.sleep(temps)
    [ p.terminate() for p in prs ]
    [ p.join() for p in prs ]
    duree = time.time()-debut
    return { 'message': 'ok', 'duree': str(duree) }

# retourne un volume de données spécifié
@app.get('/blabla/{long}')
async def blabla(long:int):
    return { 'message': 'o'*long }

# traite beaucoup de paramètres REST
# curl -X 'GET' \
#   'http://127.0.0.1:8000/param_rest/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a' \
#   -H 'accept: application/json'
# http://127.0.0.1:8000/param_rest/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a/a

@app.get('/param_rest/{p0}/{p1}/{p2}/{p3}/{p4}/{p5}/{p6}/{p7}/{p8}/{p9}/{p10}/{p11}/{p12}/{p13}/{p14}/{p15}/{p16}/{p17}/{p18}/{p19}/{p20}/{p21}/{p22}/{p23}/{p24}/{p25}/{p26}/{p27}/{p28}/{p29}')
async def param_rest(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29):
    tas = p0+p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20+p21+p22+p23+p24+p25+p26+p27+p28+p29
    return { 'message': 'ok', 'long': len(tas) }

# traite beaucoup de paramètres dans l'URL
# curl -X 'GET' \
#   'http://127.0.0.1:8000/param_url/?p0=a&p1=a&p2=a&p3=a&p4=a&p5=a&p6=a&p7=a&p8=a&p9=a&p10=a&p11=a&p12=a&p13=a&p14=a&p15=a&p16=a&p17=a&p18=a&p19=a&p20=a&p21=a&p22=a&p23=a&p24=a&p25=a&p26=a&p27=a&p28=a&p29=a' \
#   -H 'accept: application/json'
# http://127.0.0.1:8000/param_url/?p0=a&p1=a&p2=a&p3=a&p4=a&p5=a&p6=a&p7=a&p8=a&p9=a&p10=a&p11=a&p12=a&p13=a&p14=a&p15=a&p16=a&p17=a&p18=a&p19=a&p20=a&p21=a&p22=a&p23=a&p24=a&p25=a&p26=a&p27=a&p28=a&p29=a

@app.get('/param_url/')
async def param_url(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29):
    tas = p0+p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20+p21+p22+p23+p24+p25+p26+p27+p28+p29
    return { 'message': 'ok', 'long': len(tas) }

# traite beaucoup de paramètres dans la charge (payload)
@app.post('/param_url/')
async def param_url(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29):
    tas = p0+p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20+p21+p22+p23+p24+p25+p26+p27+p28+p29
    return { 'message': 'ok', 'long': len(tas) }

from pydantic import BaseModel
from typing import Optional, Dict, List
from fastapi import Header, Cookie, Response

class Fiche(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post('/fiche/')
async def fiche(fiche:Fiche):
    return fiche

class Niv3(BaseModel):
    a: str
    b: str
    value: List[str]

class Niv2(BaseModel):
    p0: Niv3
    p1: Niv3
    p2: Niv3
    p3: Niv3
    p4: Niv3
    value: List[str]

class Niv1(BaseModel):
    p0: Niv2
    p1: Niv2
    p2: Niv2
    p3: Niv2
    p4: Niv2
    value: List[str]

@app.post("/imbrique/")
async def imbrique(racine: Niv1):
    return racine.p1.p2.value

# curl -X 'POST' \
#   'http://127.0.0.1:8000/mesures/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '[
#   0, 2,3,5,6,8,7,5,7,1,7,8,5,12,4
# ]'
@app.post("/mesures/")
async def mesures(mes: List[float]):
    return { 'message': 'ok', 'long': len(mes) }

# curl -X 'POST' \
#   'http://127.0.0.1:8000/mesures_numerotees/' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "1": 7,
#   "2": 8,
#   "3": 9
# }'
@app.post("/mesures_numerotees/")
async def mesures_numerotees(mes: Dict[int, float]):
    return { 'message': 'ok', 'long': len(mes) }

class Reponse(BaseModel):
    re_info: str = Header(None)
    un_cookie: str = Cookie(None)
    message: str
    value: str

@app.get("/reponse/{message}")
async def reponse(message, info, cookie, r : Response):
    r.headers['X-info'] = info
    r.set_cookie(key='un_cookie', value= cookie)
    return {'message': 'ok', 'value': message}

@app.get("/reponse2/{message}", response_model= Reponse)
async def reponse(message, info, cookie):
    return {'message': 'ok', 'value': message, 're_info': info, "un_cookie": cookie}

'''
@app.get('/param_rest/{p0}/{p1}/{p2}/{p3}/{p4}/{p5}/{p6}/{p7}/{p8}/{p9}/{p10}/{p11}/{p12}/{p13}/{p14}/{p15}/{p16}/{p17}/{p18}/{p19}/{p20}/{p21}/{p22}/{p23}/{p24}/{p25}/{p26}/{p27}/{p28}/{p29}/{p30}/{p31}/{p32}/{p33}/{p34}/{p35}/{p36}/{p37}/{p38}/{p39}/{p40}/{p41}/{p42}/{p43}/{p44}/{p45}/{p46}/{p47}/{p48}/{p49}/{p50}/{p51}/{p52}/{p53}/{p54}/{p55}/{p56}/{p57}/{p58}/{p59}/{p60}/{p61}/{p62}/{p63}/{p64}/{p65}/{p66}/{p67}/{p68}/{p69}/{p70}/{p71}/{p72}/{p73}/{p74}/{p75}/{p76}/{p77}/{p78}/{p79}/{p80}/{p81}/{p82}/{p83}/{p84}/{p85}/{p86}/{p87}/{p88}/{p89}/{p90}/{p91}/{p92}/{p93}/{p94}/{p95}/{p96}/{p97}/{p98}/{p99}/{p100}/{p101}/{p102}/{p103}/{p104}/{p105}/{p106}/{p107}/{p108}/{p109}/{p110}/{p111}/{p112}/{p113}/{p114}/{p115}/{p116}/{p117}/{p118}/{p119}/{p120}/{p121}/{p122}/{p123}/{p124}/{p125}/{p126}/{p127}/{p128}/{p129}/{p130}/{p131}/{p132}/{p133}/{p134}/{p135}/{p136}/{p137}/{p138}/{p139}/{p140}/{p141}/{p142}/{p143}/{p144}/{p145}/{p146}/{p147}/{p148}/{p149}/{p150}/{p151}/{p152}/{p153}/{p154}/{p155}/{p156}/{p157}/{p158}/{p159}/{p160}/{p161}/{p162}/{p163}/{p164}/{p165}/{p166}/{p167}/{p168}/{p169}/{p170}/{p171}/{p172}/{p173}/{p174}/{p175}/{p176}/{p177}/{p178}/{p179}/{p180}/{p181}/{p182}/{p183}/{p184}/{p185}/{p186}/{p187}/{p188}/{p189}/{p190}/{p191}/{p192}/{p193}/{p194}/{p195}/{p196}/{p197}/{p198}/{p199}')
async def param_rest(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,p31,p32,p33,p34,p35,p36,p37,p38,p39,p40,p41,p42,p43,p44,p45,p46,p47,p48,p49,p50,p51,p52,p53,p54,p55,p56,p57,p58,p59,p60,p61,p62,p63,p64,p65,p66,p67,p68,p69,p70,p71,p72,p73,p74,p75,p76,p77,p78,p79,p80,p81,p82,p83,p84,p85,p86,p87,p88,p89,p90,p91,p92,p93,p94,p95,p96,p97,p98,p99,p100,p101,p102,p103,p104,p105,p106,p107,p108,p109,p110,p111,p112,p113,p114,p115,p116,p117,p118,p119,p120,p121,p122,p123,p124,p125,p126,p127,p128,p129,p130,p131,p132,p133,p134,p135,p136,p137,p138,p139,p140,p141,p142,p143,p144,p145,p146,p147,p148,p149,p150,p151,p152,p153,p154,p155,p156,p157,p158,p159,p160,p161,p162,p163,p164,p165,p166,p167,p168,p169,p170,p171,p172,p173,p174,p175,p176,p177,p178,p179,p180,p181,p182,p183,p184,p185,p186,p187,p188,p189,p190,p191,p192,p193,p194,p195,p196,p197,p198,p199):
    tas = p0+p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20+p21+p22+p23+p24+p25+p26+p27+p28+p29+p30+p31+p32+p33+p34+p35+p36+p37+p38+p39+p40+p41+p42+p43+p44+p45+p46+p47+p48+p49+p50+p51+p52+p53+p54+p55+p56+p57+p58+p59+p60+p61+p62+p63+p64+p65+p66+p67+p68+p69+p70+p71+p72+p73+p74+p75+p76+p77+p78+p79+p80+p81+p82+p83+p84+p85+p86+p87+p88+p89+p90+p91+p92+p93+p94+p95+p96+p97+p98+p99+p100+p101+p102+p103+p104+p105+p106+p107+p108+p109+p110+p111+p112+p113+p114+p115+p116+p117+p118+p119+p120+p121+p122+p123+p124+p125+p126+p127+p128+p129+p130+p131+p132+p133+p134+p135+p136+p137+p138+p139+p140+p141+p142+p143+p144+p145+p146+p147+p148+p149+p150+p151+p152+p153+p154+p155+p156+p157+p158+p159+p160+p161+p162+p163+p164+p165+p166+p167+p168+p169+p170+p171+p172+p173+p174+p175+p176+p177+p178+p179+p180+p181+p182+p183+p184+p185+p186+p187+p188+p189+p190+p191+p192+p193+p194+p195+p196+p197+p198+p199
    return { 'message': 'ok', 'long': len(tas) }

@app.get('/param_url/')
async def param_url(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,p31,p32,p33,p34,p35,p36,p37,p38,p39,p40,p41,p42,p43,p44,p45,p46,p47,p48,p49,p50,p51,p52,p53,p54,p55,p56,p57,p58,p59,p60,p61,p62,p63,p64,p65,p66,p67,p68,p69,p70,p71,p72,p73,p74,p75,p76,p77,p78,p79,p80,p81,p82,p83,p84,p85,p86,p87,p88,p89,p90,p91,p92,p93,p94,p95,p96,p97,p98,p99,p100,p101,p102,p103,p104,p105,p106,p107,p108,p109,p110,p111,p112,p113,p114,p115,p116,p117,p118,p119,p120,p121,p122,p123,p124,p125,p126,p127,p128,p129,p130,p131,p132,p133,p134,p135,p136,p137,p138,p139,p140,p141,p142,p143,p144,p145,p146,p147,p148,p149,p150,p151,p152,p153,p154,p155,p156,p157,p158,p159,p160,p161,p162,p163,p164,p165,p166,p167,p168,p169,p170,p171,p172,p173,p174,p175,p176,p177,p178,p179,p180,p181,p182,p183,p184,p185,p186,p187,p188,p189,p190,p191,p192,p193,p194,p195,p196,p197,p198,p199):
    tas = p0+p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20+p21+p22+p23+p24+p25+p26+p27+p28+p29+p30+p31+p32+p33+p34+p35+p36+p37+p38+p39+p40+p41+p42+p43+p44+p45+p46+p47+p48+p49+p50+p51+p52+p53+p54+p55+p56+p57+p58+p59+p60+p61+p62+p63+p64+p65+p66+p67+p68+p69+p70+p71+p72+p73+p74+p75+p76+p77+p78+p79+p80+p81+p82+p83+p84+p85+p86+p87+p88+p89+p90+p91+p92+p93+p94+p95+p96+p97+p98+p99+p100+p101+p102+p103+p104+p105+p106+p107+p108+p109+p110+p111+p112+p113+p114+p115+p116+p117+p118+p119+p120+p121+p122+p123+p124+p125+p126+p127+p128+p129+p130+p131+p132+p133+p134+p135+p136+p137+p138+p139+p140+p141+p142+p143+p144+p145+p146+p147+p148+p149+p150+p151+p152+p153+p154+p155+p156+p157+p158+p159+p160+p161+p162+p163+p164+p165+p166+p167+p168+p169+p170+p171+p172+p173+p174+p175+p176+p177+p178+p179+p180+p181+p182+p183+p184+p185+p186+p187+p188+p189+p190+p191+p192+p193+p194+p195+p196+p197+p198+p199
    return { 'message': 'ok', 'long': len(tas) }

@app.post('/param_url/')
async def param_url(p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p30,p31,p32,p33,p34,p35,p36,p37,p38,p39,p40,p41,p42,p43,p44,p45,p46,p47,p48,p49,p50,p51,p52,p53,p54,p55,p56,p57,p58,p59,p60,p61,p62,p63,p64,p65,p66,p67,p68,p69,p70,p71,p72,p73,p74,p75,p76,p77,p78,p79,p80,p81,p82,p83,p84,p85,p86,p87,p88,p89,p90,p91,p92,p93,p94,p95,p96,p97,p98,p99,p100,p101,p102,p103,p104,p105,p106,p107,p108,p109,p110,p111,p112,p113,p114,p115,p116,p117,p118,p119,p120,p121,p122,p123,p124,p125,p126,p127,p128,p129,p130,p131,p132,p133,p134,p135,p136,p137,p138,p139,p140,p141,p142,p143,p144,p145,p146,p147,p148,p149,p150,p151,p152,p153,p154,p155,p156,p157,p158,p159,p160,p161,p162,p163,p164,p165,p166,p167,p168,p169,p170,p171,p172,p173,p174,p175,p176,p177,p178,p179,p180,p181,p182,p183,p184,p185,p186,p187,p188,p189,p190,p191,p192,p193,p194,p195,p196,p197,p198,p199):
    tas = p0+p1+p2+p3+p4+p5+p6+p7+p8+p9+p10+p11+p12+p13+p14+p15+p16+p17+p18+p19+p20+p21+p22+p23+p24+p25+p26+p27+p28+p29+p30+p31+p32+p33+p34+p35+p36+p37+p38+p39+p40+p41+p42+p43+p44+p45+p46+p47+p48+p49+p50+p51+p52+p53+p54+p55+p56+p57+p58+p59+p60+p61+p62+p63+p64+p65+p66+p67+p68+p69+p70+p71+p72+p73+p74+p75+p76+p77+p78+p79+p80+p81+p82+p83+p84+p85+p86+p87+p88+p89+p90+p91+p92+p93+p94+p95+p96+p97+p98+p99+p100+p101+p102+p103+p104+p105+p106+p107+p108+p109+p110+p111+p112+p113+p114+p115+p116+p117+p118+p119+p120+p121+p122+p123+p124+p125+p126+p127+p128+p129+p130+p131+p132+p133+p134+p135+p136+p137+p138+p139+p140+p141+p142+p143+p144+p145+p146+p147+p148+p149+p150+p151+p152+p153+p154+p155+p156+p157+p158+p159+p160+p161+p162+p163+p164+p165+p166+p167+p168+p169+p170+p171+p172+p173+p174+p175+p176+p177+p178+p179+p180+p181+p182+p183+p184+p185+p186+p187+p188+p189+p190+p191+p192+p193+p194+p195+p196+p197+p198+p199
    return { 'message': 'ok', 'long': len(tas) }

print(','.join([ 'p'+ str(i) for i in range(200) ]))
print('/'.join([ '{p'+ str(i)+'}' for i in range(200) ]))
print('+'.join([ 'p'+ str(i) for i in range(200) ]))
print('\n'.join([ 'p'+ str(i)+': Niv3' for i in range(5) ]))

'''

# un décorateur qui utilise signal pour limiter le temps d'execution d'une fonction
'''
import time
import signal

class TimeoutException(Exception):   # Custom exception class
    pass


def break_after(seconds=2):
    def timeout_handler(signum, frame):   # Custom signal handler
        raise TimeoutException
    def function(function):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                res = function(*args, **kwargs)
                signal.alarm(0)      # Clear alarm
                return res
            except TimeoutException:
                print u'Oops, timeout: %s sec reached.' % seconds, function.__name__, args, kwargs
            return
        return wrapper
    return function
'''
