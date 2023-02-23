<img align=right width="200" src="../docs/img/sick-logo.jpg"/> 

Device Configuration via CoLa
---

CoLa (Command Language) is SICK proprietary way to serialize and deserialize data. Its a low level and proofed approach for many years. For the listed sensors it utilizes TCP as a transport layer and is used to read and write parameters.

In general we differentiate between CoLa A (ASCII) and CoLa B (binary).

---------

<details>
  <summary>Table of content</summary>

- [Examples](#examples)
- [Variable types](#variable-types)
- [Command basics](#command-basics)
- [Required user level](#required-user-level)
- [CoLa B](#cola-b)
- [CoLa A](#cola-a)
- [CoLa telegram overview](#cola-telegram-overview)
- [CoLa error codes](#cola-error-codes)


</details>

---------

# Examples
All available examples can be found [here](examples/).

# Variable types

| Variable type | Length (byte)     | Value range                          | Sign |
| ------------- | ----------------- | ------------------------------------ | ---- |
| `Bool`        | 1                 | 0 or 1                               | No   |
| `Uint8`       | 1                 | 0 … 255                              | No   |
| `Int_8 `      | 1                 | \-128 … +127                         | Yes  |
| `Uint16`      | 2                 | 0 … 65,535                           | No   |
| `Int16`       | 2                 | \-32,768 … +32,767                   | Yes  |
| `Uint32`      | 4                 | 0 … 4,294,967,295                    | No   |
| `Int32`       | 4                 | \-2,147,483,648 … +2,147,483,647     | Yes  |
| `Enum8`       | 1                 | Certain values defined in a list     | No   |
| `Enum16`      | 2                 | Certain values defined in a list     | No   |
| `String`      | Context-dependent | Strings are not terminated in zeroes |      |

# Command basics

| Description   | Value ASCII | Binary Value | Hex   Value                  |
| ------------- | ----------- | ------------ | ---------------------------- |
| Start of text | `STX`       | `2`          | `02 02 02 02` + given length |
| End of text   | `ETX`       | `3`          | Calculated checksum          |
| Read          | `sRN`       | `73524E`     | `73524E`                     |
| Write         | `sWN`       | `73574E`     | `73574E`                     |
| Method        | `sMN`       | `734D4E`     | `734D4E`                     |
| Event         | `sEN`       | `73454E`     | `73454E`                     |
| Answer        | `sRA`       | `735241`     | `735241`                     |
| Answer        | `sWA`       | `735741`     | `735741`                     |
| Answer        | `sAN`       | `73414E`     | `73414E`                     |
| Answer        | `sEA`       | `734541`     | `734541`                     |
| Answer        | `sSN`       | `73534E`     | `73534E`                     |
| Space         | `SPC`       | `20`         | `20`                         |

If values are divided into two parts (e.g. measurement data), they are documented according to LSB (e.g. `00` `07`), output however is according to MSB (e.g. `07` `00`).

# Required user level

Whether a parameter can be written or a method can be executed by a user depends on the least user level.
Defined user levels are:

| # User level | User level        | Hash value |
| ------------ | ----------------- | ---------- |
| 1            | Operator          | -          |
| 2            | Maintenance       | `B21ACE26` |
| 3            | Authorized Client | `F4724744` |
| 4            | Service           | `81BE23AA` |

This table indicates which user level you need for which actions.

| Task               | Required user level |
| ------------------ | ------------------- |
| Reading parameters | None                |
| Writing parameters | Authorized Client   |
| Manage password    | Service             |

In general, every `sWN` command for changing parameters requires to log in to the sensor first. When being logged in, any desired parameter valid for this user level can be changed. All changes become active only after having logged off again from the sensor via the `sMN Run` command.

# CoLa B

The binary telegram is the basic protocol of the scanner (CoLa B). All values are in hexadecimal code and grouped into pairs of two digits (1 `byte`). The string consists of four parts: `header`, `data length`, `data` and `checksum` (CS).
The `header` indicates with 4 × `STX` (`02` `02` `02` `02`) the start of the telegram.
The `data length` defines the size of the data part (command part) by indicating the number of digit pairs in the third part. The size of the data length itself is 4 bytes, which means that the data part might have a maximum of 2<sup>32</sup> digit pairs.
The `data` part comprises the actual command with letters and characters converted to Hex (according to the [ASCII](https://www.google.com/search?q=ASCII) chart) and the parameters of either decimal numbers converted to Hex or fixed Hex values with a specific, intrinsic meaning (no conversion). There is always a blank (20<sub>hex</sub>) between the command and the parameters, but not between the different parameter values.
The `checksum` finally serves to verify that the telegram has been transferred correctly. The length of the checksum is 1 byte, CRC8. It is calculated with XOR.

This is an example telegram for setting the user level “AuthorizedClient”:

|               | Hex Data                                                | Note                                                                                                 |
| ------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `Header`      | `02` `02` `02` `02`                                     |                                                                                                      |
| `Data length` | `00 00 00 17`                                           | `12`<sub>hex</sub> = `23`<sub>dec</sub>  digit pairs                                                 |
| `Data`        | `73 4D 4E 20 53 65 74 41 63 63 65 73 73 4D 6F 64 65 20` | `SetAccessMode` = actual command for setting the user level (and `20` = blank)                       |
| `Data`        | `03`                                                    | `03` = fixed Hex value meaning user level “Authorized Client”                                        |
| `Data`        | `F4 72 47 44`                                           | `F4 72 47 44` = fixed Hex value, serving as password for the selected user level “Authorized Client” |
| `CS`          | `B3`                                                    | `B3` = checksum from XOR calculation                                                                 |

# CoLa A
The ASCII telegram is an alternative to the binary telegram. Due to the variable string length of ASCII telegrams, the Binary telegram (CoLa B) is recommended when using scanners with a PLC. The ASCII telegram has the advantage that commands can be written in plaintext. The string consists only of two parts: the framing and the data part. The framing indicates with `STX` and `ETX` the start and stop of each telegram. The data part comprises the actual command with letters and characters (plaintext), parameter values either in decimal (special indicator required) or in hexadecimal (e.g.: a frequency of 25 Hz = +2500<sub>dez</sub> = 9C4<sub>hex</sub>) and fixed hexadecimal values with a specific, intrinsic meaning. As leading zeros are being deleted, there is always a blank required between all command parts and parameter parts. 

> NOTE
The sensor will confirm parameter values always in hexadecimal code, regardless of the code sent.

As further alternative within CoLa A, depending on the preferences of the user, all values can be written directly in Hex. This means however a 1:1 conversion of all letters and characters including numbers and fixed hexadecimal values via the ASCII chart.

This is again an example telegram for setting the user level “Authorized Client”. As only fixed hexadecimal parameter values are needed, the option to use parameter values in decimal code with special indicator cannot be applied here:

| Hex Data                                 | ASCII Data      | Note                                                                                 |
| ---------------------------------------- | --------------- | ------------------------------------------------------------------------------------ |
| `02`                                     | `STX`           | Framing                                                                              |
| `73 4D 4E`                               | `sMN`           | start of SOPAS  command                                                              |
| `20`                                     | `SPC`           | Blank                                                                                |
| `53 65 74 41 63 63 65 73 73 4D 6F 64 65` | `SetAccessMode` | command for setting the user level                                                   |
| `20`                                     | `SPC`           | Blank                                                                                |
| `30 33`                                  | `31`            | fixed Hex value meaning user level “Authorized Client”                               |
| `20`                                     | `SPC`           | Blank                                                                                |
| `46 34 37 32 34 37 34 34`                | `F4724744`      | fixed Hex value, serving as password for the selected user level “Authorized Client” |
| `03`                                     | `ETX`           | Framing                                                                              |

# CoLa telegram overview

Please refer to the following CoLa specifications. These are used to describe the CoLa interface of the listed sensors. The majority of CoLa telegrams can be used among all listed sensors. Due to hardware specifics some telegrams requests are only valid for some sensors.

- :link: [Telegram Listing]([device-configuration/cola/cola-general.md](https://cdn.sick.com/media/docs/7/27/927/technical_information_telegram_listing_ranging_sensors_lms1xx_lms5xx_tim2xx_tim5xx_tim7xx_lms1000_mrs1000_mrs6000_nav310_ld_oem15xx_ld_lrs36xx_lms4000_lrs4000_en_im0045927.pdf))


# CoLa error codes

| Error code                  | Description                                                                                                                                                                                                                    | Dec | Hex |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- | --- |
| Ok                          | No error                                                                                                                                                                                                                       | 0   | 0   |
| METHODIN_ACCESSDENIED       | Wrong user level, access to method not allowed                                                                                                                                                                                 | 1   | 1   |
| METHODIN_UNKNOWNINDEX       | Trying to access a method with an unknown  index                                                                                                                                                                               | 2   | 2   |
| VARIABLE_UNKNOWNINDEX       | Trying to access a variable with an unknown  index                                                                                                                                                                             | 3   | 3   |
| LOCALCONDITIONFAILED        | Local condition violated, e.g. giving a value that exceeds the minimum or maximum allowed value for this variable                                                                                                              | 4   | 4   |
| INVALID_DATA                | Invalid data given for variable, this error code is deprecated (is not used anymore).                                                                                                                                          | 5   | 5   |
| UNKNOWN_ERROR               | An error with unknown reason occurred, this error code is deprecated.                                                                                                                                                          | 6   | 6   |
| BUFFER_OVERFLOW             | The communication buffer was too small for the amount of data that should be serialized.                                                                                                                                       | 7   | 7   |
| BUFFER_UNDERFLOW            | More data was expected, the allocated buffer could not be filled.                                                                                                                                                              | 8   | 8   |
| UNKNOWN_TYPE                | The variable that shall be serialized has an un­known type. This can only happen when there are variables in the firmware of the sensor that do not exist in the released description of the sensor. This should never happen. | 9   | 9   |
| VARIABLE_WRITE_ACCESSDENIED | It is not allowed to write values to this variable. Probably the variable is defined as read-only.                                                                                                                             | 10  | A   |
| UNKNOWN_CMD_FOR_NAMESERVER  | When using names instead of indices, a command was issued that the name server does not under­stand.                                                                                                                           | 11  | B   |
| UNKNOWN_COLA_COMMAND        | The CoLa protocol specification does not define the given command, command is unknown.                                                                                                                                         | 12  | C   |
| METHODIN_SERVER_BUSY        | It is not possible to issue more than one command at a time to an SRT sensor.                                                                                                                                                  | 13  | D   |
| FLEX_OUT_OF_BOUNDS          | An array was accessed over its maximum length.                                                                                                                                                                                 | 14  | E   |
| EVENTREG_UNKNOWNINDEX       | The event you wanted to register for does not exist, the index is unknown.                                                                                                                                                     | 15  | F   |
| COLA_A_VALUE_OVERFLOW       | The value does not fit into the value field, it is too large.                                                                                                                                                                  | 16  | 10  |
| COLA_A_INVALID_CHARACTER    | Character is unknown, probably not alphanumeric.                                                                                                                                                                               | 17  | 11  |
| OSAI_NO_MESSAGE             | Only when using SRTOS in the firmware and distri­buted variables this error can occur. It is an indica­tion that no operating system message could be created. This happens when trying to GET a vari­able.                    | 18  | 12  |
| OSAI_NO_ANSWER_MESSAGE      | This is the same as OSAI_NO_MESSAGE with the difference that it is thrown when trying to PUT a variable.                                                                                                                       | 19  | 13  |
| INTERNAL                    | Internal error in the firmware, problably a pointer to a parameter was null.                                                                                                                                                   | 20  | 14  |
| HubAddressCorrupted         | The Sopas Hubaddress is either too short or too long.                                                                                                                                                                          | 21  | 15  |
| HubAddressDecoding          | The Sopas Hubaddress is invalid, it can not be decoded (Syntax).                                                                                                                                                               | 22  | 16  |
| HubAddressAddressExceeded   | Too many hubs in the address                                                                                                                                                                                                   | 23  | 17  |
| HubAddressBlankExpected     | When parsing a HubAddress an expected blank was not found. The HubAddress is not valid.                                                                                                                                        | 24  | 18  |
| AsyncMethodsAreSuppressed   | An asynchronous method call was made although the sensor was built with “AsyncMethodsSuppressed”. This is an internal error that should never happen in a released sensor.                                                     | 25  | 19  |
| ComplexArraysNotSupported   | sensor was built with „ComplexArraysSuppressed“ because the compiler does not allow recursions. But now a complex array was found. This is an in­ternal error that should never happen in a released sensor.                   | 26  | 20  |