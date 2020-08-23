# nlp_project_innoabdt
### Общий принцип работы проекта
![alt text](https://github.com/DmitriyVahrushev/nlp_project_innoabdt/blob/master/materails/scheme_1.png "Logo Title Text 1")

### Инструкция по запуску
В каждом ноутбуке используются библиотеки pymystem3, nltk, pandas, numpy.

Для запуска кода по распознаванию продуктов (ProductRecognition) потребуются библиотеки natasha == 0.10.0 и yargy==0.12.0 . 
Для запуска кода по вычислению f1-меры для NER дополнительно потребуется библиотека deeppavlov 

### Описание структуры проектов и файлов
В папке ProductRecognition:
ProductRecognition.ipynb - модель по распознаванию продуктов, вычисление accuracy для него. 
NER_filters -  вспомогательные функции для нахождения различных сущностей
product_types - названия текущих продуктов, синонимы к ним, ключевые слова
products.csv - типы продуктов (кредиты, карты и т.д.)
test_2.csv - тестовый датасет для ProductRecognition. 105 размеченных сообщений. 2 колонки: text - текст сообщения, product - название продукта о котором говорится в сообщении. 
extractor.py, number.py - функции для извлечения чисел из текста

В папке metrics_calculation:
natash_vs_deeppavlov -  сравнение библиотек natasha и deeppavlov по времени работы, по качеству распознавания сум и денежных сумм
остальные файлы в папке - размеченные датасеты 
