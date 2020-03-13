

This little script allows a Raspberry Pi using the different LSG tools to connect to the LSG-Broker. #installation

    sudo apt-get update && sudo apt-get upgrade
    sudo apt-get install git
    git clone https://github.com/FrancoMaxime/lsg-mqtt
    sudo cp /lsg-connect/LSG-MQTT.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable LSG-MQTT
    sudo systemctl start LSG-MQTT
    systemctl status LSG-MQTT
    sudo reboot

Don't forget to change the BROKER_ADDRESS with the IP of the lsg-Broker.
Don't forget to change the ID_TRAY with the name of the tray inside the lsg-web.
