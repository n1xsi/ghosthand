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

Имеется уже готовое меню с следующими рабочими **настраиваемыми** функциями:
* AimPull _(тянет прицел к определённому цвету + FOV circle поверх игры)_
* Autopistol _(быстрый автоповтор ЛКМ)_
* Mini-Recoil Control _(тянет прицел вниз при зажатии ЛКМ)_
* Pixel Trigger Bot _(меняются пиксели у прицела - стреляет)_
* Flick Anti-Aim _(быстро отводит камеру в сторону и обратно)_
* Bhop _(автоповтор пробела при его зажатии)_
* Anti-AFK _(ходит в стороны раз в несколько секунд)_
* Snap Tap _(быстрая смена направления движения на A/D)_
* FastZoom _(быстрое прицеливание+выстрел)_
* 180°-turn _(поворот на 180 градусов)_
* PANIC KEY _(выключение/включение всех функций на Pause)_

Функции включаются через чекбоксы, у каждой функции свой бинд (который можно посмотреть во вкладке `Keybinds`), значения в функциях можно менять через ползунок или нажав по ползунку Ctrl+LMB и введя значение.

## 🎮 Совместимость с играми
Так как софт использует WinAPI, теоретически он будет работать **везде**. Ниже список протестированных игр (он будет пополняться):
<details>
  <summary>🤝 Список проверенных игр </summary>
  <br>

  **:accessibility: Полная совместимость** _(корректно работает бо́льшая часть функций)_:
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/10/6b0312cda02f5f777efa2f3318c307ff9acafbb5.jpg" align="top"> CS 1.6
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/240/9052fa60c496a1c03383b27687ec50f4bf0f0e10.jpg" align="top"> CS:S
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/4465480/c42651245856bf11a1201a4b521040ae830f2b07.jpg" align="top"> CS:GO
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/500/428df26bc35b09319e31b1ffb712487b20b3245c.jpg" align="top"> Left 4 Dead **+** Left 4 Dead 2
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/70/95be6d131fc61f145797317ca437c9765f24b41c.jpg" align="top"> Half-Life 1
  * <img src="https://cdn2.steamgriddb.com/icon/3fd33fca2c8309458ce87fc2777e51f6/32/32x32.png" align="top"> Postal 2 Multiplayer
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/40/c525f76c8bc7353db4fd74b128c4ae2028426c2a.jpg" align="top"> Deathmatch Classic
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/1280770/a40efa7f154decf48622a25f8b4fe9b67929d7e3.jpg" align="top"> Redmatch 2
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/706990/84e0869208df5df1d65605ebb5bb0b95d6f2d596.jpg" align="top"> BLOCKPOST (LEGACY)
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/20/38ea7ebe3c1abbbbf4eabdbef174c41a972102b9.jpg" align="top"> TF Classic

  **:feelsgood: Только в Secured-режиме** _(высокий риск детекта античитом за какие-то функции)_:
  * <img src="https://shared.fastly.steamstatic.com/community_assets/images/apps/730/8dbc71957312bbd3baea65848b545be9eae2a355.jpg" align="top"> CS 2
  * Некоторые прочие игры с Vanguard / EAC / BattlEye.
</details>

## ⚙ Стек технологий
* [Python 3.12.12](https://www.python.org/downloads/release/python-31212/) – язык программы
* [DearPyGui](https://dearpygui.readthedocs.io/) – быстрый GPU-ускоренный интерфейс
* [ctypes (WinAPI)](https://docs.python.org/3/library/ctypes.html) – низкоуровневая эмуляция клавиатуры/мыши через SendInput
* [threading](https://docs.python.org/3/library/threading.html) – многопоточность для считывания разных клавиш
* [mss](https://python-mss.readthedocs.io/stable/) & [numpy](https://numpy.org/doc/stable/user/index.html#user) – cверхбыстрый захват экрана и матричные вычисления для AimPull
* [tkinter](https://docs.python.org/3/library/tkinter.html) – gрозрачные Click-Through оверлеи поверх экрана
