# Описание
Это доработанная версия pipboy, которая представлена в этой статье: https://vc.ru/u/3244565-rostislav-shackiy/1154205-fallout-style-chat-s-neyrosetyu-llama3-70b-dlya-lichnyh-nuzhd-i-horoshego-nastroeniya   
В этой версии не нужно использовать ключи и другие сервисы для доступа к языковой модели. 
Добавлено сохранение истории сообщений, добавление файла в Path при запуске от имени администратора, файл копирует себя в C:\pipboy.  
Для этого нужно запустить pipboy.exe на рабочем столе от имени администратора.  
Также добавлено новое оформление и при общении с ботом теперь можно будет запустить фоновую музыку.
# Использование
1. Клонировать репозиторий:  
```git clone https://github.com/Processori7/pipboy.git```
2. Перейти в папку:  
```cd /d pipboy```
3. Создать виртуальное окружение:  
```python -m venv venv```
4. Активировать виртуальное окружение:  
```venv\Scripts\activate```
4. Установить зависимости:  
```pip install -r requirements.txt```
5. Запустить файл: 
```python pipboy.py```