# 2FA Python-based Authenticator
Python-Based Crossplatform CLI TOTP 2FA Authenticator with AES-256 encryption for better security.
### What is TOTP ?
The Time-based One-time Password algorithm (TOTP) is an extension of the HMAC-based One-time Password algorithm (HOTP) generating a one-time password by instead taking uniqueness from the current time. It has been adopted as Internet Engineering Task Force standard RFC 6238, is the cornerstone of Initiative For Open Authentication (OATH), and is used in a number of two-factor authentication systems. **So it's default Password algorithm, which is used in many variations of 2FA authenticators, such as Google Authenticator, andOTP, Authy, etc.**

  [Wikipedia - TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_algorithm)
### What is 2FA ?
Two-factor authentication (also known as 2FA) is a type, or subset, of multi-factor authentication. It is a method of confirming users' claimed identities by using a combination of two different factors:

  1. something they know
  2. something they have
  3. something they are.

A good example of two-factor authentication is the withdrawing of money from an ATM; only the correct combination of a bank card (something the user possesses) and a PIN (something the user knows) allows the transaction to be carried out.

Two other examples are to supplement a user-controlled password with a one-time password (OTP) or code generated or received by a device (e.g. a security token or smartphone) that only the user possesses.

  [Wikipedia - Multi-Factor Authentication](https://en.wikipedia.org/wiki/Multi-factor_authentication)
### Features
1. Simple CLI Interface.
2. Simple Installation.
3. Simple in use.
4. Configuration file [AES-256](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard) Encryption.
5. PIN Code
### How to install ?
```
  git clone https://github.com/dimankiev/authenticator
  cd authenticator
  pip3 install -r requirements.txt
  python3 authenticator.py
```
### How to use ?
1. Start the script
2. Set up your new PIN code
3. When step 1 and 2 done - type `help` in opened CLI
4. Use command `add service_name`, then enter special 2FA key that was provided by your service on which you want to set up 2FA. _(service_name example: google, github, etc.)_
5. Use command `list` to see added apps
6. Use command `get service_name` to start receiving 2FA codes.
7. Use command `remove service_name` to remove app from the authenticator
8. Use command `exit` or combination `Ctrl+C` to close the script
### Credits
**Code written by** - [dimankiev](https://t.me/dimankiev)

All rights reserved. dimankiev &copy; 2019

[aaa114-project](http://aaa114-project.pp.ua)