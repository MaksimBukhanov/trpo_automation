#ifndef STARTEGYLAB_H
#define STARTEGYLAB_H

#include <QObject>
#include <QtXml>

/**
 * @brief Класс для проверки лабораторных работ
 *  по паттерну 'Стратегия'
 */
class StrategyLab: public QObject
{
    Q_OBJECT

private:
    int labNumber;
    QString comments;
    QFile xmlFile;

public:
    explicit StrategyLab(int, QObject* parent = nullptr);
    ~StrategyLab();
    bool check(const QList<QString>);
    bool hasComments() const { return !comments.isEmpty(); }
    QString getComments() const { return comments; }

private:
    bool checkInside(const QList<QString>, const QDomNode&);
};

#endif // STARTEGYLAB_H
