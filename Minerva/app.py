from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def main():
"""    server = Thread(target=job)
    server.start()
    server.join()"""
    return "Minerva update is running!"

def run():
    app.run(host="0.0.0.0", port=8080)
'''
def keep_alive():
    server = Thread(target=run)
    server.daemon = True
    server.start()
'''

def job():
    os.system('python gradeupdate.py')