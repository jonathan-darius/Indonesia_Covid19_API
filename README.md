COVID19 Cases & Vaccination Rates in Indonesia
==============================================

Repository ini berisikan source code project untuk menampilkan data penyebaran kasus covid19 berdasarkan Tahun, Bulan, dan tanggal.


### Bagaimana cara kerjanya?
* Generate data untuk dimasukan database terlebih dahulu dengan cara `POST http://host:port/daily/update_data`.
* Maka secara otomatis server akan memperbaharui data di database sesuai dengan data pada `https://data.covid19.go.id/public/api/update.json`.
* Setelah itu API siap digunakan.

### Endpoint
#### 1. Entry point untuk semua API, menyediakan data kasus covid 19 secara umum.
```
GET http://host:port/
```
Contoh Response:
```
{
    "ok":true,
    "data":{
        "total_positive":156865,
        "total_recovered":5955577,
        "total_deaths":6143431,
        "total_active":2483,
        "new_positive":5085,
        "new_recovered":2596,
        "new_deaths":6,
        "new_active":2483
    },
    "message":true
}
```
#### 2. Mengambil Data Berdasarkan Tahun
```
GET http://host:port/yearly/{year}
```
Contoh Response `GET http://host:port/yearly/2020`:
```
{
    "ok": true,
    "data": {
        "year": "2020",
        "positive": 22138,
        "recovered": 611097,
        "deaths": 743198,
        "active": 109963
    },
    "message": true
}
```
#### 3. Mengambil Data Berdasarkan Bulan
```
GET http://host:port/monthly/{year}/{month}
```
Contoh Response `GET http://host:port/monthly/2020/12`:
```
{
    "ok": true,
    "data": {
        "month": "2020-12",
        "positive": 22138,
        "recovered": 611097,
        "deaths": 743198,
        "active": 109963
    },
    "message": true
}
```

#### 4. Mengambil Data Berdasarkan Tanggal
```
GET http://host:port/daily/{year}/{month}/{date}
```
Contoh Response `GET http://host:port/daily/2021/01/01`:
```
{
    "ok": true,
    "data": {
        "month": "2021-01-01",
        "positive": 8072,
        "recovered": 6839,
        "deaths": 191,
        "active": 1042
      },
    "message": true
}
```
#### 5. Memperbaharui data pada Database
```
POST http://host:port/daily/update_data
```
Contoh Response:
```
{
    "Update": {
        "positif": 5085,
        "date": "2022-07-19",
        "kum_meninggal": 6143431,
        "kum_sembuh": 5955577,
        "kum_dirawat": 30989,
        "meninggal": 6,
        "sembuh": 2596,
        "dirawat": 2483,
        "kum_positif": 156865
    },
    "daily": [
        {
          "positif": 2,
          "date": "2020-03-02",
          "kum_meninggal": 2,
          "kum_sembuh": 0,
          "kum_dirawat": 2,
          "meninggal": 0,
          "sembuh": 0,
          "dirawat": 2,
          "kum_positif": 0
        },
        {
          "positif": 0,
          "date": "2020-03-03",
          "kum_meninggal": 2,
          "kum_sembuh": 0,
          "kum_dirawat": 2,
          "meninggal": 0,
          "sembuh": 0,
          "dirawat": 0,
          "kum_positif": 0
        },
        ...
    ]
}
```