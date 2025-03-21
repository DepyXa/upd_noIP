---

# No-IP Updater (`upd_noIP`)

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/upd_noIP)](https://pypi.org/project/upd_noIP/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](https://opensource.org/licenses/MIT)

Модуль `upd_noIP` призначений для автоматичного оновлення IP-адреси на сервісі **No-IP**. Він підтримує IPv4 та IPv6, зберігає останні налаштування та працює на всіх основних платформах: **Windows**, **Linux**, **macOS** та **Android (Termux)**.

---

## Встановлення

### 1. Встановлення через `pip`

1. Установка:
   ```bash
   pip install upd_noIP
   ```
2. Після встановлення модуль можна запустити з командного рядка:

   ```bash
   upd-noip username="ваш_логін" password="ваш_пароль" hostname="ваш_домен"
   ```
   
### 2. Встановлення через `git clone`

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/DepyXa/upd_noIP.git
   ```

2. Перейдіть у папку проекту:
   ```bash
   cd upd_noIP
   ```

3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустіть модуль:
   ```bash
   python -m upd_noIP.cli username="ваш_логін" password="ваш_пароль" hostname="ваш_домен"
   ```
   

---

### Параметри командного рядка

| Параметр       | Опис                                                                 | Приклад значення       |
|----------------|---------------------------------------------------------------------|------------------------|
| `username`     | Логін для No-IP                                                     | `user123`              |
| `password`     | Пароль для No-IP                                                    | `pass123`              |
| `hostname`     | Домен, який потрібно оновити                                        | `example.ddns.net`     |
| `record_type`  | Тип домену (`A` або `AAAA`)                                         | `AAAA`                 |
| `check_interval` | Інтервал перевірки зміни IP (у секундах, за замовчуванням: 300)    | `600`                  |
| `retry_interval` | Інтервал повторної спроби при відсутності інтернету (у секундах)   | `30`                   |
| `log_info`     | Логування інформаційних повідомлень (`true` або `false`)            | `true`                 |
| `log_update`   | Логування повідомлень про оновлення (`true` або `false`)            | `true`                 |
| `log_error`    | Логування помилок (`true` або `false`)                              | `true`                 |

### Приклад

```bash
upd-noip username="user123" password="pass123" hostname="example.ddns.net" record_type="AAAA" check_interval=600 retry_interval=30
```

---

## Збереження налаштувань

Модуль автоматично зберігає останні введені значення у файлі конфігурації. Після першого запуску ви можете опустити параметри, і модуль використає збережені значення:

```bash
upd-noip
```

Файл конфігурації зберігається за шляхом:
- **Linux/macOS/Termux**: `~/.noip_updater_config.ini`
- **Windows**: `%USERPROFILE%\.noip_updater_config.ini`

---

## Особливості

- **Підтримка IPv4 та IPv6**: Модуль автоматично визначає тип IP-адреси та оновлює її на No-IP.
- **Автоматичне збереження налаштувань**: Останні введені значення зберігаються для подальшого використання.
- **Крос-платформність**: Працює на Windows, Linux, macOS та Android (Termux).
- **Логування**: Модуль підтримує різні рівні логування (інформація, оновлення, помилки).

---

## Приклад файлу конфігурації

Файл конфігурації має наступний формат:

```ini
[DEFAULT]
username = user123
password = pass123
hostname = example.ddns.net
record_type = AAAA
check_interval = 600
retry_interval = 30
log_info = true
log_update = true
log_error = true
```

---

## Завершення роботи

Для завершення роботи модуля:
- На **Linux/macOS/Termux**: Натисніть **Ctrl + Q**.
- На **Windows/Termux**: Натисніть **Ctrl + C**.

---

## Часто задавдані запитання 

### 1. У мене мобільний пристрій на мобільному операторі, що я можу зробити?:
Для початку потрібно створити на No-IP домен на типі **AAAA**, після чтого можна використовувати цей модуль.
Навідь не потрібно вказувати при запуску record_type="AAAA", адже цей тип є по умовчанням.

### 2. Не можу завершити роботу у Termux за допомогою **Ctrl+Q**, у вас помилка!:
Частково так, альтернатива спробуйте **Ctrl + C** повино спрацювати.

---

## Ліцензія

Цей проект ліцензовано за умовами **MIT License**. Детальніше див. у файлі [LICENSE](LICENSE).

---

## Автор

- **Дмитро Колоднянський**
- **Email**: gosdepyxa@gmail.com
- **GitHub**: [GitHub](https://github.com/DepyXa)
- **Telegram**: [Telegram](https://t.me/depyxa)

---

## Подяка

Якщо вам сподобався цей модуль, будь ласка, поставте зірку на GitHub! ⭐

---

## Підтримка

Якщо у вас виникли питання або проблеми, будь ласка, створіть [issue](https://github.com/DepyXa/upd_noIP/issues) на GitHub.

---
