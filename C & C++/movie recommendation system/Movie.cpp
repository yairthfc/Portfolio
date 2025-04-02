
#include "Movie.h"
#define HASH_START 17
#define RES_MULT 31

/**
 * hash function used for a unordered_map (implemented for you)
 * @param movie shared pointer to movie
 * @return an integer for the hash map
 */
std::size_t sp_movie_hash(const sp_movie& movie){
    std::size_t res = HASH_START;
    res = res * RES_MULT + std::hash<std::string>()(movie->get_name());
    res = res * RES_MULT + std::hash<int>()(movie->get_year());
    return res;
}

/**
 * equal function used for an unordered_map (implemented for you)
 * @param m1
 * @param m2
 * @return true if the year and name are equal else false
 */
bool sp_movie_equal(const sp_movie& m1,const sp_movie& m2){
    return !(*m1 < *m2) && !(*m2 < *m1);
}


Movie ::Movie(const std::string &name, int year)
{
    _name = name;
    _year = year;
}

//bool check_words(const string& a,const string& b){
//    int i =0;
//    while(i< (int) a.length() & i < (int) b.length()){
//        if ((a[i] == b[i])){
//            i++;
//            continue;
//        }
//        if(a[i] < b[i]){
//            return true;
//        }
//        else{return false;}
//    }
//    if(a.length() < b.length()){
//        return true;
//    }
//    else{return false;}
//}

bool Movie::operator<(const Movie &movie) const
{
    auto a = this->_name;
    if (this->_name == movie._name)
    {
        return false;
    }
    if (this->_year == movie._year){
        return this->_name < movie._name;
    }
    return this->_year < movie._year;
}


std::ostream& operator<<(std::ostream& os, const Movie& movie){
    os << movie._name << "(" << movie._year << ")" << std::endl;
    return os;
}