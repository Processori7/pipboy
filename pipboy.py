import os
import winreg
import pygame
import asyncio
import ctypes
import shutil
import sys
import time
from webscout import WEBS as w
from datetime import datetime
from colorama import init, Fore
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Скрываю сообщения от pygame


init()  # Инициализация colorama
pygame.init()

async def play_music():
    global is_music_playing
    # Проверяем, существует ли файл music.mp3
    if os.path.exists('music.mp3'):
        is_music_playing = True
        pygame.mixer.music.load("music.mp3")
        while True:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            pygame.mixer.music.rewind()
    else:
        # Если файл не существует, устанавливаем путь к файлу
        music_file_path = 'C:\\pipboy\\music.mp3'
        is_music_playing = True
        pygame.mixer.music.load(music_file_path)
        while True:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            pygame.mixer.music.rewind()


def add_to_path(path, root=winreg.HKEY_CURRENT_USER, key_path='Environment', access=winreg.KEY_ALL_ACCESS):
    root_key = winreg.ConnectRegistry(None, root)
    key = winreg.OpenKey(root_key, key_path, 0, access)
    value, value_type = winreg.QueryValueEx(key, 'path')
    value = value.rstrip(';') + ';' + path
    winreg.SetValueEx(key, 'path', 0, value_type, value)
    winreg.CloseKey(key)
    winreg.CloseKey(root_key)


async def clear_terminal():
    """Очищает терминал асинхронно."""
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"Ошибка при очистке терминала: {e}")


def print_flush2(text, delay=0.003):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)  # Задержка в секундах
    time.sleep(0.005)  # Задержка перед очисткой терминала


def print_flush3(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
    print()
    time.sleep(0.00003)  # Задержка перед очисткой терминала

async def print_history():
    if os.path.exists("history.txt"):
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
        \n""")
        with open("history.txt", "r") as f:
            for line in f:
                print(line.strip())
        ans = input("\nДля возврата в меню введите 'да' или 'yes'\nДля очистки истории введите cls: ")
        if ans.lower() in ['да', 'yes']:
            await main()
        elif ans.lower() == 'cls':
            print("""                                     
                               .:.                          
                             -#*=+#*.                       
                      .---==##:::::-++*++-                  
             =%=    =%+-:-=*=:::::::::::-*#.                
           -%=@=::=*=:::::::::::::::::::::-*:               
           %:::=+=-::::-:::::-+**-::::::::::*#=             
           %::::::::+*==+*+*#*++*@*:::::::::::+%:           
           *#:::::=#-            .=%+=++*#%#=::-@:          
          -%=++++*=                .::.   .+@=::+@:         
          =*:=%:-=*+          .=:          :@=:::@#         
           #*%. .:-:          =#%#+.     -*#-::::%%         
           =%.  :-                ..     =+*-::::@#         
          .@:  :@@-    +=    .*%:        :++=*::=@=         
          %+   .#*.  .#=     :@@:        -*++-#:%#          
         -@:       .+@-       ::         =+-***%@.          
         +@.       #@+                   =:+:*%@=           
         *@.       .*@=                  := .=@=            
         =@:  :=:.   .        .              :@@            
         .@+ .%#%-+=--.-.=:==+**+#=.          %@            
          *@.==*%##%*%+@=@*#**@--@#==.      -#@:            
           %#. ..-==#:@.@:#:+--: :*+%-  -%##*-              
           .%#.  -+=-:....:.       .  :*@+                  
             *%:    .:---::.        .*@+                    
              :#*-               .=#@@-                     
                .=*=:            -::%*                      
                   .=%#+=-:::   .-*%=                       
                     .*@@@#+=+*%%+:                         
                        .:---:.                             
                                                            
            \n""")
            os.remove("history.txt")
            print("Готово")
            await main()
    else:
        print("Ой! История не найдена!\n")


async def communicate_with_model(message, model):
    """Взаимодействует с моделью для генерации ответа."""
    try:
        response = w().chat(message, model=model)  # o3-mini, GPT-4.o mini, mixtral-8x7b, llama-3-70b, claude-3-haiku
        return response
    except Exception as e:
        return f"Ошибка при общении с ThinkAnyAI: {e}"

async def main():
    """Основная функция программы."""
    try:
        is_music_playing = False  # Глобальная переменная для отслеживания состояния воспроизведения музыки
        # Проверяем, запущен ли скрипт от имени администратора
        if ctypes.windll.shell32.IsUserAnAdmin():
            # Папка для копирования файла
            pipboy_folder = "C:\\pipboy\\"
            if not os.path.exists(pipboy_folder):
                os.makedirs(pipboy_folder)
                add_to_path(pipboy_folder)

            # Проверяем наличие файла pipboy.exe в папке C:\pipboy
            pipboy_exe_path = os.path.join(pipboy_folder, "pipboy.exe")
            if not os.path.exists(pipboy_exe_path):
                # Если файл не найден, копируем его из папки Desktop
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                source_path = os.path.join(desktop_path, "pipboy.exe")
                shutil.copy(source_path, pipboy_folder)
                shutil.copy('music.mp3', 'C:\\pipboy\\music.mp3')

            # Запуск основного цикла событий
        global music_task
        music_task = asyncio.create_task(play_music())

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
   :-----=**+-.=#+++++++++++*##*+++++++++*-.....*+++++*++++++++++++*= 
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
            """
        )
        print_flush2(
            """
            Pipboy 3000 готов к общению.
            Основные команды: 
            - Введите 'выход' или 'ex' или 'exit', чтобы завершить.
            - Введите 'очистить' или 'cls' или 'clear', чтобы удалить переписку.
            - Введите 'история' или 'hsitory', чтобы вывести истрию переписки на экран.
            - Введите 'музыка' или 'music' или 'старт' или 'start' для запуска музыки.
            - Введите 'стоп' или 'stop' для остановки воспроизведения.
            - Введите 'модель' или 'model' для выбора модели LLM.\n
            """)

        history = []

        while True:
            user_input = input(Fore.LIGHTGREEN_EX + "Вы: " + Fore.WHITE)
            print()

            if user_input.lower() in ['история', 'history']:
                await print_history()
            elif user_input.lower() in ['выход', 'ex', 'exit']:
                print("До свидания!")
                if music_task:
                    music_task.cancel()
                sys.exit()
            elif user_input.lower() in ['очистить', 'cls', 'clear']:
                await clear_terminal()
                history = []
                await main()
            elif user_input.lower() in ['музыка', 'music', 'start', 'старт']:
                if not is_music_playing:
                    music_task = asyncio.create_task(play_music())

            elif user_input.lower() in ['стоп', 'stop']:
                if music_task and pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    is_music_playing = False
                    music_task.cancel()
                    music_task = None  # Устанавливаем music_task в None, но сохраняем ссылку на задачу
            elif user_input.lower() in ['model', 'модель']:
                models = {
                    "claude-3-haiku": "claude-3-haiku-20240307",
                    "gpt-4o-mini": "gpt-4o-mini",
                    "llama-3.1-70b": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                    "mixtral-8x7b": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                    "o3-mini": "o3-mini"
                }
                key = models.keys()
                print_flush2("Выберите модель:")
                for i, model in enumerate(key, 1):
                    print_flush2(f"\n{i}. {model}\n")
                model_choice = input("Введите номер модели: ")
                if model_choice.isdigit() and 1 <= int(model_choice) and int(model_choice) <= len(models):
                    model_choice = list(models.keys())[int(model_choice) - 1]
                    print_flush2(f"Выбрана модель: {model_choice}\n")
                    user_input = input(Fore.LIGHTGREEN_EX + "Вы: " + Fore.WHITE)
                    response = await communicate_with_model(user_input, model_choice)
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    history.append((timestamp, user_input, response))

                    print(Fore.YELLOW + "PipBoy 3000 LLM:" + Fore.WHITE, end=' ')
                    print_flush3(response + "\n")

                    # Сохранение истории в файл
                    with open("history.txt", "a") as f:
                        for entry in history:
                            f.write(f"{entry[0]}\nВопрос пользователя: {entry[1]}\nОтвет PipBoy 3000: {entry[2]}\n\n")

            else:
                response = await communicate_with_model(user_input, "o3-mini")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history.append((timestamp, user_input, response))

                print(Fore.YELLOW + "PipBoy 3000 LLM:" + Fore.WHITE, end=' ')
                print_flush3(response + "\n")

                # Сохранение истории в файл
                with open("history.txt", "a") as f:
                    for entry in history:
                        f.write(f"{entry[0]}\nВопрос пользователя: {entry[1]}\nОтвет PipBoy 3000: {entry[2]}\n\n")

    except KeyboardInterrupt:
        print("До свидания!")
        music_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
