<h1 align="center">

  <img src="assets/preview.png" align="top" alt="Logo Preview" width="30%"><br>

  [![Python](https://custom-icon-badges.demolab.com/badge/3.12.12-a990e2?logo=pythonn&label=Python&labelColor=383838&style=for-the-badge)](#)
  [![DearPyGui](https://custom-icon-badges.demolab.com/badge/2.2-a990e2?logo=dearpygui&label=DearPyGui&labelColor=383838&style=for-the-badge)](#)
  [![ctypes](https://custom-icon-badges.demolab.com/badge/1.1.0-a990e2?logo=ctypes&label=ctypes&labelColor=383838&style=for-the-badge)](#)

</h1>

**GhostHand** – это универсальный софт с набором автоматизированных скриптов для помощи во всех FPS-играх.

Проект является _external assistaint tool'ом_, который помогает в прицеливании, передвижении и т.д.

> [!WARNING]
> Repo still in development. _**Everything is in its "raw" form.**_
> 
> **Disclaimer: This project is created for educational purposes and programming practice only. The author is not responsible for any account bans or violations of Terms of Service in any games. USE AT YOUR OWN RISK!**

> [!Important]
> Данный софт – это заскриптованная имитация нажатий клавишей клавиатуры/мыши, поэтому какие-то функции могут работать дёргано, некорректно или вовсе мешать (в зависимости от ситуации или игры).
> 
> Для лучшей работы программы её **рекомендуется** запускать от имени администратора, а в играх использовать режим отображения окна _"Полноэкранный в окне"_ или _"Оконный"_.

## ✅ Функции, реализованные на данный момент
Имеется уже готовое меню с следующими рабочими **настраиваемыми** функциями:
* AimPull _(тянет прицел к определённому цвету)_
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
В теории GhostHand полностью совместим со всеми играми (ибо софт имитирует нажатия клавиш и просто сканит экран), но вот точный список проверенных игр (он будет пополняться):

**:accessibility: Полная совместимость (бо́льшая часть функций):**
* <img src="https://cdn2.steamgriddb.com/icon/2ec6c9b2b8bd4007bf7959141ef58651/32/32x32.png" align="top"> cs 1.6
* <img src="https://cdn2.steamgriddb.com/icon/052c3ffc93bd3a4d5fc379bf96fabea8/32/32x32.png" align="top"> cs:s
* <img src="https://cdn2.steamgriddb.com/icon/1854878c9953ed65c26b5f12760fed2c/32/32x32.png" align="top"> cs:go
* <img src="https://cdn2.steamgriddb.com/icon/01c262a2f7d8fa498b3ca5dd8837353e/32/32x32.png" align="top"> l4d + l4d2
* <img src="https://cdn2.steamgriddb.com/icon/9e8c7ed7adbba14c3937afb4ee263e66/32/32x32.png" align="top"> hl1
* <img src="https://cdn2.steamgriddb.com/icon/3fd33fca2c8309458ce87fc2777e51f6/32/32x32.png" align="top"> postal 2 multiplayer
* <img src="https://cdn2.steamgriddb.com/icon/60cf63b263ca6b6955d9bb680cc85ca9/24/32x32.png" align="top"> deathmatch classic

**:feelsgood: Только в Secured-режиме:**
* <img src="https://cdn2.steamgriddb.com/icon/e1bd06c3f8089e7552aa0552cb387c92/8/32x32.png" align="top"> cs2

## ⚙ Стек технологий
* [Python 3.12.12](https://www.python.org/downloads/release/python-31212/)
* [DearPyGui](https://dearpygui.readthedocs.io/)
* [ctypes (WinAPI)](https://docs.python.org/3/library/ctypes.html)
* [threading](https://docs.python.org/3/library/threading.html)
