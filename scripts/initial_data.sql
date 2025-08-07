-- Optional initial data for FAPP
INSERT INTO core_usuario (id, username, password, is_superuser, is_staff, is_active, date_joined)
VALUES (1, 'admin', 'pbkdf2_sha256$600000$JrwId25yhTkQFiZX6AocXa$UNUGpXvQZkjwU6VrTMfwu/Le1gu8fafnwz0vGfAyrfk=', true, true, true, NOW());

INSERT INTO core_cliente (id, usuario_id, nombre, cif, direccion, email, telefono, activo)
VALUES (1, 1, 'Cliente Demo', '00000000A', 'Calle Falsa 123', 'cliente@demo.com', '600000000', true);
