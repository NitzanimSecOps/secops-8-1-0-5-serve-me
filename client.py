import socket

from protocol import recv_msg, send_msg

PORT = 2405


def main() -> None:
    # connect to 127.0.0.1:PORT, then read a line from the user until "exit" (close and end)
    # "send {data}": send_msg the data, then print the server's reply
    pass


if __name__ == "__main__":
    main()
