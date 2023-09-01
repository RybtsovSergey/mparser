--Создание таблицы subjects

CREATE TABLE IF NOT EXISTS public.subject
(
    subject_id bigint NOT NULL,
    CONSTRAINT subject_pkey PRIMARY KEY (subject_id)
);
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_name text;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_parent_name text;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_full_name text;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_products_raw json;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_summary_raw json;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_price_segmentation_raw json;
