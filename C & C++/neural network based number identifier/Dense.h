#ifndef DENSE_H
#define DENSE_H

#include "Activation.h"

// Insert Dense class here...
class Dense
{
    Matrix _weights, _bias;
    ActivationFunction _func;
public:
    Dense(Matrix &weights, Matrix &bias, ActivationFunction func);//constructor
    Matrix get_weights(); //get weights
    Matrix get_bias(); //get bias
    ActivationFunction get_activation(); // get func activation
    Matrix operator()(const Matrix& input) const; // puts input in Dense
};

#endif //DENSE_H
