#!/usr/bin/python3

import requests
import json
from os import system

REQUEST = "http://steamcommunity.com/inventory/<>/238460/2?l=english&count=500"
WALTER = "A collector of fine confections.  " # cylinder Walter description
EXCLUDE = ['Yarn Ball', 'Gems']

with open("items.json") as f:
    ITEMS = json.load(f)

def get_inventory(profile):
    request = REQUEST.replace("<>", profile)
    inventory = requests.get(request).json()['descriptions']

    ## two differently-shaped heads in the game are both named "Walter"
    for i in inventory:
        if i['descriptions'][0]['value'] == WALTER:
            i['name'] = "Walter [cylinder]"

    names = list(set([i['name'] for i in inventory]))
    return [i for i in names if i not in EXCLUDE]

def count_inventory(inventory):
    circles = triangles = squares = cylinders = stars = weapons = 0
    
    for i in inventory:
        if i in ITEMS['heads']['circle']:
            circles += 1
            
        if i in ITEMS['heads']['triangle']:
            triangles += 1

        if i in ITEMS['heads']['square']:
            squares += 1

        if i in ITEMS['heads']['cylinder']:
            cylinders += 1

        if i in ITEMS['heads']['special']:
            stars += 1

        if i in ITEMS['weapons']:
            weapons += 1

    return (circles, triangles, squares, cylinders, stars, weapons)

if __name__ == '__main__':
    user = input("Enter your Steam user ID (SteamID64): ")
    items = count_inventory(get_inventory(user))

    print("Circle heads: {}/64".format(items[0]))
    print("Triangle heads: {}/64".format(items[1]))
    print("Square heads: {}/64".format(items[2]))
    print("Cylinder heads: {}/64".format(items[3]))
    print("Star heads: {}/64".format(items[4]))
    print("Weapons: {}/13".format(items[5]))

    print("\nPress Enter to exit.")
    system('pause')
