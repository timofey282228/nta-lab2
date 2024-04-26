# Алгоритм Сілвера-Поліга-Геллмана

Це реалізація алгоритму С-П-Г.
Всю інформацію про порядок використання можна отримати
через інтерфейс командного рядка.

## Docker

```shell
docker pull timofey282228/nta-lab2
# Тепер образ контейнера доступний локально і з ним можна працювати
# Виведемо всі опції
docker run --rm -it timofey282228/nta-lab2 --help
```

> [!NOTE]
> Команда `benchmark` в Docker-контейнері __не працюватиме__,
> оскільки вимагає наявності `docker` для запуску контейнера генератора задач.

## Local

```shell
git clone https://github.com/timofey282228/nta-lab2.git
cd nta-lab2
poetry install
poetry run python -m nta_lab2 --help
```
