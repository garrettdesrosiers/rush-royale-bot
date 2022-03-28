from pyautogui import *
import pyautogui
import time
import keyboard
import random
import cv2 as cv
import numpy as np

def game_is_over(screenshot):
    game_over_image = cv.imread('gameover.png')
    game_over_image = game_over_image[:,:,:3]
    screenshot_array = np.array(screenshot)
    screenshot_array = screenshot_array[:, :, ::-1].copy()
    result = cv.matchTemplate(screenshot_array, game_over_image, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    #print(str(max_loc))
    #print(str(max_val))
    threshold = 0.9
    locations = np.where(result >= threshold)
    if max_val > .9:
        return True
    return False

def find_character(name, board):
    char_image = cv.imread(name, cv.IMREAD_UNCHANGED)
    char_image = char_image[:,:,:3]
    result = cv.matchTemplate(board, char_image, cv.TM_CCOEFF_NORMED)
    threshold = 0.25
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    char_width = char_image.shape[1]
    char_height = char_image.shape[0]

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), char_width, char_height]
        rectangles.append(rect)
        rectangles.append(rect)
    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
    points = []
    for (x, y, w, h) in rectangles:
        center_x = x + int(w/2) + 818
        center_y = y + int(h/2) + 639
        points.append((center_x, center_y))
    #print(points)
    #print(weights)
    weightsdict = dict(zip(points, weights))
    #print(points)
    #print(weights)
    #print()
    points.sort(key=weightsdict.get)
    return points

def merge(pos1, pos2):
    pyautogui.moveTo(pos1[0], pos1[1])
    pyautogui.dragTo(pos2[0], pos2[1], .2, button='left')

def main():
    #open screen, allows for time to prepare window before running bot
    pyautogui.confirm(text='You are about to start Garrett\'s Rush Royale bot, make sure you have Rush Royale open in google chrome on a 1920x1080 pixel screen on windows. Rush Royale should be open to the home page. The bot will continuously run through co-op games. To quit, move the mouse to the upper right hand corner of the screen to close out the window. This will disable the bot. Would you like to continue?', title='', buttons=['Start Bot', 'Cancel'])

    #flag is true if new co-op game should be started
    #set to true at first, and reset to true when a game finishes
    new_game = True
    spawn_count = 0
    while keyboard.is_pressed('q') == False:

        #checks new_game
        if new_game == True:
            print("Starting new game.")
            pyautogui.click(x=1056, y=812)
            time.sleep(5)
            pyautogui.click(x=867, y=562)
            time.sleep(17)
            spawn_count = 0
            new_game = False

        #takes screenshot of whole screen
        screen = pyautogui.screenshot()

        #gets color of spawn button pixel
        spawn = screen.getpixel((966, 852))
        #if can spawn, spawn a new character
        levelone = screen.getpixel((767, 941))
        leveltwo = screen.getpixel((834, 942))
        levelthree = screen.getpixel((901, 940))
        levelfour = screen.getpixel((968, 942))
        levelfive = screen.getpixel((1035, 941))

        if not (spawn[0]==spawn[1]==spawn[2]==193):
            pyautogui.click(966, 852)
            spawn_count += 1

        #checks to see if level upgrade is available for each card in deck
        elif (levelone[2] > 250):
            pyautogui.click(778, 905)
        elif (leveltwo[2] > 250):
            pyautogui.click(847, 905)
        elif (levelthree[2] > 250):
            pyautogui.click(914, 905)
        elif (levelfour[2] > 250):
            pyautogui.click(983, 905)
        elif (levelfive[2] > 250):
            pyautogui.click(1048, 905)

        #clicks hero ability periodically
        hero = screen.getpixel((1132, 889))
        if hero[0] != hero[1]:
            pyautogui.click(1132, 889)

        #if more than 10 units spawned, begin to merge
        if spawn_count > 8:
            merge_screenshot = pyautogui.screenshot(region=(818, 639, 284, 164))
            merge_screenshot = np.array(merge_screenshot)
            merge_screenshot = merge_screenshot[:, :, ::-1].copy()
            Executioners = find_character('Executioner.png', merge_screenshot)
            #print('Executioners')
            #print(Executioners)
            if Executioners != None and len(Executioners) > 2:
                print("Merging Executioners")
                merge(Executioners[0], Executioners[1])
            Corsairs = find_character('Corsair.png', merge_screenshot)
            #print('Corsairs')
            #print(Corsairs)
            if Corsairs != None and len(Corsairs) > 2:
                print("Merging Corsairs")
                merge(Corsairs[0], Corsairs[1])
            Crystalmancers = find_character('Crystalmancer.png', merge_screenshot)
            #print('Crystalmancers')
            #print(Crystalmancers)
            if Crystalmancers != None and len(Crystalmancers) > 2:
                print("Merging Crystalmancers")
                merge(Crystalmancers[0], Crystalmancers[1])
            Frosts = find_character('Frost.png', merge_screenshot)
            #print('Frosts')
            #print(Frosts)
            if Frosts != None and len(Frosts) > 2:
                print("Merging Frosts")
                merge(Frosts[0], Frosts[1])
            Bombardiers = find_character('Bombardier.png', merge_screenshot)
            #print('Bombardiers')
            #print(Bombardiers)
            if Bombardiers != None and len(Bombardiers) > 2:
                print("Merging Bombardiers")
                merge(Bombardiers[0], Bombardiers[1])
        #check to see if game is over
        if game_is_over(screen) == True:
            print("Game is over.")
            spawn_count = 0
            new_game = True
            time.sleep(5)
            pyautogui.click(960, 900)
            time.sleep(5)
            pyautogui.click(960, 900)
            time.sleep(5)
            pyautogui.click(960, 900)
            time.sleep(15)

if __name__ == '__main__':
    main()
