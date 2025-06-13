
# Chess Game Project

<img src="https://github.com/user-attachments/assets/956dde0d-f4cd-4b29-91c8-c7e582b832fc" width="400" height="400"> <img src="https://github.com/user-attachments/assets/85e37080-fc34-490c-ab95-36fec46ffa66" width="400" height="400">


## Introduction

This project is a full-featured chess game implemented in **Python**. It supports a graphical window interface (using **Pygame**) and a console-based interface.
The modular project separates the game logic, rendering, input handling, and networking. It also includes a **Server-Client** module for remote multiplayer games,
which is currently under development, and a suite of unit tests to ensure code quality.

## Features

<img src="https://github.com/user-attachments/assets/4abb0e19-dfa6-4b38-8192-d212a3652c61" width="400" height="400"> <img src="https://github.com/user-attachments/assets/dc206680-1dce-450c-b2e9-995d2c4f3d6a" width="400" height="400">

#### Play Chess in Two Modes:
- Pygame Window: Enjoy a graphical chessboard, drag-and-drop pieces, and visual feedback.
- Console: Play chess directly in the terminal by entering moves using algebraic notation.
  
#### Game Logic:
- Full chess rules: legal moves, check, checkmate, and capture detection.
- Move validation and board state management.
- Turn management and move history.
  
#### Server-Client Multiplayer (Under Development):
- The server-client module is being developed to allow remote multiplayer games.
- When complete, it will enable hosting a chess server and connecting with a remote player as a client.
- Moves will be synchronized between the server and the client.
- Graceful handling of connections and disconnections is planned.

#### Testing:
- Unit tests for core logic (move validation, check/checkmate, board state).
- Mocking and integration tests for handlers.

## How to Play
### 1. Pygame Window Application
- #### Start the game:
``` python chessgame.py ```
- A window will open with a chessboard.
- Use your mouse to select and move pieces.
- The interface displays check and checkmate states.
- Game state updates in real time.
### 2. Console Mode
- #### Start the game:
``` python main.py ```
- Enter moves using standard chess notation (e.g., 12 24).
- The board is displayed in the console.

## Server-Client Module
> The Server-Client module is currently **under development**. Multiplayer over the network is not yet fully supported. Please check back for updates in future releases.

## Getting started
#### 1. Install dependencies:
```pip install -r requirements.txt ```
#### 2. Run the game:
```python chessgame.py ```

## Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new features.

**Enjoy playing chess and exploring the code!**
