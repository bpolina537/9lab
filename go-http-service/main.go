package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "time"
)

type ComputeRequest struct {
    Numbers []int `json:"numbers"`
}

type ComputeResponse struct {
    Result  int     `json:"result"`
    TimeMs  float64 `json:"time_ms"`
}

func main() {
    http.HandleFunc("/compute", computeHandler)
    fmt.Println("HTTP Server listening on port 8081")
    log.Fatal(http.ListenAndServe(":8081", nil))
}

func computeHandler(w http.ResponseWriter, r *http.Request) {
    start := time.Now()

    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    var req ComputeRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    // Тяжёлые вычисления: сумма квадратов
    result := 0
    for _, n := range req.Numbers {
        result += n * n
    }

    // Искусственная задержка для имитации тяжёлой работы
    time.Sleep(100 * time.Millisecond)

    elapsed := time.Since(start).Seconds() * 1000

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(ComputeResponse{
        Result: result,
        TimeMs: elapsed,
    })
}