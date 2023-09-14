from pynput.mouse import Button, Controller
from pynput import mouse
import numpy as np
import time

mouse_controller = Controller()

clicked = False
def on_click(x, y, button, pressed) -> None:
    global clicked
    clicked = pressed


def get_coord(prompt: str) -> (int, int):
    print(prompt)
    while clicked == False:
        pass
    while clicked == True:
        pass
    mouse_position = mouse_controller.position
    print(mouse_position)
    return mouse_position


def get_document():
    global positions
    global clicked
    positions['referenceTL'] = get_coord("Click TOP LEFT (┌) corner of reference document")
    clicked = False
    positions['referenceBR'] = get_coord("Click BOTTOM RIGHT (┘) corner of reference document")
    clicked = False
    positions['actualTL'] = get_coord("Click TOP LEFT (┌) corner of actual document")
    clicked = False
    positions['actualBR'] = get_coord("Click BOTTOM RIGHT (┘) corner of actual document")
    clicked = False


def get_datums():
    global positions
    global clicked
    input('Click enter to continue to datum definition')
    positions['referenceDatum'] = get_coord("Click datum of the reference object")
    clicked = False
    positions['actualDatum'] = get_coord("Click datum of the actual object")
    clicked = False


def move_mouse():
    global positions
    global clicked
    # Calculations
    # Coordinates of the top-left corner and bottom-right corner of both documents
    ref_top_left = positions['referenceTL']
    clicked = False
    ref_bottom_right = positions['referenceBR']
    clicked = False

    actual_top_left = positions['actualTL']
    clicked = False
    actual_bottom_right = positions['actualBR']
    clicked = False

    # Point on the reference document
    ref_point = positions['referenceDatum']

    # Calculate scaling factors
    scale_x = (actual_bottom_right[0] - actual_top_left[0]) / (ref_bottom_right[0] - ref_top_left[0])
    scale_y = (actual_bottom_right[1] - actual_top_left[1]) / (ref_bottom_right[1] - ref_top_left[1])

    # Calculate translation vector
    translation_x = actual_top_left[0] - ref_top_left[0] * scale_x
    translation_y = actual_top_left[1] - ref_top_left[1] * scale_y

    # Apply the transformation to the reference point
    actual_point_x = ref_point[0] * scale_x + translation_x
    actual_point_y = ref_point[1] * scale_y + translation_y

    # Update the positions dictionary with the new actual coordinates
    new_actual_datum = (actual_point_x, actual_point_y)

    print("Await till' move; Please let go of mouse")

    for i in range(1):
        print(f'Move in {i}')
        time.sleep(1)

    mouse_controller.position = positions['actualDatum']
    time.sleep(0.1)
    mouse_controller.press(Button.left)
    time.sleep(0.1)
    mouse_controller.position = new_actual_datum
    time.sleep(0.1)
    mouse_controller.release(Button.left)


listener = mouse.Listener(
    on_click=on_click,)
listener.start()
# Getting positions
positions = {
    'referenceTL': (None, None),
    'referenceBR': (None, None),
    'actualTL': (None, None),
    'actualBR': (None, None),
    'referenceDatum': (None, None),
    'actualDatum': (None, None),
}
get_document()

while True:
    get_datums()
    move_mouse()


