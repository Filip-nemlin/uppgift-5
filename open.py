import csv
import os
from time import sleep


def load_data(filename): 
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


def remove_product(products, id):
    temp_product = None

    for product in products:
        if product["id"] == id:
            temp_product = product
            break

    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"


def view_product(products, id):
    for product in products:
        if product["id"] == id:
            return f"Visar produkt: {product['name']} {product['desc']}"
    
    return "Produkten hittas inte"


def view_products(products):
    product_list = []
    for index, product in enumerate(products, 1):
        product_info = f"{index}) (#{product['id']}) {product['name']} \t {product['desc']} \t {product['price']:.2f} kr"
        product_list.append(product_info)
    
    return "\n".join(product_list)


def add_product(products, name, desc, price, quantity):
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
    return f"lade till produkt: {id}"


os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('db_products.csv')

while True:
    try:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(view_products(products))  # Visa alla produkter

        choice = input("Vill du (V)isa, (T)a bort, (L)ägga till eller (Ä)ndra en produkt? ").strip().upper()

        if choice == "L":  # Lägg till produkt
            name = input("Namn: ")
            desc = input("Beskrivning: ")
            price = float(input("Pris: "))
            quantity = int(input("Kvantitet: "))
            print(add_product(products, name, desc, price, quantity))
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

