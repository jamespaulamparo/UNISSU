-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 11, 2026 at 10:06 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dbisyswear`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add uniform', 7, 'add_uniform'),
(26, 'Can change uniform', 7, 'change_uniform'),
(27, 'Can delete uniform', 7, 'delete_uniform'),
(28, 'Can view uniform', 7, 'view_uniform'),
(29, 'Can add uniform size', 8, 'add_uniformsize'),
(30, 'Can change uniform size', 8, 'change_uniformsize'),
(31, 'Can delete uniform size', 8, 'delete_uniformsize'),
(32, 'Can view uniform size', 8, 'view_uniformsize'),
(33, 'Can add order', 9, 'add_order'),
(34, 'Can change order', 9, 'change_order'),
(35, 'Can delete order', 9, 'delete_order'),
(36, 'Can view order', 9, 'view_order'),
(37, 'Can add order item', 10, 'add_orderitem'),
(38, 'Can change order item', 10, 'change_orderitem'),
(39, 'Can delete order item', 10, 'delete_orderitem'),
(40, 'Can view order item', 10, 'view_orderitem'),
(41, 'Can add profile', 11, 'add_profile'),
(42, 'Can change profile', 11, 'change_profile'),
(43, 'Can delete profile', 11, 'delete_profile'),
(44, 'Can view profile', 11, 'view_profile');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(11, 'pbkdf2_sha256$600000$gX2Bk5X9cpFe6vc7SSGoWC$udoYffAd9HgJ2lwYbzgs6zxv4C/HbMDyoLheSXjJV40=', NULL, 1, 'admin', 'Campus', 'Administrator', 'admin@dmmmsu.edu.ph', 1, 1, '2026-10-07 14:10:52.653236'),
(14, 'pbkdf2_sha256$600000$DRzucGaOmtsaWG4SUPNKaA$OjQyKFCkmjuAS7XnBKMvLmWdLbaTrN9lGZ8w07/ni2Q=', '2026-10-10 03:11:58.666184', 1, 'james', '', '', 'jamespaulamparo@gmail.com', 1, 1, '2026-10-08 15:57:23.971658'),
(15, 'pbkdf2_sha256$600000$WLC8Lq4yWow9VJ9xSh4XoQ$3p05wNxUokD+CpATfhIVit51ibO6npQgi+1hKNvCrUI=', '2026-10-10 02:41:17.384247', 0, 'sample1', 'sampleuser', '', 'sampleuser@gmail.com', 0, 1, '2026-10-10 02:28:38.351986');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(9, 'orders', 'order'),
(10, 'orders', 'orderitem'),
(7, 'products', 'uniform'),
(8, 'products', 'uniformsize'),
(6, 'sessions', 'session'),
(11, 'users', 'profile');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-10-02 05:43:05.640419'),
(2, 'auth', '0001_initial', '2026-10-02 05:43:05.936204'),
(3, 'admin', '0001_initial', '2026-10-02 05:43:06.047628'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-10-02 05:43:06.052841'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-10-02 05:43:06.058168'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-10-02 05:43:06.096186'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-10-02 05:43:06.134166'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-10-02 05:43:06.144241'),
(9, 'auth', '0004_alter_user_username_opts', '2026-10-02 05:43:06.149154'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-10-02 05:43:06.178913'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-10-02 05:43:06.180668'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-10-02 05:43:06.185968'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-10-02 05:43:06.194649'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-10-02 05:43:06.203323'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-10-02 05:43:06.211998'),
(16, 'auth', '0011_update_proxy_permissions', '2026-10-02 05:43:06.216787'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-10-02 05:43:06.224825'),
(18, 'orders', '0001_initial', '2026-10-02 05:43:06.233406'),
(19, 'orders', '0002_remove_order_product_id_remove_order_quantity_and_more', '2026-10-02 05:43:06.372082'),
(20, 'orders', '0003_auto_20260405_2133', '2026-10-02 05:43:06.373676'),
(21, 'orders', '0004_alter_order_status', '2026-10-02 05:43:06.383328'),
(22, 'products', '0001_initial', '2026-10-02 05:43:06.392158'),
(23, 'products', '0002_uniform_image_url_alter_uniform_gender_and_more', '2026-10-02 05:43:06.483824'),
(24, 'sessions', '0001_initial', '2026-10-02 05:43:06.502891'),
(25, 'users', '0001_initial', '2026-10-02 05:43:06.556699'),
(26, 'users', '0002_emailverification', '2026-10-02 05:43:06.612063'),
(27, 'users', '0003_alter_emailverification_id_alter_profile_id', '2026-10-02 05:43:06.682940'),
(28, 'users', '0004_delete_emailverification', '2026-10-02 05:43:06.688878'),
(29, 'users', '0005_profile_assigned_products', '2026-10-02 05:43:06.771656'),
(30, 'users', '0006_profile_course_year_profile_created_at_profile_role_and_more', '2026-10-07 13:56:12.574446'),
(31, 'products', '0003_uniform_category', '2026-10-09 12:25:11.035339'),
(32, 'products', '0004_alter_uniform_category', '2026-10-10 01:51:11.913728');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('5iicmbbp5zhnp9f3lupwc6bvap41sjzc', '.eJxVjEEKwjAQAP-yZwmb2KS1R---IWw2WxuVRJoWFPHvUulBrzPDvMDTMo9-qTL5FKGHA-x-WSC-Sl5FvFA-F8Ulz1MKak3UZqs6lSi349b-DUaqI_TAwaBFim1g7gJaQia9Z0tMbtDiyLTUaHEumI4aFIORmmE4aKupNd13WqXWVLKXxz1NT-jx_QHCdj_T:1xESLP:tNz5CoMpRA1JS4E1oncKsq3sMk-pP42BPElzS3uhxnQ', '2026-10-21 14:10:07.159379'),
('7k6enrcrohzvm15jyot0narafss6kauz', '.eJxVjMEOwiAQBf-FsyFQimV79O43EGAXixow0CYa478bkh70-mbevJl127rYrVG1CdnMpGCH39G7cKPcCV5dvhQeSl5r8rwrfKeNnwvS_bS7f4HFtaW_dUDppBdSCgAYJqVw8gYAxijIqBFVHAi9MYFkdNrBAACodCStwpF6tFFrqWRLz0eqLzaLzxeoaz9c:1xESLP:rY7wA__AvaQMozUnLrRKAU4VNEfa-Y5tjs3QreCHlJQ', '2026-10-21 14:10:07.774968'),
('9cyw9156uzzsswojdz1ef6yu8snxqzad', '.eJxVjEEKwjAQAP-yZwmb2KS1R---IWw2WxuVRJoWFPHvUulBrzPDvMDTMo9-qTL5FKGHA-x-WSC-Sl5FvFA-F8Ulz1MKak3UZqs6lSi349b-DUaqI_TAwaBFim1g7gJaQia9Z0tMbtDiyLTUaHEumI4aFIORmmE4aKupNd13WqXWVLKXxz1NT-jx_QHCdj_T:1xESLP:tNz5CoMpRA1JS4E1oncKsq3sMk-pP42BPElzS3uhxnQ', '2026-10-21 14:10:07.356999'),
('9husvvccahr2bnns3ewo0a68m66d3bfa', '.eJxVjDEOgzAMAP_iuYqImwTD2J03RHbiFNoKJAJT1b9XSAztene6N0TetzHuVdc4ZejBw-WXCaenzofID57vi0nLvK2TmCMxp61mWLK-bmf7Nxi5jtCDJfIk1nfYIbUkScRnZ52wv3atC-RCYmm42JBKg7agYlEWDaG1iASfL8hsN3g:1xES0n:uscT1DtWLERdX3nIR8CnRkayz3D-8YA6H_c84XnSN2Y', '2026-10-21 13:48:49.065053'),
('aig0oakowd51uxyzyn0j913ijcg1wqm0', '.eJxVjEEKwjAQAP-yZwmb2KS1R---IWw2WxuVRJoWFPHvUulBrzPDvMDTMo9-qTL5FKGHA-x-WSC-Sl5FvFA-F8Ulz1MKak3UZqs6lSi349b-DUaqI_TAwaBFim1g7gJaQia9Z0tMbtDiyLTUaHEumI4aFIORmmE4aKupNd13WqXWVLKXxz1NT-jx_QHCdj_T:1xESLO:zcyqdXawfP5I9OwJS4krG7ycH2K5ioFb9o7oZ-Sf9NI', '2026-10-21 14:10:06.955002'),
('hevdrdkaff20i8bypyty7f028e2zgm4v', '.eJxVjLsOwjAMAP_FM4pCnaShIzvfENmxSwookfqYEP-OKnWA9e50b0i0rSVti85pEhggwumXMeWn1l3Ig-q9mdzqOk9s9sQcdjG3Jvq6Hu3foNBSYAAMGjjaKIgURspeXBD0PbpLtNZZHPNovXXIgdj7vjuzSnbaCbGiD_D5AtbZN8c:1xES0z:lhV5adw-1Efxi-FffwA0Ea6WjQWEwmVBgfAQLLpllj4', '2026-10-21 13:49:01.529346'),
('iux7rgremg89ccy3rdqqlmlel1p13w4t', '.eJxVjEEOwiAQAP-yZ0MKpZTt0btvILsFLGqgKW2iMf7dNOlBrzOTeYOjbZ3cVsPikocBpIbTL2Qa7yHvxt8oX4sYS16XxGJPxGGruBQfHuej_RtMVCcYIGqK1nRdJ3tFiqNvuSf2jbGsdG-C1CpKki2NjBERg7SokI32jLGxdp_WUGsq2YXnnJYXDM3nC7siP1Y:1xF9ga:e-xWD96X0IWxVq_Q8Ta20NebHU1E30V6JqIsQorFwuk', '2026-10-23 12:26:52.918480'),
('ljhefziy557fcn6budj36f1fl5nv4vkz', '.eJxVjEEOwiAQAP-yZ0O6Al22R-99A2GBStXQpLQn499Nkx70OjOZN_iwb8XvLa9-TjAAweWXSYjPXA-RHqHeFxWXuq2zqCNRp21qXFJ-3c72b1BCKzCAkHWZJaOe4lU0M_Y6TNQxOWaDTixLNIkkoRPNnRgrFm00gUykHuHzBdyiN2A:1xES0z:IDblk3YDhP_a-Wy2A7p-5pa9pIr9SH9hxFs_8DGFWRY', '2026-10-21 13:49:01.325792'),
('pb6n0a16qr7wldxo6het7wi4o5gwuoqc', '.eJxVjDsOwjAQBe-yNbLWJv4kJX3OED2vHRJAtpRPhbg7ipQC2pnRvGnAvk3DvuZlmBN11NLll0XIM5dDpAfKvSqpZVvmqI5EnXZVfU35dTvbv8GEdaKOJBq2jOSjSIhswQJ9FQuBG3V2MB6Nzs5FE9BwNpzQjGOrrYY3IdHnCwx3OJY:1xESLO:6mDrzHxI2Wj5xgxQFFZyDE0tJLi-xiHzv-AJbkM_gMI', '2026-10-21 14:10:06.850989'),
('wibw66toury265bpgp0jfx0fbgmvlxwa', '.eJxVj8FqwzAQRH_F7NkIS5ZtSbf2ni8IRaysVaw2sYpXgZaQfy-mPrS3Yd5jYB7g8V4Xf2fafI7gQGpo_5YB5w9adxLfcb0UMZe1bjmIXREHZXEqka6vh_tvYEFewEHSmMw4DIOcFKqQYh8mDLEbTVB6GklqlSTKHudgk7WWpLHKhlHHYFNnzD7KxJzL6unrM2_f4LoWZtwquMfzN_kbMeOFGNwZXmKk2ORKt6aWZscC3lq4Ildftngc7p8_ojFWfQ:1xFPUd:ako3hWvwLc98B-BSn0cQX3q4_cXMWAZSzOBq9pmFWxo', '2026-10-24 05:19:35.696744');

-- --------------------------------------------------------

--
-- Table structure for table `orders_order`
--

CREATE TABLE `orders_order` (
  `id` bigint(20) NOT NULL,
  `customer_name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `order_date` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders_order`
--

INSERT INTO `orders_order` (`id`, `customer_name`, `email`, `address`, `order_date`, `status`, `phone`, `total_amount`, `updated_at`, `user_id`) VALUES
(1, 'sampleuser', 'sampleuser@gmail.com', 'CIS Faculty Pickup', '2026-10-10 02:28:48.975578', 'pending', '', 65.00, '2026-10-10 02:28:48.975589', 15),
(2, 'sampleuser', 'sampleuser@gmail.com', 'CIS Faculty Pickup', '2026-10-10 02:41:23.065979', 'pending', '', 2510.00, '2026-10-10 02:41:23.065990', 15),
(3, 'james', 'jamespaulamparo@gmail.com', 'CIS Faculty Pickup', '2026-10-10 05:19:35.666472', 'pending', '', 65.00, '2026-10-10 05:19:35.666487', 14);

-- --------------------------------------------------------

--
-- Table structure for table `orders_orderitem`
--

CREATE TABLE `orders_orderitem` (
  `id` bigint(20) NOT NULL,
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int(10) UNSIGNED NOT NULL CHECK (`quantity` >= 0),
  `price` decimal(10,2) NOT NULL,
  `order_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders_orderitem`
--

INSERT INTO `orders_orderitem` (`id`, `product_id`, `product_name`, `quantity`, `price`, `order_id`) VALUES
(1, 9, 'DMMMSU Official Institutional Lanyard', 1, 65.00, 1),
(2, 7, 'CIS Department Uniform', 5, 450.00, 2),
(3, 9, 'DMMMSU Official Institutional Lanyard', 4, 65.00, 2),
(4, 9, 'DMMMSU Official Institutional Lanyard', 1, 65.00, 3);

-- --------------------------------------------------------

--
-- Table structure for table `products_uniform`
--

CREATE TABLE `products_uniform` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` longtext DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `size` longtext NOT NULL,
  `gender` varchar(10) NOT NULL,
  `color` varchar(100) NOT NULL,
  `stock` int(10) UNSIGNED NOT NULL CHECK (`stock` >= 0),
  `image` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `category` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products_uniform`
--

INSERT INTO `products_uniform` (`id`, `name`, `description`, `price`, `size`, `gender`, `color`, `stock`, `image`, `created_at`, `updated_at`, `image_url`, `category`) VALUES
(1, 'DMMMSU Official Uniform Top (Female)', 'Official DMMMSU NLUC uniform top for female students.', 450.00, 'S, M, L, XL', 'Female', 'White/Green', 40, '', '2026-10-07 14:04:45.452011', '2026-10-07 14:04:45.452036', '/static/images/mdfem.jpg', 'uniforms'),
(2, 'DMMMSU Official Uniform Top (Male)', 'Official DMMMSU NLUC uniform top for male students.', 450.00, 'S, M, L, XL', 'Male', 'White/Green', 35, '', '2026-10-07 14:04:45.460938', '2026-10-07 14:04:45.460951', '/static/images/mdmale.jpg', 'uniforms'),
(3, 'CIS Tuesday Uniform (Female)', 'College of Information Systems Tuesday organizational uniform (Female).', 650.00, 'S, M, L, XL', 'Female', 'Green/Gold', 25, '', '2026-10-07 14:04:45.466661', '2026-10-07 14:04:45.466674', '/static/images/tdfem.jpg', 'uniforms'),
(4, 'CIS Tuesday Uniform (Male)', 'College of Information Systems Tuesday organizational uniform (Male).', 650.00, 'S, M, L, XL', 'Male', 'Green/Gold', 25, '', '2026-10-07 14:04:45.472345', '2026-10-07 14:04:45.472358', '/static/images/tdmale.jpg', 'uniforms'),
(5, 'CIS Uniform Slacks (Female)', 'Formal uniform slacks for female students.', 450.00, 'S, M, L, XL', 'Female', 'Black', 30, '', '2026-10-07 14:04:45.478454', '2026-10-07 14:04:45.478468', '/static/images/slacksF.jpg', 'bottoms'),
(6, 'CIS Uniform Slacks (Male)', 'Formal uniform slacks for male students.', 450.00, 'S, M, L, XL', 'Male', 'Black', 30, '', '2026-10-07 14:04:45.484218', '2026-10-07 14:04:45.484232', '/static/images/slacksM.jpg', 'bottoms'),
(7, 'CIS Department Uniform', 'CIS Wednesday departmental polo shirt.', 450.00, 'S, M, L, XL', 'Unisex', 'Emerald Green', 40, '', '2026-10-07 14:04:45.490066', '2026-10-07 14:04:45.490079', '/static/images/wed.jpg', 'department'),
(8, 'CIS Organization Uniform', 'CIS Thursday departmental polo shirt.', 450.00, 'S, M, L, XL', 'Unisex', 'Gold/White', 40, '', '2026-10-07 14:04:45.495950', '2026-10-07 14:04:45.495965', '/static/images/thu.jpg', 'organization'),
(9, 'DMMMSU Official Institutional Lanyard', 'Official DMMMSU NLUC RFID-compatible lanyard with metal hook.', 65.00, 'S, M, L, XL', 'Unisex', 'Institutional Green', 150, '', '2026-10-07 14:04:45.501709', '2026-10-07 14:04:45.501723', '/static/images/newlace.jpg', 'lanyards'),
(10, 'DMMMSU Classic Campus Lanyard', 'DMMMSU classic heritage campus lanyard.', 55.00, 'S, M, L, XL', 'Unisex', 'Heritage Green', 75, '', '2026-10-07 14:04:45.504060', '2026-10-07 14:04:45.504073', '/static/images/oldLace.jpg', 'lanyards');

-- --------------------------------------------------------

--
-- Table structure for table `products_uniformsize`
--

CREATE TABLE `products_uniformsize` (
  `id` bigint(20) NOT NULL,
  `size` varchar(10) NOT NULL,
  `stock` int(10) UNSIGNED NOT NULL CHECK (`stock` >= 0),
  `uniform_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products_uniformsize`
--

INSERT INTO `products_uniformsize` (`id`, `size`, `stock`, `uniform_id`) VALUES
(1, 'S', 10, 1),
(2, 'M', 10, 1),
(3, 'L', 10, 1),
(4, 'XL', 10, 1),
(5, 'S', 10, 2),
(6, 'M', 10, 2),
(7, 'L', 10, 2),
(8, 'XL', 10, 2),
(9, 'S', 10, 3),
(10, 'M', 10, 3),
(11, 'L', 10, 3),
(12, 'XL', 10, 3),
(13, 'S', 10, 4),
(14, 'M', 10, 4),
(15, 'L', 10, 4),
(16, 'XL', 10, 4),
(17, 'S', 10, 5),
(18, 'M', 10, 5),
(19, 'L', 10, 5),
(20, 'XL', 10, 5),
(21, 'S', 10, 6),
(22, 'M', 10, 6),
(23, 'L', 10, 6),
(24, 'XL', 10, 6),
(25, 'S', 10, 7),
(26, 'M', 10, 7),
(27, 'L', 10, 7),
(28, 'XL', 10, 7),
(29, 'S', 10, 8),
(30, 'M', 10, 8),
(31, 'L', 10, 8),
(32, 'XL', 10, 8),
(33, 'ONE_SIZE', 10, 9),
(34, 'ONE_SIZE', 10, 10);

-- --------------------------------------------------------

--
-- Table structure for table `users_profile`
--

CREATE TABLE `users_profile` (
  `id` bigint(20) NOT NULL,
  `full_name` varchar(150) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `address` longtext DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `course_year` varchar(100) DEFAULT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `student_id` varchar(30) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users_profile`
--

INSERT INTO `users_profile` (`id`, `full_name`, `phone_number`, `address`, `user_id`, `course_year`, `created_at`, `role`, `student_id`, `updated_at`) VALUES
(3, 'Campus Administrator', NULL, NULL, 11, NULL, '2026-10-07 14:10:52.654562', 'admin', NULL, '2026-10-07 14:10:52.775763'),
(6, 'james', NULL, NULL, 14, NULL, '2026-10-08 15:57:24.069634', 'admin', NULL, '2026-10-08 15:57:24.069648'),
(7, 'sampleuser', NULL, NULL, 15, 'BSIS 3B', '2026-10-10 02:28:38.450285', 'student', '127-0755-1', '2026-10-10 02:28:38.462807');

-- --------------------------------------------------------

--
-- Table structure for table `users_profile_assigned_products`
--

CREATE TABLE `users_profile_assigned_products` (
  `id` bigint(20) NOT NULL,
  `profile_id` bigint(20) NOT NULL,
  `uniform_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `orders_order`
--
ALTER TABLE `orders_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_order_user_id_e9b59eb1_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `orders_orderitem`
--
ALTER TABLE `orders_orderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` (`order_id`);

--
-- Indexes for table `products_uniform`
--
ALTER TABLE `products_uniform`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products_uniformsize`
--
ALTER TABLE `products_uniformsize`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `products_uniformsize_uniform_id_size_24b2f0fa_uniq` (`uniform_id`,`size`);

--
-- Indexes for table `users_profile`
--
ALTER TABLE `users_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `users_profile_assigned_products`
--
ALTER TABLE `users_profile_assigned_products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_profile_assigned_p_profile_id_uniform_id_5037fb11_uniq` (`profile_id`,`uniform_id`),
  ADD KEY `users_profile_assign_uniform_id_d4659ab9_fk_products_` (`uniform_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `orders_order`
--
ALTER TABLE `orders_order`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `orders_orderitem`
--
ALTER TABLE `orders_orderitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `products_uniform`
--
ALTER TABLE `products_uniform`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `products_uniformsize`
--
ALTER TABLE `products_uniformsize`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `users_profile`
--
ALTER TABLE `users_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `users_profile_assigned_products`
--
ALTER TABLE `users_profile_assigned_products`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `orders_order`
--
ALTER TABLE `orders_order`
  ADD CONSTRAINT `orders_order_user_id_e9b59eb1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `orders_orderitem`
--
ALTER TABLE `orders_orderitem`
  ADD CONSTRAINT `orders_orderitem_order_id_fe61a34d_fk_orders_order_id` FOREIGN KEY (`order_id`) REFERENCES `orders_order` (`id`);

--
-- Constraints for table `products_uniformsize`
--
ALTER TABLE `products_uniformsize`
  ADD CONSTRAINT `products_uniformsize_uniform_id_339cf5ed_fk_products_uniform_id` FOREIGN KEY (`uniform_id`) REFERENCES `products_uniform` (`id`);

--
-- Constraints for table `users_profile`
--
ALTER TABLE `users_profile`
  ADD CONSTRAINT `users_profile_user_id_2112e78d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `users_profile_assigned_products`
--
ALTER TABLE `users_profile_assigned_products`
  ADD CONSTRAINT `users_profile_assign_profile_id_24e4c5ed_fk_users_pro` FOREIGN KEY (`profile_id`) REFERENCES `users_profile` (`id`),
  ADD CONSTRAINT `users_profile_assign_uniform_id_d4659ab9_fk_products_` FOREIGN KEY (`uniform_id`) REFERENCES `products_uniform` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
