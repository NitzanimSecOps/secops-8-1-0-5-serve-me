import socket

from protocol import recv_msg, send_msg

PORT = 2405


def main() -> None:
    # socket, SO_REUSEADDR, bind ("127.0.0.1", PORT), listen, then for each client:
    #     recv_msg and send_msg the same message back until the client leaves
    #     a client that vanishes (BrokenPipeError, ConnectionResetError) must not stop the server
    # when a client is gone, wait for the next one
    pass


if __name__ == "__main__":
    main()
