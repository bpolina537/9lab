use pyo3::prelude::*;

// Структура с полем factor
#[pyclass]
struct DataProcessor {
    factor: i32,
}

#[pymethods]
impl DataProcessor {
    // Конструктор
    #[new]
    fn new(factor: i32) -> Self {
        DataProcessor { factor }
    }

    // Метод process: умножает каждое число в списке на factor
    fn process(&self, data: Vec<i32>) -> Vec<i32> {
        data.iter().map(|x| x * self.factor).collect()
    }

    // Метод для получения factor
    fn get_factor(&self) -> i32 {
        self.factor
    }
}

// Модуль для Python
#[pymodule]
fn rust_processor(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<DataProcessor>()?;
    Ok(())
}

// ============================================
// Юнит-тесты
// ============================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_processor() {
        let p = DataProcessor::new(5);
        assert_eq!(p.get_factor(), 5);
    }

    #[test]
    fn test_new_processor_negative() {
        let p = DataProcessor::new(-3);
        assert_eq!(p.get_factor(), -3);
    }

    #[test]
    fn test_new_processor_zero() {
        let p = DataProcessor::new(0);
        assert_eq!(p.get_factor(), 0);
    }

    #[test]
    fn test_process_positive() {
        let p = DataProcessor::new(3);
        let result = p.process(vec![1, 2, 3, 4, 5]);
        assert_eq!(result, vec![3, 6, 9, 12, 15]);
    }

    #[test]
    fn test_process_negative_numbers() {
        let p = DataProcessor::new(2);
        let result = p.process(vec![-1, -2, -3]);
        assert_eq!(result, vec![-2, -4, -6]);
    }

    #[test]
    fn test_process_negative_factor() {
        let p = DataProcessor::new(-2);
        let result = p.process(vec![1, 2, 3]);
        assert_eq!(result, vec![-2, -4, -6]);
    }

    #[test]
    fn test_process_zero_factor() {
        let p = DataProcessor::new(0);
        let result = p.process(vec![1, 2, 3]);
        assert_eq!(result, vec![0, 0, 0]);
    }

    #[test]
    fn test_process_empty() {
        let p = DataProcessor::new(10);
        let result = p.process(vec![]);
        assert_eq!(result, Vec::<i32>::new());
    }

    #[test]
    fn test_process_single() {
        let p = DataProcessor::new(7);
        let result = p.process(vec![42]);
        assert_eq!(result, vec![294]);
    }

    #[test]
    fn test_process_large_numbers() {
        let p = DataProcessor::new(100);
        let result = p.process(vec![1000, 2000, 3000]);
        assert_eq!(result, vec![100000, 200000, 300000]);
    }

    #[test]
    fn test_factor_unchanged() {
        let p = DataProcessor::new(4);
        assert_eq!(p.get_factor(), 4);
        let _ = p.process(vec![1, 2, 3]);
        assert_eq!(p.get_factor(), 4);
    }

    #[test]
    fn test_multiple_calls() {
        let p = DataProcessor::new(2);
        let result1 = p.process(vec![1, 2, 3]);
        let result2 = p.process(vec![4, 5, 6]);
        assert_eq!(result1, vec![2, 4, 6]);
        assert_eq!(result2, vec![8, 10, 12]);
    }
}