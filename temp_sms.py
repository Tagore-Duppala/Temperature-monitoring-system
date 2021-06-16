import conf,json,time
from boltiot import Sms, Bolt
minimum_limit = 300
maximum_limit = 600


mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
#mailer = Email(conf.MAILGUN_API_KEY, conf.SANDBOX_URL, conf.SENDER_EMAIL, conf.RECIPIENT_EMAIL)


while True:
    print ("Reading sensor value")
    response = mybolt.analogRead('A0')
    data = json.loads(response)
    print("Sensor value is: " + str(data['value']))
    try:
        sensor_value = int(data['value'])
        mybolt.digitalWrite('3', 'LOW') 
        if sensor_value > maximum_limit or sensor_value < minimum_limit:
            print("Making request to Twilio to send a SMS")
            Temperature=(100*sensor_value)/1024 
            response = sms.send_sms("The Current temperature value is " +str(Temperature))
            print("Response received from Twilio is: " + str(response))
            print("Status of SMS at Twilio is :" + str(response.status))
            mybolt.digitalWrite('1', 'HIGH')
            mybolt.digitalWrite('3', 'HIGH')   
            print("Making request to Mailgun to send an email")
            #response = mailer.send_email("Alert", "The Current temperature sensor value is " +str(Temperature))
            response_text = json.loads(response.text)
            print("Response received from Mailgun is: " + str(response_text['message']))
    except Exception as e:
        print ("Error occured: Below are the details")
        print (e)
    time.sleep(10)