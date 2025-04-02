//
// Created by yairt on 04/09/2023.
//

#include <iostream>
#include "Matrix.h"
#include "cmath"
#define DEF_SIZE_MAT 1
#define DEF_MAT_VAL 0
#define PRINT_CONST 0.1

Matrix ::Matrix(int rows, int cols) :_rows(rows), _cols(cols)
{
    if (_rows < 0 || _cols < 0){
        throw std::length_error("wrong dimentions");
    }
    _mat = new float[rows*cols];
    for (int i = 0; i <rows*cols ; i++)
    {
        _mat[i] = DEF_MAT_VAL;
    }
}

Matrix::Matrix()
{
    _cols = DEF_SIZE_MAT ;
    _rows = DEF_SIZE_MAT;
    _mat = new float[DEF_SIZE_MAT];
    _mat[0] = DEF_MAT_VAL;
}

Matrix::Matrix(const Matrix &matrix)
{
    this ->_rows = matrix._rows;
    this->_cols = matrix._cols;
    this ->_mat = new float[_rows*_cols];
    for (int i = 0; i < _rows*_cols ; i++)
    {
        _mat[i] = matrix._mat[i];
    }
}

Matrix& Matrix::transpose()
{

    auto *new_mat = new float[_rows * _cols];
    for (int i = 0; i < _rows ; ++i)
    {
        for (int j = 0; j < _cols ; ++j){
            new_mat[j * _rows + i] = _mat[i * _cols + j];
        }
    }
    int temp = _rows;
    _rows = _cols;
    _cols = temp;
    float *old_mat = _mat;
    _mat = new_mat;
    delete[] old_mat;
    return *this;
}


Matrix& Matrix::vectorize()
{
    int new_rows = _rows * _cols;
    _rows = new_rows;
    _cols = DEF_SIZE_MAT;
    return *this;
}


void Matrix::plain_print()
{
    for (int i = 0; i < _rows; i++){
        int row_start = i* _cols;
        for (int j=0; j<_cols; j++){
            std::cout << _mat[row_start + j] << " ";
        }
        std::cout<< std::endl;
    }
}


Matrix Matrix::dot(const Matrix &mat) const
{
    if(_rows != mat._rows || _cols != mat._cols){
        throw std::length_error("Matrix dimentions don't match, therfore "
                                 "Error recived1");
    }
    Matrix new_mat(_rows, _cols);
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            new_mat._mat[row_start + j] = this ->_mat[row_start + j] *
                    mat._mat[row_start +j];
        }
    }
    return new_mat;
}


float Matrix::norm() const
{
    float sum = 0;
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            sum += this->_mat[row_start +j] * this->_mat[row_start + j];
        }
    }
    return std::sqrt(sum);
}


int Matrix::argmax() const
{
    int max = 0;
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            if (this->_mat[row_start + j] > this->_mat[max]){
                max = this->_mat[row_start +j];
            }
        }
    }
    return max;
}


float Matrix::sum() const
{
    float sum = 0;
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            sum += _mat[row_start + j];
        }
    }
    return sum;
}


Matrix &Matrix::operator+=(const Matrix &mat)
{
    if(_cols != mat._cols || _rows != mat._rows){
        throw std::length_error("Matrix dimentions don't match, therfore "
                                 "Error "
                                 "recived2");
    }
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            this ->_mat[row_start + j] += mat._mat[row_start +j];
        }
    }
    return *this;
}


Matrix Matrix::operator+(const Matrix &mat) const
{
    if(_cols != mat._cols || _rows != mat._rows){
        throw std::length_error("Matrix dimentions don't match, therfore "
                                 "Error "
                           "recived3");
    }
    Matrix new_mat(_rows, _cols);
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            new_mat._mat[row_start + j] = this ->_mat[row_start + j] +
                                           mat._mat[row_start +j];
        }
    }
    return new_mat;
}


Matrix &Matrix::operator=(const Matrix &mat)
{
    if (this == &mat){
        return *this;
    }
    this->_cols = mat._cols;
    this->_rows = mat._rows;
    auto* new_mat = new float[_rows * _cols];
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            new_mat[row_start + j] = mat._mat[row_start +j];
        }
    }
    delete[] this->_mat;
    this->_mat = new_mat;
    return *this;
}



Matrix Matrix::operator*(const Matrix &mat) const
{
    if(_cols != mat._rows) {
        throw std::length_error("Matrix dimentions don't match, therfore "
                                 "Error "
                                 "recived");
    }
    Matrix new_mat(_rows, mat._cols);
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i *_cols;
        for (int j = 0; j< mat._cols; j++){
            float sum = 0;
            for (int e = 0; e < mat._rows; e++){
                sum += this->_mat[row_start + e] *
                        mat._mat[j + mat._cols * e];
            }
            new_mat._mat[i * mat._cols + j] = sum;
        }
    }
    return new_mat;
}



Matrix Matrix::operator*(float c)
{
    Matrix new_mat(_rows, _cols);
    for (int i = 0 ; i<_rows; i++ ){
        int row_start = i*_cols;
        for (int j = 0; j< _cols; j++){
            new_mat._mat[row_start + j] = this->_mat[row_start +j] * c;
        }
    }
    return new_mat;
}



Matrix operator* (float c,const Matrix &mat )
{
    Matrix new_mat(mat._rows, mat._cols);
    for (int i = 0 ; i<mat._rows; i++ ){
        int row_start = i*mat._cols;
        for (int j = 0; j< mat._cols; j++){
            new_mat._mat[row_start + j] = mat._mat[row_start +j] * c;
        }
    }
    return new_mat;
}



float Matrix::operator()(int i, int j) const
{
    if ( i> _rows || j> _cols || i<0 || j<0){
        throw std::out_of_range("invalid a");
    }
    return _mat[i* _cols + j];
}


float& Matrix::operator()(int i, int j)
{
    if ( i> _rows || j> _cols || i<0 || j<0){
        throw std::out_of_range("invalid b");
    }
    return _mat[i* _cols + j];
}


float& Matrix::operator[](int i)
{
    if ( i>=(_cols * _rows) ||i<0){
        throw std::out_of_range("invalid c");
    }
    return _mat[i];
}


float Matrix::operator[](int i) const
{
    if ( i>= (_cols * _rows) ||i<0){
        throw std::out_of_range("invalid d");
    }
    return _mat[i];
}


std::ostream &operator<< (std::ostream &ostream, const Matrix &matrix)
{
    for(int i = 1; i <= matrix._rows; i++){
        for (int j=1; j <= matrix._cols; j++){
            if (matrix(i,j) > PRINT_CONST){
                ostream << "**" ;
            }
            else{ostream << "  ";}
        }
        ostream << std::endl;
    }
    return ostream;
}


std::istream &operator>>(std::istream &is, Matrix &matrix)
{
    for (int i = 0; i < matrix.get_rows(); i++) {
        for (int j = 0; j < matrix.get_cols(); j++) {
            is.read((char *) &matrix(i, j), sizeof(float)* matrix._cols
            * matrix._rows);
        }
    }
    return is;
}