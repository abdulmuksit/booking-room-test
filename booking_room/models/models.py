# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re
from odoo.exceptions import UserError, ValidationError

class masterRoom(models.Model):
    _name = 'master.room'
    _description = 'Master Room'

    name = fields.Char('Nama Ruangan', required=True)
    tipe_ruangan = fields.Selection([
        ('meeting_room_kecil','Meeting Room Kecil'),
        ('meeting_room_besar','Meeting Room Besar'),
        ('aula','Aula')
    ], string="Tipe Ruangan", required=True)
    lokasi_ruangan = fields.Selection([
        ('1A', '1A'),
        ('1B', '1B'),
        ('1C', '1C'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('2C', '2C'),
    ], string="Lokasi Ruangan", required=True)
    foto_ruangan = fields.Binary(string="Foto Ruangan", required=True)
    kapasitas = fields.Integer(string="Kapasitas Ruangan", required=True)
    keterangan = fields.Text(string="Keterangan")

    @api.model
    def create(self, vals):
        res = super(masterRoom, self).create(vals)
        if res:
            same_room = self.search([('name','=',res.name),('id','!=',res.id)])
            if same_room:
                raise UserError("Nama ruangan sudah digunakan, silahkan ganti dengan nama baru")
        return res
    
    def write(self, vals):
        res = super(masterRoom, self).write(vals)
        if res:
            same_room = self.search([('name','=',self.name),('id','!=',self.id)])
            if same_room:
                raise UserError("Nama ruangan sudah digunakan, silahkan ganti dengan nama baru")
        return res
    
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not re.match("^[A-Za-z ]+$", record.name):
                raise ValidationError("Nama pemesan hanya boleh berisi huruf dan spasi.")
            
    @api.constrains('kapasitas')
    def _check_kapasitas(self):
        for record in self:
            if record.kapasitas <= 0:
                raise ValidationError("Kapasitas ruangan harus lebih besar dari 0.")

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            same_room = self.search([('name','=',self.name)])
            for room in same_room:
                if room.id != self.id:
                    raise UserError("Nama ruangan sudah digunakan, silahkan ganti dengan nama baru")

class PemesananRuangan(models.Model):
    _name = 'pemesanan.ruangan'
    _description = 'Pemesanan Ruangan'
    _order = 'name asc'

    name = fields.Char(string="Nomor Pemesanan", copy=False, readonly=True, index=True)
    room_id = fields.Many2one('master.room', string="Ruangan", required=True)
    nama_pemesanan = fields.Char(string="Nama Pemesanan", required=True)
    tanggal_pemesanan = fields.Date(string="Tanggal Pemesanan", required=True)
    status_pemesanan = fields.Selection([
        ('draft', 'Draft'),
        ('on_going', 'On Going'),
        ('done', 'Done'),
    ], string="Status Pemesanan", default='draft', required=True)
    catatan_pemesanan = fields.Text(string="Catatan Pemesanan")

    @api.model
    def create(self, vals):
        res = super(PemesananRuangan, self).create(vals)
        if res:
            same_name = self.search([('nama_pemesanan','=',res.nama_pemesanan),('id','!=',res.id)])
            same_booking = self.search([('room_id','=',res.room_id.id),('tanggal_pemesanan','=',res.tanggal_pemesanan),('id','!=',res.id)])
            if same_name:
                raise UserError("Nama pemesanan sudah digunakan, silahkan ganti dengan nama baru")
            if same_booking:
                raise UserError("Sudah ada pemesanan ruangan %s di tanggal yang di pilih, silahkan ganti tanggal atau ganti ruangan" % res.room_id.name)
            
            if not res.name:
                tipe_ruangan = res.room_id.tipe_ruangan
                tipe_str = {
                    'meeting_room_kecil': 'MRK',
                    'meeting_room_besar': 'MRB',
                    'aula': 'AU',
                }.get(tipe_ruangan, 'XX')
                sequence = self.env['ir.sequence'].next_by_code('pemesanan.ruangan') or '/'
                res.name = sequence.replace('tipe_ruangan', tipe_str)

        return res
    
    def write(self, vals):
        res = super(PemesananRuangan, self).write(vals)
        if res:
            same_name = self.search([('nama_pemesanan','=',self.nama_pemesanan),('id','!=',self.id)])
            same_booking = self.search([('room_id','=',self.room_id.id),('tanggal_pemesanan','=',self.tanggal_pemesanan),('id','!=',self.id)])
            if same_name:
                raise UserError("Nama pemesanan sudah digunakan, silahkan ganti dengan nama baru")
            if same_booking:
                raise UserError("Sudah ada pemesanan ruangan %s di tanggal yang di pilih, silahkan ganti tanggal atau ganti ruangan" % self.room_id.name)

        return res
    
    @api.onchange('nama_pemesanan')
    def _onchange_nama_pemesanan(self):
        if self.nama_pemesanan:
            same_name = self.search([('nama_pemesanan','=',self.nama_pemesanan)])
            for name in same_name:
                if name.id != self.id:
                    raise UserError("Nama pemesanan sudah digunakan, silahkan ganti dengan nama baru")
                
    @api.onchange('room_id','tanggal_pemesanan')
    def _onchange_room_id_tanggal_pemesanan(self):
        if self.room_id and self.tanggal_pemesanan:
            same_booking = self.search([('room_id','=',self.room_id.id),('tanggal_pemesanan','=',self.tanggal_pemesanan)])
            for booking in same_booking:
                if booking.id != self.id:
                    raise UserError("Sudah ada pemesanan ruangan %s di tanggal yang di pilih, silahkan ganti tanggal atau ganti ruangan" % self.room_id.name)
    
    def action_proses_pemesanan(self):
        for record in self:
            if record.status_pemesanan == 'draft':
                record.status_pemesanan = 'on_going'

    def action_selesai_pemesanan(self):
        for record in self:
            if record.status_pemesanan == 'on_going':
                record.status_pemesanan = 'done'
