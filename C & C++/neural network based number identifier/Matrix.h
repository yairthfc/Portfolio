// Matrix.h
#ifndef MATRIX_H
#define MATRIX_H
#include <iostream>
#include <fstream>
#include <cmath>
/**
 * @struct matrix_dims
 * @brief Matrix dimensions container. Used in MlpNetwork.h and main.cpp
 */
typedef struct matrix_dims
{
	int rows, cols;
} matrix_dims;

// Insert Matrix class here...

class Matrix{
private:
    int _rows;
    int _cols;
    float* _mat;

public:
    // constructors and destructors
    Matrix(int rows, int cols);  // constructor
    Matrix();  // default constructor
    Matrix(const Matrix& matrix);  // copy constructor
    ~Matrix(){delete[] _mat;};  // destructor
    // Methods and Functions
    int get_rows() const {return _rows;};  // get rows
    int get_cols() const {return _cols;};  // get cols
    Matrix& transpose();  // transposes the matrix
    Matrix& vectorize();  // vectorizing the matrix
    void plain_print();  // prints the matrix
    Matrix dot(const Matrix& mat) const;  // return the element-wise
    // multiplication of 2 metrics
    float norm() const; // returns the norm of the matrix
//  Matrix rref() const;
    int argmax() const; // return the index of the maximum
    // element in the matrix
    float sum() const;
    Matrix& operator+=(const Matrix& mat);
    Matrix operator+(const Matrix& mat) const;
    Matrix& operator=(const Matrix& mat);
    Matrix operator*(const Matrix& mat) const;
    Matrix operator*(float c);
    friend Matrix operator*(float c, const Matrix &other);
    float operator()(int i, int j) const;
    float& operator()(int i, int j);
    float operator[](int i) const;
    float& operator[] (int i);
    friend std::ostream& operator<<(std::ostream& os, const Matrix& mat);
    friend std::istream &operator>>(std::istream &is, Matrix &matrix);
};

#endif //MATRIX_H