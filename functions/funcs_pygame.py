from defs_parameters import *
import pygame


def place_line_and_overlay(screen, location):
    draw_horizontal_line(screen, position_y=PX_HEIGHT_OFFSET)
    draw_vertical_line(screen, position_y=PX_HEIGHT_OFFSET)
    place_overlay(screen, location, alpha=125)


def place_text_msg(screen, msg, font_size, font_color, vertical_displacement=0):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(f"{msg}", True, font_color)
    location = center_text_horizontally(msg, font_size, vertical_displacement)
    screen.blit(text_surface, location)


def center_text_horizontally(msg, font_size, vertical_displacement):
    font = pygame.font.Font(None, font_size)
    text_width, text_height = font.size(msg)
    x_position = (SCREEN_WIDTH - text_width) // 2
    y_position = 50 + vertical_displacement
    return (x_position, y_position)


def scale_image_keep_ratio(img, new_width=None, new_height=None):
    w, h = img.get_size()
    if new_width is not None:
        scale = new_width / w
    elif new_height is not None:
        scale = new_height / h
    else:
        return img
    return pygame.transform.scale(img, (int(w * scale), int(h * scale)))


def load_icon(path, new_width=None, new_height=None):
    icon = pygame.image.load(path).convert_alpha()
    if new_width or new_height:
        icon = scale_image_keep_ratio(icon, new_width, new_height)
    return icon


def update_surface(object_id, pose):
    rotated = pygame.transform.rotate(object_id, pose[2])
    rectangle = rotated.get_rect(center=(pose[0], pose[1]))
    return rotated, rectangle


def place_icon_on_screen(screen, icon, pose):
    rotated, rect = update_surface(icon, pose)
    screen.blit(rotated, rect.topleft)


def get_interfaces_icons_positions_for_info(employed_interfaces):

    VERTICAL_DISPLACEMENT = 175

    y_left = PX_HEIGHT_OFFSET + PX_WS_HEIGHT // 2 - 50
    y_right = PX_HEIGHT_OFFSET + PX_WS_HEIGHT // 2 - 50

    lst_left_interfaces, lst_right_interfaces = [], []

    if employed_interfaces is not None:

        for name in employed_interfaces:
            revised_name = " ".join(word.capitalize() for word in name.split("_"))

            if "Left" in revised_name:
                lst_left_interfaces.append([revised_name, y_left])
                y_left = y_left + VERTICAL_DISPLACEMENT

            elif "Right" in revised_name:
                lst_right_interfaces.append([revised_name, y_right])
                y_right = y_right + VERTICAL_DISPLACEMENT

        return lst_left_interfaces, lst_right_interfaces

    else:
        return False


def get_icon_moving_object(interface):
    if interface == INTERFACES[0]["name"] or interface == 0:
        return DIR_ICN_LEFT_HAND, ICON_SCALING_HAND

    elif interface == INTERFACES[1]["name"] or interface == 1:
        return DIR_ICN_RIGHT_HAND, ICON_SCALING_HAND

    elif interface == INTERFACES[2]["name"] or interface == 2:
        return DIR_ICN_LEFT_FOOT, ICON_SCALING_FOOT

    elif interface == INTERFACES[3]["name"] or interface == 3:
        return DIR_ICN_RIGHT_FOOT, ICON_SCALING_FOOT

    else:
        return False


def get_icon_target_object(interface):
    if interface == INTERFACES[0]["name"] or interface == 0:
        return DIR_ICN_LEFT_HAND_TGT, ICON_SCALING_HAND

    elif interface == INTERFACES[1]["name"] or interface == 1:
        return DIR_ICN_RIGHT_HAND_TGT, ICON_SCALING_HAND

    elif interface == INTERFACES[2]["name"] or interface == 2:
        return DIR_ICN_LEFT_FOOT_TGT, ICON_SCALING_FOOT

    elif interface == INTERFACES[3]["name"] or interface == 3:
        return DIR_ICN_RIGHT_FOOT_TGT, ICON_SCALING_FOOT

    else:
        return False


def draw_horizontal_line(screen, position_y=PX_WS_HEIGHT // 3):
    pygame.draw.line(screen, BLACK, (0, position_y), (SCREEN_WIDTH, position_y), 4)


def draw_vertical_line(screen, position_x=PX_WS_WIDTH, position_y=PX_WS_HEIGHT // 3):
    pygame.draw.line(
        screen, BLACK, (position_x, position_y), (position_x, SCREEN_HEIGHT), 4
    )


def place_overlay(screen, location, alpha=125):
    # alpha=250 : not transparent
    if location == "top":
        rect = pygame.Rect(0, 0, SCREEN_WIDTH, PX_HEIGHT_OFFSET)

    elif location == "left":
        rect = pygame.Rect(0, PX_HEIGHT_OFFSET, PX_WS_WIDTH, PX_WS_HEIGHT)

    elif location == "right":
        rect = pygame.Rect(PX_WS_WIDTH, PX_HEIGHT_OFFSET, PX_WS_WIDTH, PX_WS_HEIGHT)

    overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    overlay.fill((180, 180, 180, alpha))
    screen.blit(overlay, rect.topleft)
