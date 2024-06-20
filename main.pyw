import dearpygui.dearpygui as dpg
import requests
from threading import Thread
from inspect import stack
from os.path import dirname, abspath
from os import getenv

import locale
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
dpg.create_context()

app_path: str = dirname(
    abspath(stack()[0].filename)
).removesuffix('\\PyInstaller\\loader').removesuffix('\\_internal')
print(app_path)


def parce_http():
    city_name = dpg.get_value('city_name')
    API = getenv('OPENWEATHER_WeatherForecast_API')  # the error has been accounted for
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city_name.lower().capitalize()}&appid={API}&units=metric"
    try:
        res = requests.get(URL).json()
    except Exception as err:
        dpg.set_value('img', er_data)
        return err
    print(res)
    if res['cod'] in {'400', '440', '430'}:
        dpg.set_value('temp', res['cod'])
        dpg.set_value('img', er_data)
        return
    
    match res['clouds']['all']:
        case x if 0 <= x <= 10:
            dpg.set_value('sit', 'Clearly')
            # self.icon.setPixmap(QtGui.QPixmap("img/sun.png"))
            dpg.set_value('img', sun_data)
        case x if 11 <= x <= 39:
            dpg.set_value('sit', 'Mostly Sunny')
            # self.icon.setPixmap(QtGui.QPixmap("img/sunny.png"))
            dpg.set_value('img', sny_data)
        case x if 40 <= x <= 60:
            dpg.set_value('sit', 'Mostly Cloudy')
            # self.icon.setPixmap(QtGui.QPixmap("img/sunny.png"))
            dpg.set_value('img', sny_data)
        case x if 61 <= x <= 100:
            dpg.set_value('sit', 'Cloudy')
            # self.icon.setPixmap(QtGui.QPixmap("img/sky.png"))
            dpg.set_value('img', sky_data)
    
    dpg.set_value('vis', f"visibility: {res['visibility']}")
    
    dpg.set_value('temp', f"{res['main'].setdefault('temp', 'N-F')}")
    dpg.set_value(
        'min_max',
        f"min: {res['main'].setdefault('temp_min', 'N-F')} max:  {res['main'].setdefault('temp_max', 'N-F')}"
    )
    
    dpg.set_value('f_l', f"feels like: {res['main'].setdefault('feels_like', 'N-F')}")
    
    dpg.set_value('wind', f"wind speed: {res['wind'].setdefault('speed', 'N-F')} m/s")
    
    match res['wind'].setdefault('deg', None):
        case x if (340 <= x <= 359) or (0 <= x <= 20):
            dpg.set_value('deg', 'degr: N')
        case x if 21 <= x <= 70:
            dpg.set_value('deg', 'degr: NV')
        case x if 71 <= x <= 111:
            dpg.set_value('deg', 'degr: V')
        case x if 112 <= x <= 160:
            dpg.set_value('deg', 'degr: SV')
        case x if 161 <= x <= 201:
            dpg.set_value('deg', 'degr: S')
        case x if 202 <= x <= 250:
            dpg.set_value('deg', 'degr: SW')
        case x if 251 <= x <= 290:
            dpg.set_value('deg', 'degr: W')
        case x if 291 <= x <= 339:
            dpg.set_value('deg', 'degr: NW')
        case None:
            dpg.set_value('deg', 'N-F')
    
    dpg.set_value('gust', f"gust: {res['wind'].setdefault('gust', 'N-F')}")


def set_w_data():
    Thread(target=parce_http).start()


def drag_handle(sender, data):
    if dpg.is_item_hovered(main_win):
        dpg.set_viewport_width(dpg.get_viewport_width())
        dpg.set_viewport_height(dpg.get_viewport_height())
        p = dpg.get_viewport_pos()
        dpg.set_viewport_pos((p[0] + data[1], p[1] + data[2]))


def exit():
    global running
    running = False


""" Инициализация Dear PyGui """
dpg.create_context()
running = True
""" ОБРАБОТКА НАЖАТИЙ """
with dpg.handler_registry():
    dpg.add_mouse_drag_handler(callback=drag_handle)

""" Загрузка TEXTURES """
with dpg.texture_registry():
    tb_width, tb_height, _, tb_data = dpg.load_image(f"{app_path}/presets/ico.png")
    
    img_width, img_height = 512, 512
    
    _, _, _, er_data = dpg.load_image(f"{app_path}/presets/error.png")
    _, _, _, ld_data = dpg.load_image(f"{app_path}/presets/load.png")
    
    _, _, _, sky_data = dpg.load_image(f"{app_path}/presets/sky.png")
    _, _, _, sun_data = dpg.load_image(f"{app_path}/presets/sun.png")
    _, _, _, sny_data = dpg.load_image(f"{app_path}/presets/sunny.png")
    _, _, _, cd_data = dpg.load_image(f"{app_path}/presets/cloud.png")
    dpg.add_static_texture(width=tb_width, height=tb_height, default_value=tb_data, tag="main_ico")
    dpg.add_dynamic_texture(img_width, img_height, ld_data, tag='img')

""" Загрузка SysFonts """
with dpg.font_registry():
    arial_font = dpg.add_font('C:\Windows\Fonts\ARIALN.TTF', 40)
    arial_font_50 = dpg.add_font('C:\Windows\Fonts\ARIALNB.TTF', 100)
""" THEMES """
with dpg.theme() as exit_button_style:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (230, 75, 50), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (150, 150, 150), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (70, 70, 70), category=dpg.mvThemeCat_Core)
with dpg.theme() as comment_font_style:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, (120, 120, 120), category=dpg.mvThemeCat_Core)

""" Create MAIN window """
with dpg.window(no_move=True, no_scrollbar=True, no_close=True, no_collapse=True) as main_win:
    # manu-bar
    with dpg.menu_bar(show=False) as main_bar:
        id_ = dpg.add_image('main_ico')
        # City menu
        with dpg.menu(label='City') as city_bar_file:
            # name
            dpg.add_input_text(label='name', tag='city_name', default_value='Sochi', width=240)
            # comment
            dpg.add_text(default_value='City name on english')
            dpg.bind_item_theme(dpg.last_item(), comment_font_style)
        # exit
        dpg.add_button(label='Exit', callback=exit, pos=(575 - 55, 0))
        dpg.bind_item_theme(dpg.last_item(), exit_button_style)
    with dpg.group(horizontal=True, horizontal_spacing=10) as main_gr_group:
        dpg.add_button(
            label='update',
            width=575 - 16,
            callback=set_w_data
        )
    
    # main group
    with dpg.group(horizontal=True) as main_group:
        with dpg.group() as left_gr:
            dpg.add_image('img', width=256, height=256)
            dpg.add_separator()
            dpg.add_text(default_value='situation', tag='sit')
            dpg.add_text(default_value='visibility', tag='vis')
        dpg.add_separator()
        with dpg.group() as right_gr:
            dpg.add_text(default_value='temperature', tag='temp')
            dpg.set_item_font(dpg.last_item(), arial_font_50)
            dpg.add_separator()
            dpg.add_text('min_max', tag='min_max')
            dpg.add_text('feels like', tag='f_l')
            dpg.add_text('wind speed', tag='wind')
            dpg.add_text('degrees', tag='deg')
            dpg.add_text('gust', tag='gust')

dpg.bind_font(arial_font)
""" START """
dpg.create_viewport(
    title='Custom Title', width=575, height=475, decorated=False
)
dpg.set_primary_window(main_win, True)
dpg.setup_dearpygui()
dpg.show_viewport()

set_w_data()
""" MAIN-LOOP """
while running:
    # Обработка событий DPG
    dpg.render_dearpygui_frame()

# Очистка ресурсов
dpg.destroy_context()
