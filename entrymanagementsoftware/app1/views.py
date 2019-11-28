from django.shortcuts import *
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.core.mail import *
import datetime

import requests
import json
from app1.models import *


def mainpageshow(req):
    #checking if checkout session exist or not
    try:
        a = req.session["checkout"]
        del req.session["checkout"]
        req.session.modified = True
        return render(req,'app1/mainpage.html',{"success":"You are successfully checked-out"})
    except:
        #checking if checkIn sesson exist or not
        try:
            del req.session["checkin"]
            req.session.modified = True
            return render(req,'app1/mainpage.html',{"success":"You are successfully checked-In. Please remember your Email id for checkout"})
        except:
            return render(req,'app1/mainpage.html',{})
        

def checkin(req):
    if(req.method=="POST"):
        # Fetchng value from form ]=p
        guestName = req.POST.get("guestName")
        guestEmail = req.POST.get("guestEmail")
        guestMobile = req.POST.get("guestMobileNo")  
        hostName = req.POST.get("hostName")
        hostEmail = req.POST.get("hostEmail")
        hostMobile = req.POST.get("hostMobileNo")
        current_time = timeInStandardform()

        #This try is for checking if a visitor who is already checkedIn tries to checkin again which is discarded without doing operation
        try:
            visitor = Meeting.objects.get(guestemail=guestEmail,isCheckOut=False)
            return render(req,'app1/EntryDetail.html',{"error":"The Person with this credentials is already CheckedIn"})
        except:

            # This try is for checking correct credentials like mail and mobile is entered or not
            try:

                #SENDING EMAIL
                subject = 'There is a visitor for you ' + hostName
                message = "Visitor's Detail :\n" + "Name - " +guestName + "\n"+ "Email -" + guestEmail + "\n" + "Phone -" +guestMobile + "\n"+"Checkin Time - "+ current_time
                from_email = settings.EMAIL_HOST_USER
                to_list = [str(hostEmail),]
                send_mail(subject,message,from_email,to_list,fail_silently=False)

                #sending sms
                URL = 'https://www.way2sms.com/api/v1/sendCampaign'
                response = sendPostRequest(URL, 'USE_YOUR_OWN_WAY2SMS_API_KEY', 'USE_YOUR_OWN_WAY@SMS_SECRET_KEY', 'stage', hostMobile, 'USE_YOUR_WAY2SMS_USERID', message )
                

                #storing vlue in database
                a = Meeting(guestname=guestName,guestemail=guestEmail,guestmobileNo=guestMobile,hostname=hostName,hostemail=hostEmail,hostmobileNo=hostMobile,checkInTime=current_time,isCheckOut=False)
                a.save()
                
                #creating session so that appropriate succes message can be seen on mainpage 
                # after being redirected to http://127.0.0.1:8000/. This session is deleted as soon as
                #http://127.0.0.1:8000/page is rendered.

                req.session["checkin"] = guestEmail
                return redirect('http://127.0.0.1:8000/')

            except:
                return render(req,'app1/EntryDetail.html',{"error":"The entered emailid is invalid . Please fill the form again"})
    else:
        return render(req,'app1/EntryDetail.html')

def checkout(req):
    if(req.method=="POST"):
        email = req.POST.get("email")
        try:
            #checking if person wih entered email check-In or not
            a = Meeting.objects.get(guestemail=email,isCheckOut=False)
            current_time = timeInStandardform()
            a.isCheckOut = True
            a.checkOutTime = current_time
            a.save()
            
            #sending email to guest on check-out
            address = "221B Baker Street London"
            subject = 'Summary of your Visit'
            message = "Detail of visit :\nName - " +a.guestname + "\nPhone -" + a.guestmobileNo + "\nCheck-in Time - "+ a.checkInTime + "\nCheck-out time - "+a.checkOutTime+"\nHostname - "+a.hostname+"\nAddress - "+address
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(a.guestemail),]
            send_mail(subject,message,from_email,to_list,fail_silently=False)

            #sending sms to guest on check-out
            URL = 'https://www.way2sms.com/api/v1/sendCampaign'
            response = sendPostRequest(URL, 'USE_YOUR_OWN_WAY2SMS_API_KEY', 'USE_YOUR_OWN_WAY@SMS_SECRET_KEY', 'stage', a.hostmobileNo, 'USE_YOUR_WAY2SMS_USERID', message )
            print(response)
            # creating session to show success check-out message upon redirected to mainpage.
            # This sesson is deleted as soon as http://127.0.0.1:8000/ url is redirected
            req.session["checkout"] = email
            return redirect("http://127.0.0.1:8000/")

        except:
            return render(req,'app1/checkout.html',{"error":"The person with this email didn't check-in .Please enter your check-in registered email"})
    else:
        return render(req,'app1/checkout.html',{})

#function to calculate the current time in standard from as per the requirement of the problem
def timeInStandardform():
    current_hour = datetime.datetime.now().time().hour
    current_minute = datetime.datetime.now().time().minute
    current_time = ""
    if(current_minute>9):
        current_minute = str(current_minute)
    else:
        current_minute = "0"+ str(current_minute)
    if(current_hour>12):
        current_hour -= 12
        current_time +=str(current_hour)+":"+current_minute+" PM IST"
    else:
        current_time +=str(current_hour)+":"+current_minute+" AM IST"

    return current_time

#function to send sms
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
    print("hello")
    req_params = {
        'apikey':apiKey,
        'secret':secretKey,
        'usetype':useType,
        'phone': phoneNo,
        'message':textMessage,  
        'senderid':senderId
        }
    return requests.post(reqUrl, req_params)
