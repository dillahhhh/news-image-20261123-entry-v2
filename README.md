# Dunia dalam Satu Halaman — Senin, 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/dillahhhh/news-image-20261123-entry-v2/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

Satu gambar yang merangkum berita dunia Senin, 23 November 2026: 34 cerita
dalam satu halaman koran berbahasa Indonesia — dari serangan tanker di Selat
Hormuz dan peringatan Trump ke Iran, mayoritas DPR AS untuk Demokrat (258
kursi), hingga COP31 yang berakhir tanpa kesepakatan. Hasil olahraga akhir
pekan (Alcaraz, Márquez, Liverpool 4-0 Man Utd, Boca) diberi label jelas
sebagai AKHIR PEKAN di strip bawah.

## Isi repo

- `entry.png` — gambar final 1024×1024 (171.647 byte), dirender oleh
  `build_image.py` dari 34 cerita yang diriset dan ditulis segar di sesi
  build ini. Setiap cerita dicek tanggalnya terhadap sumber berita 23 Nov
  2026; klaim yang tak terverifikasi tidak dipakai.
- `build_image.py` — renderer (Python + PIL) yang menggambar halaman koran:
  masthead, pita tanggal, berita utama, dua sorotan, tiga kolom seksi
  (Perang & Konflik, Politik, Ekonomi & Teknologi, Dunia), dan strip akhir
  pekan. Deterministik: dua run menghasilkan byte yang sama.
- `main.py` — program entri (stdlib saja): menyalin `entry.png` ke
  `/output/entry.png`.

## Menjalankan

```sh
python3 build_image.py          # render ulang entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # uji program entri
```

## Kompetisi

[news-image-20261123 — Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123)
($100, 50 besar dibayar; entri ditutup 25 November 2026 07:00 WIB).
