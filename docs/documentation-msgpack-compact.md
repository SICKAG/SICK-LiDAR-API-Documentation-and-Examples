<img align=right width="200" src="../docs/img/sick-logo.jpg"/> 

Measurement Data Streaming via COMPACT and MSGPACK
---

---------

<details>
  <summary>Table of content</summary>

- [Examples](#examples)
- [COMPACT Format](#compact-format)
- [MSGPACK Format](#msgpack-format)


</details>

---------

# Examples
All available examples can be found [here](examples/).

# COMPACT Format

- *SICK proprietary LiDAR format*
- *works via UDP*
- *more information will follow*

# MSGPACK Format

MSGPACK is a binary data serialization format that is designed to be more efficient and COMPACT than [JSON](https://www.json.org/json-en.html).

One of the main advantages of MSGPACK is its COMPACT binary representation, which can significantly reduce the size of data when compared to JSON. This makes it well-suited for use cases where bandwidth or storage space is limited, such as in embedded systems or mobile devices.

MSGPACK also supports a wide range of data types, including integers, floats, strings, arrays, and maps. This allows it to handle complex data structures with ease. MSGPACK is that it is language-independent, which means that you can use it to communicate between different programming languages. It has implementations for many programming languages like C, C++, C#, D, Go, Java, Lua, Perl, PHP, Python, Ruby, Rust, Scala, Shell, Swift and more. This works via UDP.


