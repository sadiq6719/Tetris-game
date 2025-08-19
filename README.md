Python Tetris Game with GUI

A classic Tetris game implemented in Python using Pygame. This version includes a graphical user interface (GUI) with score display, next piece preview, and a game-over screen.
🎮 Features

    Classic Tetris gameplay: Move, rotate, and drop Tetris pieces.

    GUI side panel: Shows score and next piece.

    Scoring system: 100 points per cleared row.

    Game over screen: Displays final score when the game ends.

    Keyboard controls:

        Left Arrow – Move piece left

        Right Arrow – Move piece right

        Down Arrow – Move piece down faster

        Up Arrow – Rotate piece

🖥️ Installation

    Clone the repository:

git clone https://github.com/your-username/python-tetris.git
cd python-tetris

    Install dependencies:

Make sure you have Python 3 installed. Install Pygame:

pip install pygame

    Run the game:

python tetris.py

🛠️ How it works

    Grid and Pieces: The game board is a grid. Pieces are defined in matrices with their shapes and colors.

    Piece Movement: Players can move and rotate pieces. The game checks for collisions with walls or other pieces.

    Row Clearing: Full rows are removed and the remaining blocks drop down.

    Scoring: Players earn points for clearing rows.

    Game Over: When new pieces cannot fit at the top, the game ends and shows the final score.

📂 File Structure

python-tetris/
├── tetris.py        # Main game code
├── README.md        # This file

⚡ Contribution

Feel free to fork the repository, submit issues, or create pull requests.
