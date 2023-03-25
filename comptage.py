import cv2
import pymongo
from pymongo import MongoClient
from datetime import datetime
import requests 






# Connection to MongoDB Atlas
client = MongoClient("mongodb+srv://sam:rfid@cluster0.dt27d.mongodb.net/?retryWrites=true&w=majority")

class comptage:
    stop,stop_2 = 1,1
     
    def send(self):
        requests.post('https://api.mynotifier.app', {
        "apiKey": 'b0ad018e-b4fa-4e6b-8977-ffcec28520f5', # à changer par votre propre clé
        "message": "Attention!!", 
        "description": "Vous faites attention un intrus a été detécté"})
    
        # Fonction d'incrémentation a utiliser quand y'a un intrus
    def incrementIntruders(self):
        db = client["AItruders"]
        collection = db["Count"]
        collection.update_one(
            {"_id":"IntrudersCount"},
            {"$inc":{"value":1}},
            upsert=True
        )
        counter = collection.find_one({"_id": "IntrudersCount"})
        print(f"Number of intruders: {counter['value']}")

    ######## Pour faire le comptage du nombre de travailleur a l'intérieur
    def incrementWorkers(self):
        db = client["AItruders"]
        collection = db["Count"]
        collection.update_one(
            {"_id":"WorkersCount"},
            {"$inc":{"value":1}},
            upsert=True
        )
        counter = collection.find_one({"_id": "WorkersCount"})
        print(f"Number of workers in site : {counter['value']}")

    def decrementWorkers(self):
        db = client["AItruders"]
        collection = db["Count"]
        collection.update_one(
            {"_id":"WorkersCount"},
            {"$inc":{"value":-1}},
            upsert=True
        )
        counter = collection.find_one({"_id": "WorkersCount"})
        print(f"Number of workers in site : {counter['value']}")


    ################### fonctions pour inserer des intrus ou travailleur dans la base de données(image +date)###################
    def addWorker(self):
       db = client["AItruders"]
       collection = db["Workers"]
       with open("worker.jpg", "rb") as f:
          picture_data = f.read()

       worker = collection.insert_one({"picture": picture_data,"Time": datetime.now()})
       print("Worker added in database with id : ", worker.inserted_id)

    def addIntruder(self):
       db = client["AItruders"]
       collection = db["Intruders"]
       with open("intruder.jpg", "rb") as f:
          picture_data = f.read()

       intruder = collection.insert_one({"picture": picture_data,"Time": datetime.now()})
       print("Intruder added in database with id : ", intruder.inserted_id)
    
    def counts(self,bbox_tensor,frame):
        global workers_in
        # Calculer le centre du bounding box selon l'axe OX
        if (len(bbox_tensor) > 0):
            moy = (bbox_tensor[0][0] + bbox_tensor[0][2]) / 2
            
            if (bbox_tensor[0][5] == 1):
                # Si un worker a été détécté + a dépassé la ligne
                if (moy < 220 and comptage.stop == 1):
                    cv2.imwrite('worker.jpg',frame)
                    comptage.addWorker(self)
                    comptage.incrementWorkers(self)
                    comptage.stop = 0
                    
                elif (moy > 220 and comptage.stop == 0):
                    comptage.stop = 1
                    comptage.decrementWorkers(self)
                
            elif (bbox_tensor[0][5] == 0):
                if (moy < 220 and comptage.stop_2 == 1):
                    print("un intru est rentré")
                    cv2.imwrite('intruder.jpg',frame)
                    comptage.send(self)
                    comptage.incrementIntruders(self)
                    comptage.addIntruder(self)
                    comptage.stop_2 = 0
                elif (moy > 220 and comptage.stop_2 == 0):
                    comptage.stop_2 = 1
                





