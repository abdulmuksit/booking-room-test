# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response

class BookingRoom(http.Controller):
    @http.route('/api/tracking_pemesanan', auth='public', website=False, csrf=False, type='json', methods=['POST'])
    def tracking_pemesanan(self, **post):
        nomor_pemesanan = post.get('nomor_pemesanan')
        if not nomor_pemesanan:
            return Response("Nomor pemesanan tidak ditemukan.", status=400)

        pemesanan = request.env['pemesanan.ruangan'].sudo().search([('name', '=', nomor_pemesanan)], limit=1)
        if not pemesanan:
            return Response("Pemesanan tidak ditemukan.", status=404)

        data = {
            'nomor_pemesanan': pemesanan.name,
            'ruangan': pemesanan.room_id.name,
            'nama_pemesanan': pemesanan.nama_pemesanan,
            'tanggal_pemesanan': pemesanan.tanggal_pemesanan.strftime('%Y-%m-%d'),
            'status_pemesanan': pemesanan.status_pemesanan,
            'catatan_pemesanan': pemesanan.catatan_pemesanan or "Tidak ada catatan"
        }

        return data
