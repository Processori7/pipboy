from colorama import init, Fore
import os
import subprocess
import sys
import time
from freeGPT import AsyncClient
import asyncio

init()  # Инициализация colorama

def clear_terminal():
    """Очищает терминал."""
    try:
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
    except Exception as e:
        print(f"Ошибка при очистке терминала: {e}")

def print_flush(text, delay=0.1):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)  # Задержка в секундах
    time.sleep(0.5)  # Задержка перед очисткой терминала

def print_flush2(text, delay=0.003):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)  # Задержка в секундах
    time.sleep(0.005)  # Задержка перед очисткой терминала

def print_flush3(text, delay=0.00003):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)  # Задержка в секундах
    time.sleep(0.00003)  # Задержка перед очисткой терминала

async def communicate_with_model(message):
    """Взаимодействует с моделью для генерации ответа."""
    try:
        resp = await AsyncClient.create_completion("gpt3", message)
        return resp
    except Exception as e:
        return f"Ошибка при общении с моделью: {e}"

async def main():
    """Основная функция программы."""
    try:
        clear_terminal()
        print_flush("pip...")
        clear_terminal()
        print_flush("pip...")
        clear_terminal()
        print_flush2(
"""
Pipboy GPT3 готова к общению.
Основные команды: 
- Введите 'выход' или 'ex' или 'exit', чтобы завершить.
- Введите 'очистить' или 'cl' или 'clear', чтобы удалить переписку.

""")
        while True:
            user_input = input(Fore.LIGHTGREEN_EX + "Вы: " + Fore.WHITE)
            print()
            if user_input.lower() in ['выход', 'ex', 'exit']:
                print("До свидания!")
                break
            elif user_input.lower() in ['очистить', 'cl', 'clear']:
                clear_terminal()
                continue
            response = await communicate_with_model(user_input)
            print(Fore.YELLOW + "Pipboy GPT3 LLM:" + Fore.WHITE, end=' ')
            print_flush3(response + "\n")

    except KeyboardInterrupt:
        print("\nПрограмма завершена пользователем.")

if __name__ == "__main__":
    asyncio.run(main())