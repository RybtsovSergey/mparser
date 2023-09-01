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
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_revenue bigint;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_top_product_id bigint;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_top_product_revenue bigint;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_top_product_feedbacks bigint;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_hhi bigint;
ALTER TABLE public.subject ADD COLUMN IF NOT EXISTS subject_price_mean bigint;


CREATE TABLE IF NOT EXISTS public.product
(
    product_id bigint NOT NULL,
    CONSTRAINT product_pkey PRIMARY KEY (product_id)
);
ALTER TABLE public.product ADD COLUMN IF NOT EXISTS product_subject_id bigint;
ALTER TABLE public.product ADD COLUMN IF NOT EXISTS product_name text;
ALTER TABLE public.product ADD COLUMN IF NOT EXISTS product_subject_id text;
ALTER TABLE public.product ADD COLUMN IF NOT EXISTS product_brand_name text;
ALTER TABLE public.product ADD COLUMN IF NOT EXISTS product_rating real;
ALTER TABLE public.product ADD COLUMN IF NOT EXISTS product_feedbacks bigint;
