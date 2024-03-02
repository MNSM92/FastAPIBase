"""v1.2 lschedules

Revision ID: ef754684c678
Revises: e83f6bc0c3c7
Create Date: 2023-05-27 08:00:28.463157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef754684c678'
down_revision = 'e83f6bc0c3c7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('leasee',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('name', sa.String, nullable=False),
                    sa.Column('f_name', sa.String, nullable=False),
                    sa.Column('address', sa.String, nullable=False),
                    sa.Column('district', sa.String, sa.ForeignKey("district.name", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('upazilla', sa.String, sa.ForeignKey("upazilla.name", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('remarks', sa.String, nullable=True),
                    sa.Column('nid_number', sa.String, nullable=False, unique=True),
                    sa.Column('dob', sa.Date, nullable=False),
                    sa.Column('phone_number', sa.String, nullable=False, unique=True),
                    sa.Column('alt_phone_number', sa.String, nullable=True),
                    sa.Column('sex', sa.String, nullable=False),
                    sa.Column('profile', sa.String, nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()'))
                    )

    op.create_table('vpcase',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('number', sa.String, nullable=False, unique=True),
                    sa.Column('mouza', sa.String, sa.ForeignKey("mouza.name", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()'))
                    )
    op.create_table('lschedule',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('land_id', sa.Integer,  nullable=False, unique=True),
                    sa.Column('vpcase', sa.String, sa.ForeignKey("vpcase.number", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('mutation_number_past', sa.String, nullable=False),
                    sa.Column('plot_number_past', sa.String, nullable=False),
                    sa.Column('mutation_number_new', sa.String, nullable=False),
                    sa.Column('plot_number_new', sa.String, nullable=False),
                    sa.Column('land_area', sa.Float, nullable=False),
                    sa.Column('land_class', sa.String, nullable=False),
                    sa.Column('is_shop', sa.Boolean, nullable=False, default=False),
                    sa.Column('shop_sqf', sa.Float, nullable=False, default=0),
                    sa.Column('renewed_upto', sa.Integer, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()'))
                    )
    op.create_table('application',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('vpcase', sa.String, sa.ForeignKey("vpcase.number", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('leasee', sa.String, nullable=False),
                    sa.Column('nid_number', sa.String, sa.ForeignKey("leasee.nid_number", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('application_date', sa.Date, nullable=False),
                    sa.Column('leasee_type', sa.String, nullable=False),
                    sa.Column('applicant_type', sa.String, nullable=False),
                    sa.Column('representative_name', sa.String, nullable=True),
                    sa.Column('rep_phone_number', sa.String, nullable=True),
                    sa.Column('user', sa.String, sa.ForeignKey('role.name', ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('user_by', sa.String, sa.ForeignKey('role.name', ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('application_status', sa.String, nullable=False),
                    sa.Column('applied_for', sa.String, nullable=False),
                    sa.Column('fee', sa.Integer, nullable=False),
                    sa.Column('application_for', sa.String, nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                              server_default=sa.text('now()')),
                    )
    op.create_table('note',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('application_id', sa.Integer, sa.ForeignKey("application.id", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('order_no', sa.Integer, nullable=False),
                    sa.Column('order_date', sa.Date, nullable=False),
                    sa.Column('last_date', sa.Date, nullable=False),
                    sa.Column('description', sa.String, nullable=False),

                    sa.Column('sent_from', sa.String, sa.ForeignKey('users.username', ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('sent_to', sa.String, sa.ForeignKey('users.username', ondelete="CASCADE"),
                              nullable=False, unique=False),

                    sa.Column('actions_taken', sa.String, nullable=True),

                    sa.Column('sent_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
                    )
    op.create_table('report',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('application_id', sa.Integer, sa.ForeignKey("application.id", ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('order_no', sa.Integer, nullable=False),

                    sa.Column('report_no', sa.Integer, nullable=False),
                    sa.Column('report_date', sa.Date, nullable=False),
                    sa.Column('description', sa.String, nullable=False),
                    sa.Column('actions_taken', sa.String, nullable=True),

                    sa.Column('sent_from', sa.String, sa.ForeignKey('users.username', ondelete="CASCADE"),
                              nullable=False, unique=False),
                    sa.Column('sent_to', sa.String, sa.ForeignKey('users.username', ondelete="CASCADE"), nullable=False,
                              unique=False),

                    sa.Column('sent_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    )
    op.create_table('dcr',
                    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('application_id', sa.Integer, sa.ForeignKey("application.id", ondelete="CASCADE"),
                              nullable=False, unique=True),
                    sa.Column('dcr_date', sa.Date, nullable=False),
                    sa.Column('signature_by', sa.String, sa.ForeignKey('users.username', ondelete="CASCADE"), nullable=False,
                              unique=False),
                    sa.Column('sent_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    )
    pass


def downgrade() -> None:
    op.drop_table('dcr')
    op.drop_table('report')
    op.drop_table('note')
    op.drop_table('application')
    op.drop_table('lschedule')
    op.drop_table('vpcase')
    op.drop_table('leasee')
    pass
