--
-- PostgreSQL database dump
--

-- Dumped from database version 17.2
-- Dumped by pg_dump version 17.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: final_price(integer, character varying, date); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.final_price(price integer, cat character varying, imp date) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
fprice INTEGER;
BEGIN
IF ((cat = 'us') AND  ( (imp - CURRENT_DATE) <= 3)) THEN
RETURN price - LEAST(50, price/5);
ELSIF ((cat = 'per') AND  ((imp - CURRENT_DATE) <= 1)) THEN
RETURN price - LEAST(50, price/5);
ELSE
RETURN price;
END IF;
END;
$$;


ALTER FUNCTION public.final_price(price integer, cat character varying, imp date) OWNER TO postgres;

--
-- Name: report(integer); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.report(mode integer) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
IF (mode = 0) THEN
DELETE FROM price_change;
END IF;
INSERT INTO price_change (curr_date, cat, arcl, name_of_good, measure, remains, old_price, new_price) SELECT CURRENT_DATE, category, article, name, measurement, remain, price, Final_Price(price, category, imp_period) FROM goods;
END;
$$;


ALTER FUNCTION public.report(mode integer) OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: adress; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.adress (
    id integer NOT NULL,
    country character varying(20),
    city character varying(20),
    street character varying(20),
    house character varying(5),
    new_id integer NOT NULL
);


ALTER TABLE public.adress OWNER TO postgres;

--
-- Name: adress_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.adress_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.adress_id_seq OWNER TO postgres;

--
-- Name: adress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.adress_id_seq OWNED BY public.adress.id;


--
-- Name: adress_new_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.adress_new_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.adress_new_id_seq OWNER TO postgres;

--
-- Name: adress_new_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.adress_new_id_seq OWNED BY public.adress.new_id;


--
-- Name: cars; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cars (
    car_id integer NOT NULL,
    model_name character varying(30),
    manifacturing_year integer,
    price integer,
    spare_key boolean,
    km_driven integer,
    ownership integer,
    imperfections integer,
    repainted_parts integer
);


ALTER TABLE public.cars OWNER TO postgres;

--
-- Name: cars_car_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cars_car_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.cars_car_id_seq OWNER TO postgres;

--
-- Name: cars_car_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cars_car_id_seq OWNED BY public.cars.car_id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id integer NOT NULL,
    full_name character varying(50),
    email character varying(20),
    job_title character varying(20),
    CONSTRAINT jt_check CHECK ((((job_title)::text = 'cashier'::text) OR ((job_title)::text = 'manager'::text) OR ((job_title)::text = 'stock clerk'::text) OR ((job_title)::text = 'cleaner'::text)))
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.employees_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.employees_id_seq OWNER TO postgres;

--
-- Name: employees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.employees_id_seq OWNED BY public.employees.id;


--
-- Name: goods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.goods (
    delivery_date date,
    category character varying(50),
    article character(8),
    name character varying(50),
    measurement character varying(5),
    price integer,
    remain integer,
    imp_period date,
    CONSTRAINT cat_check CHECK ((((category)::text = 'us'::text) OR ((category)::text = 'per'::text)))
);


ALTER TABLE public.goods OWNER TO postgres;

--
-- Name: models; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.models (
    model_name character varying(30) NOT NULL,
    manifacturing_year integer NOT NULL,
    engine_capacity integer,
    transmission character varying(10),
    fuel_type character varying(10)
);


ALTER TABLE public.models OWNER TO postgres;

--
-- Name: price_change; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_change (
    curr_date date,
    cat character varying(20),
    arcl character(8),
    name_of_good character varying(50),
    measure character varying(5),
    remains integer,
    old_price integer,
    new_price integer,
    id integer
);


ALTER TABLE public.price_change OWNER TO postgres;

--
-- Name: adress id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adress ALTER COLUMN id SET DEFAULT nextval('public.adress_id_seq'::regclass);


--
-- Name: adress new_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adress ALTER COLUMN new_id SET DEFAULT nextval('public.adress_new_id_seq'::regclass);


--
-- Name: cars car_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars ALTER COLUMN car_id SET DEFAULT nextval('public.cars_car_id_seq'::regclass);


--
-- Name: employees id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees ALTER COLUMN id SET DEFAULT nextval('public.employees_id_seq'::regclass);


--
-- Data for Name: adress; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.adress (id, country, city, street, house, new_id) FROM stdin;
2	Russia	Orekhuevo-Zuevo	Kolotuskina	20	5
3	Russia	Orekhuevo-Zuevo	Kolotuskina	20	1
1	Russia	Moscow	Pryanishnikova	2A	4
4	Russia	Moscow	Parkovaya	9/26	3
\.


--
-- Data for Name: cars; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cars (car_id, model_name, manifacturing_year, price, spare_key, km_driven, ownership, imperfections, repainted_parts) FROM stdin;
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, full_name, email, job_title) FROM stdin;
1	Tamara V. Smirnova	smirnova@yandex.ru	cashier
4	Yulianna V. Perepyolkina	polytech@yandex.ru	manager
2	Michael P. Zchmyshenko	mafiozi@gmail.com	cashier
3	Vladimir D. Konev	123koneva@gmail.com	cleaner
5	Ivan I. Ivanov	a@gmail.com	cleaner
\.


--
-- Data for Name: goods; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.goods (delivery_date, category, article, name, measurement, price, remain, imp_period) FROM stdin;
2025-02-07	us	22345679	buckwheat russian	g	70	24	2025-02-13
2025-02-08	us	00000001	rice basmati	g	100	14	2025-02-20
2025-02-10	per	00000002	raw milk	l	115	27	2025-02-14
2025-02-11	per	00000003	greek yogurt	ml	50	27	2025-02-17
2025-02-12	per	00000004	cocktail	ml	250	10	2025-02-13
2025-02-12	us	00000005	chicken	kg	270	10	2025-02-14
\.


--
-- Data for Name: models; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.models (model_name, manifacturing_year, engine_capacity, transmission, fuel_type) FROM stdin;
\.


--
-- Data for Name: price_change; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.price_change (curr_date, cat, arcl, name_of_good, measure, remains, old_price, new_price, id) FROM stdin;
2025-02-19	us	22345679	buckwheat russian	g	24	70	56	\N
2025-02-19	us	00000001	rice basmati	g	14	100	80	\N
2025-02-19	per	00000002	raw milk	l	27	115	92	\N
2025-02-19	per	00000003	greek yogurt	ml	27	50	40	\N
2025-02-19	per	00000004	cocktail	ml	10	250	200	\N
2025-02-19	us	00000005	chicken	kg	10	270	220	\N
2025-02-19	us	22345679	buckwheat russian	g	24	70	56	\N
2025-02-19	us	00000001	rice basmati	g	14	100	80	\N
2025-02-19	per	00000002	raw milk	l	27	115	92	\N
2025-02-19	per	00000003	greek yogurt	ml	27	50	40	\N
2025-02-19	per	00000004	cocktail	ml	10	250	200	\N
2025-02-19	us	00000005	chicken	kg	10	270	220	\N
\N	\N	\N	\N	\N	\N	\N	\N	1
\.


--
-- Name: adress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.adress_id_seq', 11, true);


--
-- Name: adress_new_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.adress_new_id_seq', 3, true);


--
-- Name: cars_car_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cars_car_id_seq', 1, false);


--
-- Name: employees_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.employees_id_seq', 5, true);


--
-- Name: adress adress_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adress
    ADD CONSTRAINT adress_pkey PRIMARY KEY (id);


--
-- Name: cars cars_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT cars_pkey PRIMARY KEY (car_id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: models pk_models; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.models
    ADD CONSTRAINT pk_models PRIMARY KEY (model_name, manifacturing_year);


--
-- Name: goods unique_article; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goods
    ADD CONSTRAINT unique_article UNIQUE (article);


--
-- Name: price_change unique_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_change
    ADD CONSTRAINT unique_id UNIQUE (id);


--
-- Name: adress adress_new_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.adress
    ADD CONSTRAINT adress_new_id_fkey FOREIGN KEY (new_id) REFERENCES public.employees(id);


--
-- Name: cars fk_cars; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cars
    ADD CONSTRAINT fk_cars FOREIGN KEY (model_name, manifacturing_year) REFERENCES public.models(model_name, manifacturing_year);


--
-- PostgreSQL database dump complete
--

