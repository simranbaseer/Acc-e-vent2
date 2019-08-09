import paho.mqtt.client as Cli
import sqlite3
import time
import string
import random
from datetime import datetime
broker = 'postman.cloudmqtt.com'
port = 10601
user = 'velofqbk'
password = 'uy4FH4uiHP8i'
client = Cli.Client('client2')
conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()


def add(msg):
    ls = msg.split(',')
    #check authentication - if uid exists for the mid and time >unique for an> event
    cur.execute('select event_id from student_event_details where mid=? and datetime('now') >= start_time and datetime('now')<=end_time;',(ls[1]))
    eid = cur.fetchone()
    #enter into visitor log
    cur.execute('insert into student_visitor_log(uid,mid,event_id,time) values(?,?,?,?);', (ls[0], ls[1],eid, datetime.now()))
    #extract uid from tag
    cur.execute('select tag from student_event_details where event_id =?;',eid)
    sel = cur.fetchone()
    ls2 = sel.split(',')
    #checking if uid is allowed for current event
    for i in ls2:
        if (ls2[i] == ls[0]):
            print("Authorized entry")
            flag = 0
            client.publish('CheckIn2',payload=flag)
            cur.execute('update student_visitor_log set attempt =? where uid=? and event_id=?;',(flag,ls[0],eid))
        else:
            print("Unauthorized Entry")
            flag =1
            client.publish('CheckIn2',payload=flag)
            cur.execute('update student_visitor_log set attempt=? where uid=? and event_id=?;',(flag,ls[0],eid))
            #get client's id
            cur.execute('select client_id from student_event_details where mid=? and event_id=?;'(ls[1],eid))
            #send alert to client using email id

def on_connect(client, userdata, flags, rc):
    print('Subscribing')
    client.subscribe("checkIn")
    time.sleep(2)


def on_message(client, userdata, message):
    msg = str(message.payload.decode('UTF-8'))
    print('Message received ', msg)
    add(msg)
    conn.commit()






client.on_connect=on_connect
client.on_message=on_message
client.username_pw_set(user, password)
client.connect(broker, port=port)
client.loop_forever()
