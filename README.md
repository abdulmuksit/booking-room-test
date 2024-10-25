Catatan modul booking room
1. Tahapan instalasi
   - Clone modul booking-room
   - Masukan directory modul kedalam config pada bagian addons_path
   - Running menggunakan odoo 16
   - Login menggunakan database baru
   - Masuk kedalam menu Apps
   - Masuk kedalam modoul debug dengan cara menulis ?debug=1 pada url setelah tulisan web (e.g. http://localhost:8016/web?debug=1)
   - Cari modul booking_room
   - Klik activate
   - Instalasi selesai

2. Tahapan penggunaan
   - Masuk kedalam menu Pemesanan Ruangan
   - Terdapat 2 menu didalamnya yaitu menu master ruangan dan pemesanan
   - Klik menu master ruangan untuk membuat master data ruangan
   - Isi seluruh field yang required
   - Klik menu pemesanan untuk melakukan pemesanan ruangan (harus sudah punya master data ruangan)
   - Buat pemesanan dengan mengisi semua field yang ada
   - Field ruangan akan berisi master data ruangan
   - Terdapat button proses pemesanan untuk memindahkan status ke on progress
   - Terdapat button selesai pemesanan untuk memindahkan status ke done

3. Penggunaan API
   - Akses RestAPI menggunakan aplikasi untuk pengecekan API seperti postman
   - Setting method menjadi POST lalu akses URL http://localhost:8069/api/tracking_pemesanan
   - Pilih raw di bagian body lalu isi bagian body dengan {"nomor_pemesanan": "PSN-SM-20231024-001"} (Pastikan nomor pesanan sesuai dengan yang ada pada ERP
   - Hasil akan muncul pada bagian body

4. Dokumentasi API ada pada file openAPI.json
