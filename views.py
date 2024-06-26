from django.contrib.auth.models import User, auth
from django.contrib import messages
import pandas as pd
import csv
import os
import datetime
from .predict import prod
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
import home.models as homeling
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from twilio.rest import Client as Clientelle
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json
from django.templatetags.static import static
import base64
from heyoo import WhatsApp
from joblib import dump, load
import numpy as np
from django.contrib.auth.decorators import login_required
import logging
# Create your views here.

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

ngroklink = "https://8f48-197-221-232-182.ngrok-free.app/prediction"

account_sid = "ACd8e544bd7bc5d86eeb29419ec7cc9942"
auth_token = "246038c4fe422242d3a642ba9899bd46"
clientelle = Clientelle(account_sid, auth_token)

messenger = WhatsApp('EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD',  phone_number_id='115080538244848')

VERIFY_TOKEN = "23189345712"

head = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'}

def call():
    cally = clientelle.calls.create(
                        twiml='<Response><Say>Please Check the platform there is a client who is in distress!</Say></Response>',
                        to='+263774657905',
                        from_='+19083491055'
                    )

    print(cally.sid)

def getngroklink():

    settings = Settings.objects.get(pk=1)

    return settings.ngroklink

@login_required(login_url='login')
def home(request):
    patients = Client.objects.filter(clientType="Ordinary")

    doctors = Doctor.objects.all()

    doctors_count = doctors.count()

    patients_count = patients.count()

    user = request.user

    appointments = Appointment.objects.filter(user=user)

    appointment_count = appointments.count()

    context = {'user': user, 'doctors': doctors, 'doctors_count': doctors_count, 'patients_count': patients_count, 'appointment_count': appointment_count}

    return render(request, 'index.html', context)

def schedule(request):
    if request.method == 'POST':

        date =  request.POST.get('date')

        date = datetime.datetime.strptime(date, "%Y-%m-%d")

        calendarevents = MaternCalendar.objects.all()

        events = []

        user = request.user

        book = PatientSpecial.objects.create(user=user, start=date)

        book.save();

        """

        for matcal in calendarevents:

            matcal.save()

            if matcal.pk == 1:

                eventstart = date

                eventend = eventstart + timedelta(days=14)

                thisdict = {
                    "week" : matcal.week,
                    "body" : matcal.body.replace("'", ""),
                    "baby" : matcal.babydev.replace("'", ""),
                    "symptoms" : matcal.symptoms.replace("'", ""),
                    "tips" : matcal.tips.replace("'", ""),
                    "start":eventstart,
                    "end":eventend
                }

                events.append(thisdict)

            else:

                eventstart = date + timedelta(days=(7 * matcal.pk))

                eventend = eventstart + timedelta(days=7)

                thisdict = {
                    "week" : matcal.week,
                    "body" : matcal.body.replace("'", ""),
                    "baby" : matcal.babydev.replace("'", ""),
                    "symptoms" : matcal.symptoms.replace("'", ""),
                    "tips" : matcal.tips.replace("'", ""),
                    "start":eventstart,
                    "end":eventend

                }

                events.append(thisdict)"""

        events = serializers.serialize("json", MaternCalendar.objects.all())

        context = {'user': user, 'events': events, 'state':True, 'startDate': date}

        context = {'user': user, 'events': events, 'state':True}

        return render(request, 'schedule.html', context)

    else:

        user = request.user

        if PatientSpecial.objects.filter(user=user).first() != None:

            patientcheck = PatientSpecial.objects.get(user=user)

            calendarevents = MaternCalendar.objects.all()

            date = patientcheck.start

            events = []

            user = request.user
            """
            for matcal in calendarevents:


                if matcal.pk == 1:

                    eventstart = date

                    eventend = eventstart + timedelta(days=14)

                    thisdict = {

                    "week" : matcal.week,
                    "body" : matcal.body,
                    "baby" : matcal.babydev,
                    "symptoms" : matcal.symptoms,
                    "tips" : matcal.tips,
                    "start":eventstart,
                    "end":eventend

                }

                    events.append(thisdict)

                else:

                    eventstart = date + timedelta(days=(7 * matcal.pk))

                    eventend = eventstart + timedelta(days=7)

                    matcal.body = matcal.body.replace('"', '')

                    matcal.babydev = matcal.babydev.replace('"', '')

                    matcal.symptoms = matcal.symptoms.replace('"', '')

                    matcal.tips = matcal.tips.replace('"', '')

                    thisdict = {
                    "week" : matcal.week,
                    "body" : matcal.body,
                    "baby" : matcal.babydev,
                    "symptoms" : matcal.symptoms,
                    "tips" : matcal.tips,
                    "start":eventstart,
                    "end":eventend,

                }

                    events.append(thisdict)
            """
            #events = json.dumps(events, indent=4, sort_keys=True, default=str)

            events = serializers.serialize("json", MaternCalendar.objects.all())

            context = {'user': user, 'events': events, 'state':True, 'startDate': patientcheck.start}

            return render(request, 'schedule.html', context)

        else:
            context = {'user': user, 'state':False}

            return render(request, 'schedule.html', context)



def admin(request):
    return redirect('admin/')

def logout(request):

	auth.logout(request)

	return redirect('login')

def appointment_reg(request):
    user = request.user
    context = {'user': user}
    return render(request, 'Medilab/logs/appointments.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:

                auth.login(request, user)
                return redirect('home')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def meetTest(request, meetID):
    attempted_user = request.user
    booking = Appointment.objects.get(pk=meetID)
    context = {'booking': booking.id, 'attempted_user': attempted_user}
    return render(request, 'Medilab/logs/meetroom.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        location = request.POST['location']
        phone = request.POST['phone']
        email_address = request.POST['email_address']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if username == "" or first_name == "" or last_name == "" or location == "" or phone == "" or email_address == "" or password1 == "":
            messages.info(request, 'Incomplete registration details')
            return redirect('register')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email_address).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email_address, first_name=first_name, last_name=last_name, is_staff=False)
                user.save();
                client = Client.objects.create(user=user, location=location, phone=phone)
                client.save();
                return redirect('login')
    else:
        return render(request, 'register.html')


def appointment(request):
    if request.method == 'POST':
        message = request.POST['message']
        date =  request.POST['date']


        user = request.user
        book = Appointment.objects.create(message=message, date=date, user=user)
        book.save();
        user = request.user
        appointments = Appointment.objects.filter(user=user)
        context = {'appointments': appointments, 'user': user}
        return render(request, 'appointment.html', context)

    else:
            cli = Client.objects.get(user=request.user)
            if cli.clientType == "Doctor":


                user = request.user
                appointments = Appointment.objects.filter(user=user)
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentView.html', context)
            if cli.clientType == "Midwifery Nurse":

                user = request.user
                appointments = Appointment.objects.all()
                context = {'appointments': appointments, 'user': user}
                return render(request, 'Medilab/logs/appointmentViewAdmin.html', context)

            if cli.clientType == "Ordinary":

                user = request.user
                appointments = Appointment.objects.filter(user=user)
                context = {'appointments': appointments, 'user': user}
                return render(request, 'appointment.html', context)

def calling(request):
    call()
    return render(request, 'calling.html')


def appointmentAdmin(request):
    if request.method == 'POST':
        tag = request.POST['id']

        if Appointment.objects.get_or_create(animal=tag):
            status = request.POST['status']
            book = Appointment.objects.update_or_create(animal=tag, status=status)
            book.save()

    else:
        animal = Appointment.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/appointments_admin.html', context)

def sales(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']

        sale = Sales.objects.create(user=user, treatment=treatment)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/sales.html', context)

def salesAdmin(request):
    if request.method == 'POST':
        user = request.POST['user']
        treatment = request.POST['treatment']
        status = request.POST['status']

        sale = Sales.objects.create(user=user, treatment=treatment, status=status)
        sale.save();

    else:
        animal = Sales.objects.all()
        animal = {'treats': treats, 'user': user}
        return render(request, 'Medilab/logs/sales_admin.html', context)

def prediction(request):
    save_path = "saved_model/"
    model_name = "model"

    if request.method == 'POST':
        Age = request.POST['age']
        SystolicBP = request.POST['systolicBP']
        DiastolicBP = request.POST['diastolicBP']
        bs = request.POST['BS']
        bodytemp = request.POST['BodyTemp']

        report = Report.objects.create( user = request.user, age = Age, systolicBP = SystolicBP, diastolicBP = DiastolicBP, bs =bs, bodytemp = bodytemp)
        report.save();

        datobj = { "age": Age, "SystolicBP": SystolicBP, "DiastolicBP" : DiastolicBP, "bs": bs, "bodytemp": bodytemp}

        dataobject = [Age, SystolicBP, DiastolicBP, bs, bodytemp]

        result = prod(dataobject)


        suggestion = "Please click the button below to make a call, so that the doctors will respond to you shortly"

        if result == ['low']:
            suggestion ="Your symptoms shows you are at low risk, you can request for a call if you are in need for further assistance"

        context = {'result': result, 'suggestion' : suggestion}
        return render(request, 'emergency.html', context)
    else:

        return render(request, 'emergency.html')


class HelloView(APIView):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        print(incoming_message)


        sms(request)



        return HttpResponse()

@csrf_exempt
def linkupload(request, link):
    if request.method == 'GET':

        settings, _ = Settings.objects.get_or_create(pk=1)

        link = "https://" + link

        settings.ngroklink = link
        settings.save()

        return HttpResponse('OK')



        

        

@csrf_exempt
def sms(request):
    if request.method == 'POST':

        incoming_message = json.loads(request.body.decode('utf-8'))

        profile = ""
        print(incoming_message)
        print("the_incoming_message")
        income = incoming_message['entry']
        entry = income[-1]
        for message in entry['changes']:
            valu = message['value']

            if 'messages' in valu:

                for contactlist in valu['contacts']:

                    number = contactlist['wa_id']

                    profile = contactlist['profile']['name']

                for messag in valu['messages']:

                    if messag['type'] == 'text':

                        msg = messag['text']['body']





                        msgid = messag['id']

                        datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

                        logging.info(respo.text)
                        print(respo.text)



                        tabol(number, msg, profile)
                        return HttpResponse("OK")

                    if messag['type'] == 'image':

                        msg = messag['image']['caption']

                        msgid = messag['id']

                        media_id = messag['image']['id']

                        datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

                        logging.info(respo.text)
                        print(respo.text)

                        r = requests.get(f"https://graph.facebook.com/v14.0/{media_id}", headers=head)

                        print(r.json()["url"])


                        media_url = r.json()["url"]

                        r = requests.get(media_url, headers=head)

                        print(r)

                        img = r.content

                        #tabol(number, msg, profile, media_url)

                    if messag['type'] == 'interactive':

                        msgid = messag['id']

                        if messag['interactive']['type'] == 'list_reply':

                            msg = messag['interactive']['list_reply']['id']



                            datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                            respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

                            logging.info(respo.text)
                            print(respo.text)

                            tabol(number, msg, profile)
                        if messag['interactive']['type'] == 'button_reply':

                            msg = messag['interactive']['button_reply']['id']



                            datobj = {
                                  "messaging_product": "whatsapp",
                                  "status": "read",
                                  "message_id": msgid
                                }

                            respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

                            logging.info(respo.text)
                            print(respo.text)

                            tabol(number, msg, profile)


def tabol(number, mesg, profile, media=None):

    print("now here now")



    main = ("HI *"+ str(profile)+"* \n\nWelcome to Martenology Services CHATBOT \n\n"
        "Below is our main menu NB: Click the links below each category or section to get access to that section's menu \n\n ")

    watnum = number[3:]
    print(watnum)
    msg = mesg

    watnum = "0" + watnum

    print(watnum)

    member = Client.objects.filter(phone=watnum).first()



    print(member.phone)

    careerg = "careerguide"

    print(msg)
    msg = msg.lower()

    if str(msg) == "hi":

        if member is not None :


            print("Check Now")

            #respons = messenger.send_image(image="https://i.imgur.com/Fh7XVYY.jpeg", recipient_id=number,)
            #print(respons)

            datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                    "text": main
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "button": "Responces",
                    "sections": [
                        {
                        "title": "Menu",
                        "rows": [
                            {
                            "id": "predictionair",
                            "title": "Emergency Check",
                            "description": "Interms of not feeling well select this button"
                            },
                            {
                            "id": "appointair",
                            "title": "Appointments",
                            "description": "View or Book appointments with the infirmary",
                            },
                            {
                                "id": "calling",
                                "title": "Call",
                                "description": "Emergency Call"
                            }
                        ]
                        },

                    ]
                    }
                }
                }




            respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )
            logging.info(respo.text)
            print(respo.text)

            return HttpResponse("OK")

        else:

            #Change to default

            datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "list",
                    "body": {
                    "text": main
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "button": "Responces",
                    "sections": [
                        {
                        "title": "Menu",
                        "rows": [
                            {
                            "id": "predictionair",
                            "title": "Emergency Check",
                            "description": "Interms of not feeling well select this button"
                            },
                            {
                            "id": "appointair",
                            "title": "Appointments",
                            "description": "View or Book appointments with the infirmary",
                            },
                            {
                                "id": "calling",
                                "title": "Call",
                                "description": "Emergency Call"
                            }
                        ]
                        },

                    ]
                    }
                }
                }



            respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

            logging.info(respo.text)
            print(respo.text)

            return HttpResponse("OK")

    if "predictionair" in str(msg):

        repo = ("Please use this formart to enter this format \n\n age=25, systolicbp=130.0,\n diastolicbp=50.0, \n bs=7, \n bodytemp=39.9,\n ")

        datobj = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": repo
            }
            }

        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

        logging.info(respo.text)
        print(respo.text)

        return HttpResponse("OK")

    if "age=" in str(msg):
        msgstop = 0
        msgstart = msg.index("age=", msgstop)
        msgstop = msg.index(",", msgstart)
        msgRealStart = msgstart + 4
        msgRealStop = msgstop
        age = msg[msgRealStart:msgRealStop]

        print(age)

        msgsyststop = 0
        msgsyststart = msg.index("systolicbp=", msgsyststop)
        msgsyststop = msg.index(",", msgsyststart)
        msgRealStart = msgsyststart + 11
        msgRealStop = msgsyststop
        systolicbp = msg[msgRealStart:msgRealStop]

        print(systolicbp)

        msgdiaststop = 0
        msgdiaststart = msg.index("diastolicbp=", msgdiaststop)
        msgdiaststop = msg.index(",", msgdiaststart)
        msgRealStart = msgdiaststart + 12
        msgRealStop = msgdiaststop
        diastolicbp = msg[msgRealStart:msgRealStop]

        print(diastolicbp)

        msgbsstop = 0
        msgbsstart = msg.index("bs=", msgbsstop)
        msgbsstop = msg.index(",", msgbsstart)
        msgRealStart = msgbsstart + 3
        msgRealStop = msgbsstop
        bs = msg[msgRealStart:msgRealStop]

        print(bs)

        msgbodytempstop = 0
        msgbodytempstart = msg.index("bodytemp=", msgbodytempstop)
        msgbodytempstop = msg.index(",", msgbodytempstart)
        msgRealStart = msgbodytempstart + 9
        msgRealStop = msgbodytempstop
        bodytemp = msg[msgRealStart:msgRealStop]

        print(bodytemp)

        report = Report.objects.create( user = member.user, age = age, systolicBP = systolicbp, diastolicBP = diastolicbp, bs =bs, bodytemp = bodytemp)
        report.save()
        
        dataobject = [age, systolicbp, diastolicbp, bs, bodytemp]

        result = prod(dataobject)

        logging.info(result)

        suggestion = "It seems like you are not feeling well please press the below button to request for a call"

        if result == "['low']":
            suggestion ="It seems you are not feeling well please press the button below to reach out to our doctors"

        datobj = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": number,
                "type": "interactive",
                "interactive": {
                    "type": "button",
                    "body": {
                    "text": suggestion
                    },
                    "footer": {
                    "text": "Visit wenextafrica.org"
                    },
                    "action": {
                    "buttons": [
                            {
                            "type": "reply",
                            "reply": {
                                "id": "calling",
                                "title": "Call"
                            }
                            }
                        ]
                    }
                }
                }

        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

        logging.info(respo.text)
        print(respo.text)

        return HttpResponse("OK")

    if str(msg) == "calling":

        call()

        firstinfo = "call successfully requested, the doctor will call you soon\n\n "

        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

        logging.info(respo.text)
        print(respo.text)

        return HttpResponse("OK")



    if str(msg) == "animalis":

        animals = Animal.objects.all().filter(user=member.user)

        firstinfo = "View the listing of all the cattle you have registered \n\n "


        for animaly in animals:

            animalsingle= "Tag: "+ str(animaly.tag) + "," + "\n BREED: "+ animaly.breed   + "\n Sex: "+ animaly.sex  + "\n Weight: "+ str(animaly.weight)  + "\n Years: "+ animaly.years  + " \n\n"

            firstinfo = firstinfo + animalsingle



        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

        logging.info(respo.text)
        print(respo.text)

        return HttpResponse("OK")

    if str(msg) == "appointair":

        appointments = Appointment.objects.all().filter(user=member.user)

        firstinfo = "View the listing of all the appointments you have booked with the infirmary \n\n "

        for appointee in appointments:

            stat = ""

            if appointee.status == 1:
                stat = "approved"
            else:
                stat = "pending"

            appoinmentsingle= "Date: " + appointee.date + "\n Message: "+ appointee.message + "," + "\n Status: "+ stat   + " \n\n"

            firstinfo = firstinfo + appoinmentsingle



        datobj = {
              "messaging_product": "whatsapp",
              "recipient_type": "individual",
              "to": number,
              "type": "text",
              "text": {
                  "body": firstinfo
              }
              }

        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

        logging.info(respo.text)
        print(respo.text)

        return HttpResponse("OK")


    if str(msg) == "reciptair":
        receipts = Sales.objects.all().filter(user=member.user, paid=True)

        firstinfo = "View the listing of all the receipts \n\n "

        for receiptee in receipts:

            receiptsingle= "Animal Tag: " + str(receiptee.animal.tag) + "\n Date: "+ receiptee.date + "," + "\n Description: "+ receiptee.description   + "\n Treatment Name: " + receiptee.treatment.name   + "\n Cost: "+ str(receiptee.treatment.cost)  + " \n\n"

            firstinfo = firstinfo + receiptsingle

        datobj = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": firstinfo
            }
            }

        respo = requests.post('https://graph.facebook.com/v19.0/115080538244848/messages', json = datobj, headers = {'Authorization' : 'Bearer EAACqZAdInbjIBO45dHYKzDcbQl8CafIAhGmPza2bJkG78wDiZAEAF7OSvDauC3iZAlw3M9ZBs6H2th3ADKK3KCfPLMxqvKoVqZBlVFw6jrQO72WSn3xeSGJcYB2fLHmOnZARTZAihpPp9zBZCqPoKs2iOP25ENg8ig3We5DwAIx7eDIcSQJTfMZA790bISvZCtc5Iqm6Dmjo3RxHhhh0BHPIEZD'} )

        logging.info(respo.text)
        print(respo.text)

