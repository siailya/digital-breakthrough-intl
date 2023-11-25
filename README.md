# PublicPulse AI
## Решение команды flint3s для хакатона "Цифровой Прорыв 2023" (международный)

---  

## Демо: https://publicpulse.flint3s.ru/

### Модели

В решении используются BERT-модели для классификации тем, групп тем и исполнителей. Так же используется фреймворк natasha для NER (извлечение адресов).  

Код обучения находится в папке `/notebooks` в ветке [slavchik](https://github.com/siailya/digital-breakthrough-intl/tree/slavchik/notebooks)

**Скачать обученные модели**: https://drive.google.com/drive/folders/1v-11MdeCbrQ07oyLs3pGhCdt9yeInIZ0?usp=sharing

### Бэкенд

Так же для удобного инференса моделей написан бэкенд на fastapi. Для запуска необходимо уставновить библиотеки:

```shell
pip install -r requirements.txt
```

Обученные модели необходимо сложить в папку `/models` со следующей структурой:

- `models`
- - `models/executor`
- - - `models/executor/checkpoint`
- - - `models/executor/label_encoder.pkl`

Аналогично для моделей subject и subject_group

Для запуска бэкенда:

```shell
python api.py
```

### Фронтенд

Для удобного взаимодействия разработан фронтенд на Vue.js.

Для запуска необходимо уставновить библиотеки:

```shell
npm install
```

Для запуска фронтенда:
```shell
npm run dev
```