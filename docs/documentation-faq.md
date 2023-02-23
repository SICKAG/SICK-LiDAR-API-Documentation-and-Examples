<img align=right width="200" src="../docs/img/sick-logo.jpg"/> 

FAQ
---

# Table of content


- [Table of content](#table-of-content)
- [How to export all settings or parameter?](#how-to-export-all-settings-or-parameter)
- [I can not connect to my sensor? Any ideas?](#i-can-not-connect-to-my-sensor-any-ideas)
  - [Change subnet of client system](#change-subnet-of-client-system)
    - [Windows](#windows)
    - [Linux](#linux)
  - [Change sensor IP address](#change-sensor-ip-address)



# How to export all settings or parameter?

Currently there is no automated solution to export all settings.

# I can not connect to my sensor? Any ideas?

Make sure your sensor and client system is in the same subnet. You want to either change the subnet of your ethernet interface or you want to change the IP address of the sensor.

## Change subnet of client system

You want make sure
> NOTE 
> It's important to note that changes the IP address on your computer may affect your ability to connect to other sensors on your network or access the internet. 

### Windows
To change the IP address on a Windows computer, you can follow these steps:
  
- Open the Start menu and search for "Control Panel."
- Click on "Network and Sharing Center" in the Control Panel.
- Click on "Change adapter settings" on the left side of the window.
- Right-click on the network adapter that you want to change the IP address for and select "Properties."
- Select "Internet Protocol Version 4 (TCP/IPv4)" and then click the "Properties" button.
- Select "Use the following IP address" and enter the new IP address, subnet mask, and default gateway.
  - IP address (example): `192.168.0.10`
  - Subnet mask (example): `255.255.255.0`
- Click "OK" to save the changes.
- Close all open windows.

### Linux
- Open the network settings on your Linux distribution, depending on the Linux distribution you are using the location may vary.
- You can find it in the settings, preferences or system settings.
- Once you've found it, select the network adapter you want to change the IP address for.
- enter the new IP address, subnet mask, and default gateway.
  - IP address (example): `192.168.0.10`
  - subnet mask (example): `255.255.255.0`
- save the changes and close the settings.

## Change sensor IP address
- Open the sensor web browser: http://192.168.0.1/
- Navigate to `Configuration` &rarr; `Connection options`
- Change the IP address and the sub net mask