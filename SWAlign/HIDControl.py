from pynput.mouse import Button, Controller
from pynput.keyboard import Key
from pynput.keyboard import Controller as KeyController
from pynput import mouse
import time


def click_detected(x, y, button, pressed) -> None:
    global clicked
    clicked = pressed

keyboard_controller = KeyController()
mouse_controller = Controller()
clicked = False
listener = mouse.Listener(
    on_click=click_detected,)
listener.start()


def get_mouse_coordinates(prompt: str) -> (int, int):
    global clicked
    global mouse_controller
    print(prompt)
    while clicked == False:
        pass
    while clicked == True:
        pass
    mouse_position = mouse_controller.position
    print(mouse_position)
    clicked = False
    return mouse_position


def get_document_dimensions(positions):
    global clicked
    positions['referenceTL'] = get_mouse_coordinates("Click TOP LEFT (┌) corner of reference document")
    positions['referenceBR'] = get_mouse_coordinates("Click BOTTOM RIGHT (┘) corner of reference document")
    positions['actualTL'] = get_mouse_coordinates("Click TOP LEFT (┌) corner of actual document")
    positions['actualBR'] = get_mouse_coordinates("Click BOTTOM RIGHT (┘) corner of actual document")
    return positions


def get_datum_locations() -> dict:
    global positions
    global clicked
    referenceDatum = get_mouse_coordinates("Click datum of the reference object")
    actualDatum = get_mouse_coordinates("Click datum of the actual object")
    return {
        'referenceDatum':referenceDatum ,
        'actualDatum':actualDatum,
    }


def move_mouse(datum_reference:(int, int), datum_actual:(int, int), positions:dict) -> None:
    global clicked
    global mouse_controller
    
    # Calculations
    # Coordinates of the top-left corner and bottom-right corner of both documents
    ref_top_left = positions['referenceTL']
    ref_bottom_right = positions['referenceBR']

    actual_top_left = positions['actualTL']
    actual_bottom_right = positions['actualBR']

    # Point on the reference document
    ref_point = datum_reference

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


    mouse_controller.position = datum_actual
    keyboard_controller.press(Key.alt)
    time.sleep(0.1)
    mouse_controller.press(Button.left)
    time.sleep(0.1)
    mouse_controller.position = new_actual_datum
    time.sleep(0.1)
    mouse_controller.release(Button.left)
    keyboard_controller.release(Key.alt)
    