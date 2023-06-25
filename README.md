# FWINISM, Front-end Web-based IOT Networking Included System Module

Accidental discovery.

## ESP32

### Requirements

- An ESP32 Microcontroller flashed with Micropython
- Jumpwires, Breadboard, LED (*optional)

Copy the scripts in `esp32` to the board.

## App

### Requirements

- Gradle, Android SDK, NodeJS, Cordova
- Be in `app` directory

```sh
cordova platform add browser
cordova platform add android
cordova plugin add cordova-custom-config
```

### Testing

#### Browser

```sh
cordova run browser
```

#### Android

```sh
cordova build android
```

Install the output <code>apk</code> to test.
