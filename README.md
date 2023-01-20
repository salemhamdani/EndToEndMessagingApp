
<div align="center">
<h1 style="color:#FEBB59">EndToEndMessagingApp</h1>
  <p align="center">
    E2E communication based on x509 certificates and  rsa encryption.
    <br />
  </p>
</div>

## Contributors
This project was made by :
* Ismail Charfi
* Salem Hamdani
## Details 
* The server which is also the certificate authority creates a certificate and auto sign it with its private key
* A client can connect to the server using the app, can create an account or log in
*  we wanted to use ldap for authentication, but we had some troubles installing OpenLDAP 
* using rsa encryption all communications between any parties are secure (client-server or client-client)
* a user can enter the chat page and can list the connected users
* a user can choose a person to chat with
* a handshake is made between them with exchanging keys and verification of the certificate
* a channel is created between them so the chat will be purely peer to peer without the server's intervention

## Dependencies
* To run the project you should install the libraries used for the ui and for encryption adn generating certificates:
  -  rsa
  - threading
  - socket
  - pyOpenSSL
  - sqlite3
  - Tkinter
  - PIL pillow
## Demo
https://drive.google.com/drive/folders/1oBnSO-S0rTT1xyYp-WNI2nTF-ialKEVO