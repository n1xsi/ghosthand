<h1 align="center">

  <img src="assets/preview.png" align="top" alt="Logo Preview" width="30%"><br>

  [![Python](https://custom-icon-badges.demolab.com/badge/3.12.12-a990e2?logo=pythonn&label=Python&labelColor=383838&style=for-the-badge)](#)
  [![DearPyGui](https://custom-icon-badges.demolab.com/badge/2.2-a990e2?logo=dearpygui&label=DearPyGui&labelColor=383838&style=for-the-badge)](#)
  [![ctypes](https://custom-icon-badges.demolab.com/badge/1.1.0-a990e2?logo=ctypes&label=ctypes&labelColor=383838&style=for-the-badge)](#)

</h1>

**GhostHand** – это универсальный external-софт с набором автоматизированных макросов и скриптов для помощи во всех FPS-играх.

Проект является _external assistaint tool'ом_, который помогает в прицеливании, передвижении и т.д.

> [!WARNING]
> 🚧 **Статус проекта:** Находится в активной разработке. Весь код представлен в "сыром" виде.
> 
> ⚖️ **Disclaimer:** This project is created for educational purposes and programming practice only. The author is not responsible for any account bans or violations of Terms of Service in any games. **USE AT YOUR OWN RISK!**

> [!Important]
> Данный софт – это заскриптованная имитация ввода клавишей клавиатуры/мыши (WinAPI) и чтение пикселей экрана, поэтому какие-то функции могут работать дёргано, некорректно или вовсе мешать (в зависимости от ситуации, игры или производительности ПК).
> 
> * 👑 **Обязательно** запускайте консоль/IDE от имени **Администратора**.
> * 🪟 В играх используйте режим экрана _"Полноэкранный в окне" (Borderless)_ или _"Оконный"_. В эксклюзивном Fullscreen оверлей и чтение экрана работать не будут!

## 🧩 Функционал

<p align="center">
  <img src="https://i.imgur.com/y0uBAXS.png" align="center" width="40%">
</p>

Функции включаются через чекбоксы в GUI. У каждой функции есть свои настройки (ползунки) и бинды (вкладка `Keybinds`).

### 🔫 Aim Assist (Помощь в стрельбе)
* AimPull – Color Aimbot. Плавно тянет прицел к заданному цвету с заданной скоростью.
  * FOV Circle – Оверлей поверх экрана, показывающий радиус работы AimPull (можно менять цвет).
* Pixel Trigger Bot – Автоматический выстрел при изменении пикселей в центре прицела (реакция на появление врага).
* Mini-Recoil Control – Лёгкий макрос, тянущий прицел вниз при зажатии `ЛКМ` (для компенсации отдачи).
* Autopistol – Автоматический спам ЛКМ при удержании кнопки.

### 🚫🎯 Anti-Aim (Защита от headshot'а)
* Flick Anti-Aim – Резкий отвод камеры в сторону и обратно для "поломки" хитбоксов головы на сервере. Можно регулировать скорость, угол поворота, включение/выключение по кнопке `F` (toggle).

### 🏃 Movement (Передвижение)
* Bhop – Классический баннихоп (спам пробела) с настройкой задержек и рандомизацией таймингов для скрытности.
* Snap Tap – Приоритет последнего нажатия клавиш `A`/`D` (быстрая смена направления движения).

### 🎨 Visuals (Внешний вид)
* Watermark – Стильная плашка в углу экрана со статусом софта и временем.
* UI Scale – Изменение размеров окна и интерфейса (для всех мониторов и разрешений экранов).  

### ⭐ Misc (Разное)
* Anti-AFK – Автоматическое нажатие `WASD` раз в несколько секунд, чтобы сервер не кикнул за бездействие.
* FastZoom – Макрос для снайперских винтовок (Прицел -> Выстрел -> Быстрый свап нажатием `Q` -> Снова `Q`, который можно отключить).
* 180°-turn – Моментальный разворот камеры на 180 градусов (настраивается под любую сенсу).
* Global Pause (Panic Key) – Мгновенная блокировка всех функций одной кнопкой (Pause).

## 🎮 Совместимость с играми
Так как софт использует WinAPI, теоретически он будет работать **везде**. Ниже список протестированных игр (он будет пополняться):
<details>
  <summary>🤝 Список проверенных игр </summary>
  <br>

  **:accessibility: Полная совместимость** _(корректно работает бо́льшая часть функций)_:
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/3065800/ac94c44cc0d83393f57578e5a122eac481e68933.jpg" align="top"> Marathon *(ez BattleEye)*
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/10/6b0312cda02f5f777efa2f3318c307ff9acafbb5.jpg" align="top"> CS 1.6 *(ez old vac)*
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/240/9052fa60c496a1c03383b27687ec50f4bf0f0e10.jpg" align="top"> CS:S *(ez vac)*
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/4465480/c42651245856bf11a1201a4b521040ae830f2b07.jpg" align="top"> CS:GO *(ez vac)*
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/1280770/a40efa7f154decf48622a25f8b4fe9b67929d7e3.jpg" align="top"> Redmatch 2 *(ez enforcer)*
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/706990/84e0869208df5df1d65605ebb5bb0b95d6f2d596.jpg" align="top"> BLOCKPOST LEGACY *(ez in-game AC)*
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/500/428df26bc35b09319e31b1ffb712487b20b3245c.jpg" align="top"> Left 4 Dead **+** Left 4 Dead 2 *(ez vac)*
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/70/95be6d131fc61f145797317ca437c9765f24b41c.jpg" align="top"> Half-Life 1
  * <img src="https://cdn2.steamgriddb.com/icon/3fd33fca2c8309458ce87fc2777e51f6/32/32x32.png" align="top"> Postal 2 Multiplayer
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/40/c525f76c8bc7353db4fd74b128c4ae2028426c2a.jpg" align="top"> Deathmatch Classic
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/360/40b8a62efff5a9ab356e5c56f5c8b0532c8e1aa3.jpg" align="top"> Half-Life Deathmatch: Source
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/20/38ea7ebe3c1abbbbf4eabdbef174c41a972102b9.jpg" align="top"> TF Classic
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/41070/2e7a17d4b345ffb13ef3d9e39257c2659fe4a86b.jpg" align="top"> Serious Sam 3: BFE

  **:feelsgood: Только в Secured-режиме** _(высокий риск детекта античитом за какие-то функции)_:
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/730/8dbc71957312bbd3baea65848b545be9eae2a355.jpg" align="top"> CS 2 **(bad for VACNET)**
  * Некоторые прочие игры с Vanguard / EAC / BattlEye.

  **:speak_no_evil: Скорее бесполезно, чем полезно** _(полезна лишь малая часть функций)_:
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/1422450/f6da1420a173324d49bcd470fa3eee781ad0fa5e.jpg" align="top"> Deadlock
</details>

## 🚀 Установка и запуск
Пока софт находится в **разработке** и запустить его можно только следующим образом:

1. Склонируйте репозиторий
  ```bash
  git clone https://github.com/n1xsi/ghosthand.git
  cd ghosthand
  ```
2. Установите необходимые библиотеки (рекомендуется использовать виртуальное окружение venv):
  ```bash
  pip install dearpygui mss numpy keyboard
  ```
3. Запустите в IDE/CMD главный файл от имени Администратора:
  ```bash
  python main.py
  ```

## ⚙ Стек технологий
* [Python 3.12.12](https://www.python.org/downloads/release/python-31212/) – язык программы
* [DearPyGui](https://dearpygui.readthedocs.io/) – быстрый GPU-ускоренный интерфейс
* [ctypes (WinAPI)](https://docs.python.org/3/library/ctypes.html) – низкоуровневая эмуляция клавиатуры/мыши через SendInput
* [threading](https://docs.python.org/3/library/threading.html) – многопоточность для считывания разных клавиш
* [mss](https://python-mss.readthedocs.io/stable/) & [numpy](https://numpy.org/doc/stable/user/index.html#user) – cверхбыстрый захват экрана и матричные вычисления для AimPull
* [tkinter](https://docs.python.org/3/library/tkinter.html) – gрозрачные Click-Through оверлеи поверх экрана
