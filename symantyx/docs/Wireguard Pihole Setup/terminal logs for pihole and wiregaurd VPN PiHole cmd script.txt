#!/bin/bash

echo "=== Updating system ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing WireGuard ==="
sudo apt install wireguard -y

WG_DIR="/etc/wireguard"
SERVER_KEY="$WG_DIR/server.key"
SERVER_PUB="$WG_DIR/server.pub"
CLIENT_KEY="$WG_DIR/client.key"
CLIENT_PUB="$WG_DIR/client.pub"

echo "=== Generating server keys ==="
sudo wg genkey | sudo tee $SERVER_KEY | sudo wg pubkey | sudo tee $SERVER_PUB

echo "=== Generating client keys ==="
sudo wg genkey | sudo tee $CLIENT_KEY | sudo wg pubkey | sudo tee $CLIENT_PUB

SERVER_PRIVATE=$(sudo cat $SERVER_KEY)
SERVER_PUBLIC=$(sudo cat $SERVER_PUB)
CLIENT_PRIVATE=$(sudo cat $CLIENT_KEY)
CLIENT_PUBLIC=$(sudo cat $CLIENT_PUB)

echo "=== Creating WireGuard server config ==="
sudo bash -c "cat > /etc/wireguard/wg0.conf" <<EOF
[Interface]
Address = 10.8.0.1/24
ListenPort = 51820
PrivateKey = $SERVER_PRIVATE
DNS = 127.0.0.1

PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o wlan0 -j MASQUERADE

[Peer]
PublicKey = $CLIENT_PUBLIC
AllowedIPs = 10.8.0.2/32
EOF

echo "=== Enabling WireGuard service ==="
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

echo "=== WireGuard server is running ==="
echo ""
echo "=== Windows Client Config (copy into WireGuard) ==="
echo ""
echo "[Interface]"
echo "PrivateKey = $CLIENT_PRIVATE"
echo "Address = 10.8.0.2/32"
echo "DNS = 10.8.0.1"
echo ""
echo "[Peer]"
echo "PublicKey = $SERVER_PUBLIC"
echo "Endpoint = YOUR_PUBLIC_IP:51820"
echo "AllowedIPs = 0.0.0.0/0"
echo "PersistentKeepalive = 25"
echo ""
echo "=== Done ==="
