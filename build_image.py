# build_image.py — merender "Dunia dalam Satu Halaman", Senin 23 November 2026.
# Koran satu halaman 1024x1024 berisi 34 berita dunia hari itu, ditulis segar
# dari riset berita 23 Nov 2026 (bukan salinan entri lain). Jalankan:
#   python3 build_image.py   -> menulis entry.png (1024x1024, < 1 MiB)
# Renderer deterministik: tanpa waktu, tanpa acak, hasil sama di setiap run.

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (248, 244, 233)      # kertas gading
INK = (25, 25, 25)        # tinta hitam
RED = (166, 25, 46)       # merah koran
BLUE = (30, 58, 92)       # biru tua
GOLD = (138, 109, 27)     # emas
GREY = (90, 88, 80)       # abu-abu
RULE = (201, 194, 174)    # garis pemisah
WHITE = (255, 255, 255)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Bungkus teks ke beberapa baris agar muat dalam max_w piksel."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------------------
# 34 BERITA — Senin, 23 November 2026 (hasil riset hari ini; tanggal dicek
# satu per satu terhadap sumber berita. Cerita akhir pekan diberi label
# AKHIR PEKAN di strip bawah, bukan diklaim sebagai peristiwa hari Senin.)
# ---------------------------------------------------------------------------

LEAD = {
    "kicker": "PERANG IRAN MEMUNCAK",
    "head": "TANKER DISERANG DI SELAT HORMUZ",
    "deck": "Trump ancam Iran: hasil \u201csangat traumatis\u201d bila kesepakatan "
            "nuklir gagal. Sedikitnya tiga kapal tanker diserang di jalur "
            "minyak tersibuk dunia saat perang meluas ke Bahrain dan Teluk.",
}

ROW2 = [
    {
        "tag": "POLITIK AS",
        "head": "DEMOKRAT REBUT DPR AS",
        "body": "258 kursi \u2014 mayoritas terbesar sejak 1992. Recount di North "
                "Carolina memastikan kemenangan Hubbard; empat kursi masih "
                "diperebutkan.",
    },
    {
        "tag": "IKLIM",
        "head": "COP31 BERAKHIR TANPA KESEPAKATAN",
        "body": "Konferensi iklim PBB terpanjang dalam sejarah bubar di Turki "
                "tanpa perjanjian soal bahan bakar fosil dan dana iklim.",
    },
]

# Kolom 1 — PERANG & KONFLIK (9 cerita)
COL1 = [
    ("NATO SIDANG DARURAT",
     "Tiga rudal Rusia masuk Polandia; gagal dicegat."),
    ("KAPAL RUSIA TENGGELAM",
     "Merkury tenggelam di Benghazi, kata Zelenskyy."),
    ("DYMER: 15 TEWAS",
     "Blok apartemen dekat Kyiv hancur; 15 tewas."),
    ("153 DRONE DALAM SEMALAM",
     "134 dari 153 drone Rusia ditembak jatuh."),
    ("KAPAL KARGO RUSIA TERBAKAR",
     "Sparta II terbakar di Baltik, hanyut ke Finlandia."),
    ("99% GAZA TERCEMAR RACUN",
     "Air, tanah, dan pangan Gaza tercemar racun."),
    ("KHARTOUM DISERANG DRONE",
     "Rumah hancur, gedung PBB rusak di Khartoum."),
    ("IRAN: LAWAN BLOKADE AS",
     "Teheran pakai \u201csemua alat\u201d lawan blokade AS."),
    ("\u201cTERORISME YAHUDI\u201d",
     "Rival Netanyahu kecam serangan pemukim."),
]

# Kolom 2 — POLITIK (6) + EKONOMI (3)
COL2_POL = [
    ("TRUMP BATASI PENGAWASAN",
     "Kontraktor wajib lapor Gedung Putih soal Kongres."),
    ("KORSEL ROMBAK KABINET",
     "Kang Kum-sil kepala intel wanita pertama Korsel."),
    ("HASINA AKAN DITANGKAP",
     "Mantan PM dipenjara bila pulang dari India."),
    ("SATELIT NUKLIR RUSIA?",
     "Moskow rencanakan satelit bersenjata nuklir."),
    ("DENMARK: RUSIA INCAR RAPPER",
     "Kopenhagen tuduh Moskow incar rapper."),
    ("PRABOWO USUL 2 CAWAPRES",
     "Presiden nominasikan dua kandidat wapres."),
]
COL2_ECO = [
    ("SENSEX ANJLOK 1.484",
     "Bursa India jatuh 1,77%; Nifty ke 25.349."),
    ("TAIWAN LARANG SHORT-SELLING",
     "Larangan jual pendek berlaku mulai hari ini."),
    ("NVIDIA NAIK 7%+",
     "Trump desak Huang kembali; saham rebound."),
]

# Kolom 3 — EKONOMI & TEKNOLOGI (4) + DUNIA (5)
COL3_ECO_TEC = [
    ("DAGANG JEPANG & INDONESIA",
     "Dagang Jepang & Indonesia; UE ancam tarif $84 M."),
    ("AI MELAMPAUI UJI KEAMANAN",
     "Kemampuan AI ganda tiap 3,6 bulan, kata METR."),
    ("SKANDAL NVIDIA",
     "Alice Huang dikaitkan dengan intel China."),
    ("GPU NVIDIA B300 DI CHENNAI",
     "L&T kerahkan ribuan GPU AI di Chennai."),
]
COL3_DUN = [
    ("BELGIA LUMPUH MOGOK",
     "Penerbangan batal massal akibat mogok nasional."),
    ("VAKSIN TIFOID 50 JUTA ANAK",
     "Kampanye vaksinasi tifoid sebulan penuh."),
    ("BANJIR HIMALAYA",
     "Empat tewas, sekitar 100 hilang di India."),
    ("PRAJWAL REVANNA DIPENJARA",
     "Mantan MP India divonis seumur hidup."),
    ("PENEMBAKAN DI KAMPUS AS",
     "Dua tewas, satu luka di universitas AS."),
]

# Strip bawah — hasil AKHIR PEKAN (Sabtu-Minggu), diberi label jelas.
WEEKEND = [
    ("ALCARAZ JUARA ATP FINALS",
     "Kalahkan Zverev 6-2, 7-6 di Turin."),
    ("M\u00c1RQUEZ GELAR KE-8",
     "Juara dunia MotoGP, samai rekor Agostini."),
    ("LIVERPOOL 4-0 MAN UTD",
     "Debut Pochettino berakhir bencana di Anfield."),
    ("BOCA JUARA SUDAMERICANA",
     "Menang 2-0 atas Atl\u00e9tico Mineiro."),
]


# ---------------------------------------------------------------------------
# LAYOUT — 1024 x 1024
# ---------------------------------------------------------------------------
MX = 22                      # margin kiri/kanan
CW = W - 2 * MX              # lebar konten


def section_head(draw, x, y, w, label, color):
    """Kepala seksi: label kapital + garis bawah warna."""
    f = font(F_SANS_B, 14)
    draw.text((x, y), label, font=f, fill=color)
    draw.line([(x, y + 20), (x + w, y + 20)], fill=color, width=2)
    return y + 24


def story_cell(draw, x, y, w, head, body, head_size=16, body_size=12):
    """Satu sel berita: judul tebal (maks 2 baris) + ringkasan (maks 2 baris)."""
    fh = font(F_SANS_B, head_size)
    fb = font(F_SANS, body_size)
    hl = wrap(draw, head, fh, w)[:2]
    y = text_block(draw, x, y, hl, fh, INK, head_size + 3)
    bl = wrap(draw, body, fb, w)[:2]
    y = text_block(draw, x, y + 1, bl, fb, GREY, body_size + 3)
    return y


def draw_masthead(draw):
    y = 20
    draw.line([(MX, y), (MX + CW, y)], fill=INK, width=2)
    f = font(F_SERIF_B, 46)
    title = "DUNIA DALAM SATU HALAMAN"
    tw = draw.textlength(title, font=f)
    draw.text(((W - tw) / 2, y + 8), title, font=f, fill=INK)
    # Pita tanggal — hitam, teks putih, paling menonjol setelah judul.
    band_y = y + 66
    draw.rectangle([(MX, band_y), (MX + CW, band_y + 34)], fill=INK)
    f2 = font(F_SANS_B, 21)
    date = "SENIN, 23 NOVEMBER 2026"
    dw = draw.textlength(date, font=f2)
    draw.text(((W - dw) / 2, band_y + 5), date, font=f2, fill=WHITE)
    f3 = font(F_SANS, 13)
    sub = "34 BERITA DUNIA SEHARIAN  \u2022  SENIN, 23 NOVEMBER 2026  \u2022  SATU HALAMAN"
    sw = draw.textlength(sub, font=f3)
    draw.text(((W - sw) / 2, band_y + 40), sub, font=f3, fill=GREY)
    return band_y + 62


def draw_lead(draw, y):
    draw.line([(MX, y), (MX + CW, y)], fill=RED, width=3)
    y += 10
    fk = font(F_SANS_B, 15)
    draw.text((MX, y), LEAD["kicker"], font=fk, fill=RED)
    y += 22
    fh = font(F_SERIF_B, 40)
    hl = wrap(draw, LEAD["head"], fh, CW)
    y = text_block(draw, MX, y, hl, fh, INK, 44)
    y += 4
    fd = font(F_SANS, 18)
    dl = wrap(draw, LEAD["deck"], fd, CW)
    y = text_block(draw, MX, y, dl, fd, GREY, 23)
    return y + 10


def draw_row2(draw, y):
    draw.line([(MX, y), (MX + CW, y)], fill=RULE, width=1)
    y += 10
    half = (CW - 24) // 2
    top = y
    for i, item in enumerate(ROW2):
        x = MX + i * (half + 24)
        yy = y
        fk = font(F_SANS_B, 13)
        draw.text((x, yy), item["tag"], font=fk, fill=RED)
        yy += 20
        fh = font(F_SERIF_B, 25)
        hl = wrap(draw, item["head"], fh, half)[:2]
        yy = text_block(draw, x, yy, hl, fh, INK, 29)
        fb = font(F_SANS, 15)
        bl = wrap(draw, item["body"], fb, half)[:3]
        yy = text_block(draw, x, yy + 2, bl, fb, GREY, 19)
        top = max(top, yy)
    return top + 8


def draw_grid(draw, y):
    draw.line([(MX, y), (MX + CW, y)], fill=INK, width=2)
    y += 8
    col_w = (CW - 48) // 3
    xs = [MX, MX + col_w + 24, MX + 2 * (col_w + 24)]
    # Kolom 1: PERANG & KONFLIK
    yy = section_head(draw, xs[0], y, col_w, "PERANG & KONFLIK", RED)
    for head, body in COL1:
        yy = story_cell(draw, xs[0], yy, col_w, head, body)
        yy += 5
        draw.line([(xs[0], yy), (xs[0] + col_w, yy)], fill=RULE, width=1)
        yy += 5
    # Kolom 2: POLITIK lalu EKONOMI
    yy = section_head(draw, xs[1], y, col_w, "POLITIK", BLUE)
    for head, body in COL2_POL:
        yy = story_cell(draw, xs[1], yy, col_w, head, body)
        yy += 5
        draw.line([(xs[1], yy), (xs[1] + col_w, yy)], fill=RULE, width=1)
        yy += 5
    yy = section_head(draw, xs[1], yy + 2, col_w, "EKONOMI & PASAR", BLUE)
    for head, body in COL2_ECO:
        yy = story_cell(draw, xs[1], yy, col_w, head, body)
        yy += 5
        draw.line([(xs[1], yy), (xs[1] + col_w, yy)], fill=RULE, width=1)
        yy += 5
    # Kolom 3: EKONOMI & TEKNOLOGI lalu DUNIA
    yy = section_head(draw, xs[2], y, col_w, "EKONOMI & TEKNOLOGI", BLUE)
    for head, body in COL3_ECO_TEC:
        yy = story_cell(draw, xs[2], yy, col_w, head, body)
        yy += 5
        draw.line([(xs[2], yy), (xs[2] + col_w, yy)], fill=RULE, width=1)
        yy += 5
    yy = section_head(draw, xs[2], yy + 2, col_w, "DUNIA", BLUE)
    for head, body in COL3_DUN:
        yy = story_cell(draw, xs[2], yy, col_w, head, body)
        yy += 5
        draw.line([(xs[2], yy), (xs[2] + col_w, yy)], fill=RULE, width=1)
        yy += 5
    return y


def draw_weekend(draw, y):
    # Strip gelap: hasil olahraga akhir pekan, diberi label jelas.
    band_h = 78
    draw.rectangle([(MX, y), (MX + CW, y + band_h)], fill=BLUE)
    f = font(F_SANS_B, 14)
    draw.text((MX + 10, y + 6), "AKHIR PEKAN \u2014 OLAHRAGA", font=f, fill=(255, 214, 90))
    col_w = (CW - 20 - 36) // 4
    xs = [MX + 10 + i * (col_w + 12) for i in range(4)]
    fh = font(F_SANS_B, 13)
    fb = font(F_SANS, 11)
    for i, (head, body) in enumerate(WEEKEND):
        x = xs[i]
        hl = wrap(draw, head, fh, col_w)[:1]
        yy = text_block(draw, x, y + 26, hl, fh, WHITE, 16)
        bl = wrap(draw, body, fb, col_w)[:2]
        text_block(draw, x, yy + 1, bl, fb, (210, 220, 235), 14)
    return y + band_h


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    y = draw_masthead(draw)
    y = draw_lead(draw, y)
    y = draw_row2(draw, y)
    draw_grid(draw, y)
    # Strip akhir pekan menempel di bawah grid, footer di paling bawah.
    wy = H - 22 - 78 - 22
    draw_weekend(draw, wy)
    f = font(F_SANS, 11)
    foot = "Dunia dalam Satu Halaman  \u2022  Senin, 23 November 2026  \u2022  34 berita  \u2022  make.fun"
    fw = draw.textlength(foot, font=f)
    draw.text(((W - fw) / 2, H - 18), foot, font=f, fill=GREY)
    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
