# 🌲 DruidQ

**DruidQ** is a lightweight, event-based architecture for tabletop RPG sessions, built around [MQTT](https://mqtt.org/) and powered by Mosquitto. It runs on a personal k3s cluster and acts as a central forest of magic, where **Evokers** publish events and **Sprites** respond to them in real time.

> 🐻 Broker: \`DruidQ\`  
> 🧙‍♂️ Publishers: \`Evokers\`  
> 🧚‍♂️ Consumers: \`Sprites\`

---

## 🛠 Architecture Overview

- **DruidQ** (Mosquitto MQTT broker)  
  - Stateless  
  - Exposed via TLS and WebSockets  
  - Routes messages between components

- **Evokers** (Publishers)  
  - Push events into DruidQ  
  - Can be CLI tools, APIs, or game integrations

- **Sprites** (Consumers)  
  - Subscribe to MQTT topics  
  - Perform logic or side-effects (e.g., notify, modify state, etc.)

---

## ✨ License

MIT — because magic wants to be free.
