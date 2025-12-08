###############################################################################
#
#    OpenEduCat Inc
#    Copyright (C) 2009-TODAY OpenEduCat Inc(<https://www.openeducat.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OpStudentCourse(models.Model):
    _name = "op.student.course"
    _description = "Student Course Details"
    _inherit = "mail.thread"
    _rec_name = 'student_id'

    student_id = fields.Many2one('op.student', 'Student',
                                 ondelete="cascade", tracking=True)
    course_id = fields.Many2one('op.course', 'Course', required=True, tracking=True)
    batch_id = fields.Many2one('op.batch', 'Batch', tracking=True)
    roll_number = fields.Char('Roll Number', tracking=True)
    subject_ids = fields.Many2many('op.subject', string='Subjects')
    academic_years_id = fields.Many2one('op.academic.year', 'Academic Year')
    academic_term_id = fields.Many2one('op.academic.term', 'Terms')
    state = fields.Selection([('running', 'Running'),
                              ('finished', 'Finished')],
                             string="Status", default="running")

    _sql_constraints = [
        ('unique_name_roll_number_id',
         'unique(roll_number,course_id,batch_id,student_id)',
         'Roll Number & Student must be unique per Batch!'),
        ('unique_name_roll_number_course_id',
         'unique(roll_number,course_id,batch_id)',
         'Roll Number must be unique per Batch!'),
        ('unique_name_roll_number_student_id',
         'unique(student_id,course_id,batch_id)',
         'Student must be unique per Batch!'),
    ]

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Student Course Details'),
            'template': '/openeducat_core/static/xls/op_student_course.xls'
        }]


class OpStudent(models.Model):
    _name = "op.student"
    _description = "Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {"res.partner": "partner_id"}

    name_cn = fields.Char('姓名', translate=True, required=False,
                          help="学生中文全名；同步至联系人名称与拆分字段")
    first_name = fields.Char('First Name', translate=True)
    middle_name = fields.Char('Middle Name', translate=True)
    last_name = fields.Char('Last Name', translate=True)
    birth_date = fields.Date('Birth Date')
    blood_group = fields.Selection([
        ('A+', 'A+ve'),
        ('B+', 'B+ve'),
        ('O+', 'O+ve'),
        ('AB+', 'AB+ve'),
        ('A-', 'A-ve'),
        ('B-', 'B-ve'),
        ('O-', 'O-ve'),
        ('AB-', 'AB-ve')
    ], string='Blood Group')
    gender = fields.Selection([
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ], 'Gender', required=True, default='m')
    nationality = fields.Many2one('res.country', 'Nationality')
    emergency_contact = fields.Many2one('res.partner', 'Emergency Contact')
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    partner_id = fields.Many2one('res.partner', 'Partner',
                                 required=True, ondelete="cascade")
    user_id = fields.Many2one('res.users', 'User', ondelete="cascade")
    gr_no = fields.Char("Registration Number", size=20)
    category_id = fields.Many2one('op.category', 'Category')
    course_detail_ids = fields.One2many('op.student.course', 'student_id',
                                        'Course Details',
                                        tracking=True)
    active = fields.Boolean(default=True)
    certificate_number = fields.Char(
        string='Certificate No.',
        readonly=True,
        copy=False,)

    _sql_constraints = [(
        'unique_gr_no',
        'unique(gr_no)',
        'Registration Number must be unique per student!'
    )]

    @api.model
    def create(self, vals):
        vals = self._sync_cn_name_vals(vals, current_record=None)
        return super().create(vals)

    def write(self, vals):
        # apply per-record defaults to avoid losing existing names when vals misses name_cn
        for record in self:
            synced_vals = record._sync_cn_name_vals(dict(vals), current_record=record)
            super(OpStudent, record).write(synced_vals)
        return True

    def _sync_cn_name_vals(self, vals, current_record=None):
        """确保 name_cn 与 res.partner.name 及拆分字段保持一致，兼容旧数据。"""
        cn_name = vals.get('name_cn')
        fname = vals.get('first_name')
        mname = vals.get('middle_name')
        lname = vals.get('last_name')

        # 如果传入中文姓名，则覆盖拆分字段与联系人名称
        if cn_name:
            vals.setdefault('first_name', cn_name)
            vals.setdefault('middle_name', False)
            vals.setdefault('last_name', False)
            vals['name'] = cn_name
            return vals

        # 没传中文名，用现有或传入的英文拆分字段拼接
        current_fname = fname if fname is not None else (current_record.first_name if current_record else False)
        current_mname = mname if mname is not None else (current_record.middle_name if current_record else False)
        current_lname = lname if lname is not None else (current_record.last_name if current_record else False)
        merged = " ".join(filter(None, [current_fname, current_mname, current_lname])).strip()

        if merged:
            vals.setdefault('name_cn', merged)
            vals.setdefault('name', merged)

        return vals

    @api.onchange('name_cn')
    def _onchange_name_cn(self):
        """单字段中文名，驱动联系人名称与英文拆分字段保持一致。"""
        for record in self:
            if record.name_cn:
                record.name = record.name_cn
                record.first_name = record.name_cn
                record.middle_name = False
                record.last_name = False

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name_1(self):
        # 兼容旧表单：若仍填写英文拆分字段，自动合并为姓名
        fname = self.first_name or ""
        mname = self.middle_name or ""
        lname = self.last_name or ""

        if fname or mname or lname:
            merged = " ".join(filter(None, [fname, mname, lname])).strip()
            self.name = merged or "New"
            self.name_cn = merged or self.name_cn
        else:
            self.name = "New"

    @api.constrains('birth_date')
    def _check_birthdate(self):
        for record in self:
            if record.birth_date and record.birth_date > fields.Date.today():
                raise ValidationError(_(
                    "Birth Date can't be greater than current date!"))

    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Students'),
            'template': '/openeducat_core/static/xls/op_student.xls'
        }]

    def create_student_user(self):
        user_group = self.env.ref("base.group_portal") or False
        users_res = self.env['res.users']
        for record in self:
            if not record.user_id:
                user_id = users_res.create({
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'login': record.email,
                    'groups_id': user_group,
                    'is_student': True,
                    'tz': self._context.get('tz'),
                })
                record.user_id = user_id
