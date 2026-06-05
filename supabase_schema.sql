create table if not exists public.users (
    id bigserial primary key,
    username text unique not null,
    email text unique not null,
    password text not null,
    created_at timestamptz default now()
);

alter table public.users enable row level security;
