import RPi.GPIO as gpio
import picamera
import time
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.image import MIMEImage
from datetime import datetime
import dlib


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
landmarks = predictor(img_gray, face)


 
from smbus2 import SMBus
from mlx90614 import MLX90614

time.sleep(0.5)
bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
print("Ambient Temperature :", sensor.get_ambient())
print("Object Temperature :", sensor.get_object_1())

temp = sensor.get_object_1()
bus.close()


newtemp=round(temp,2)
today = datetime.today ()
tday = today.strftime ("%m-%d-%Y")
now= datetime.now()
current_time=now.strftime("%H:%M:%S")

fromaddr = "beproject7421@gmail.com"
toaddr = "beproject7421@gmail.com"
 
mail = MIMEMultipart()

mail['From'] = fromaddr
mail['To'] = toaddr
mail['Subject'] = "New entry alert!!"
if temp < 38 and temp > 28:
body = "Entry alert: Please find the attached image, Person with temperature within the normal human body temperature range: "+ str(newtemp) +"°C and wearing a mask has entered the premises on "+str(tday)+" at "+str(current_time)+""
else:
body = "Do not allow the entrance of this person!! Please find the attached image, Person with temperature exceeding the normal human body temperature range: "+ str(newtemp) +"°C and wearing a mask is not to be given permission to enter the premises on "+str(tday)+" at "+str(current_time)+""

data="" 
def sendMail(data):
    mail.attach(MIMEText(body, 'plain'))
    print(data)
    dat='%s.jpg'%data
    print(data)
    attachment = open(dat, 'rb')
    image=MIMEImage(attachment.read())
    attachment.close()
    mail.attach(image)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "beproject")
    text = mail.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
 
def capture_image():
    data= time.strftime("%d_%b_%Y|%H:%M:%S")
    camera.start_preview()
    time.sleep(5)
    print(data)
    camera.capture('%s.jpg'%data)
    camera.stop_preview()
    time.sleep(1)
    sendMail(data)
 
camera = picamera.PiCamera()
camera.rotation=180
camera.awb_mode= 'auto'
camera.brightness=55
 





