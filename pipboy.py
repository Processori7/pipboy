import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
import re
import time
import asyncio
import requests
import configparser
import pygame
import ctypes
import subprocess
import shutil
import threading
import webbrowser

from datetime import datetime
from colorama import init, Fore
from packaging import version

# Инициализация
init()
pygame.init()

# === Глобальные переменные ===
is_music_playing = False
music_task = None

# === Настройки ===
CURRENT_VERSION = "1.6"
config_file = "config.ini"
ansi_folder = "C:\\pipboy\\"
pipboy_config_file_path = os.path.join(ansi_folder, config_file)

# === Функции ===

def update_app(update_url):
   webbrowser.open(update_url)

def check_for_updates():
    try:
        response = requests.get("https://api.github.com/repos/Processori7/pipboy/releases/latest")
        response.raise_for_status()
        latest_release = response.json()

        assets = latest_release["assets"]
        for asset in assets:
            if asset["name"].endswith(".exe"):
                download_url = asset["browser_download_url"]
                break
        else:
            print("Не удалось найти файл exe для последней версии.")
            return

        latest_version_str = latest_release["tag_name"]
        match = re.search(r'\d+\.\d+', latest_version_str)
        latest_version = match.group() if match else latest_version_str

        if version.parse(latest_version) > version.parse(CURRENT_VERSION):
            ans = input(f"Доступна новая версия {latest_version}. Хотите обновить?\nВведите да - для обновления.\n>>> ").lower()
            if ans == 'да':
                update_app(download_url)
    except requests.exceptions.RequestException as e:
        print("Ошибка при проверке обновлений:", e)

def remove_emojis(text):
    return re.sub(r'[\U00010000-\U0010ffff]', '', text)

def remove_sponsor_block(text):
    return re.sub(r'---\*\*Sponsor.*?', '', text, flags=re.DOTALL).strip()

def sanitize_text(text):
    return remove_sponsor_block(remove_emojis(text))

async def read_config_from_drive_c():
    config = configparser.ConfigParser()
    try:
        config.read(pipboy_config_file_path)
        if 'model' in config and 'name' in config['model']:
            return config.get('model', 'name').strip()
        else:
            return 'o3-mini'
    except Exception as e:
        print(f"Ошибка при чтении C:\\pipboy\\config.ini: {e}")
        return 'o3-mini'

async def read_model_config():
    try:
        config = configparser.ConfigParser()
        if os.path.exists(pipboy_config_file_path):
            config.read(pipboy_config_file_path)
        else:
            config.read('config.ini')
        if 'model' in config and 'name' in config['model']:
            return config.get('model', 'name').strip()
        else:
            return 'o3-mini'
    except Exception as e:
        print(f"Ошибка при чтении config.ini: {e}")
        return 'o3-mini'

async def write_model_config(model_name):
    config = configparser.ConfigParser()
    config.add_section('model')
    config.set('model', 'name', str(model_name))
    with open('config.ini', 'w') as f:
        config.write(f)

async def write_model_config_to_drive_c(model_name):
    config = configparser.ConfigParser()
    config.add_section('model')
    config.set('model', 'name', str(model_name))
    with open(pipboy_config_file_path, 'w') as f:
        config.write(f)

def play_music():
    global is_music_playing
    music_file = 'music.mp3'
    pipboy_folder = "C:\\pipboy\\"
    full_path = os.path.join(pipboy_folder, music_file)

    try:
        pygame.mixer.init()
        if os.path.exists(music_file):
            pygame.mixer.music.load(music_file)
        elif os.path.exists(full_path):
            pygame.mixer.music.load(full_path)
        else:
            print(f"Музыкальный файл не найден: {music_file} или {full_path}")
            is_music_playing = False
            return

        pygame.mixer.music.play(-1)  # Бесконечное воспроизведение
        is_music_playing = True

    except Exception as e:
        print(f"Ошибка воспроизведения музыки: {e}")
        is_music_playing = False

def print_flush2(text, delay=0.003):
    cleaned_text = sanitize_text(text)
    for char in cleaned_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    time.sleep(0.005)

def print_flush3(text):
    cleaned_text = sanitize_text(text)
    for char in cleaned_text:
        sys.stdout.write(char)
        sys.stdout.flush()
    print()
    time.sleep(0.00003)

async def print_history():
    history_file = os.path.join(ansi_folder, "history.txt")
    if os.path.exists(history_file):
        print("""
             :---:.             
                                      -++-=-:-==++-         
                                     +=::-=::::::::=+.      
                                   -*:::-=:::::::-:::+.     
                            .*+========+#+-::::::-::::+     
                          -+====##*+==+==-*##=::::::::*     
                        .*#*+==*+-**#*==+#*:-+*=+==:::+     
                       .#%*.%@..+=+#::@%..**:::.:+%%%%*     
                       :#%+ =**:==+*  +#*:+=-:-:.+*=:-++:   
                       =@#%+:.:=*=+#*:..:=*--*-..-=*@#+:=*  
                      =-:+#%%#=---*-*****+*:::...+.=*=*#+*. 
                     *=::::::+    =--.::::-===..+@#-        
                    -+::::::#*====-#=..:-...:@%#*--*:       
                    *:::::::-:::::::=+-:.....==:::::=+      
                   .*:::::::::::::::--:-:::...*:::::::*-    
                   .*:::::::::::::-:-=*=:...:=++:::::::=+   
                    -=====-----=====::=-:::++==#-:::::::=*  
                           ....    =-----==:---=%::::::::%  
                                   ----=:-------=*-:::::+-  
                                   -:::-:-::::::--=+*+==:   
                                   ----::--:----::::-       
                                   -:::::-::::::::::=       
                                   ===---=-:::::-==+*       
                                   -+++===+=+**++=+**.      
                                   .+++==+==+++****++       
                                    :+++=+++++++++++*       
                                     :+++=+++++++++==       
                                      .==+=====+++++.       
                                        -----:----=+        
                                         -.....-+===        
                                         :::...-:::.-=.     
                                         :.....=-:..:=*.    
                                 :-==- :-=-:..:- +--=+=++   
                                +=++=*+===-:-:=  =+-=====*  
                                *==+*+=+==++=:- .:*+===+=-  
                                 =*==++=====*=.-======++.   
                                   ::-=+++=+-  -+=====+:    
                                     .+=-=+:    .+*++:.     
                                        ..              
""")
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                for line in f:
                    cleaned_line = remove_emojis(line.strip())
                    cleaned_line = remove_sponsor_block(cleaned_line)
                    print(cleaned_line)
        except UnicodeDecodeError:
            print("Файл истории повреждён или записан в другой кодировке.")
            print("Попытка перечитать с автоматическим определением кодировки...")
            try:
                with open(history_file, "r", encoding="utf-8-sig") as f:
                    for line in f:
                        cleaned_line = remove_emojis(line.strip())
                        cleaned_line = remove_sponsor_block(cleaned_line)
                        print(cleaned_line)
            except Exception as e:
                print(f"Не удалось прочитать файл: {e}")
                print("Рекомендуется очистить историю командой 'cls'")
        ans = input("\nДля возврата в меню введите 'да' или 'yes'\nДля очистки истории введите cls: ")
        if ans.lower() in ['да', 'yes']:
            await main()
        elif ans.lower() == 'cls':
            os.remove(history_file)
            print("Готово")
            await main()
    else:
        print("Ой! История не найдена!\n")

async def communicate_with_Pollinations_chat(user_input, model):
    try:
        url = f"https://text.pollinations.ai/'{user_input}'?model={model}"
        resp = requests.get(url)
        if resp.ok:
            try:
                data = resp.json()
                return sanitize_text(data.get('reasoning_content', ''))
            except requests.exceptions.JSONDecodeError:
                return sanitize_text(resp.text)
        else:
            return f"Ошибка сервера: {resp.status_code}"
    except Exception as e:
        return str(e)

async def save_histoy(user_input, response):
    history_file = os.path.join(ansi_folder, "history.txt")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(ansi_folder):
        os.makedirs(ansi_folder)
    cleaned_response = remove_sponsor_block(response)
    with open(history_file, "a", encoding="utf-8") as f:
        f.write(f"Дата и время: {timestamp}\n"
                f"Вопрос пользователя: {user_input}\n"
                f"Ответ PipBoy 3000: {cleaned_response}\n\n")

async def get_Polinations_chat_models():
    names = []
    try:
        url = "https://text.pollinations.ai/models"
        resp = requests.get(url)
        if resp.ok:
            models = resp.json()
            for model in models:
                if isinstance(model, dict) and "name" in model:
                    model_name = model["name"]
                    model_description = model.get("description", "Без описания")
                    print(f"Название модели: {model_name} Описание: {model_description}")
                    names.append(str(model_name))
            return names
        else:
            print(f"Ошибка получения списка моделей: {resp.status_code}")
            return ["o3-mini"]
    except Exception as e:
        print(f"Ошибка при получении списка моделей: {e}")
        return ["o3-mini"]

async def disable_history():
    config = configparser.ConfigParser()

    # Проверяем, существует ли файл конфигурации
    if os.path.exists(pipboy_config_file_path):
        config.read(pipboy_config_file_path)
    else:
        config.read('config.ini')

    if not config.has_section('history'):
        config.add_section('history')

    # Устанавливаем значение 'write_history' в False, если его нет
    config.set('history', 'write_history', 'False')

    if os.path.exists(pipboy_config_file_path):
        # Записываем изменения в файл конфигурации
        with open(pipboy_config_file_path, 'w') as configfile:
            config.write(configfile)
    else:
        with open(pipboy_config_file_path, 'w') as configfile:
            config.write(configfile)

async def enable_history():
    config = configparser.ConfigParser()

    # Проверяем, существует ли файл конфигурации
    if os.path.exists(pipboy_config_file_path):
        config.read(pipboy_config_file_path)
    else:
        config.read('config.ini')

    # Проверяем, есть ли секция 'history'
    if not config.has_section('history'):
        config.add_section('history')

        # Устанавливаем значение 'write_history' в True, если его нет
    config.set('history', 'write_history', 'True')

    # Записываем изменения в файл конфигурации
    if os.path.exists(pipboy_config_file_path):
        # Записываем изменения в файл конфигурации
        with open(pipboy_config_file_path, 'w') as configfile:
            config.write(configfile)
    else:
        with open(pipboy_config_file_path, 'w') as configfile:
            config.write(configfile)

# === Основная функция ===
async def main():
    global is_music_playing, music_task

    # Проверяем администратора
    if ctypes.windll.shell32.IsUserAnAdmin():
        if not os.path.exists(ansi_folder):
            os.makedirs(ansi_folder)
        pipboy_exe_path = os.path.join(ansi_folder, "pipboy.exe")
        if not os.path.exists(pipboy_exe_path) and os.path.exists('pipboy.exe'):
            shutil.copy('pipboy.exe', pipboy_exe_path)
        if os.path.exists('music.mp3') and not os.path.exists(os.path.join(ansi_folder, 'music.mp3')):
            shutil.copy('music.mp3', ansi_folder)

    # Загрузка модели
    if os.path.exists(pipboy_config_file_path):
        model = await read_config_from_drive_c()
    else:
        model = await read_model_config()
        await write_model_config_to_drive_c(model)

    # Приветствие
    print(
        """
                                           -+==:                      
                                     :----+-:::-==-:                  
                              :+#. -+-:::::::::::::-+:                
                              #:-==-:===--=+#*-::::::==.              
                              *=:::=+:..---:.:++-==++=:=:             
                             .*=++==............:...:%=:=             
                             .*++:-=:.......=*=....:=*-:-=            
                              ==..=...........:....=+=::=:            
         .::.                .*..=%:..=-...+%......-+=+-+             
       ==:.:-+               =:...:.-*-....--......-++=#-             
      +.....:=               +......#+.............=-:++              
      +....:*                +..:...:=.....=..........+:              
      +....=-                :=:%-:::-----:=%-........=-              
      .*....+:                *:-:---------:=......===-               
.------++=-..:=:               +-...-+=..........-=                   
#.........:==..:+               -=.............=*:                    
-++++++=-:..=:..:*+-:           :++=-........:=+#::==-:               
+=.....:-==**...--*++**+======**+=..:##*=-:.:=*=:..*+++*+-:           
+-.::......:=..:*:*++++++++++++++*+-..-=++++=-...:+#+++++++*=:        
 *+=========*.-#--*++++++++++++++++**+=-:.....:=+#*+++++++++++*=      
:+..:......+:.:*.*+++++++++++++++++++++**=.....*++++++++++++++++*=    
 -=::==+==+*-=*:-*+++++++++++++++++++++++*.....=++++++*+++++++++++*:  
   :-----=**+-.=#+++++++++++*##*+++++++++*-.....*+++++*++##+++++++++*
           :--*#*********#**%*++++++++++++=.....=+++++**++++++++++++*=
                  ......    ++++++++++++++*......*+++++*++##+++++++++*
                            :*++++++++++++*:.....++++++*+#*+++++++++#:
                            .#+++++++++++++-.....=+++++*#*+++++++++*=
                             #+++++++++++++-.....-*++++##+++++++++*-
                             ***+++++++++++=.....:*+*#+-****+++++*-
                             +.:=+*******+*=......==-...=::-=***+     
                             +......:--====:............-:....=-      
                            :=........................:=#=...:+.      
                            :*=:...................-=*#*++.=*-        
                            +++**++=--:::::--==+**##*++++*.:=+        
                            #+++++++***********++++++++++#-:.         
                           :*++++++++++++++++++++++++++++#.           
                           *+++++++++++++++*#++++++++++++#:           
                           #++++++++++++++*#+++++++++++++#.           
                          =*+++++++++++++*%++++++++++++++#            
                          #++++++++++++++**++++++++++++++#            
                         :*+++++++++++++# -*++++++++++++++            
                         #+++++++++++++*: :*++++++++++++*:            
                        -*++++++++++++++  .#++++++++++++#             
                        #+++++++++++++#.  .#+++++++++++++             
                       =+++++++++++++*-   :#+++++++++++#.             
                      .#++++++++++++++    :*+++++++++++*              
                      ++++++++++++++*     -*++++++++++#:              
                      #++++++++++++#.     =*++++++++++*               
                      **+++++++++*+.      .###########*-:             
                     .*#########=:         =*#####******##+:          
                     =#*******#:                .-=+*#####*+          
                      *#**##*-                                        
            """)
    print_flush2(
        """
        Pipboy 3000 готов к общению. По умолчанию ведение истории выключено.
        Основные команды: 
        - Введите 'выход' или 'ex' или 'exit', чтобы завершить.
        - Введите 'очистить' или 'cls' или 'clear', чтобы удалить переписку.
        - Введите 'история' или 'history', чтобы вывести историю переписки на экран.
        - Введите 'музыка' или 'music' или 'старт' или 'start' для запуска музыки.
        - Введите 'стоп' или 'stop' для остановки воспроизведения.
        - Введите 'модель' или 'model' для выбора модели LLM.
        - Введите 'dishistory' или 'выклисторию' чтобы выключить ведение истории
        - Введите 'onhistory' или 'вклисторию' чтобы включить ведение истории
        """)

    while True:
        user_input = input(Fore.LIGHTGREEN_EX + "\nВы: " + Fore.WHITE)
        print()
        if user_input.lower() in ['история', 'history']:
            await print_history()
        elif user_input.lower() in ['выход', 'ex', 'exit']:
            print("До свидания!")
            sys.exit()
        elif user_input.lower() in ['очистить', 'cls', 'clear']:
            subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        elif user_input.lower() in ['музыка', 'music', 'start', 'старт']:
            if not is_music_playing:
                music_thread = threading.Thread(target=play_music, daemon=True)
                music_thread.start()
        elif user_input.lower() in ['стоп', 'stop']:
            if is_music_playing:
                pygame.mixer.music.stop()
                is_music_playing = False
        elif user_input.lower() in ['модель', 'model']:
            print("Сейчас используется:", model)
            print("Доступные модели:")
            models = await get_Polinations_chat_models()
            choice = input("Введите название модели: ")
            if choice in models:
                selected_model = choice
                if os.path.exists(pipboy_config_file_path):
                    await write_model_config_to_drive_c(selected_model)
                else:
                    await write_model_config(selected_model)
                print(f"Модель изменена на: {selected_model}")
                model = selected_model
        elif user_input.lower() in ['dishistory', 'выклисторию']:
            await disable_history()
            continue
        elif user_input.lower() in ['onhistory', 'вклисторию']:
            await enable_history()
            continue
        else:
            response = await communicate_with_Pollinations_chat(user_input, model)
            all = f"PipBoy 3000 {model}: {response}"
            config = configparser.ConfigParser()
            if os.path.exists(pipboy_config_file_path):
                config.read(pipboy_config_file_path)
            else:
                config.read('config.ini')

            # Безопасная проверка на наличие write_history
            if config.has_option('history', 'write_history'):
                ans = config.get('history', 'write_history')
                if ans.lower() == 'true':
                    await save_histoy(user_input, all)
            print_flush3(all + "\n")

if __name__ == "__main__":
    check_for_updates()
    asyncio.run(main())