'''
OPEN.PY: Kort beskrivning

__author__  = "Filip Nemlin"
__version__ = "1.0.0"
__email__   = "filip.nemlin@ga.ntig.se"
'''

import csv
import os
from time import sleep
from colors import bcolors


def load_data(filename): 
    """Laddar produktdata från en CSV-fil."""
    products = [] 
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = int(row['id'])
                name = row['name']
                desc = row['desc']
                price = float(row['price'])
                quantity = int(row['quantity'])
                
                products.append(        
                    {                    
                        "id": id,       
                        "name": name,
                        "desc": desc,
                        "price": price,
                        "quantity": quantity
                    }
                )
    except FileNotFoundError:
        print(f"Filen {filename} hittades inte.")
    return products


def truncate(text, length):
    """Avkortar text om den är längre än angiven längd."""
    return (text[:length] + "...") if len(text) > length else text


def __str__(self):
    truncated_name = truncate(self["name"], 35)  # Avkortning av namn
    truncated_desc = truncate(self["desc"], 40)  # Avkortning av beskrivning
    return f"{self['id']:<5} {truncated_name:<35} {truncated_desc:<40} {self['price']:<15.2f} {self['quantity']:<10}"


def remove_product(products, id):
    """Tar bort en produkt baserat på ID."""
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break

    if temp_product:
        products.remove(temp_product)
        return f"Produkt: {id} {temp_product['name']} togs bort."
    else:
        return f"Produkt med id {id} hittades inte."


def view_product(products, id):
    """Visar en produkt baserat på ID."""
    for product in products:
        if product["id"] == id:
            return f"Visar produkt: {product['name']} - {product['desc']} - {product['price']} kr - Antal: {product['quantity']}"
    return "Produkten hittas inte."


def view_products(products):  #Visar en tabell med alla produkter."""
    header = f"{'ID':<6} {'NAME':<26} {'DESCRIPTION':<51} {'PRICE':<15} {'QUANTITY':<10}"
    separator = "-" * 110  # linjen uppe
    

    rows = []
    for product in products:
        truncated_name = truncate(product["name"], 20)
        truncated_desc = truncate(product["desc"], 40)
        row = f"{product['id']:<6} {truncated_name:<26} {truncated_desc:<51} {product['price']:<15.2f} {product['quantity']:<10}"
        rows.append(row)
    

    inventory_table = "\n".join([header, separator] + rows)
    return inventory_table


def add_product(products, name, desc, price, quantity):  #Lägg till en ny produkt.
    if products:
        max_id = max(products, key=lambda x: x["id"])
        id_value = max_id["id"]
    else:
        id_value = 0

    id = id_value + 1

    products.append(
        {
            "id": id,       
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity
        }
    )
    return f"Lade till produkt: {id}"


os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('db_products.csv')

while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))  # Visa alla produkter

        choice = input(bcolors.GREEN + "Vill du (V)isa, (T)a bort, (L)ägga till eller (Ä)ndra en produkt? ").strip().upper()

        if choice == "L":  # Lägg till produkt
            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))
            print(add_product(bcolors.DEFAULT + products, name, desc, price, quantity))
            sleep(0.5)

        else:
            id = int(input("Ange produktens ID: "))

            if choice == "V":   # Visa produkt
                print(view_product(products, id))
                input("Tryck på enter för att fortsätta...")

            elif choice == "T": # Ta bort produkt
                print(remove_product(products, id))
                sleep(0.5)

            elif choice == "Ä": # Ändra produkt
                selected_product = next((product for product in products if product["id"] == id), None)
                if selected_product:
                    print("Skriv något nytt eller tryck enter direkt för att behålla det som var innan.")
                    selected_product['name'] = input(f"Nytt namn (behåll {selected_product['name']}): ") or selected_product['name']
                    selected_product['desc'] = input(f"Ny beskrivning (behåll {selected_product['desc']}): ") or selected_product['desc']
                    selected_product['price'] = float(input(f"Nytt pris (behåll {selected_product['price']}): ") or selected_product['price'])
                    selected_product['quantity'] = int(input(f"Nytt antal (behåll {selected_product['quantity']}): ") or selected_product['quantity'])

                    print(f"Produkten med id {selected_product['id']} uppdaterades.")
                    sleep(0.5)

                else:
                    print("Ogiltig produkt")
                    sleep(0.3)
        
    except ValueError:
        print("Välj en produkt med siffror")
        sleep(0.5)
