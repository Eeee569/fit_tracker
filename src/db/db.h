//
// Created by will on 9/17/22.
//

#ifndef FIT_TRACKER_DB_H
#define FIT_TRACKER_DB_H


class DB
{
private:
    int m_year;
    int m_month;
    int m_day;

public:
    DB(int year, int month, int day);

    void SetDate(int year, int month, int day);

    int getYear() { return m_year; }
    int getMonth() { return m_month; }
    int getDay()  { return m_day; }
};


#endif //FIT_TRACKER_DB_H



