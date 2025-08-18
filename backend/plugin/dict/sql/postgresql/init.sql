insert into sys_dict_type (id, name, code, status, remark, created_time, updated_time)
values
(1, 'General Status', 'sys_status', 1, 'System general status: enabled/disabled', now(), null),
(2, 'Menu Type', 'sys_menu_type', 1, 'System menu type', now(), null),
(3, 'Login Log Status', 'sys_login_status', 1, 'User login log status', now(), null),
(4, 'Data Rule Operator', 'sys_data_rule_operator', 1, 'Data permission rule operator', now(), null),
(5, 'Data Rule Expression', 'sys_data_rule_expression', 1, 'Data permission rule expression', now(), null),
(6, 'Frontend Config', 'sys_frontend_config', 1, 'Frontend parameter config type', now(), null),
(7, 'Data Permission Filter', 'sys_data_permission', 1, 'Data permission filter type', now(), null),
(8, 'Menu Display', 'sys_menu_display', 1, 'Whether menu is displayed', now(), null),
(9, 'Menu Cache', 'sys_menu_cache', 1, 'Whether menu is cached', now(), null);

insert into sys_dict_data (id, type_code, label, value, sort, status, remark, type_id, created_time, updated_time)
values
(1, 'sys_status', 'Disabled', '0', 1, 1, 'System disabled status', 1, now(), null),
(2, 'sys_status', 'Enabled', '1', 2, 1, 'System enabled status', 1, now(), null),
(3, 'sys_menu_type', 'Directory', '0', 1, 1, 'Menu directory type', 2, now(), null),
(4, 'sys_menu_type', 'Menu', '1', 2, 1, 'Normal menu type', 2, now(), null),
(5, 'sys_menu_type', 'Button', '2', 3, 1, 'Button permission type', 2, now(), null),
(6, 'sys_menu_type', 'Embedded', '3', 4, 1, 'Embedded page type', 2, now(), null),
(7, 'sys_menu_type', 'External Link', '4', 5, 1, 'External link type', 2, now(), null),
(8, 'sys_login_status', 'Failed', '0', 1, 1, 'Login failed status', 3, now(), null),
(9, 'sys_login_status', 'Success', '1', 2, 1, 'Login success status', 3, now(), null),
(10, 'sys_data_rule_operator', 'AND', '0', 1, 1, 'Logical AND operator', 4, now(), null),
(11, 'sys_data_rule_operator', 'OR', '1', 2, 1, 'Logical OR operator', 4, now(), null),
(12, 'sys_data_rule_expression', 'Equal (==)', '0', 1, 1, 'Equal comparison expression', 5, now(), null),
(13, 'sys_data_rule_expression', 'Not Equal (!=)', '1', 2, 1, 'Not equal comparison expression', 5, now(), null),
(14, 'sys_data_rule_expression', 'Greater Than (>)', '2', 3, 1, 'Greater than comparison expression', 5, now(), null),
(15, 'sys_data_rule_expression', 'Greater Than or Equal (>=)', '3', 4, 1, 'Greater than or equal comparison expression', 5, now(), null),
(16, 'sys_data_rule_expression', 'Less Than (<)', '4', 5, 1, 'Less than comparison expression', 5, now(), null),
(17, 'sys_data_rule_expression', 'Less Than or Equal (<=)', '5', 6, 1, 'Less than or equal comparison expression', 5, now(), null),
(18, 'sys_data_rule_expression', 'Contains (in)', '6', 7, 1, 'Contains expression', 5, now(), null),
(19, 'sys_data_rule_expression', 'Does Not Contain (not in)', '7', 8, 1, 'Does not contain expression', 5, now(), null),
(20, 'sys_frontend_config', 'No', '0', 1, 1, 'Not a frontend parameter config', 6, now(), null),
(21, 'sys_frontend_config', 'Yes', '1', 2, 1, 'Is a frontend parameter config', 6, now(), null),
(22, 'sys_data_permission', 'No', '0', 1, 1, 'No data permission filtering', 7, now(), null),
(23, 'sys_data_permission', 'Yes', '1', 2, 1, 'Data permission filtering', 7, now(), null),
(24, 'sys_menu_display', 'Hidden', '0', 1, 1, 'Menu hidden', 8, now(), null),
(25, 'sys_menu_display', 'Shown', '1', 2, 1, 'Menu shown', 8, now(), null),
(26, 'sys_menu_cache', 'Not Cached', '0', 1, 1, 'Menu not cached', 9, now(), null),
(27, 'sys_menu_cache', 'Cached', '1', 2, 1, 'Menu cached', 9, now(), null);

-- reset auto-increment values for each table based on max id
select setval(pg_get_serial_sequence('sys_dict_type', 'id'),coalesce(max(id), 0) + 1, true) from sys_dict_type;
select setval(pg_get_serial_sequence('sys_dict_data', 'id'),coalesce(max(id), 0) + 1, true) from sys_dict_data;
