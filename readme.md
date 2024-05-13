# Описание
Это доработанная версия pipboy, которая представлена в этой статье: https://vc.ru/u/3244565-rostislav-shackiy/1154205-fallout-style-chat-s-neyrosetyu-llama3-70b-dlya-lichnyh-nuzhd-i-horoshego-nastroeniya   
В этой версии не нужно использовать ключу и другие сервисы для доступа к языковой модели. 
# Использование
1. Клонировать репозиторий:  
```git clone https://github.com/Processori7/pipboy.git```
2. Перейти в папку:  
```cd /d pipboy```
3. Создать виртуальное окружение:  
```python -m venv venv```
4. Установить зависимости:  
```pip install -r requirements.txt```
5. Запустить файл: 
```python pipboy.py```
# Дополнительно
Данный файл можно собрать в исполняемый с помощью auto-py-to-exe и добавить его в системную переменную Path.  
Тогда можно будет вызывать этот инстумент в cmd, просто написав pipboy.