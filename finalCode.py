#!/usr/bin/env python3

#Use Comments
#Program Title: Moniter soil humidity
#Program Description: Send an email every three hours to report the condition of the soil and whether watering is required
#Name: Meng jintong
#Student ID: 202283890010    20110014
#Course and year: ProjectSmester 2025
#Date: 21/4/25

import RPi.GPIO as GPIO
import smtplib
import time
from email.message import EmailMessage

# ===== Sensor Configuration =====
SENSOR_PIN = 4         # GPIO4 (BCM numbering)
CHECK_INTERVAL = 3     # Check interval (hours)
status_map = {
    1: ("Water needed!", "[Alert] Plant needs water"),
    0: ("Moisture sufficient", "[OK] Plant status normal")
}

# ===== Email Configuration (163 example) =====
SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 25
SENDER_EMAIL = "19852895328@163.com"
SENDER_PASSWORD = "MPphAZGVA3mTDKsX"  # Authorization code
RECEIVER_EMAIL = "58866248@qq.com"

# ===== GPIO Initialization =====
def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    print("GPIO initialization completed")

# ===== Email Sending Function =====
def send_email(subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully")

    except Exception as e:
        print(f"Email sending failed: {str(e)}")

# ===== Main Program =====
if __name__ == "__main__":
    try:
        setup_gpio()
        check_interval = CHECK_INTERVAL * 3600  # Convert to seconds
        
        print(f"Plant monitoring system started, reporting every {CHECK_INTERVAL} hours...")
        
        while True:
            # Read sensor status
            current_status = GPIO.input(SENSOR_PIN)
            
            # Generate email content
            message, subject = status_map[current_status]
            email_body = f"""\
Detection time: {time.strftime('%Y-%m-%d %H:%M')}
Current status: {message}
Sensor reading: {'Dry' if current_status else 'Wet'}"""
            
            # Send status report
            send_email(subject, email_body)
            
            # Wait for next cycle
            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        GPIO.cleanup()
