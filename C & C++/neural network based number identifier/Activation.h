#ifndef ACTIVATION_H
#define ACTIVATION_H

#include "Matrix.h"
// Insert Activation namespace here...
namespace activation {
    Matrix relu(const Matrix& mat);
    Matrix softmax(const Matrix& mat);
};

typedef Matrix (*ActivationFunction)(const Matrix& matrix);

#endif //ACTIVATION_H