--Создание таблицы subjects

CREATE TABLE IF NOT EXISTS public.subject
(
    subject_id bigint NOT NULL,
    CONSTRAINT subject_pkey PRIMARY KEY (subject_id)
);
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_name text;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_parent_name text;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_full_name text;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_goods_raw json;
