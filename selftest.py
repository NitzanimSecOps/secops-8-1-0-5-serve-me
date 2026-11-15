"""Local tester for server.py and client.py - not the hidden grader.

    python3 selftest.py

Starts your server.py in the background, talks to it with send_msg and recv_msg, drops a client in
the middle of a message, and then runs your client.py. Change the examples and try your own.
"""
import os
import socket
import struct
import subprocess
import sys
import time

HOST = "127.0.0.1"
PORT = 2405


def port_is_taken():
    try:
        socket.create_connection((HOST, PORT), timeout=1).close()
        return True
    except OSError:
        return False


def main():
    if port_is_taken():
        print(f"Something (probably a server.py you started) is already listening on port {PORT}.")
        print("Stop it with Ctrl+C in its window, then run selftest.py again.")
        sys.exit(1)
    here = os.path.dirname(os.path.abspath(__file__))
    server = subprocess.Popen([sys.executable, os.path.join(here, "server.py")], cwd=here)
    try:
        time.sleep(1)
        if server.poll() is not None:
            print("server.py stopped right after starting (its error is printed above).")
            sys.exit(1)
        sys.path.insert(0, here)
        from protocol import recv_msg, send_msg

        with socket.create_connection((HOST, PORT)) as s:
            s.settimeout(5)
            for text in (b"hello", b"again", b"and again"):
                send_msg(s, text)
                print("echo:", recv_msg(s))

        with socket.create_connection((HOST, PORT)) as s:
            s.sendall(struct.pack("!I", 1000) + b"partial")
        time.sleep(0.2)

        s = socket.create_connection((HOST, PORT))
        s.sendall(struct.pack("!I", 3) + b"bye")
        s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
        s.close()
        time.sleep(0.2)

        with socket.create_connection((HOST, PORT)) as s:
            s.settimeout(5)
            send_msg(s, b"still serving?")
            print("after a cut-off client and a reset:", recv_msg(s))

        result = subprocess.run(
            [sys.executable, os.path.join(here, "client.py")],
            input="send hello from the client\nexit\n", capture_output=True, text=True, timeout=10, cwd=here,
        )
        print("client.py printed:", result.stdout.strip(), result.stderr.strip())
    finally:
        server.kill()


if __name__ == "__main__":
    main()
