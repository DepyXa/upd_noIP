import asyncio
import sys
import signal
import platform
from configparser import ConfigParser
from pathlib import Path
from .noip import NoIPUpdater
from .agents import USER_AGENTS_DICT

# Шлях до файлу конфігурації
CONFIG_PATH = Path.home() / ".noip_updater_config.ini"

DEFAULTS = {
    "username": "#username",  # Логін No-IP
    "password": "#password",  # Пароль No-IP
    "hostname": "#hostname",  # Домен No-IP
    "check_interval": "300",   # Інтервал перевірки IP (секунди) [5 хв]
    "retry_interval": "20",    # Інтервал повторної спроби (секунди)
    "log_info": "True",  # Логування INFO
    "log_update": "True", # Логування UPDATE
    "log_error": "True"   # Логування ERROR
}

def load_config():
    """
    Завантажує конфігурацію з файлу, якщо він існує.
    """
    config = ConfigParser()
    if CONFIG_PATH.exists():
        config.read(CONFIG_PATH)
        return config["DEFAULT"]
    return {}

def save_config(args):
    """
    Зберігає конфігурацію у файл.
    """
    config = ConfigParser()
    config["DEFAULT"] = args
    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)

def parse_args():
    """
    Розбирає аргументи командного рядка та повертає оновлений словник.
    """
    args = DEFAULTS.copy()
    config = load_config()

    # Завантажуємо значення з конфігурації, якщо вони є
    for key in args:
        if key in config:
            args[key] = config[key]

    # Оновлюємо значення з аргументів командного рядка
    for arg in sys.argv[1:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            if key in args:
                args[key] = value

    # Зберігаємо оновлену конфігурацію
    save_config(args)

    return args

async def main():
    """
    Основна функція для запуску моніторингу IP та оновлення No-IP.
    """
    args = parse_args()

    # Перевірка обов'язкових аргументів
    if not all([args["username"], args["password"], args["hostname"]]):
        print("Помилка: необхідно вказати логін, пароль та домен.")
        return

    print(f"Запуск з параметрами: {args}")

    updater = NoIPUpdater(
        username=args["username"],
        password=args["password"],
        hostname=args["hostname"],
        user_agents=USER_AGENTS_DICT,
        check_interval=int(args["check_interval"]),
        retry_interval=int(args["retry_interval"]),
        log_levels={
            "info": args["log_info"].lower() == "true",
            "update": args["log_update"].lower() == "true",
            "error": args["log_error"].lower() == "true"
        }
    )

    def signal_handler(sig, frame):
        """Обробник сигналів для завершення роботи."""
        print("\nОтримано сигнал завершення. Завершення роботи...")
        asyncio.create_task(shutdown())

    async def shutdown():
        """Коректне завершення роботи."""
        await updater.close()
        sys.exit(0)

    # Налаштування обробки сигналів
    if platform.system() == "Windows":
        # На Windows використовуємо SIGINT (Ctrl + C)
        signal.signal(signal.SIGINT, signal_handler)
    else:
        # На Linux, macOS та Termux використовуємо SIGQUIT (Ctrl + Q)
        signal.signal(signal.SIGQUIT, signal_handler)

    try:
        await updater.monitor_ip_changes()
    except asyncio.CancelledError:
        print("Програму зупинено.")
    except Exception as e:
        print(f"Виникла критична помилка: {e}")
    finally:
        await updater.close()

if __name__ == "__main__":
    asyncio.run(main())
