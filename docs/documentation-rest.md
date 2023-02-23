<img align=right width="200" src="../docs/img/sick-logo.jpg"/> 

Device Configuration via HTTP / REST
---

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

# Background Information

TCP is a transport-layer protocol that ensures reliable data transmission, HTTP is an application-layer protocol that is used to transmit data over the internet, REST is an architectural style for building web services that is based on the principles of HTTP, and OpenAPI specification (formerly known as Swagger) is a specification for building RESTful web services that helps to ensure consistency and ease of use for developers.

# OpenAPI Specification

<img align=right width="200" src="docs/img/openapi.jpg"/> 

The use of an OpenAPI Specification brings several advantages.

:+1: Improved documentation: OpenAPI provides a standardized format for documenting APIs, making it easier for developers to understand and use the API. It's easy to navigate the endpoints, query parameters, request and response payloads, and other details of an API.

:+1: Code generation: OpenAPI specifications can be used to generate code in a variety of programming languages, which can speed up the development process and reduce the risk of errors.

:+1: Testing: OpenAPI specifications can be used to test sensors fast and easily.

:+1: Interoperability: OpenAPI is an open-source and vendor-neutral specification, which means that APIs written in different languages and frameworks can be described using the same format, making it easier to integrate them with other systems.

:+1: Tooling: OpenAPI specification is widely adopted and supported by various tools, frameworks and libraries, which can make it easier to work with an API that has an OpenAPI specification.

:+1: Community: OpenAPI has a large community of developers, which means that there is a lot of support and resources available for working with OpenAPI.


Please refer to the following OpenAPI Specifications. These are used to describe the HTTP interface of the listed sensors. The majority of HTTP requests can be used among all listed sensors. Due to hardware specifics some HTTP requests are only valid for some sensors.

- :link: [openapi-multiScan100.json](examples/rest/openapi-multiScan100.json)

# Challenge and response process
To prevent unauthorized access, the HTTP interfaces underlies an Challenge-response process. It is a participant’s secure authentication process based on knowledge. For this purpose, a participant poses a challenge to which others have to respond in order to prove that he or she knows a certain shared secret without having to transmit this information themselves. This is protection against a password from being listened to by attackers on the line.

For this purpose, there are different detailed methods that are based on this basic principle: If one side (Alice) wants to be authenticated with respect to the other side (Bob), Bob sends a random number N (nonce) to Alice (Bob poses the challenge). Alice adds her password to this number N, applies a cryptological hash function or encryption to this combination, and sends the result to Bob (and consequently returns the response). Bob, who knows the random number, the shared secret (= Alice’s password) as well as the hash function used or encryption, carries out the same calculation, and compares his result to the response from Alice. If both files are identical, Alice is successfully authenticated.

<img style="right;"  width="1000" src="../docs/img/challenge-response.png"/> 

*Overview challenge and response process*

# Insomnia Collection

Sometimes it is helpful to test an interface with a REST client like Insomnia. If you want to write a sensor parameter via RES, you must first log in and pass a corresponding header via a challenge response procedure for each write operation.

To make this easier you can use this Insomnia [plugin](examples/rest/insomina/insomnia-plugin-rest.zip) and import the following Insomnia collection to test the device via the HTTP/REST interface.
Additionally, you can find an Insomnia Collection [here ](examples/rest/insomina/insomina-collection-multiScan100.json) to work with the sensors.

