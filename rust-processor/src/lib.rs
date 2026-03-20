use pyo3::prelude::*;

#[pyclass]
struct DataProcessor {
    factor: i32,
}

#[pymethods]
impl DataProcessor {
    #[new]
    fn new(factor: i32) -> Self {
        DataProcessor { factor }
    }

    fn process(&self, data: Vec<i32>) -> Vec<i32> {
        data.iter().map(|x| x * self.factor).collect()
    }

    fn get_factor(&self) -> i32 {
        self.factor
    }
}

#[pymodule]
fn rust_processor(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<DataProcessor>()?;
    Ok(())
}