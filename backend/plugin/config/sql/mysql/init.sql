insert into sys_config (id, name, type, `key`, value, is_frontend, remark, created_time, updated_time)
values
(1, 'Status', 'EMAIL', 'EMAIL_STATUS', '1', 0, null, now(), null),
(2, 'Server Address', 'EMAIL', 'EMAIL_HOST', 'smtp.qq.com', 0, null, now(), null),
(3, 'Server Port', 'EMAIL', 'EMAIL_PORT', '465', 0, null, now(), null),
(4, 'Email Account', 'EMAIL', 'EMAIL_USERNAME', 'fba@qq.com', 0, null, now(), null),
(5, 'Email Password', 'EMAIL', 'EMAIL_PASSWORD', '', 0, null, now(), null),
(6, 'SSL Encryption', 'EMAIL', 'EMAIL_SSL', '1', 0, null, now(), null),
