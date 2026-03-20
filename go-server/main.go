package main

import (
    "bufio"
    "fmt"
    "net"
    "os"
)

func main() {
    // Запускаем TCP-сервер на порту 8080
    listener, err := net.Listen("tcp", ":8080")
    if err != nil {
        fmt.Println("Error starting server:", err)
        os.Exit(1)
    }
    defer listener.Close()

    fmt.Println("TCP Server listening on port 8080")

    for {
        // Принимаем соединение
        conn, err := listener.Accept()
        if err != nil {
            fmt.Println("Error accepting connection:", err)
            continue
        }

        // Обрабатываем каждое соединение в отдельной горутине
        go handleConnection(conn)
    }
}

func handleConnection(conn net.Conn) {
    defer conn.Close()

    // Читаем сообщение от клиента
    message, err := bufio.NewReader(conn).ReadString('\n')
    if err != nil {
        fmt.Println("Error reading:", err)
        return
    }

    fmt.Printf("Received: %s", message)

    // Отвечаем "OK"
    conn.Write([]byte("OK\n"))
}