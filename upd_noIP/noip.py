import aiohttp
import base64
import asyncio
import random
import time
import ipaddress
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NoIPUpdater:
    def __init__(self, username: str, password: str, hostname: str, user_agents, 
                 check_interval: int = 300, retry_interval: int = 30, 
                 log_levels: dict = None):
        """
        Ініціалізація асинхронного об'єкта для оновлення No-IP.
        """
        self.username = username
        self.password = password
        self.hostname = hostname
        self.check_interval = check_interval
        self.retry_interval = retry_interval
        self.auth_header = self._generate_auth_header()
        self.current_ip = None
        self.lost_connection_time = None
        self.log_levels = log_levels if log_levels else {"info": True, "update": True, "error": True}
        self.session = None
        self.notified_no_internet = False
        self.user_agents = user_agents

    def _generate_auth_header(self) -> str:
        """Генерує Basic Authorization заголовок."""
        auth_string = f"{self.username}:{self.password}"
        return "Basic " + base64.b64encode(auth_string.encode()).decode()

    def _get_random_user_agent(self) -> str:
        """Отримує випадковий User-Agent."""
        return random.choice(self.user_agents)

    async def _create_session(self):
        """Створює та зберігає глобальну сесію aiohttp."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def get_current_ip(self) -> str:
        """Отримує IP-адресу, перевіряє формат IPv6 та використовує IPv4 за необхідності."""
        async def fetch_ip(url: str) -> str:
            """Допоміжна функція для отримання IP."""
            try:
                async with self.session.get(url, timeout=10) as response:
                    return await response.text()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if self.log_levels["error"]:
                    logger.error(f"Помилка з'єднання: {e}")
                return None

        ip = await fetch_ip("https://api64.ipify.org?format=text")

        if ip and ":" in ip:  # Проста перевірка на IPv6
            if self.log_levels["info"]:
                logger.info(f"Отримано IPv6 ({ip}), пробуємо отримати IPv4...")
            ip = await fetch_ip("https://api4.ipify.org?format=text")

        return ip

    async def update_ip(self, new_ip: str) -> str:
        """Оновлює IP на No-IP з повторними спробами."""
        await self._create_session()
        url = f"https://dynupdate.no-ip.com/nic/update?hostname={self.hostname}&myip={new_ip}"
        headers = {
            "Authorization": self.auth_header,
            "User-Agent": self._get_random_user_agent()
        }
        
        for attempt in range(3):
            try:
                async with self.session.get(url, headers=headers) as response:
                    response_text = await response.text()
                    return self._parse_response(response_text)
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if self.log_levels["error"]:
                    logger.error(f"Спроба {attempt + 1}: помилка з'єднання: {e}")
                await asyncio.sleep(5)

        return "Не вдалося оновити IP після 3 спроб."

    def _parse_response(self, response_text: str) -> str:
        """Обробляє відповідь від No-IP."""
        responses = {
            "good": "IP успішно оновлено.",
            "nochg": "IP не змінився.",
            "nohost": "Хост не знайдено.",
            "badauth": "Невірний логін або пароль.",
            "badagent": "Заблокований User-Agent.",
            "!donator": "Функція доступна лише для платних акаунтів.",
            "abuse": "Аккаунт заблоковано за зловживання.",
            "911": "Помилка сервера No-IP, спробуйте пізніше."
        }
        key = response_text.split()[0]
        return responses.get(key, f"Невідома відповідь: {response_text}")

    async def monitor_ip_changes(self):
        """Моніторить зміну IP та оновлює No-IP при зміні."""
        await self._create_session()
        
        while True:
            try:
                new_ip = await self.get_current_ip()

                if new_ip is None:
                    if not self.notified_no_internet:
                        if self.log_levels["error"]:
                            logger.error("Втрата Інтернет-з'єднання.")
                        self.notified_no_internet = True
                    await self._wait_for_connection()
                    continue

                if self.notified_no_internet:
                    if self.log_levels["info"]:
                        logger.info("Інтернет відновлено.")
                    self.notified_no_internet = False

                if new_ip != self.current_ip:
                    if self.log_levels["info"]:
                        logger.info(f"Новий IP: {self.current_ip} -> {new_ip}")
                    result = await self.update_ip(new_ip)
                    if self.log_levels["update"]:
                        logger.info(f"Оновлення: {result}")
                    self.current_ip = new_ip

                    if "badagent" in result.lower() and self.log_levels["error"]:
                        logger.warning("User-Agent заблоковано! Змінюємо...")

            except Exception as e:
                if self.log_levels["error"]:
                    logger.error(f"Виникла помилка: {e}")

            await asyncio.sleep(self.check_interval)

    async def _wait_for_connection(self):
        """Очікує відновлення Інтернет-з'єднання."""
        while True:
            await asyncio.sleep(self.retry_interval)
            if await self.get_current_ip():
                break

    async def close(self):
        """Закриває сесію aiohttp при завершенні роботи."""
        if self.session and not self.session.closed:
            await self.session.close()
