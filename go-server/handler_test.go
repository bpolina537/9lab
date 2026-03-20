package main

import (
    "bufio"
    "net"
    "testing"
    "time"
)

func TestHandleConnection(t *testing.T) {
    server, client := net.Pipe()
    defer server.Close()
    defer client.Close()

    go handleConnection(server)

    message := "hello\n"
    client.Write([]byte(message))

    response, err := bufio.NewReader(client).ReadString('\n')
    if err != nil {
        t.Fatalf("Failed to read response: %v", err)
    }

    expected := "OK\n"
    if response != expected {
        t.Errorf("Expected %q, got %q", expected, response)
    }
}

func TestHandleConnectionMultipleMessages(t *testing.T) {
    server, client := net.Pipe()
    defer server.Close()
    defer client.Close()

    go handleConnection(server)

    // Отправляем одно сообщение
    message := "test\n"
    client.Write([]byte(message))

    response, err := bufio.NewReader(client).ReadString('\n')
    if err != nil {
        t.Fatalf("Failed to read response: %v", err)
    }

    if response != "OK\n" {
        t.Errorf("Expected OK, got %q", response)
    }
}

func TestConcurrency(t *testing.T) {
    listener, err := net.Listen("tcp", ":8082")
    if err != nil {
        t.Fatalf("Failed to start server: %v", err)
    }
    defer listener.Close()

    go func() {
        for {
            conn, err := listener.Accept()
            if err != nil {
                return
            }
            go handleConnection(conn)
        }
    }()

    time.Sleep(100 * time.Millisecond)

    const numClients = 10
    done := make(chan bool, numClients)

    for i := 0; i < numClients; i++ {
        go func(id int) {
            conn, err := net.Dial("tcp", "localhost:8082")
            if err != nil {
                t.Errorf("Client %d failed to connect: %v", id, err)
                done <- false
                return
            }
            defer conn.Close()

            message := "test\n"
            conn.Write([]byte(message))

            response := make([]byte, 1024)
            n, err := conn.Read(response)
            if err != nil {
                t.Errorf("Client %d failed to read: %v", id, err)
                done <- false
                return
            }

            if string(response[:n]) != "OK\n" {
                t.Errorf("Client %d expected OK, got %q", id, string(response[:n]))
                done <- false
                return
            }
            done <- true
        }(i)
    }

    successCount := 0
    for i := 0; i < numClients; i++ {
        if <-done {
            successCount++
        }
    }

    if successCount != numClients {
        t.Errorf("Only %d/%d clients succeeded", successCount, numClients)
    }
}

func BenchmarkHandleConnection(b *testing.B) {
    server, client := net.Pipe()
    defer server.Close()
    defer client.Close()

    go handleConnection(server)

    message := "bench\n"
    for i := 0; i < b.N; i++ {
        client.Write([]byte(message))
        bufio.NewReader(client).ReadString('\n')
    }
}