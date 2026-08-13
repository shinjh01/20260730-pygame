import websocket

# Connect to WebSocket server
ws = websocket.WebSocket()
ws.connect("ws://172.16.2.56")

print("Connected to WebSocket server")

# Ask the user for some input and transmit it
text = input("Say something: ")
ws.send(text)

# Wait for server to respond and print it
result = ws.recv()
print("Received: " + result)

# Gracefully close WebSocket connection
ws.close()