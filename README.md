# Rock, Paper, Scissors - The Battle Royale Simulation
![Python Version](https://img.shields.io/badge/python-3.x-blue.svg) ![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg) ![License](https://img.shields.io/badge/license-MIT-lightgrey.svg) ![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

Ever seen those viral meme videos of a massive Rock, Paper, Scissors battle where one group eventually takes over? This is that simulation, brought to life with Python and Pygame!

This project is a fully interactive simulation where you can set the parameters and watch the chaos unfold until a single victor remains.

---

## Preview


**The Settings Menu**
![Image](https://github.com/user-attachments/assets/c3748717-829c-45c4-9fcb-4b43087764c6)

**The Simulation in Action!**
![Image](https://github.com/user-attachments/assets/8adcab49-b6c3-4deb-9742-c371c22be930)
---

## ✨ Features

* **Interactive Settings:** A user-friendly menu to customize the simulation before it starts.
* **Customizable Simulation:** Control the screen size, total number of objects, object size, and movement speed.
* **Physics-Based Movement:** Objects move dynamically and bounce realistically off the walls.
* **RPS Battle Logic:** When objects of different types collide, the loser is converted to the winner's type based on classic Rock, Paper, Scissors rules.
* **Smooth Animations:** Objects rotate as they move, creating a more dynamic visual experience.
* **Automatic Winner Detection:** The simulation automatically stops and declares a winner when only one type of object remains.

---

## 🚀 How to Run

To run this simulation on your local machine, follow these steps.

### Prerequisites
* Python 3.x
* pip (Python package installer)

### Installation & Execution
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MG-530/RPS-Battle-Royale.git
    cd RPS-Battle-Royale
    ```

2.  **Install the required package:**
    ```bash
    pip install pygame
    ```

3.  **Run the simulation:**
    ```bash
    python rps_simulation.py
    ```
    The settings menu will appear. Choose your settings and click "START GAME"!

---

## 🎮 Controls

* **R Key**: After a winner is declared, press 'R' to restart the simulation with the same settings.
* **ESC Key**: Press 'ESC' at any time to close the game.

---

## 🛠️ Technologies Used

* **Python:** The core programming language.
* **Pygame:** The library used for creating the game window, drawing objects, and handling events.
* **Tkinter:** The standard Python library used for the initial settings GUI.

---
## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/MG-530/RPS-Battle-Royale/issues).

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

---
## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.