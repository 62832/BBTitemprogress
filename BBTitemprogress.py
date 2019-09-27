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

def show_remaining(inventory):
    circles = [i for i in ITEMS['heads']['circle'] if i not in inventory]
    triangles = [i for i in ITEMS['heads']['triangle'] if i not in inventory]
    squares = [i for i in ITEMS['heads']['square'] if i not in inventory]
    cylinders = [i for i in ITEMS['heads']['cylinder'] if i not in inventory]
    stars = [i for i in ITEMS['heads']['special'] if i not in inventory]
    weapons = [i for i in ITEMS['weapons'] if i not in inventory]

    remaining = [circles, triangles, squares, cylinders, stars, weapons]
    remaining = ["All complete!" if not i else i for i in remaining]
    return remaining

if __name__ == '__main__':
    try:
        while True:
            try:
                user = input("Enter your Steam user ID (SteamID64): ")
                items = get_inventory(user)
                count = count_inventory(items)
                remaining = show_remaining(items)
                break
            except TypeError:
                print("Invalid ID.")

        print()
        print("Circle heads: {}/64".format(count[0]))
        print("Triangle heads: {}/64".format(count[1]))
        print("Square heads: {}/64".format(count[2]))
        print("Cylinder heads: {}/64".format(count[3]))
        print("Star heads: {}/64".format(count[4]))
        print("Weapons: {}/13".format(count[5]))
        print("\n")
        print("Remaining items:\n")
        print("Circles: {}\n".format(remaining[0]))
        print("Triangles: {}\n".format(remaining[1]))
        print("Squares: {}\n".format(remaining[2]))
        print("Cylinders: {}\n".format(remaining[3]))
        print("Stars: {}\n".format(remaining[4]))
        print("Weapons: {}".format(remaining[5]))
        print()
    except requests.exceptions.ConnectionError:
        print("No connection could be made, you might be offline.")

    system('pause')
