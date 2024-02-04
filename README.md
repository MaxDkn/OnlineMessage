# Online Messaging System

Welcome to the Online Messaging System project! This system consists of a server and a client, allowing users to exchange messages online. Please note that the project is a work in progress, and the graphical interface is not yet complete.

## Getting Started

1. Open the `server.py` file and start the server by running it.
    ```bash
    python server.py
    ```

2. Open the `client.py` file, modify the address to match the one displayed by `server.py`, and then run the client.
    ```bash
    python client.py
    ```

3. The initial page prompts you to enter your credentials, which will lead to another page where you can send messages.

## Usage

- **Credential Page:**
  - Enter your username and password.

- **Messaging Page:**
  - Once authenticated, you can send messages to other users.

## Project Structure

- The project is divided into three main files:
  - `server.py`: Start the server.
  - `client.py`: Launch the client, ensuring the server's address matches.
  - `connection.py`: Functions as an API, facilitating communication between the client and server.

## Project Status

- The project was initiated in December 2022 and is a work in progress.
- The graphical interface, implemented using Pygame, is not finalized and may be redesigned with Tkinter or PyQt5 in the future.
- Despite being incomplete, the messaging functionality is fully operational through the `connection.py` file, which communicates effectively with `server.py`.

## Notes

- The server (`server.py`) must be started before launching the client.
- Feel free to contribute by suggesting improvements or reporting issues.

**Important:** The graphical interface is not finalized, and improvements are planned for future versions.

Thank you for exploring the Online Messaging System!
