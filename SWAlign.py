from SWAlign.HIDControl import get_document_dimensions, get_datum_locations, move_mouse
import numpy as np
import inquirer
import time
import os

def main():
    # Document dimensions
    positions = {
        'referenceTL': (None, None),
        'referenceBR': (None, None),
        'actualTL': (None, None),
        'actualBR': (None, None),
    }

    # All UI past this point
    questions = [
    inquirer.List('behaviour',
                    message='Select program behaviour?',
                    choices=['Move after datum selection', 'Move after datum selection (no break)', 'Move after mass selection'],
                ),
    ]
    positions = get_document_dimensions(positions)
    os.system('cls' if os.name == 'nt' else 'clear')

    answers = inquirer.prompt(questions)
    match answers['behaviour']:
        case 'Move after datum selection':
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                input('Click enter to continue to datum definition')
                try:
                    datum_locations = get_datum_locations()
                except KeyboardInterrupt:
                    print("User interrupt detected!")
                    continue
                print("Await till' move; Please let go of mouse")
                print(f'Move in 2')
                time.sleep(2)
                move_mouse(datum_locations['referenceDatum'], datum_locations['actualDatum'], positions)

        case 'Move after datum selection (no break)':
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                try:
                    datum_locations = get_datum_locations()
                except KeyboardInterrupt:
                    print("User interrupt detected!")
                    input('Click enter to continue to datum definition')
                    continue
                print("Await till' move; Please let go of mouse")
                print(f'Move in 2')
                time.sleep(2)
                move_mouse(datum_locations['referenceDatum'], datum_locations['actualDatum'], positions)

        case 'Move after mass selection':
            while True:
                datum_coordinates = []
                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('ctrl+c to continue to movement')
                    if len(datum_coordinates) != 0:
                        print(f'Current positions:   {datum_coordinates[0]}')
                        for i, e in enumerate(datum_coordinates):
                            if i == 0:
                                continue
                            print(f'                     {datum_coordinates[i]}')
                    try:
                        datum_locations = get_datum_locations()
                        datum_coordinates.append((datum_locations['referenceDatum'], datum_locations['actualDatum']))
                    except KeyboardInterrupt:
                        print('User interrupt detected!')
                        print('Please return to live document')
                        seconds_to_wait = 10
                        for i in np.arange(seconds_to_wait)[::-1] + 1:
                            print(f'Moving {i} seconds...', end='\r')
                            time.sleep(1)
                        break
                for datum in datum_coordinates:
                    move_mouse(datum[0], datum[1], positions)
                    time.sleep(0.25)


if __name__ == '__main__':
    main()