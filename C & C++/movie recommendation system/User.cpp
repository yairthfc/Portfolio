

// don't change those includes
#include "User.h"
#include "RecommendationSystem.h"


// implement your cpp code here

User ::User(std::string name, rank_map* map,
            std::shared_ptr<RecommendationSystem> system)
{
    _name = name;
    _map = map;
    _system = system;
}

void User::add_movie_to_rs(const std::string &name, int year,
                           const std::vector<double> &features, double rate)
{
    _system->add_movie(name, year, features);
    Movie movie(name, year);
    sp_movie sp = std::make_shared<Movie>(movie);
    (*_map)[sp] = rate;
}

sp_movie User::get_recommendation_by_content() const
{
    return _system->recommend_by_content(*this);
}

sp_movie User::get_recommendation_by_cf(int k) const
{
    return _system->recommend_by_cf(*this, k);
}

double User::get_prediction_score_for_movie(const std::string &name, int year,
                                            int k) const
{
    return _system->predict_movie_score(*this, _system->get_movie(name, year)
                                        , k);
}

std::ostream& operator<<(std::ostream& os, const User& user){
    os << "name: " << user._name << std::endl;
    os << *user._system;
    return os;
}