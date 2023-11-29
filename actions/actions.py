from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import sqlite3
from add_db import write, morph

# 903347596 - my id
# rasa run -m models -p 5005 --connector telegram --credentials credentials.yml --debug

#write()


class ActionGiveClothes(Action):
    def name(self) -> Text:
        return "action_give_clothes"

    def run(self, dispatcher, tracker, domain):

        location = "Moscow"
        user_id = tracker.sender_id
        with open("copy.txt", "w") as file:
            file.write(str(user_id))
        if user_id == "1391324215":
            dispatcher.utter_message("")
        else:
            api_key = "7cec94224d571b7551b886f5cf636525"
            city = "Moscow"
            url = f"http://api.openweathermap.org/data/2.5/weather?lat=55.45&lon=37.36&appid={api_key}"
            response = requests.get(url)
            data = response.json()

            # Extract the weather and temperature information from the API response
            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]

            # Determine the clothing recommendation based on the weather and temperature
            temperature = temperature - 273.15

            if temperature > 25:
                clothes = "Футболка и легкие брюки или шорты,юбка"
            elif temperature > 20:
                clothes = "Футболка и легие джинсы или брюки"
            elif temperature > 15:
                clothes = "Джинсовка или толстовка и джинсы"
            elif temperature > 10:
                clothes = "Легкая куртка,футболка и джинсы"
            elif temperature > 5:
                clothes = "Куртка, кофта и джинсы"
            elif temperature > 0:
                clothes = "Куртка, кофта и теплые джинсы или брюки"
            elif temperature > -5:
                clothes = "Куртка, толстовка, футболка и теплые брюки или джинсы"
            elif temperature > -10:
                clothes = "Теплая зимняя куртка, кофта и теплые брюки или джинсы"
            elif temperature > -15:
                clothes = "Теплая зимняя куртка, толстовка и теплые брюки или джинсы, шапка"
            elif temperature > -20:
                clothes = "Теплая зимняя куртка, толстовка, футболка и теплые брюки или джинсы, шапка и перчатки"
            elif temperature > -25:
                clothes = "Теплая зимняя куртка, толстовка, футболка и теплые брюки или джинсы, шапка и перчатки"
            else:
                clothes = "может не выходить из дома?"
            if "rain" in weather:
                clothes = clothes + "нужен зонт"

            # Pass the weather and clothing recommendation to the chatbot response
            dispatcher.utter_message(clothes + " при температуре " + str(int(temperature)))

        return []


class ActionRecClothes(Action):
    def name(self):
        return "action_rec_clothes"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        clothes = tracker.get_latest_entity_values("clothes")
        clothes = str(next(clothes))
        clothes = morph.parse(clothes)[0].normal_form


        with sqlite3.connect('clothes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "SELECT id, clothes_2 FROM Clothes WHERE clothes_name = ?",
                (clothes,)
            )
            res = curs.fetchone()

            (clothes_id, clothes_2) = res
            curs.execute("INSERT INTO User (user_id, clothes_id) VALUES (?, ?)", (user_id, clothes_id))
            if clothes_2:
                dispatcher.utter_message(clothes_2)
            else:
                dispatcher.utter_message("Извините, не знаю что подобрать")
        return []


class ActionShowHistory(Action):
    def name(self):
        return "action_show_history"

    def run(self, dispatcher, tracker, domain):
        user_id = tracker.sender_id
        history = []
        history1= []
        with sqlite3.connect('clothes.db') as conn:
            curs = conn.cursor()
            curs.execute(
                "SELECT clothes_name FROM User INNER JOIN clothes ON User.clothes_id = Clothes.id WHERE User.user_id = ?",
                (user_id,)
            )
            (history) = curs.fetchall()
            if history:
                for el in history:
                    for i in el:
                        dispatcher.utter_message("".join(str(i)))
            else:
                dispatcher.utter_message("История пуста")
        return []
