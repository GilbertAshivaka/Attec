"""Initial migration - create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2025-10-19

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if we're using PostgreSQL
    bind = op.get_bind()
    is_postgres = bind.dialect.name == 'postgresql'
    
    if is_postgres:
        # Check and create enum types for PostgreSQL only if they don't exist
        op.execute("""
            DO $$ BEGIN
                CREATE TYPE userrole AS ENUM ('admin', 'editor', 'viewer');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        op.execute("""
            DO $$ BEGIN
                CREATE TYPE contactstatus AS ENUM ('new', 'contacted', 'qualified', 'converted', 'archived');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        role_type = postgresql.ENUM('admin', 'editor', 'viewer', name='userrole', create_type=False)
        status_type = postgresql.ENUM('new', 'contacted', 'qualified', 'converted', 'archived', name='contactstatus', create_type=False)
        id_type = postgresql.UUID(as_uuid=True)
        json_type = postgresql.JSON()
        timestamp_default = sa.text('now()')
    else:
        # SQLite uses String for enums and JSON
        role_type = sa.String()
        status_type = sa.String()
        id_type = sa.String(36)  # UUIDs as strings in SQLite
        json_type = sa.Text()  # JSON as text in SQLite
        timestamp_default = sa.text("(datetime('now'))")
    
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', role_type, nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, default=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=timestamp_default),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=timestamp_default)
    )
    
    # Create contact_submissions table
    op.create_table(
        'contact_submissions',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, index=True),
        sa.Column('company', sa.String(), nullable=True),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', status_type, nullable=False),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('assigned_to', sa.String(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=False, server_default=timestamp_default),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=timestamp_default),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=timestamp_default)
    )
    
    # Create analytics_events table
    op.create_table(
        'analytics_events',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('event_type', sa.String(), nullable=False, index=True),
        sa.Column('event_data', json_type, nullable=True),
        sa.Column('session_id', sa.String(), nullable=True, index=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('referrer', sa.String(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False, server_default=timestamp_default, index=True)
    )


def downgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == 'postgresql'
    
    op.drop_table('analytics_events')
    op.drop_table('contact_submissions')
    op.drop_table('users')
    
    if is_postgres:
        op.execute('DROP TYPE contactstatus')
        op.execute('DROP TYPE userrole')
