import logging

from psychopy import logging as psycholog
from termcolor import colored

psycholog.console.setLevel(logging.CRITICAL)
import numpy as np
from random import randint
import pandas as pd
from psychopy import visual, core, event, monitors
from time import time
from pylsl import StreamInfo, StreamOutlet, local_clock
from glob import glob
from random import choice
import os

os.system('color')
from datetime import datetime
import argparse

import requests
import json
import shutil

from record import record_experiment
from threading import Thread

VERSION = '1.0beta'
API = 'fbAD8zoM5cmkTLrWgbPcprVO5Y9KfgE13ZhAt7xRF1E'

def printInfo(string):
    print(colored('[!] ' + string, 'yellow'))


def printError(string):
    print(colored('[!] ' + string, 'red'))


def printSuccess(string):
    print(colored('[!] ' + string, 'green'))


def main():
    banner = """
            ██████╗  ██████╗██╗   ████████╗███████╗ ██████╗ 
            ██╔══██╗██╔════╝██║   ╚══██╔══╝██╔════╝██╔════╝ 
            ██████╔╝██║     ██║█████╗██║   █████╗  ██║  ███╗
            ██╔══██╗██║     ██║╚════╝██║   ██╔══╝  ██║   ██║
            ██████╔╝╚██████╗██║      ██║   ██║     ╚██████╔╝
            ╚═════╝  ╚═════╝╚═╝      ╚═╝   ╚═╝      ╚═════╝ 
                                Eduardo López Bernal
    """
    print(colored(banner, 'yellow'))

    parser = argparse.ArgumentParser(description='Obtaining EEG signal. Running the experiment.', add_help=False)

    parser.add_argument('-n', '--name', dest='name',
                        default="exp_{}".format(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")),
                        help='Experiment name')
    parser.add_argument('-dim', '--dim', dest='size_monitor', default=[1920, 1080],
                        help='Size monitor (default [1920,1080])')
    parser.add_argument('-dm', '--distmon', dest='distance_monitor', default=67,
                        help='Distance to the monitor -in centimeters- (default 67)')
    parser.add_argument('-m', '--mode', dest='mode', default=2,
                        help='Program execution mode (default 2)')
    parser.add_argument('-i', '--images', dest='images', default=200,
                        help='Number of different images used in the experiment (default 200)')
    parser.add_argument('-ph', '--photos', dest='photos', default=30,
                        help='Number of images to download in each iteration (default 30)')
    parser.add_argument('-tt', dest='target_time', default=5,
                        help='Target display time -in seconds- (default 5)')
    parser.add_argument('-io', dest='image_offset', default=1,
                        help='Offset time of each image -in seconds- (default 1)')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + VERSION, help="Program version.")
    parser.add_argument('-a', '--about', action='version',
                        version='Created by Eduardo López Bernal',
                        help="Information about the creator of the program.")
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Help on using the program.')

    args = parser.parse_args()

    mode = args.mode
    total_img = int(args.images)
    photos = int(args.photos)
    photos_last_iteration = 11
    size_monitor = args.size_monitor
    distance_monitor = int(args.distance_monitor)

    diccionary = {}

    if(os.path.isfile('urls_Marivi.txt')):
        with open('urls_Marivi.txt') as f:
            for line in f:
                line = line[0:11]
                diccionary[line] = 1

    try:

        experiment = "Marivi_15"

        if not os.path.isdir('experiments/' + experiment):
            os.makedirs("experiments/{}/target".format(experiment))
            os.makedirs("experiments/{}/no_target".format(experiment))
            os.makedirs("experiments/{}/records".format(experiment))

        if not os.listdir('experiments/{}/target'.format(experiment)) or not os.listdir(
                'experiments/{}/no_target'.format(experiment)):
            if (mode == 1):
                printInfo("Mode 1 selected (Manual mode)")

            elif (mode == 2):
                printInfo("Mode 2 selected (Automatic mode)")
                printInfo("Download resources...")
                count = 0
                repeated = 0
                is_target = False

                for i in range(6):
                    print("i = {}".format(i))
                    if i != 5:
                        url_all = "https://api.unsplash.com/photos/random?count={}".format(photos)
                    else:
                        url_all = "https://api.unsplash.com/photos/random?count={}".format(photos_last_iteration)

                    headers = {
                        'orientation': 'landscape',
                        'Authorization': 'Client-ID {}'.format(API)
                    }

                    response = requests.get(url_all, headers=headers, stream=True)

                    response_json = json.loads(response.text)

                    for image in response_json:
                        url = image['urls']['raw']
                        identification = image['id']
                        
                        if identification in diccionary:
                            repeated = repeated + 1

                        else:
                            diccionary[identification] = 1

                            with open('urls_Marivi.txt', 'a+') as f:
                                f.write(identification + '\n')

                            response = requests.get(url + '&fm=jpg&fit=crop&w=1920&h=1080&q=80&fit=max', headers=headers,
                                                stream=True)

                            if not is_target:
                                with open('experiments/{}/target/target.jpeg'.format(experiment), 'wb') as out_file:
                                    shutil.copyfileobj(response.raw, out_file)
                                is_target = True
                                continue

                            with open('experiments/{}/no_target/no_target_{}.jpeg'.format(experiment, count),
                                      'wb') as out_file:
                                shutil.copyfileobj(response.raw, out_file)
                            del response

                            count = count + 1
                            
                while(repeated != 0):
                    url_all = "https://api.unsplash.com/photos/random?count={}".format(repeated)

                    response = requests.get(url_all, headers=headers, stream=True)

                    response_json = json.loads(response.text)

                    for image in response_json:
                        url = image['urls']['raw']
                        identification = image['id']

                        if identification in diccionary:
                            continue

                        else:
                            diccionary[identification] = 1

                            with open('urls_Marivi.txt', 'a+') as f:
                                f.write(identification + '\n')

                            response = requests.get(url + '&fm=jpg&fit=crop&w=1920&h=1080&q=80&fit=max', headers=headers,
                                                        stream=True)

                            if not is_target:
                                with open('experiments/{}/target/target.jpeg'.format(experiment), 'wb') as out_file:
                                    shutil.copyfileobj(response.raw, out_file)
                                is_target = True
                                continue 

                            with open('experiments/{}/no_target/no_target_{}.jpeg'.format(experiment, count),
                                      'wb') as out_file:
                                shutil.copyfileobj(response.raw, out_file)
                            del response

                            count = count + 1

                            repeated = repeated - 1

        image_offset = float(args.image_offset)
        target_time = int(args.target_time)

        experiment_time = 213.0
        process = Thread(target=record_experiment, args=[experiment, experiment_time])
        process.start()

        printInfo("Experiment name: " + experiment)
        printInfo("Screen dimensions: width={} | heigth={}".format(size_monitor[0], size_monitor[1]))
        printInfo("Experiment route: experiments/{}".format(experiment))
        printInfo("Approximate duration of the experiment: " + str(experiment_time) + " s")
        printInfo("Target pre-experiment display time: " + str(target_time * 1000) + " ms")
        printInfo("Display time of each image: " + str(image_offset) + " s")

        try:
            images = pd.read_csv('experiments/{}/metadata.txt'.format(experiment))

        except:
            printError("Metadata not found, creating random metadata...")

            img_types = np.zeros(total_img)

            number_of_1 = 40
            add = False

            while (number_of_1 != 0):
                position = randint(0, len(img_types)-1)

                if(position == 0 and img_types[position] == 0 and img_types[position+1] == 0):
                    add = True

                elif(position == len(img_types) - 1 and img_types[position] == 0 and img_types[position-1] == 0):
                    add = True

                elif(position != 0 and position != len(img_types) - 1 and img_types[position] == 0 and img_types[position-1] == 0 and img_types[position + 1] == 0):
                    add = True
                    
                if(add == True):
                    img_types[position] = 1
                    number_of_1 = number_of_1 - 1

                add = False

            images = pd.DataFrame(dict(img_type=img_types,
                                       timestamp=np.zeros(total_img)))
            images.to_csv('experiments/{}/metadata.txt'.format(experiment), index=False)


        print()
        printInfo("DataFrame generated: ")
        print()
        print(images)
        print()

        mon = monitors.Monitor('benq')
        mon.setDistance(distance_monitor)
        window = visual.Window(size_monitor, monitor=mon, units="pix",
                              fullscr=False, color=[-1, -1, -1])

        def cargarImagen(file):
            nonlocal window
            return visual.ImageStim(win=window, image=file, size=size_monitor)

        targets = []
        no_targets = []

        t_argets = glob('experiments/{}/target/*.jpeg'.format(experiment))
        for i in t_argets:
            targets.append(cargarImagen(i))

        not_argets = glob('experiments/{}/no_target/*.jpeg'.format(experiment))
        for i in not_argets:
            no_targets.append(cargarImagen(i))

        text1 = visual.TextBox(window=window,
                               text='[Eduardo López Bernal]',
                               font_size=20,
                               font_color=[1, 1, 1],
                               textgrid_shape=[55, 2],
                               pos=(0.0, 0.6),
                               # border_color=[-1, -1, 1, 1],
                               # border_stroke_width=4,
                               # grid_color=[1, -1, -1, 0.5],
                               # grid_stroke_width=1
                               )

        text2 = visual.TextBox(window=window,
                               text='Press <enter> to start the experiment...',
                               font_size=20,
                               font_color=[1, 1, 1],
                               textgrid_shape=[48, 2],
                               pos=(0.0, 0.3),
                               # border_color=[-1, -1, 1, 1],
                               # border_stroke_width=4,
                               # grid_color=[1, -1, -1, 0.5],
                               # grid_stroke_width=1
                               )

        text3 = visual.TextBox(window=window,
                               text='End of the experiment...',
                               font_size=20,
                               font_color=[1, 1, 1],
                               textgrid_shape=[55, 2],
                               pos=(0.0, 0.6),
                               # border_color=[-1, -1, 1, 1],
                               # border_stroke_width=4,
                               # grid_color=[1, -1, -1, 0.5],
                               # grid_stroke_width=1
                               )

        text4 = visual.TextBox(window=window,
                               text='¡Thank you for participating!',
                               font_size=20,
                               font_color=[1, 1, 1],
                               textgrid_shape=[48, 2],
                               pos=(0.0, 0.3),
                               # border_color=[-1, -1, 1, 1],
                               # border_stroke_width=4,
                               # grid_color=[1, -1, -1, 0.5],
                               # grid_stroke_width=1
                               )
        logo_umu = visual.ImageStim(win=window, image="experiments/umu.jpg", units='pix')
        logo_umu.pos += -0.3
        logo_umu.size = [610, 140]

        text1.draw()
        text2.draw()
        logo_umu.draw()

        window.flip()

        key = event.waitKeys()
        while ('return' not in key):
            key = event.waitKeys()

        core.wait(3)

        target = choice(targets)
        target.draw()
        window.flip()
        core.wait(target_time)
        window.flip()

        info = StreamInfo('stimulus', 'stimulus', 1, 0, 'int32', 'stimulus12310')

        outlet = StreamOutlet(info)

        nImage = 0
        nTarget = 0
        nNoTarget = 0
        core.wait(2)
        for i, trial in images.iterrows():
            img_type = images['img_type'].iloc[i]
            image = choice(targets if img_type == 1 else no_targets)
            if(image in no_targets):
                no_targets.remove(image)
                
            nImage = nImage + 1
            if img_type == 1:
                nTarget = nTarget + 1
            else:
                nNoTarget = nNoTarget + 1

            image.draw()
            timestamp = local_clock()
            images.at[i, 'timestamp'] = timestamp

            outlet.push_sample([2 if img_type == 0 else 1], timestamp)
            window.flip()

            core.wait(image_offset)

            if event.getKeys() == 'Esc':
                printError('Canceling experiment...')
                break
            event.clearEvents()

        core.wait(1.5)
        text3.draw()
        text4.draw()
        window.flip()
        core.wait(5)

        window.close()
        process.join()

        print()
        printSuccess('---------------------------------------------')
        printSuccess("Experiment data in: experiments/{}".format(experiment))
        printSuccess('---------------------------------------------')
        printSuccess('Experiment finished')
        printSuccess("Number of images displayed: " + str(nImage))
        printSuccess("Number of Target images displayed: " + str(nTarget))
        printSuccess("Number of Non-Target images displayed: " + str(nNoTarget))
        printSuccess('---------------------------------------------')
        print()
        printInfo("Final DataFrame: ")
        print()
        print(images)

        core.quit()

    except KeyboardInterrupt:
        printError('Canceling experiment...')
        window.close()
        core.quit()


if __name__ == '__main__':
    main()
